from __future__ import absolute_import, division, print_function, unicode_literals

from xml.dom.minidom import parse
import numpy as np

from pi3d.shape.Points import Points
from pi3d.Shader import Shader
from pi3d.Texture import Texture
import time

class PexParticles(Points):
  def __init__(self, pex_file, emission_rate=10, scale=1.0, rot_rate=None,
                                                rot_var=0.0, **kwargs):
    ''' has to be supplied with a pex xml type file to parse. The results
    are loaded into new attributes of the instance of this class with identifiers
    matching the Elements of the pex file. There is zero checking for the
    correct file format:
      self.texture={name:'particle.png'}
      self.sourcePosition={x:160.00,y:369.01}
      self.sourcePositionVariance={x:60.00,y:0.00}
      self.speed=138.16
      self.speedVariance=0.00
      self.particleLifeSpan=0.7000
      self.particleLifespanVariance=0.0000
      self.angle=224.38
      self.angleVariance=360.00
      self.gravity={x:0.00,y:-1400.00}
      self.radialAcceleration=0.00
      self.tangentialAcceleration=0.00
      self.radialAccelVariance=0.00
      self.tangentialAccelVariance=-0.00
      self.startColor={red:0.15,green:0.06,blue:1.00,alpha:1.00}
      self.startColorVariance={red:0.00,green:0.00,blue:0.00,alpha:0.00}
      self.finishColor={red:0.00,green:0.14,blue:0.23,alpha:0.00}
      self.finishColorVariance={red:0.00,green:0.00,blue:0.00,alpha:0.00}
      self.maxParticles=300
      self.startParticleSize=43.79
      self.startParticleSizeVariance=0.00
      self.finishParticleSize=138.11
      self.FinishParticleSizeVariance=0.00
      self.duration=-1.00
      self.emitterType=0
      self.maxRadius=100.00
      self.maxRadiusVariance=0.00
      self.minRadius=0.00
      self.rotatePerSecond=0.00
      self.rotatePerSecondVariance=0.00
      self.blendFuncSource=770
      self.blendFuncDestination=772
      self.rotationStart=0.00
      self.rotationStartVariance=0.00
      self.rotationEnd=0.00
      self.rotationEndVariance=0.00
    '''
    # first parse the pex file, json would have been nicer than xml!
    _config = parse(pex_file).childNodes[0].childNodes
    for c in _config:
      if c.localName is not None:
        key = c.localName
        val = {}
        for v in c.attributes.items():
          try:
            v_tp = int(v[1]) # try int first
          except ValueError:
            try:
              v_tp = float(v[1]) # if not try float
            except ValueError:
              v_tp = v[1] # otherwise leave as string
          if v[0] == 'value': # single value 'value' don't use dictionary
            val = v_tp
            break
          else:
            val[v[0]] = v_tp # not just a value
        self.__setattr__(key, val)

    self._emission_rate = emission_rate # particles per second
    self._last_emission_time = None
    self._last_time = None
    self.scale = scale
    self.rot_rate = rot_rate
    self.rot_var = rot_var
    
    ''' make the numpy arrays to hold the particle info
    vertices[0]   x position of centre of point relative to centre of screen in pixels
    vertices[1]   y position
    vertices[2]   z depth but fract(z) is used as a multiplier for point size
    normals[0]    rotation in radians
    normals[1]    red and green values to multiply with the texture
    normals[2]    blue and alph values to multiply with the texture. The values
                  are packed into the whole number and fractional parts of
                  the float i.e. where R and G are between 0.0 and 0.999
                  normals[:,2] = floor(999 * R) + G
    tex_coords[0] distance of left side of sprite square from left side of
                  texture in uv scale 0.0 to 1.0
    tex_coords[1] distance of top of sprite square from top of texture
    arr[8]        x velocity
    arr[9]        y velocity
    arr[10]       lifespan
    arr[11]       lifespan remaining
    arr[12:16]    rgba target values
    arr[16:20]    rgba difference
    arr[20]       size delta (finish size - start size) / full_lifespan
    arr[21]       radial acceleration
    arr[22]       tangential acceleration
    '''
    self.arr = np.zeros((self.maxParticles, 23), dtype='float32')
    self.point_size = max(self.startParticleSize + self.startParticleSizeVariance,
                    self.finishParticleSize + self.FinishParticleSizeVariance) #NB capital F!
    super(PexParticles, self).__init__(vertices=self.arr[:,0:3], 
                            normals=self.arr[:,3:6], 
                            tex_coords=self.arr[:,6:8], 
                            point_size=self.point_size * self.scale, **kwargs) # pass to Points.__init__()
    shader = Shader('uv_pointsprite')
    try:
      tex = Texture(self.texture['name']) # obvious first!
    except:
      import os
      tex = Texture(os.path.join(
                      os.path.split(pex_file)[0], self.texture['name']))
    self.set_draw_details(shader, [tex])
    self.unif[48] = 1.0 # sprite uses whole image

  def update(self):
    # work out how many new particles to create
    tm = time.time()
    # first time round dt is 0.0 else time since last update
    dt = tm - self._last_time if self._last_time is not None else 0.0
    self._last_time = tm
    if self._last_emission_time is None:
      n_new = self._emission_rate
    else:
      n_new = int(self._emission_rate * (tm - self._last_emission_time))
    if n_new > 0:
      self._last_emission_time = tm
      self.arr[:-n_new] = self.arr[n_new:] # 'age' by moving along
      # generate ALL the varying values in one step
      new_vals = (
          [self.sourcePosition['x'], self.sourcePosition['y'],   # 0,1,
           self.speed, self.particleLifeSpan, self.angle,        # 2,3,4,
           self.radialAcceleration, self.tangentialAcceleration, # 5,6
           self.startColor['red'], self.startColor['green'],     # 7,8
           self.startColor['blue'], self.startColor['alpha'],    # 9,10
           self.finishColor['red'], self.finishColor['green'],   # 11,12
           self.finishColor['blue'], self.finishColor['alpha'],  # 13,14
           self.startParticleSize, self.finishParticleSize]      # 15,16
            + (np.random.random((n_new, 17)) * 2.0 - 1.0) *
           [self.sourcePositionVariance['x'], self.sourcePositionVariance['y'],
           self.speedVariance, self.particleLifespanVariance, self.angleVariance,
           self.radialAccelVariance, self.tangentialAccelVariance,
           self.startColorVariance['red'], self.startColorVariance['green'],
           self.startColorVariance['blue'], self.startColorVariance['alpha'],
           self.finishColorVariance['red'], self.finishColorVariance['green'],
           self.finishColorVariance['blue'], self.finishColorVariance['alpha'],
           self.startParticleSizeVariance, self.FinishParticleSizeVariance]) # NB capital F!

      # x, y locations
      self.arr[-n_new:,0:2] = new_vals[:,0:2] * self.scale
      # velocities
      self.arr[-n_new:,8] = new_vals[:,2] * np.cos(np.radians(new_vals[:,4])) * self.scale
      self.arr[-n_new:,9] = new_vals[:,2] * np.sin(np.radians(new_vals[:,4])) * self.scale
      # lifeSpan
      self.arr[-n_new:,10] = new_vals[:,3]
      self.arr[-n_new:,11] = new_vals[:,3]
      # rgba target
      self.arr[-n_new:,12:16] = np.minimum(np.maximum(new_vals[:,11:15], 0.0), 0.999)
      # rgba difference
      self.arr[-n_new:,16:20] = (np.minimum(np.maximum(new_vals[:,11:15], 0.0), 0.999) - 
                                 np.minimum(np.maximum(new_vals[:,7:11], 0.0), 0.999))
      # size
      self.arr[-n_new:,2] = new_vals[:,15] * 0.999 / self.point_size # must not approx to 1.0 at medium precision
      # and reset the z distance part
      self.arr[:,2] = np.floor(np.linspace(999.0, 0.0, self.maxParticles)) + self.arr[:,2] % 1.0
      # size delta
      self.arr[-n_new:,20] = 0.95 * (new_vals[:,16] - new_vals[:,15]) / self.point_size / self.arr[-n_new:,10]
      # radial and tangential acc
      self.arr[-n_new:,21:23] = new_vals[:,5:7]
    self.arr[self.arr[:,11] <= 0.0, 5] = 0.0 # make alpha 0 for dead particles
    ix = np.where(self.arr[:,11] > 0.0)[0] # index of live particles
    radial_v = self.arr[ix,0:2] - [self.sourcePosition['x'],
                                  self.sourcePosition['y']] # vector from emitter
    radial_v /= ((radial_v ** 2).sum()) ** 0.5 # normalise
    self.arr[ix,0:2] += self.arr[ix,8:10] * dt # location change
    self.arr[ix,8:10] += ([self.gravity['x'], self.gravity['y']] + # velocity change
                          radial_v * self.arr[ix,21].reshape(-1,1) + # radial and tang acc
                          radial_v[:,::-1] * [-1.0, 1.0] * self.arr[ix,22].reshape(-1,1)) * dt * self.scale
    self.arr[ix,4:6] = np.floor(999.0 * (self.arr[ix,12:15:2] - self.arr[ix,16:19:2] *
                          (self.arr[ix,11] / self.arr[ix,10]).reshape(-1,1)))# rb change
    self.arr[ix,4:6] += 0.99 * (self.arr[ix,13:16:2] - self.arr[ix,17:20:2] *
                          (self.arr[ix,11] / self.arr[ix,10]).reshape(-1,1))# ga change
    self.arr[ix,2] += self.arr[ix,20] * dt # size change
    self.arr[ix,11] -= dt # lifespan remaining
    if self.rot_rate is not None: # rotate if this is set
      self.arr[ix,3] += (self.rot_rate + self.rot_var * 
                          (np.random.random(ix.shape) * 2.0 - 1.0)) * dt

    self.re_init(pts=self.arr[:,0:3], normals=self.arr[:,3:6], 
                  texcoords=self.arr[:,6:8]) # re-init the buffers
