#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d
import pickle
import time
from six.moves import queue
from threading import Thread

#========================================
class SceneryItem(object):
  def __init__(self, x, y, z, textures, shader, bump=0.0, shine=0.0, 
        status=0, texture_flip=False, texture_mipmap=True, priority=0, 
        put_on=None, height=300.0, model_details=None, alpha=1.0):
    '''class representing objects used in the Scene.scenery_list dictionary
    There is enough information to allow objects to be created and pickled.
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
    thr = Thread(target=load_scenery)
    thr.daemon = True
    thr.start()

    
  def do_pickle(self, fog=((0.3, 0.3, 0.4, 0.95), 500.0)): #run once to save pkl files
    for key in self.scenery_list:
      s_item = self.scenery_list[key]
      if s_item.put_on == None: #this is a map - do all these first pass
        mymap = pi3d.ElevationMap(mapfile='{}/{}.png'.format(self.path, key), name=key,
                           width=(self.msize + 0.001), depth=(self.msize + 0.001), height=s_item.height, 
                           x=s_item.x, y=s_item.y, z=s_item.z, divx=64, divy=64)
        mymap.set_fog(*fog)
        mymap.set_alpha(s_item.alpha)
        with open('{}/{}.pkl'.format(self.path, key), 'wb') as f:
          pickle.dump(mymap, f)
        s_item.shape = mymap # temp store all these for the sake of make_pickle
    for key in self.scenery_list:
      s_item = self.scenery_list[key]
      if s_item.put_on != None: #model so need to put on map
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

  def key_draw_list(self, s_item):
    return s_item.priority
    
  def key_age_list(self, key):
    return self.scenery_list[key].last_drawn

  def check_scenery(self, xm, zm):
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
        
        if abs(dx) < 1000.0 and abs(dz) < 1000.0:
          if s_item.status == 0:
            item = (key, self.path, s_item, self.texture_list, self.draw_list, 
                  offsetx, offsetz)
            jobQ.put(item)
            if key == cmap_id: #should only happen at start where need map for calcHeight
              jobQ.join()
          elif s_item.status == 2:
            s_item.shape.position(s_item.x + offsetx, s_item.y, s_item.z + offsetz)
            s_item.last_drawn = time.time()
            self.draw_list.append(s_item)
      self.draw_list = sorted(self.draw_list, key=self.key_draw_list)
      cmap = self.scenery_list[cmap_id].shape
      return xm, zm, cmap

  #################### clear out unused scenery TODO clear unused textures too
  def clear_scenery(self, threshold):
    clear_list = sorted(self.scenery_list, key=self.key_age_list, reverse=True)[:-30]
    for key in clear_list:
      s_item = self.scenery_list[key]
      if s_item.last_drawn < threshold:
        s_item.status = 0
        s_item.shape = None

jobQ = queue.Queue() #TODO ideally avoid using a global!

###################### function run in thread by check_scenery
def load_scenery():
  while True:
    item = jobQ.get() #blocks for next available job
    pickle_name = item[0]
    pickle_path = item[1]
    s_item = item[2]
    texture_list = item[3]
    draw_list = item[4]
    offsetx = item[5]
    offsetz = item[6]

    with open('{}/{}.pkl'.format(pickle_path, pickle_name), 'rb') as f:
      s_item.shape = pickle.load(f)
    t_list = []
    for t in s_item.textures:
      if t in texture_list:
        i = 0
        while i < 10 and texture_list[t].status == 1:
          time.sleep(1.0)
          i += 1
      else:
        texture_list[t] = TextureItem(status=1)
        texture_list[t].texture = pi3d.Texture('{}/{}.png'.format(pickle_path, t), 
                                    flip=s_item.texture_flip, mipmap=s_item.texture_mipmap)
        texture_list[t].status = 2
      t_list.append(texture_list[t].texture)
    if len(s_item.textures) > 0:
      s_item.shape.set_draw_details(s_item.shader, t_list, s_item.bump, s_item.shine)
    else:
      s_item.shape.set_shader(s_item.shader)
    s_item.status = 2
    s_item.shape.position(s_item.x + offsetx, s_item.y, s_item.z + offsetz)
    s_item.last_drawn = time.time()
    draw_list.append(s_item)
    jobQ.task_done()

