#
# Copyright (c) 2012 Peter de Rivaz - mods by Tim Skillman
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.
#
# Raspberry Pi 3d demo using OpenGLES 2.0 via Python
#


import ctypes
import time
import math
import random
import pymouse
import pi3d

# ALL 3D STUFF SHOULD BE DONE IN pi3d - this is just for test purposes

# Define verbose=True to get debug messages
verbose = True
# Pick up our constants extracted from the header files with prepare_constants.py
from egl import *
from gl2 import *
from gl import *
from gl2ext import *

eglint = ctypes.c_int
eglshort = ctypes.c_short
eglfloat = ctypes.c_float

# Open the libraries
bcm = ctypes.CDLL('libbcm_host.so')
opengles = ctypes.CDLL('libGLESv2.so')
openegl = ctypes.CDLL('libEGL.so')

# Define window display size
win_left = 100
win_top = 100
win_width = 600
win_height = 400
	
def eglints(L):
    """Converts a tuple to an array of eglints (would a pointer return be better?)"""
    return (eglint*len(L))(*L)

def eglfloats(L):
    return (eglfloat*len(L))(*L)

class demo():

    def __init__(self):
        

        self.quads = eglfloats(( 
        -10, -10,  10, # front
        10, -10,  10,
        -10,  10,  10,
        10,  10,  10,
        
        -10, -10, -10, #back
        -10,  10, -10,
        10, -10, -10,
        10,  10, -10,
        
        -10, -10,  10, #left
        -10,  10,  10,
        -10, -10, -10,
        -10,  10, -10,
        
        10, -10, -10, #right
        10,  10, -10,
        10, -10,  10,
        10,  10,  10,
        
        -10,  10,  10, #top
        10,  10,  10,
        -10,  10, -10,
        10,  10, -10,
        
        -10, -10,  10, #bottom
        -10, -10, -10,
        10, -10,  10,
        10, -10, -10));
        
        self.colours = eglfloats((
		1.0,  0.0,  0.0,  1.0,
		1.0,  0.0,  0.0,  1.0,
		1.0,  0.0,  0.0,  1.0,
		1.0,  0.0,  0.0,  1.0,
		
		0.0,  1.0,  0.0,  1.0,  # blue
		0.0,  1.0,  0.0,  1.0,
		0.0,  1.0,  0.0,  1.0,
		0.0,  1.0,  0.0,  1.0,
		
		0.0,  0.0,  1.0,  1.0, # green
		0.0,  0.0,  1.0,  1.0,
		0.0,  0.0,  1.0,  1.0,
		0.0,  0.0,  1.0,  1.0,
		
		0.0, 0.5, 0.5,  1.0,  # teal
		0.0, 0.5, 0.5,  1.0,
		0.0, 0.5, 0.5,  1.0,
		0.0, 0.5, 0.5,  1.0,
		
		0.5, 0.5,  0.0,  1.0, # yellow
		0.5, 0.5,  0.0,  1.0,
		0.5, 0.5,  0.0,  1.0,
		0.5, 0.5,  0.0,  1.0,
		
		0.5,  0.0, 0.5,  1.0, # purple
		0.5,  0.0, 0.5,  1.0,
		0.5,  0.0, 0.5,  1.0,
		0.5,  0.0, 0.5,  1.0));
		
        opengles.glClearColor ( eglfloat(0.0), eglfloat(0.7), eglfloat(1.0), eglfloat(1.0) );
        
       
        # Prepare viewport
        opengles.glViewport (0, 0, win_width, win_height)
        opengles.glMatrixMode(GL_PROJECTION)
        opengles.glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
        opengles.glLoadIdentity()
        
        nearp=1.0
        farp=500.0
        hht = 1 * math.tan(45.0 / 2.0 / 180.0 * 3.1415926)
        hwd = 500 * win_width / win_height
        
        opengles.glFrustumf(eglfloat(-hwd), eglfloat(hwd), eglfloat(-hht), eglfloat(hht), eglfloat(nearp), eglfloat(farp))
        
        opengles.glShadeModel(GL_FLAT);

	# Enable back face culling
	opengles.glEnable(GL_CULL_FACE)
	
        # Upload vertex data to a buffer
        opengles.glEnableClientState( GL_VERTEX_ARRAY );
        self.check
        opengles.glVertexPointer( 3, GL_BYTE, 0, ctypes.byref(self.quads) )
        self.check
        
        opengles.glEnableClientState( GL_COLOR_ARRAY );
        opengles.glColorPointer(4, GL_FLOAT, 0, ctypes.byref(self.colours) )
		
        #opengles.glBindBuffer(GL_ARRAY_BUFFER, self.buf);
        #opengles.glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(self.vertex_data),
                             #ctypes.byref(self.vertex_data), GL_STATIC_DRAW);

        
    def draw_triangles(self):

        # Clear the background (not really necessary I suppose)
        opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
        
        opengles.glMatrixMode(GL_MODELVIEW)
        opengles.glLoadIdentity()
        opengles.glTranslatef(eglfloat(0), eglfloat(0), eglfloat(-50))
        
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 0, 4 )
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 4, 4 )
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 8, 4 )
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 12, 4 )
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 16, 4 )
        opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 20, 4 )

        #opengles.glFlush()
        #opengles.glFinish()
        
           
        
    def check(self):
        e=opengles.glGetError()
        if e:
            print hex(e)
            raise ValueError
        
def showerror():
    e=opengles.glGetError()
    print hex(e)
    
if __name__ == "__main__":
    p = pi3d.init_display()
    p.make_display(win_left,win_top,win_width,win_height)
    p.setBackColour(0,0.7,1,1)
    #opengles.glClearColor ( eglfloat(0.0), eglfloat(0.7), eglfloat(1.0), eglfloat(1.0) );
        
    
    #d = demo()
    m=pymouse.start_mouse()
    
    #test for cuboid class ...
    mycuboid = pi3d.create_cuboid(10,5,8)
    mycuboid.scale(2,2,2)
    mycuboid.translate(10,5.5,0)
    print mycuboid.width , mycuboid.y
    
    #display cube (I wish!) ...
    while 1:
        #d.draw_triangles()
	opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	p.swap_buffers() 
        time.sleep(0.01)
	if m.button:
	    print "button", m.x, m.y
	    p.destroy_display()
	    win_left=m.x
	    win_top=m.y
	    p.make_display(win_left,win_top,win_width,win_height)
	    p.setBackColour(0,0.7,1,1)

	    m.button=False
	    
	#if m.finished:
	    #pi3d.destroy_display(p)
	    #win_left += 10
	    #p = pi3d.setup_display(win_left,win_top,win_width,win_height)
            #m.finished = False


    
