from __future__ import absolute_import, division, print_function, unicode_literals

from xml.dom.minidom import parse
import numpy as np

from pi3d.shape.Points import Points
from pi3d.Shader import Shader
from pi3d.Texture import Texture
import time

class PexParticles(Points):
  def __init__(self, pex_file, emission_rate=10, scale=1.0, rot_rate=None,
                        rot_var=0.0, new_batch=0.1, hardness=2.0, **kwargs):
    ''' has to be supplied with a pex xml type file to parse. The results
    are loaded into new attributes of the instance of this class with identifiers
    matching the Elements of the pex file. There is zero checking for the
    correct file format.

      pex_file:       file name. if "circle" then lite option doesn't
                      use texture lookup and used mat_pointsprite shader
      emission_rate:  new particles per second
      scale:          scale the point size and location
      rot_rate:       UV mapping rotates
      rot_var:        variance in rotation rate
      new_batch:      proportion of emission_rate to batch (for efficiency)
      hardness:       for lite version

    The following attributes are created from the pex file and can be subsequently
    altered. i.e. self.sourcePosition['x'] += 2.0

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
    self._new_batch = emission_rate * new_batch # to clump new particles
    self.scale = scale
    self.rot_rate = rot_rate
    self.rot_var = rot_var
    # make a flag to avoid this expensive operation if no accelerators
    self.any_acceleration = (self.gravity['x'] != 0.0 or self.gravity['y'] != 0.0 or
                             self.radialAcceleration != 0.0 or
                             self.tangentialAcceleration != 0.0)
    self.any_colorchange = any(self.startColor[i] != self.finishColor[i]
                               for i in ('red','green','blue','alpha'))
    ''' Buffer.array_buffer holds
    [0] vertices[0] x position of centre of point relative to centre of screen in pixels
    [1] vertices[1] y position
    [2] vertices[2] z depth but fract(z) is used as a multiplier for point size
    [3] normals[0]  rotation in radians
    [4] normals[1]  red and green values to multiply with the texture
    [5] normals[2]  blue and alph values to multiply with the texture. The values
                    are packed into the whole number and fractional parts of
                    the float i.e. where R and G are between 0.0 and 0.999
                    normals[:,2] = floor(999 * R) + G
    [6] tex_coords[0] distance of left side of sprite square from left side of
                    texture in uv scale 0.0 to 1.0
    [7] tex_coords[1] distance of top of sprite square from top of texture
       for lite version using the mat_pointsprite shader
    [3:7] hold RGBA in simple float form

       make additional numpy array to hold the particle info
    arr[0]          x velocity
    arr[1]          y velocity
    arr[2]          lifespan
    arr[3]          lifespan remaining
    arr[4:8]        rgba target values
    arr[8:12]       rgba difference
    arr[12]         size delta (finish size - start size) / full_lifespan
    arr[13]         radial acceleration
    arr[14]         tangential acceleration
    '''
    self.arr = np.zeros((self.maxParticles, 15), dtype='float32')
    self.point_size = max(self.startParticleSize + self.startParticleSizeVariance,
                    self.finishParticleSize + self.FinishParticleSizeVariance) #NB capital F!
    super(PexParticles, self).__init__(vertices=np.zeros((self.maxParticles, 3), dtype='float32'), 
                            normals=np.zeros((self.maxParticles, 3), dtype='float32'), 
                            tex_coords=np.zeros((self.maxParticles, 2), dtype='float32'), 
                            point_size=self.point_size * self.scale, **kwargs) # pass to Points.__init__()
    if self.texture['name'] == 'circle': # TODO alternative geometries
      self.lite = True
      shader = Shader('mat_pointsprite')
      self.set_shader(shader)
      self.buf[0].unib[0] = hardness
    else:
      self.lite = False
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
    b = self.buf[0].array_buffer # shortcut to change Buffer.array_buffer in place
    # work out how many new particles to create
    tm = time.time()
    # first time round dt is 0.0 else time since last update
    dt = tm - self._last_time if self._last_time is not None else 0.0
    self._last_time = tm
    if self._last_emission_time is None:
      n_new = self._emission_rate
    else:
      n_new = int(self._emission_rate * (tm - self._last_emission_time))
    if n_new > self._new_batch:
      self._last_emission_time = tm
      self.arr[:-n_new] = self.arr[n_new:] # 'age' by moving along
      b[:-n_new] = b[n_new:]
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
      b[-n_new:,0:2] = new_vals[:,0:2] * self.scale
      # velocities
      self.arr[-n_new:,0] = new_vals[:,2] * np.cos(np.radians(new_vals[:,4])) * self.scale
      self.arr[-n_new:,1] = new_vals[:,2] * np.sin(np.radians(new_vals[:,4])) * self.scale
      # lifeSpan
      self.arr[-n_new:,2] = new_vals[:,3]
      self.arr[-n_new:,3] = new_vals[:,3]
      # rgba target
      self.arr[-n_new:,4:8] = np.minimum(np.maximum(new_vals[:,11:15], 0.0), 0.999)
      # rgba difference
      self.arr[-n_new:,8:12] = (np.minimum(np.maximum(new_vals[:,11:15], 0.0), 0.999) - 
                                 np.minimum(np.maximum(new_vals[:,7:11], 0.0), 0.999))
      if self.lite:
        b[-n_new:,3:7] = new_vals[:,7:11]
      else:
        b[-n_new:,4:6] = np.floor(999.0 * self.arr[-n_new,4:7:2]) + 0.99 * self.arr[-n_new,5:8:2]
      # size
      b[-n_new:,2] = new_vals[:,15] * 0.999 / self.point_size # must not approx to 1.0 at medium precision
      # and reset the z distance part (unif[2] hold Shape z value)
      b[:,2] = np.arange(self.maxParticles + self.unif[2], self.unif[2], -1.0) + b[:,2] % 1.0
      # size delta
      self.arr[-n_new:,12] = 0.95 * (new_vals[:,16] - new_vals[:,15]) / self.point_size / self.arr[-n_new:,2]
      # radial and tangential acc
      self.arr[-n_new:,13:15] = new_vals[:,5:7]
    alph_i = 6 if self.lite else 5 # see next line
    b[self.arr[:,3] <= 0.0, alph_i] = 0.0 # make alpha 0 for dead particles
    ix = np.where(self.arr[:,3] > 0.0)[0] # index of live particles
    radial_v = b[ix,0:2] - [self.sourcePosition['x'],
                                  self.sourcePosition['y']] # vector from emitter
    radial_v /= np.linalg.norm(radial_v, axis=1)[:, np.newaxis] # normalise
    b[ix,0:2] += self.arr[ix,0:2] * dt # location change
    if self.any_acceleration:
      self.arr[ix,0:2] += ([self.gravity['x'], self.gravity['y']] + # velocity change
                          radial_v * self.arr[ix,13].reshape(-1,1) + # radial and tang acc
                          radial_v[:,::-1] * [-1.0, 1.0] * self.arr[ix,14].reshape(-1,1)) * dt * self.scale
    if self.any_colorchange:
      if self.lite:
        b[ix,3:7] = self.arr[ix,4:8] - (self.arr[ix,8:12] *
                          (self.arr[ix,3] / self.arr[ix,2]).reshape(-1,1))# colour change
      else:
        b[ix,4:6] = np.floor(999.0 * (self.arr[ix,4:7:2] - self.arr[ix,8:11:2] *
                            (self.arr[ix,3] / self.arr[ix,2]).reshape(-1,1)))# rb change
        b[ix,4:6] += 0.99 * (self.arr[ix,5:8:2] - self.arr[ix,9:12:2] *
                            (self.arr[ix,3] / self.arr[ix,2]).reshape(-1,1))# ga change
    b[ix,2] += self.arr[ix,12] * dt # size change
    self.arr[ix,3] -= dt # lifespan remaining
    if self.rot_rate is not None: # rotate if this is set
      b[ix,3] += (self.rot_rate + self.rot_var * 
                          (np.random.random(ix.shape) * 2.0 - 1.0)) * dt

    self.re_init() # re-init the buffers
