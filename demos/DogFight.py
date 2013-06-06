#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import time, math, glob

import demo
import pi3d
#display, camera, shader
DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=20)
#a default camera is created automatically but we might need a 2nd 2D camera
#for displaying the instruments etc. Also, because the landscape is large
#we need to set the far plane to 10,000
CAMERA = pi3d.Camera(lens=(1.0, 10000.0, 55.0, 1.6))

print("""===================================
== W increase power, S reduce power
== V view mode, C control mode
== B brakes
== mouse movement joystick
== Left button fire!
== X jumps to the enemy location
================================""")

SHADER = pi3d.Shader("shaders/uv_reflect") #for objects to look 3D
FLATSH = pi3d.Shader("shaders/uv_flat") #for 'unlit' objects like the background
#STAR = pi3d.Shader("shaders/star") #for fun

GRAVITY = 9.8 #m/s**2
LD = 10 #lift/drag ratio
DAMPING = 0.95 #reduce roll and pitch rate each update_variables
BOOSTER = 1.5 #extra manoevreability boost to defy 1st Low of Thermodynamics.
#load bullet images
BULLET_TEX = [] #list to hold Texture refs
iFiles = glob.glob("textures/biplane/bullet??.png") 
iFiles.sort() # order is vital to animation!
for f in iFiles:
  BULLET_TEX.append(pi3d.Texture(f))
HIT_DISTANCE = 20 #determine sucess of shoot()

#define Aeroplane class
class Aeroplane(object):
  def __init__(self, model, recalc_time):
    self.recalc_time = recalc_time #in theory use different values for enemy
    self.x, self.y, self. z = 0.0, 0.0, 0.0
    self.v_speed, self.h_speed = 0.0, 0.0
    self.rollrate, self.pitchrate, self.yaw = 0.0, 0.0, 0.0
    self.direction, self.roll, self.pitch = 0.0, 0.0, 0.0
    self.max_roll, self.max_pitch = 65, 30 #limit rotations
    self.ailerons, self.elevator = 0.0, 0.0
    self.max_ailerons, self.max_elevator = 10.0, 10.0 #limit conrol surface movement
    self.VNE = 120 #max speed (Velocity Not to be Exceeded)
    self.mass = 300
    self.a_factor, self.e_factor = 10, 10
    self.roll_inrta, self.pitch_inrta = 100, 100
    self.max_power = 2000 #force units of thrust really
    self.lift_factor = 20.0 #randomly adjusted to give required performance!
    self.power_setting = 0.0
    self.throttle_step = 20
    self.last_time = time.time()
    self.last_pos_time = self.last_time
    #create the actual model
    self.model = pi3d.Model(file_string=model, camera=CAMERA)
    self.model.set_shader(SHADER)
    #create the bullets
    plane = pi3d.Plane(h=25, w=1)
    self.bullets = pi3d.MergeShape(camera=CAMERA)
    #the merge method does rotations 1st Z, 2nd X, 3rd Y for some reason
    #for multi axis rotations you need to figure it out by rotating a
    #sheet of paper in the air in front of you (angles counter clockwise)!
    self.bullets.merge([[plane, -2.0, 0.5, 8.0, 90,0,0, 1,1,1],
                        [plane, -2.0, 0.5, 8.0, 0,90,90, 1,1,1],
                        [plane, 2.0, 0.5, 8.0, 90,0,0, 1,1,1],
                        [plane, 2.0, 0.5, 8.0, 0,90,90, 1,1,1]])
    self.num_b = len(BULLET_TEX)
    self.seq_b = self.num_b
    self.bullets.set_draw_details(FLATSH, [BULLET_TEX[0]])

  def set_ailerons(self, dx):
    self.ailerons = dx
    if abs(self.ailerons) > self.max_ailerons:
      self.ailerons = math.copysign(self.max_ailerons, self.ailerons)

  def set_elevator(self, dy):
    self.elevator = dy
    if abs(self.elevator) > self.max_elevator:
      self.elevator = math.copysign(self.max_elevator, self.elevator)

  def set_power(self, incr):
    self.power_setting += incr * self.throttle_step
    if self.power_setting < 0:
      self.power_setting = 0
    elif self.power_setting > self.max_power:
      self.power_setting = self.max_power

  def shoot(self, target):
    #animate bullets
    self.seq_b = 0
    #check for hit
    #components of direction vector
    diag_xz = math.cos(math.radians(self.pitch))
    drn_x = diag_xz * math.sin(math.radians(self.direction))
    drn_y = math.sin(math.radians(self.pitch))
    drn_z = diag_xz * math.cos(math.radians(self.direction))
    #this will already be a unit vector
    #vector from target to aeroplane
    a_x = target[0] - self.x
    a_y = target[1] - self.y
    a_z = target[2] - self.z
    #dot product
    dot_p = drn_x * a_x + drn_y * a_y + drn_z * a_z
    dx = a_x - dot_p * drn_x
    dy = a_y - dot_p * drn_y
    dz = a_z - dot_p * drn_z
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    print("distance={0:.2f}".format(distance))
    if distance < HIT_DISTANCE:
       return True
    return False

  def home(self, target):
    #turn towards target location, mainly for control of enemy aircraft
    dir_t = math.degrees(math.atan2((target[0] - self.x), (target[2] - self.z)))
    #make sure the direction is alway a value between +/- 180 degrees
    #roll so bank is half direction, 
    self.roll = -((dir_t - self.direction + 180) % 360 - 180) / 2
    #find angle between self and target
    pch_t = math.degrees(math.atan2((target[1] - self.y),
            math.sqrt((target[2] - self.z)**2 + (target[0] - self.x)**2)))
    self.pitch = pch_t
    return True

  def update_variables(self):
    #time
    tm = time.time()
    dt = tm - self.last_time
    if dt < self.recalc_time: # don't need to do all this physics every loop
      return
    self.last_time = tm
    #force from ailerons and elevators to get rotational accelerations
    spsq = self.v_speed**2 + self.h_speed**2 #speed squared
    a_force = self.a_factor * self.ailerons * spsq #ailerons force (moment really)
    roll_acc = a_force / self.roll_inrta #good old Newton
    e_force = self.e_factor * self.elevator * spsq #elevator
    pitch_acc = e_force / self.pitch_inrta
    #velocities and positions
    if abs(self.roll) > self.max_roll: #make it easier to do flight control
      self.roll = math.copysign(self.max_roll, self.roll)
      self.rollrate = 0.0
    if abs(self.pitch) > self.max_pitch:
      self.pitch = math.copysign(self.max_pitch, self.pitch)
      self.pitchrate = 0.0
    self.roll += self.rollrate * dt #update roll position
    self.pitch += self.pitchrate * dt #update roll rate
    self.rollrate += roll_acc * dt
    self.rollrate *= DAMPING # to stop going out of contol while looking around!
    self.pitchrate += pitch_acc * dt
    self.pitchrate *= DAMPING
    #angle of attack
    aofa = math.atan2(self.v_speed, self.h_speed)
    aofa = math.radians(self.pitch) - aofa # approximation to sin difference
    lift = self.lift_factor * spsq * aofa
    drag = lift / LD 
    if spsq < 100: #stall!
      lift *= 0.9
      drag *= 1.3

    cos_pitch = math.cos(math.radians(self.pitch))
    sin_pitch = math.sin(math.radians(self.pitch))
    cos_roll = math.cos(math.radians(self.roll))
    sin_roll = math.sin(math.radians(self.roll))
    h_force = (self.power_setting - drag) * cos_pitch - lift * sin_pitch
    v_force = lift * cos_pitch * cos_roll - self.mass * GRAVITY
    h_acc = h_force / self.mass
    v_acc = v_force / self.mass
    self.h_speed += h_acc * dt
    if self.h_speed > self.VNE:
      self.h_speed = self.VNE
    elif self.h_speed < 0:
      self.h_speed = 0
    self.v_speed += v_acc * dt
    if abs(self.v_speed) > self.VNE:
      self.v_speed = math.copysign(self.VNE, self.v_speed)
    turn_force = -lift * sin_roll * 1.5
    radius = self.mass * spsq / turn_force if turn_force != 0.0 else 0.0
    self.yaw = math.sqrt(spsq) / radius if radius != 0.0 else 0.0

  def update_position(self, height):
    #time
    tm = time.time()
    dt = tm - self.last_pos_time
    self.last_pos_time = tm

    self.x += self.h_speed * math.sin(math.radians(self.direction)) * dt
    self.y += self.v_speed * dt
    if self.y < (height + 3):
      self.y = height + 3
      self.v_speed = 0
      self.pitch = 2.5
      #self.roll = 0
    self.z += self.h_speed * math.cos(math.radians(self.direction)) * dt

    self.direction += math.degrees(self.yaw) * dt
    #set values of model
    sin_d = math.sin(math.radians(self.direction))
    cos_d = math.cos(math.radians(self.direction))
    sin_r = math.sin(math.radians(self.roll))
    cos_r = math.cos(math.radians(self.roll))
    sin_p = math.sin(math.radians(self.pitch))
    cos_p = math.cos(math.radians(self.pitch))
    absroll = math.degrees(math.asin(sin_r * cos_d + cos_r * sin_p * sin_d))
    abspitch = math.degrees(math.asin(sin_r * sin_d - cos_r * sin_p * cos_d))
    self.model.position(self.x, self.y, self.z)
    self.model.rotateToX(abspitch)
    self.model.rotateToY(self.direction)
    self.model.rotateToZ(absroll)
    #set values for bullets
    if self.seq_b < self.num_b:
      self.bullets.position(self.x, self.y, self.z)
      self.bullets.rotateToX(abspitch)
      self.bullets.rotateToY(self.direction)
      self.bullets.rotateToZ(absroll)
    #set values for camera
    return (self.x - 10.0 * sin_d, self.y + 4, self.z - 10.0 * cos_d, self.direction)

  def draw(self):
    self.model.draw()
    #draw the bullet sequence if not finished
    if self.seq_b < self.num_b:
      self.bullets.buf[0].textures[0] = BULLET_TEX[self.seq_b]
      self.bullets.draw()
      self.seq_b += 1

#create the instances of Aeroplane
a = Aeroplane("models/biplane.obj", 0.02)
a.z, a.direction = 900, 180
b = Aeroplane("models/biplane.obj", 0.1)
#b is the enemy so give it a flying start (!)
b.set_power(60)
b.x, b.y, b.z, b.h_speed = 4, 1000, -1000, 60
# Load textures for the environment cube
ectex = pi3d.loadECfiles("textures/ecubes", "sbox")
myecube = pi3d.EnvironmentCube(size=7000.0, maptype="FACES", camera=CAMERA)
myecube.set_draw_details(FLATSH, ectex)
myecube.set_fog((0.5,0.5,0.5,0.8), 4000)
# Create elevation map
mapwidth = 10000.0
mapdepth = 10000.0
mapheight = 1000.0
mountimg1 = pi3d.Texture("textures/mountains3_512.jpg")
bumpimg = pi3d.Texture("textures/grasstile_n.jpg")
reflimg = pi3d.Texture("textures/stars.jpg")
mymap = pi3d.ElevationMap("textures/mountainsHgt.jpg", name="map",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32, camera=CAMERA)
mymap.set_draw_details(SHADER, [mountimg1, bumpimg, reflimg], 1024.0, 0.0)
mymap.set_fog((0.5,0.5,0.5,0.8), 4000)

# init events
inputs = pi3d.InputEvents()
inputs.get_mouse_movement()
CAMERA.position((0.0, 0.0, -10.0))
cam_rot, cam_pitch = 0, 0
cam_toggle = True #control mode
"""
mymap.set_shader(STAR)
tm = 0.0
dt = 0.01
sc = 0.0
ds = 0.001
"""
while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  """
  mymap.set_custom_data(48, [tm, sc, -0.5 * sc])
  tm += dt
  sc = (sc + ds) % 10.0
  """
  inputs.do_input_events()
  mx, my, mv, mh, md = inputs.get_mouse_movement()
  if cam_toggle:
    a.set_ailerons(-mx * 0.001)
    a.set_elevator(my * 0.001)
  else:
    cam_rot -= mx * 0.1
    cam_pitch -= my * 0.1
  if inputs.key_state("KEY_W"): #increase throttle
    a.set_power(1)
  if inputs.key_state("KEY_S"): #throttle back
    a.set_power(-1)
  if inputs.key_state("KEY_X"): #jump to enemy!
    a.x, a.y, a.z = b.x, b.y + 5, b.z
  if inputs.key_state("KEY_B"): #brakes
    a.h_speed *= 0.99
  if inputs.key_state("KEY_V"): #view mode
    cam_toggle = False
    a.set_ailerons(0)
    a.set_elevator(0)
  if inputs.key_state("KEY_C"): #control mode
    cam_toggle = True
    cam_rot, cam_pitch = 0, 0
  if inputs.key_state("BTN_LEFT"): #shoot
    a.shoot([b.x, b.y, b.z])

  a.update_variables()
  loc = a.update_position(mymap.calcHeight(a.x, a.z))
  CAMERA.reset()
  #CAMERA.rotate(-20 + cam_pitch, -loc[3] + cam_rot, 0)
  CAMERA.rotate(-20 + cam_pitch, -loc[3] + cam_rot, -a.roll)
  CAMERA.position((loc[0], loc[1], loc[2]))
  a.draw()

  b.update_variables()
  b.home((a.x, a.y, a.z))
  b.update_position(mymap.calcHeight(b.x, b.z))
  b.draw()

  mymap.draw()
  myecube.position(loc[0], loc[1], loc[2])
  myecube.draw()
  #uncomment for cheap and cheerful instruments, make sure you can see terminal!
  #print("speed={0:.2f}, rate of climb={1:.2f}, power={2:.2f},
  #     altitude={3:.2f}".format(a.h_speed, a.v_speed, a.power_setting, a.y))


inputs.release()
DISPLAY.destroy()
