import math

def sqsum(x, y):
  return x * x + y * y

def distance(x, y):
  return math.sqrt(sqsum(x, y))

class Ball(object):
  def __init__(self, radius, x, y, vx=0.0, vy=0.0, decay=0.001):
    self.radius = radius
    self.x = x
    self.y = y
    self.x = x
    self.vx = vx
    self.vy = vy
    self.mass = radius * 2
    self.decay = decay

  def hit(self,otherball):
    #used for pre-checking ball positions
    dx = (self.x+self.vx)-(otherball.x+otherball.vx)
    dy = (self.y+self.vy)-(otherball.y+otherball.vy)
    rd = self.radius+otherball.radius
    if (dx**2+dy**2) <= (rd**2): return True
    else: return False

  def collisionBounce(self,otherball):
    dx = self.x-otherball.x
    dy = self.y-otherball.y
    rd = self.radius+otherball.radius

    if (dx**2+dy**2) <= (rd**2):
      cangle = math.atan2(dy,dx)
      mag1 = math.sqrt(self.vx**2+self.vy**2)
      mag2 = math.sqrt(otherball.vx**2+otherball.vy**2)
      dir1 = math.atan2(self.vy,self.vx)
      dir2 = math.atan2(otherball.vy,otherball.vx)
      nspx1 = mag1 * math.cos(dir1-cangle)
      nspy1 = mag1 * math.sin(dir1-cangle)
      nspx2 = mag2 * math.cos(dir2-cangle)
      nspy2 = mag2 * math.sin(dir2-cangle)
      fspx1 = ((self.mass-otherball.mass)*nspx1+(otherball.mass*2)*nspx2)/(self.mass+otherball.mass)
      fspx2 = ((self.mass*2)*nspx1+(otherball.mass-self.mass)*nspx2)/(self.mass+otherball.mass)
      fspy1 = nspy1
      fspy2 = nspy2
      self.vx = math.cos(cangle)*fspx1+math.cos(cangle+math.pi*.5)*fspy1
      self.vy = math.sin(cangle)*fspx1+math.sin(cangle+math.pi*.5)*fspy1
      otherball.vx = math.cos(cangle)*fspx2+math.cos(cangle+math.pi*.5)*fspy2
      otherball.vy = math.sin(cangle)*fspx2+math.sin(cangle+math.pi*.5)*fspy2

