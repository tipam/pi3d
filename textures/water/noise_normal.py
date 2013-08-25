import random
import math
from PIL import Image
""" Produce a series of Perlin noise images that tile with each other
and wrap at the end of the sequence. The pixel value are interpreted as
heights and colour values then calculated to represent a normal map.
"""
# values used by the noise function
perm = list(range(256))
random.seed(1)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
     math.cos((a+85) * 2.0 * math.pi / 256),
     math.cos((a+170) * 2.0 * math.pi / 256))
     for a in range(256)]

def noise(x, y, z, per):
  def surflet(gridX, gridY, gridZ):
    distX, distY, distZ = abs(x-gridX), abs(y-gridY), abs(z-gridZ)
    polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
    polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
    polyZ = 1 - 6*distZ**5 + 15*distZ**4 - 10*distZ**3
    hashed = perm[perm[perm[int(gridX)%per] + int(gridY)%per] + int(gridZ)%per]
    grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1] + (z-gridZ)*dirs[hashed][2]
    return polyX * polyY * polyZ * grad
    
  intX, intY, intZ = int(x), int(y), int(z)
  return (surflet(intX+0, intY+0, intZ+0) + surflet(intX+0, intY+0, intZ+1) + surflet(intX+0, intY+1, intZ+0) +
      surflet(intX+0, intY+1, intZ+1) + surflet(intX+1, intY+0, intZ+0) + surflet(intX+1, intY+0, intZ+1) +
      surflet(intX+1, intY+1, intZ+0) + surflet(intX+1, intY+1, intZ+1))
      
def fBm(x, y, z, per, octs):
  val = 0
  for o in range(octs):
    val += 0.5**o * noise(x*2**o, y*2**o, z*2**o, per*2**o)
  return val


""" variables used by the noise file generator:
num -- images in sequence
size -- size to resize each image to
freq -- frequency of noise
octs -- octaves of noise
"""
num = 128
size = 32
freq = 1/8.0
octs = 5
###################################################

for z in range (num):
  data = [] 
  print z 
  for y in range(num):
    for x in range(num):
      data.append(fBm(x*freq, y*freq, z*freq, int(num*freq), octs))
  im_data = []
  for y in range(num):
    for x in range(num):
      rVal = 0.5 + (data[((y+1)%num)*num + x] - data[y*num + x])*0.5
      gVal = 0.5 + (data[y*num + (x+1)%num] - data[y*num + x])*0.5
      bVal = 1.0/math.sqrt(1.0 + rVal**2 + gVal**2)
      im_data.append((int(255*rVal), int(255*gVal), int(255*bVal), 255))
    
  im = Image.new("RGBA", (num, num))
  im.putdata(im_data, 1.0, 0.0)
  im = im.resize((size, size))
  im.save("n_norm"+format(z, '03d')+".png")

print "finished doing it"

