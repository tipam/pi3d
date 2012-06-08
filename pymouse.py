import threading

XSIGN = 1<<4
YSIGN = 1<<5

class MouseThread ( threading.Thread ):

    def __init__(self):
        threading.Thread.__init__(self)
        self.fd = open('/dev/input/mouse0','r')
        self.x = 800
        self.y = 400
        self.height=1080
        self.width=1920
        self.finished=False
        self.button=False
        
    def run ( self ):
        while 1:
            while 1:
                buttons,dx,dy=map(ord,self.fd.read(3))
                if buttons&8:
                    break # This bit should always be set
                self.fd.read(1) # Try to sync up again
            if buttons&3:
                self.button=True
                #break  # Stop if mouse button pressed!
            if buttons&XSIGN:
                dx-=256
            if buttons&YSIGN:
                dy-=256
                
            self.x+=dx
            self.y+=dy
            if self.x<0: self.x=0
            if self.y<0: self.y=0
            self.x=min(self.x,self.width)
            self.y=min(self.y,self.height)
            #print self.x,self.y

def start_mouse():
    """Start a thread to read the PS2 mouse stream.

    Returns a mouse object, can get m.x and m.y mouse position"""
    m=MouseThread()
    m.start()
    return m
