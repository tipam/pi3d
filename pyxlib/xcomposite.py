
import ctypes

from xlib import Window, Display

libXcomposite = ctypes.CDLL('libXcomposite.so.1')


# void XCompositeRedirectSubwindows(Display *dpy, Window window, int update);
XCompositeRedirectSubwindows = libXcomposite.XCompositeRedirectSubwindows
XCompositeRedirectSubwindows.argtypes = [ctypes.POINTER(Display), Window, ctypes.c_int]
# Window XCompositeGetOverlayWindow(Display *dpy, Window window);
XCompositeGetOverlayWindow = libXcomposite.XCompositeGetOverlayWindow
XCompositeGetOverlayWindow.argtypes = [ctypes.POINTER(Display), Window]
XCompositeGetOverlayWindow.restype = Window


#define CompositeRedirectAutomatic		0
CompositeRedirectAutomatic = 0
#define CompositeRedirectManual			1
CompositeRedirectManual = 1

