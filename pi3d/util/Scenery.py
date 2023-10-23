#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d
import pickle
import time
from threading import Thread
from six_mod.moves import queue
import logging

#pi3d.Log.set_logs(file="/home/pi/pi3d_demos/templog.txt")
LOGGER = logging.getLogger(__name__)

#========================================
class SceneryItem(object):
  def __init__(self, x, y, z, textures, shader, bump=0.0, shine=0.0, 
        status=0, texture_flip=False, texture_mipmap=True, priority=0, 
        put_on=None, height=300.0, threshold=750.0,
        model_details=None, alpha=1.0):
    '''class representing objects used in the Scene.scenery_list dictionary
    There is enough information to allow objects to be created and pickled.
    
    At the moment the SceneryItems are either ElevationMaps which are
    specified by defining put_on = None. The key to this dictionary record
    is the stem of the name used as the map texture to define the elevation
    i.e. 'map00' will look for 'map00.png' which should be 33x33 pixels
    as the ElevationMap uses 32 divisions.
    
    or, if put_on is not None it will be assumed to be the key to an
    ElevationMap record in Scene.scenery_list and will be loaded as as a
    pi3d.Model using 'name.obj'
    '''
    self.x = x
    self.y = y
    self.z = z
    self.textures = textures
    self.shader = shader
    self.bump = bump
    self.shine = shine
    self.status = status
    self.texture_flip = texture_flip
    self.texture_mipmap = texture_mipmap
    self.priority = priority
    self.put_on = put_on
    self.height = height
    self.threshold = threshold
    self.threshold_sq = threshold * threshold
    self.model_details = model_details
    self.alpha = alpha
    self.shape = None
    self.last_drawn = 0.0
    
class TextureItem(object):
  def __init__(self, status=0):
    '''very simple class to hold texture items in Scene.texture_list
    '''
    self.texture = None
    self.status = status
    
class Scene(object):
  def __init__(self, path, msize=1000.0, nx=5, nz=5):
    '''class for managing scenery objects in the background of a 1st
    person navigation game.
    '''
    self.scenery_list = {}
    self.texture_list = {}
    self.draw_list = []
    self.models = {}
    self.path = path
    self.msize = msize
    self.nx = nx
    self.nz = nz
    self.thr = Thread(target=load_scenery)
    self.thr.daemon = True
    self.thr.start()

    
  def do_pickle(self, fog=((0.3, 0.3, 0.4, 0.95), 450.0)):
    '''run once to save pkl files from ElevationMaps and Models combined
    as MergeShapes as defined in the SceneryItem objects listed in
    scenery_list
    '''
    for key in self.scenery_list:
      s_item = self.scenery_list[key]
      if s_item.put_on is None: #this is a map - do all these first pass
        LOGGER.debug('pickling %s', key)
        mymap = pi3d.ElevationMap(mapfile='{}/{}.png'.format(self.path, key), name=key,
                           width=(self.msize + 0.001), depth=(self.msize + 0.001), height=s_item.height, 
                           x=s_item.x, y=s_item.y, z=s_item.z, divx=32, divy=32)
        mymap.set_fog(*fog)
        mymap.set_alpha(s_item.alpha)
        with open('{}/{}.pkl'.format(self.path, key), 'wb') as f:
          pickle.dump(mymap, f)
        s_item.shape = mymap # temp store all these for the sake of make_pickle
    for key in self.scenery_list:
      s_item = self.scenery_list[key]
      if s_item.put_on is not None: #model so need to put on map
        LOGGER.debug('pickling %s', key)
        md = s_item.model_details
        if not md['model'] in self.models:
          self.models[md['model']] = pi3d.Model(file_string='{}/{}.obj'.format(self.path, md['model']))
        m_item = self.scenery_list[s_item.put_on]
        xpos = s_item.x - m_item.x # relative to map it's put on
        zpos = s_item.z - m_item.z
        mymerge = pi3d.MergeShape(name=key, x=s_item.x, z=s_item.z)
        mymerge.cluster(self.models[md['model']], m_item.shape, 0.0, 0.0, 
                      md['w'], md['d'], md['n'], key, md['maxs'], md['mins'])
        mymerge.set_fog(*fog)
        with open('{}/{}.pkl'.format(self.path, key), 'wb') as f:
          pickle.dump(mymerge, f)
    for key in self.scenery_list: #tidy up memory usage
      s_item = self.scenery_list[key]
      s_item.shape = None

  def _key_draw_list(self, s_item):
    '''function used by sorted to make drawing follow priority order
    '''
    return s_item.priority
    
  def _key_age_list(self, key):
    '''function used by sorted to clear oldest unused items from draw_list
    '''
    return self.scenery_list[key].last_drawn

  def check_scenery(self, xm, zm):
    '''checks the scenery_list for anything that needs to be loaded
    using a background thread. It wraps the x and z values as they go
    over the edge of the end tiles and returns a tuple of their values
    plus the key to the current elevation map to be used for ground
    following (defined as 'mapXY' where X and Y are the coordinates)
    '''
    xsize = self.msize * self.nx
    zsize = self.msize * self.nz
    if xm > xsize:
      xm -= xsize
    if xm < 0.0:
      xm += xsize
    if zm > zsize:
      zm -= zsize
    if zm < 0.0:
      zm += zsize
    cmap_id = 'map{}{}'.format(int(xm / self.msize), int(zm / self.msize))
    self.draw_list = []
    for key in self.scenery_list:
      s_item = self.scenery_list[key]
      
      dx = s_item.x - xm
      offsetx = 0.0
      if dx > xsize / 2.0:
        offsetx = -xsize
      if dx < -xsize / 2.0:
        offsetx = xsize
      dx += offsetx
      
      dz = s_item.z - zm
      offsetz = 0.0
      if dz > zsize / 2.0:
        offsetz = -zsize
      if dz < -zsize / 2.0:
        offsetz = zsize
      dz += offsetz
      
      if (dx * dx + dz * dz) < s_item.threshold_sq:
        if s_item.status == 0:
          if not self.thr.is_alive():
            self.thr = Thread(target=load_scenery)
            self.thr.daemon = True
            self.thr.start()
          s_item.status = 1
          item = (key, self.path, s_item, self.texture_list, self.draw_list, 
                offsetx, offsetz)
          QDOWN.put(item)
        elif s_item.status == 2:
          s_item.shape.position(s_item.x + offsetx, s_item.y, s_item.z + offsetz)
          s_item.last_drawn = time.time()
          self.draw_list.append(s_item)
    self.draw_list = sorted(self.draw_list, key=self._key_draw_list)
    cmap = self.scenery_list[cmap_id].shape
    return xm, zm, cmap

  #################### clear out unused scenery TODO clear unused textures too
  def clear_scenery(self, threshold):
    clear_list = sorted(self.scenery_list, key=self._key_age_list, reverse=True)[:-30]
    for key in clear_list:
      s_item = self.scenery_list[key]
      if s_item.last_drawn < threshold:
        s_item.status = 0
        s_item.shape = None

QDOWN = queue.Queue()

###################### function run in thread
def load_scenery():
  while True:
    item = QDOWN.get() #blocks for next available job
    if item[0] == 'STOP':
      break
    key = item[0]
    pickle_path = item[1]
    s_item = item[2]
    texture_list = item[3]
    draw_list = item[4]
    offsetx = item[5]
    offsetz = item[6]

    #LOGGER.debug('start pkl_load {}'.format(time.time()))

    with open('{}/{}.pkl'.format(pickle_path, key), 'rb') as f:
      s_item.shape = pickle.load(f)

    #LOGGER.debug('end   pkl_load {}'.format(time.time()))

    t_list = []
    for t in s_item.textures:

      #LOGGER.debug('start tx_load {}'.format(time.time()))

      if not t in texture_list:
        texture_list[t] = TextureItem(status=1)
        texture_list[t].texture = pi3d.Texture('{}/{}.png'.format(pickle_path, t), 
                                    flip=s_item.texture_flip, mipmap=s_item.texture_mipmap)
      t_list.append(texture_list[t].texture)

      #LOGGER.debug('end   tx_load {}'.format(time.time()))

    s_item.shape.position(s_item.x + offsetx, s_item.y, s_item.z + offsetz)
    if len(s_item.textures) > 0:
      s_item.shape.set_draw_details(s_item.shader, t_list, s_item.bump, s_item.shine)
    else:
      s_item.shape.set_shader(s_item.shader)
    s_item.status = 2
    s_item.last_drawn = time.time()
    draw_list.append(s_item)

    #LOGGER.debug('end subprocess {}'.format(time.time()))


