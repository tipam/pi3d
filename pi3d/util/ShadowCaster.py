import ctypes
from PIL import Image

from pi3d.constants import *
from pi3d.Shader import Shader
from pi3d.util.OffScreenTexture import OffScreenTexture
from pi3d.Camera import Camera

class ShadowCaster(OffScreenTexture):
  """For creating a depth-of-field blurring effect on selected objects"""
  def __init__(self, emap, light):
    """ calls Texture.__init__ but doesn't need to set file name as
    texture generated from the framebuffer
    """
    super(ShadowCaster, self).__init__("shadow_caster")
    # load shader for casting shadows and camera
    self.cshader = Shader("uv_flat")
    self.mshader = Shader("mat_flat")
    # keep copy of ElevationMap
    self.emap = emap
    self.emap.set_material((0.0, 0.0, 0.0)) # hide bits below ground
    #TODO doesn't cope with  z light positions
    self.eye = [-500.0 * i for i in light.lightpos] # good distance away
    if self.eye[1] <= 0: # must have +ve y
      self.eye[1] = 500.0
    if abs(self.eye[0]) > abs(self.eye[2]): #x val is bigger than z val
      #change scale so map just fits on screen
      if self.eye[0] < 0:
        su, sv  = 1.0, 1.0
      else:
        su, sv  = -1.0, -1.0
      self.scaleu = float(self.iy) / self.emap.width
      self.scalev = float(self.ix)/ self.emap.depth
      self.eye[2] = 0
      self.scaleu = self.scaleu / self.eye[1] * (self.eye[0]**2 + self.eye[1]**2)**0.5
      self.emap.unif[50] = 1.0 #orientation flag
      self.emap.unif[53] = -3.0 * su / self.emap.width * self.eye[0] / self.eye[1] #height adjustment
    else:
      #change scale so map just fits on screen
      if self.eye[2] < 0:
        su, sv  = 1.0, -1.0
      else:
        su, sv  = -1.0, 1.0
      self.scaleu = float(self.iy) / self.emap.depth
      self.scalev = float(self.ix)/ self.emap.width
      self.eye[0] = 0
      self.scaleu = self.scaleu / self.eye[1] * (self.eye[2]**2 + self.eye[1]**2)**0.5
      self.emap.unif[50] = 0.0
      self.emap.unif[53] = -3.0 * su / self.emap.width * self.eye[2] / self.eye[1]
    if abs(self.scaleu) > abs(self.scalev):
      self.scale = 3.0 * self.scalev # multiplication factor to reduce pixeliness
    else:
      self.scale = 3.0 * self.scaleu
    self.scaleu = su * self.scale / self.scaleu # reused later in end_cast
    self.scalev = sv * self.scale / self.scalev
    self.camera0 = Camera() # default instance created as normal, just in case!
    self.camera = Camera(is_3d=False, eye=self.eye, scale=self.scale)
    # load shader for drawing map with shadows
    self.dshader = Shader("shadowcast")

  def start_cast(self, location=(0.0, 0.0,  0.0)):
    """ after calling this method all object.draw()s will rendered
    to this texture and not appear on the display. If you want blurred
    edges you will have to capture the rendering of an object and its
    background then re-draw them using the blur() method. Large objects
    will obviously take a while to draw and re-draw
    """
    opengles.glClearColor(ctypes.c_float(0.0), ctypes.c_float(0.0), 
                        ctypes.c_float(0.0), ctypes.c_float(1.0))
    super(ShadowCaster, self)._start()
    self.camera.reset(is_3d=False, scale=self.scale)
    self.camera.position((location[0], 0, location[2]))
    self.location = location

  def end_cast(self):
    """ stop capturing to texture and resume normal rendering to default
    """
    #draw the actual map
    self.emap.draw(shader=self.mshader, camera=self.camera)
    super(ShadowCaster, self)._end()
    # set third texture to this ShadowCaster texture
    texs = self.emap.buf[0].textures
    if len(texs) == 2:
      texs.append(self)
    else:
      texs[2] = self
    # change background back to blue
    opengles.glClearColor(ctypes.c_float(0.4), ctypes.c_float(0.8), 
                        ctypes.c_float(0.8), ctypes.c_float(1.0))
    # work out left, top, right, bottom for shader
    self.emap.unif[48] = 0.5 * (1.0 + self.scaleu) # left [16][0]
    self.emap.unif[49] = 0.5 * (1.0 + self.scalev) # top [16][1]
    self.emap.unif[51] = 1.0 - self.emap.unif[48] # right [17][0]
    self.emap.unif[52] = 1.0 - self.emap.unif[49] # bottom [17][1]
    
    du = float(self.location[0] / self.emap.width)
    dv = float(self.location[2] / self.emap.depth)
    self.emap.unif[48] -= self.scaleu * (du if self.emap.unif[50] == 1.0 else dv)
    self.emap.unif[49] += self.scalev * (dv if self.emap.unif[50] == 1.0 else du)
    self.emap.unif[51] -= self.scaleu * (du if self.emap.unif[50] == 1.0 else dv)
    self.emap.unif[52] += self.scalev * (dv if self.emap.unif[50] == 1.0 else du)

  def add_shadow(self, shape):
    shape.draw(shader=self.cshader, camera=self.camera)
    
  def draw_shadow(self):
    self.emap.draw(shader=self.dshader)
