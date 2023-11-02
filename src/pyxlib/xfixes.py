
import ctypes

from xlib import Window, Display, XID, XRectangle


libXFixes = ctypes.CDLL('libXfixes.so.3')


# void XFixesHideCursor(Display *dpy, Window window);
XFixesHideCursor = libXFixes.XFixesHideCursor
XFixesHideCursor.argtypes = [ctypes.POINTER(Display), Window]
# XserverRegion XFixesCreateRegion(Display *dpy, XRectangle *rectangles, int nrectangles);
XserverRegion = XID
XFixesCreateRegion = libXFixes.XFixesCreateRegion
XFixesCreateRegion.argtypes = [ctypes.POINTER(Display), ctypes.POINTER(XRectangle), ctypes.c_int]
XFixesCreateRegion.restype = XserverRegion
# void XFixesSetWindowShapeRegion(Display *dpy, Window win, int shape_kind, int x_off, int y_off, XserverRegion region);
XFixesSetWindowShapeRegion = libXFixes.XFixesSetWindowShapeRegion
XFixesSetWindowShapeRegion.argtypes = [ctypes.POINTER(Display), Window, ctypes.c_int, ctypes.c_int, ctypes.c_int, XserverRegion]
# void XFixesDestroyRegion (Display *dpy, XserverRegion region);
XFixesDestroyRegion = libXFixes.XFixesDestroyRegion
XFixesDestroyRegion.argtypes = [ctypes.POINTER(Display), XserverRegion]


#define ShapeBounding		0
ShapeBounding = 0
#define ShapeClip			1
ShapeClip = 1
#define ShapeInput			2
ShapeInput = 2

