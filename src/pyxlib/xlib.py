from ctypes import (CDLL, c_byte, c_ubyte, c_char, c_wchar, c_int, c_uint,
    c_short, c_ushort, c_long, c_ulong, c_char_p, c_wchar_p, c_void_p,
    Structure, Union, POINTER)
from ctypes.util import find_library
from .x import *

x11_name = find_library('X11')
libX11 = CDLL(x11_name) # was explicitly 'libX11.so.6'

#/*
# *  Xlib.h - Header definition and support file for the C subroutine
# *  interface library (Xlib) to the X Window System Protocol (V11).
# *  Structures and symbols starting with "_" are private to the library.
# */

XlibSpecificationRelease = 6

#~ #ifdef USG
#~ #ifndef __TYPES__
#~ #include <sys/types.h>      /* forgot to protect it... */
#~ #define __TYPES__
#~ #endif /* __TYPES__ */
#~ #else
#~ #if defined(_POSIX_SOURCE) && defined(MOTOROLA)
#~ #undef _POSIX_SOURCE
#~ #include <sys/types.h>
#~ #define _POSIX_SOURCE
#~ #else
#~ #include <sys/types.h>
#~ #endif
#~ #endif /* USG */

#~ #if defined(__SCO__) || defined(__UNIXWARE__)
#~ #include <stdint.h>
#~ #endif

#~ #include <X11/X.h>

#/* applications should not depend on these two headers being included! */
#~ #include <X11/Xfuncproto.h>
#~ #include <X11/Xosdefs.h>

#~ #ifndef X_WCHAR
#~ #ifdef X_NOT_STDC_ENV
#~ #ifndef ISC
#~ #define X_WCHAR
#~ #endif
#~ #endif
#~ #endif

#~ #ifndef X_WCHAR
#~ #include <stddef.h>
#~ #else
#~ #ifdef __UNIXOS2__
#~ #include <stdlib.h>
#~ #else
#~ /* replace this with #include or typedef appropriate for your system */
#~ typedef unsigned long wchar_t;
#~ #endif
#~ #endif

#~ #if defined(ISC) && defined(USE_XMBTOWC)
#~ #define wctomb(a,b)  _Xwctomb(a,b)
#~ #define mblen(a,b)  _Xmblen(a,b)
#~ #ifndef USE_XWCHAR_STRING
#~ #define mbtowc(a,b,c)  _Xmbtowc(a,b,c)
#~ #endif
#~ #endif

#~ extern int
#~ _Xmblen(
#~ #ifdef ISC
    #~ char const *str,
    #~ size_t len
#~ #else
    #~ char *str,
    #~ int len
#~ #endif
    #~ );

#/* API mentioning "UTF8" or "utf8" is an XFree86 extension, introduced in
#   November 2000. Its presence is indicated through the following macro. */
X_HAVE_UTF8_STRING = 1

#typedef char *XPointer;
XPointer = c_char_p

#define Bool int
Bool = c_int

#define Status int
Status = c_int

#~ #define True 1
#~ #define False 0

QueuedAlready = 0
QueuedAfterReading = 1
QueuedAfterFlush = 2

#define ConnectionNumber(dpy)   (((_XPrivDisplay)dpy)->fd)
#define RootWindow(dpy, scr)   (ScreenOfDisplay(dpy,scr)->root)
#define DefaultScreen(dpy)   (((_XPrivDisplay)dpy)->default_screen)
#define DefaultRootWindow(dpy)   (ScreenOfDisplay(dpy,DefaultScreen(dpy))->root)
#define DefaultVisual(dpy, scr) (ScreenOfDisplay(dpy,scr)->root_visual)
#define DefaultGC(dpy, scr)   (ScreenOfDisplay(dpy,scr)->default_gc)
#define BlackPixel(dpy, scr)   (ScreenOfDisplay(dpy,scr)->black_pixel)
#define WhitePixel(dpy, scr)   (ScreenOfDisplay(dpy,scr)->white_pixel)
#define AllPlanes     ((unsigned long)~0L)
#define QLength(dpy)     (((_XPrivDisplay)dpy)->qlen)
#define DisplayWidth(dpy, scr)   (ScreenOfDisplay(dpy,scr)->width)
#define DisplayHeight(dpy, scr) (ScreenOfDisplay(dpy,scr)->height)
#define DisplayWidthMM(dpy, scr)(ScreenOfDisplay(dpy,scr)->mwidth)
#define DisplayHeightMM(dpy, scr)(ScreenOfDisplay(dpy,scr)->mheight)
#define DisplayPlanes(dpy, scr) (ScreenOfDisplay(dpy,scr)->root_depth)
#define DisplayCells(dpy, scr)   (DefaultVisual(dpy,scr)->map_entries)
#define ScreenCount(dpy)   (((_XPrivDisplay)dpy)->nscreens)
#define ServerVendor(dpy)   (((_XPrivDisplay)dpy)->vendor)
#define ProtocolVersion(dpy)   (((_XPrivDisplay)dpy)->proto_major_version)
#define ProtocolRevision(dpy)   (((_XPrivDisplay)dpy)->proto_minor_version)
#define VendorRelease(dpy)   (((_XPrivDisplay)dpy)->release)
#define DisplayString(dpy)   (((_XPrivDisplay)dpy)->display_name)
#define DefaultDepth(dpy, scr)   (ScreenOfDisplay(dpy,scr)->root_depth)
#define DefaultColormap(dpy, scr)(ScreenOfDisplay(dpy,scr)->cmap)
#define BitmapUnit(dpy)   (((_XPrivDisplay)dpy)->bitmap_unit)
#define BitmapBitOrder(dpy)   (((_XPrivDisplay)dpy)->bitmap_bit_order)
#define BitmapPad(dpy)     (((_XPrivDisplay)dpy)->bitmap_pad)
#define ImageByteOrder(dpy)   (((_XPrivDisplay)dpy)->byte_order)
#ifdef CRAY /* unable to get WORD64 without pulling in other symbols */
#define NextRequest(dpy)  XNextRequest(dpy)
#else
#define NextRequest(dpy)  (((_XPrivDisplay)dpy)->request + 1)
#endif
#define LastKnownRequestProcessed(dpy)  (((_XPrivDisplay)dpy)->last_request_read)

#/* macros for screen oriented applications (toolkit) */

#define ScreenOfDisplay(dpy, scr)(&((_XPrivDisplay)dpy)->screens[scr])
#define DefaultScreenOfDisplay(dpy) ScreenOfDisplay(dpy,DefaultScreen(dpy))
#define DisplayOfScreen(s)  ((s)->display)
#define RootWindowOfScreen(s)  ((s)->root)
#define BlackPixelOfScreen(s)  ((s)->black_pixel)
#define WhitePixelOfScreen(s)  ((s)->white_pixel)
#define DefaultColormapOfScreen(s)((s)->cmap)
#define DefaultDepthOfScreen(s)  ((s)->root_depth)
#define DefaultGCOfScreen(s)  ((s)->default_gc)
#define DefaultVisualOfScreen(s)((s)->root_visual)
#define WidthOfScreen(s)  ((s)->width)
#define HeightOfScreen(s)  ((s)->height)
#define WidthMMOfScreen(s)  ((s)->mwidth)
#define HeightMMOfScreen(s)  ((s)->mheight)
#define PlanesOfScreen(s)  ((s)->root_depth)
#define CellsOfScreen(s)  (DefaultVisualOfScreen((s))->map_entries)
#define MinCmapsOfScreen(s)  ((s)->min_maps)
#define MaxCmapsOfScreen(s)  ((s)->max_maps)
#define DoesSaveUnders(s)  ((s)->save_unders)
#define DoesBackingStore(s)  ((s)->backing_store)
#define EventMaskOfScreen(s)  ((s)->root_input_mask)

#/*
# * Extensions need a way to hang private data on some structures.
# */
#~ typedef struct _XExtData {
  #~ int number;    /* number returned by XRegisterExtension */
  #~ struct _XExtData *next;  /* next item on list of data for structure */
  #~ int (*free_private)(  /* called to free private storage */
  #~ struct _XExtData *extension
  #~ );
  #~ XPointer private_data;  /* data private to this extension. */
#~ } XExtData;
class _XExtData(Structure): pass
_XExtData._fields_ = [
  ('number', c_int),
  ('next', POINTER(_XExtData)),
  ('free_private', c_void_p),
  ('private_data', XPointer),
]
XExtData = _XExtData

#/*
# * This file contains structures used by the extension mechanism.
# */
#~ typedef struct {    /* public to extension, cannot be changed */
  #~ int extension;    /* extension number */
  #~ int major_opcode;  /* major op-code assigned by server */
  #~ int first_event;  /* first event number for the extension */
  #~ int first_error;  /* first error number for the extension */
#~ } XExtCodes;
class XExtCodes(Structure):
  _fields_ = [
    ('extension', c_int),
    ('major_opcode', c_int),
    ('first_event', c_int),
    ('first_error', c_int),
  ]

#/*
# * Data structure for retrieving info about pixmap formats.
# */

#~ typedef struct {
    #~ int depth;
    #~ int bits_per_pixel;
    #~ int scanline_pad;
#~ } XPixmapFormatValues;
class XPixmapFormatValues(Structure):
  _fields_ = [
    ('depth', c_int),
    ('bits_per_pixel', c_int),
    ('scanline_pad', c_int),
  ]

#/*
# * Data structure for setting graphics context.
# */
#~ typedef struct {
  #~ int function;    /* logical operation */
  #~ unsigned long plane_mask;/* plane mask */
  #~ unsigned long foreground;/* foreground pixel */
  #~ unsigned long background;/* background pixel */
  #~ int line_width;    /* line width */
  #~ int line_style;     /* LineSolid, LineOnOffDash, LineDoubleDash */
  #~ int cap_style;      /* CapNotLast, CapButt,
           #~ CapRound, CapProjecting */
  #~ int join_style;     /* JoinMiter, JoinRound, JoinBevel */
  #~ int fill_style;     /* FillSolid, FillTiled,
           #~ FillStippled, FillOpaeueStippled */
  #~ int fill_rule;      /* EvenOddRule, WindingRule */
  #~ int arc_mode;    /* ArcChord, ArcPieSlice */
  #~ Pixmap tile;    /* tile pixmap for tiling operations */
  #~ Pixmap stipple;    /* stipple 1 plane pixmap for stipping */
  #~ int ts_x_origin;  /* offset for tile or stipple operations */
  #~ int ts_y_origin;
        #~ Font font;          /* default text font for text operations */
  #~ int subwindow_mode;     /* ClipByChildren, IncludeInferiors */
  #~ Bool graphics_exposures;/* boolean, should exposures be generated */
  #~ int clip_x_origin;  /* origin for clipping */
  #~ int clip_y_origin;
  #~ Pixmap clip_mask;  /* bitmap clipping; other calls for rects */
  #~ int dash_offset;  /* patterned/dashed line information */
  #~ char dashes;
#~ } XGCValues;
class XGCValues(Structure):
  _fields_ = [
    ('function', c_int),
    ('plane_mask', c_ulong),
    ('foreground', c_ulong),
    ('background', c_ulong),
    ('line_width', c_int),
    ('line_style', c_int),
    ('cap_style', c_int),
    ('join_style', c_int),
    ('fill_style', c_int),
    ('fill_rule', c_int),
    ('arc_mode', c_int),
    ('tile', Pixmap),
    ('stipple', Pixmap),
    ('ts_x_origin', c_int),
    ('ts_y_origin', c_int),
    ('font', Font),
    ('subwindow_mode', c_int),
    ('graphics_exposures', Bool),
    ('clip_x_origin', c_int),
    ('clip_y_origin', c_int),
    ('clip_mask', Pixmap),
    ('dash_offset', c_int),
    ('dashes', c_char),
  ]

#/*
# * Graphics context.  The contents of this structure are implementation
# * dependent.  A GC should be treated as opaque by application code.
# */

#~ typedef struct _XGC
#~ #ifdef XLIB_ILLEGAL_ACCESS
#~ {
    #~ XExtData *ext_data;  /* hook for extension to hang data */
    #~ GContext gid;  /* protocol ID for graphics context */
    #~ /* there is more to this structure, but it is private to Xlib */
#~ }
#~ #endif
#~ *GC;
class _XGC(Structure):
  _fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('gid', GContext),
  ]
GC = POINTER(_XGC)

#/*
# * Visual structure; contains information about colormapping possible.
# */
#~ typedef struct {
  #~ XExtData *ext_data;  /* hook for extension to hang data */
  #~ VisualID visualid;  /* visual id of this visual */
#~ #if defined(__cplusplus) || defined(c_plusplus)
  #~ int c_class;    /* C++ class of screen (monochrome, etc.) */
#~ #else
  #~ int class;    /* class of screen (monochrome, etc.) */
#~ #endif
  #~ unsigned long red_mask, green_mask, blue_mask;  /* mask values */
  #~ int bits_per_rgb;  /* log base 2 of distinct color values */
  #~ int map_entries;  /* color map entries */
#~ } Visual;
class Visual(Structure):
  _fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('visualid', VisualID),
    ('c_class', c_int),
    ('red_mask', c_ulong),
    ('green_mask', c_ulong),
    ('blue_mask', c_ulong),
    ('bits_per_rgb', c_int),
    ('map_entries', c_int),
  ]

#/*
# * Depth structure; contains information for each possible depth.
# */
#~ typedef struct {
  #~ int depth;    /* this depth (Z) of the depth */
  #~ int nvisuals;    /* number of Visual types at this depth */
  #~ Visual *visuals;  /* list of visuals possible at this depth */
#~ } Depth;
class Depth(Structure):
  _fields_ = [
    ('depth', c_int),
    ('nvisuals', c_int),
    ('visuals', POINTER(Visual)),
  ]

#/*
# * Information about the screen.  The contents of this structure are
# * implementation dependent.  A Screen should be treated as opaque
# * by application code.
# */

#~ struct _XDisplay;    /* Forward declare before use for C++ */
class _XDisplay(Structure): pass
#_XDisplay._pack_ = 1

#~ typedef struct {
  #~ XExtData *ext_data;  /* hook for extension to hang data */
  #~ struct _XDisplay *display;/* back pointer to display structure */
  #~ Window root;    /* Root window id. */
  #~ int width, height;  /* width and height of screen */
  #~ int mwidth, mheight;  /* width and height of  in millimeters */
  #~ int ndepths;    /* number of depths possible */
  #~ Depth *depths;    /* list of allowable depths on the screen */
  #~ int root_depth;    /* bits per pixel */
  #~ Visual *root_visual;  /* root visual */
  #~ GC default_gc;    /* GC for the root root visual */
  #~ Colormap cmap;    /* default color map */
  #~ unsigned long white_pixel;
  #~ unsigned long black_pixel;  /* White and Black pixel values */
  #~ int max_maps, min_maps;  /* max and min color maps */
  #~ int backing_store;  /* Never, WhenMapped, Always */
  #~ Bool save_unders;
  #~ long root_input_mask;  /* initial root input mask */
#~ } Screen;
class Screen(Structure):
  _fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('display', POINTER(_XDisplay)),
    ('root', Window),
    ('width', c_int),
    ('height', c_int),
    ('mwidth', c_int),
    ('mheight', c_int),
    ('ndepths', c_int),
    ('depths', POINTER(Depth)),
    ('root_depth', c_int),
    ('root_visual', POINTER(Visual)),
    ('default_gc', GC),
    ('cmap', Colormap),
    ('white_pixel', c_ulong),
    ('black_pixel', c_ulong),
    ('max_maps', c_int),
    ('min_maps', c_int),
    ('backing_store', c_int),
    ('save_unders', Bool),
    ('root_input_mask', c_long),
  ]

#/*
# * Format structure; describes ZFormat data the screen will understand.
# */
#~ typedef struct {
  #~ XExtData *ext_data;  /* hook for extension to hang data */
  #~ int depth;    /* depth of this image format */
  #~ int bits_per_pixel;  /* bits/pixel at this depth */
  #~ int scanline_pad;  /* scanline must padded to this multiple */
#~ } ScreenFormat;
class ScreenFormat(Structure):
  _fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('depth', c_int),
    ('bits_per_pixel', c_int),
    ('scanline_pad', c_int),
  ]

#/*
# * Data structure for setting window attributes.
# */
#~ typedef struct {
    #~ Pixmap background_pixmap;  /* background or None or ParentRelative */
    #~ unsigned long background_pixel;  /* background pixel */
    #~ Pixmap border_pixmap;  /* border of the window */
    #~ unsigned long border_pixel;  /* border pixel value */
    #~ int bit_gravity;    /* one of bit gravity values */
    #~ int win_gravity;    /* one of the window gravity values */
    #~ int backing_store;    /* NotUseful, WhenMapped, Always */
    #~ unsigned long backing_planes;/* planes to be preseved if possible */
    #~ unsigned long backing_pixel;/* value to use in restoring planes */
    #~ Bool save_under;    /* should bits under be saved? (popups) */
    #~ long event_mask;    /* set of events that should be saved */
    #~ long do_not_propagate_mask;  /* set of events that should not propagate */
    #~ Bool override_redirect;  /* boolean value for override-redirect */
    #~ Colormap colormap;    /* color map to be associated with window */
    #~ Cursor cursor;    /* cursor to be displayed (or None) */
#~ } XSetWindowAttributes;
class XSetWindowAttributes(Structure):
  _fields_ = [
    ('background_pixmap', Pixmap),
    ('background_pixel', c_ulong),
    ('border_pixmap', Pixmap),
    ('border_pixel', c_ulong),
    ('bit_gravity', c_int),
    ('win_gravity', c_int),
    ('backing_store', c_int),
    ('backing_planes', c_ulong),
    ('backing_pixel', c_ulong),
    ('save_under', Bool),
    ('event_mask', c_long),
    ('do_not_propagate_mask', c_long),
    ('override_redirect', Bool),
    ('colormap', Colormap),
    ('cursor', Cursor),
  ]

#~ typedef struct {
    #~ int x, y;      /* location of window */
    #~ int width, height;    /* width and height of window */
    #~ int border_width;    /* border width of window */
    #~ int depth;            /* depth of window */
    #~ Visual *visual;    /* the associated visual structure */
    #~ Window root;          /* root of screen containing window */
#~ #if defined(__cplusplus) || defined(c_plusplus)
    #~ int c_class;    /* C++ InputOutput, InputOnly*/
#~ #else
    #~ int class;      /* InputOutput, InputOnly*/
#~ #endif
    #~ int bit_gravity;    /* one of bit gravity values */
    #~ int win_gravity;    /* one of the window gravity values */
    #~ int backing_store;    /* NotUseful, WhenMapped, Always */
    #~ unsigned long backing_planes;/* planes to be preserved if possible */
    #~ unsigned long backing_pixel;/* value to be used when restoring planes */
    #~ Bool save_under;    /* boolean, should bits under be saved? */
    #~ Colormap colormap;    /* color map to be associated with window */
    #~ Bool map_installed;    /* boolean, is color map currently installed*/
    #~ int map_state;    /* IsUnmapped, IsUnviewable, IsViewable */
    #~ long all_event_masks;  /* set of events all people have interest in*/
    #~ long your_event_mask;  /* my event mask */
    #~ long do_not_propagate_mask; /* set of events that should not propagate */
    #~ Bool override_redirect;  /* boolean value for override-redirect */
    #~ Screen *screen;    /* back pointer to correct screen */
#~ } XWindowAttributes;
class XWindowAttributes(Structure):
  _fields_ = [
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('depth', c_int),
    ('visual', POINTER(Visual)),
    ('root', Window),
    ('c_class', c_int),
    ('bit_gravity', c_int),
    ('win_gravity', c_int),
    ('backing_store', c_int),
    ('backing_planes', c_ulong),
    ('backing_pixel', c_ulong),
    ('save_under', Bool),
    ('colormap', Colormap),
    ('map_installed', Bool),
    ('map_state', c_int),
    ('all_event_masks', c_long),
    ('your_event_mask', c_long),
    ('do_not_propagate_mask', c_long),
    ('override_redirect', Bool),
    ('screen', POINTER(Screen)),
  ]

#/*
# * Data structure for host setting; getting routines.
# *
# */

#~ typedef struct {
  #~ int family;    /* for example FamilyInternet */
  #~ int length;    /* length of address, in bytes */
  #~ char *address;    /* pointer to where to find the bytes */
#~ } XHostAddress;
class XHostAddress(Structure):
  _fields_ = [
    ('family', c_int),
    ('length', c_int),
    ('address', c_char_p),
  ]

#/*
# * Data structure for ServerFamilyInterpreted addresses in host routines
# */
#~ typedef struct {
  #~ int typelength;    /* length of type string, in bytes */
  #~ int valuelength;  /* length of value string, in bytes */
  #~ char *type;    /* pointer to where to find the type string */
  #~ char *value;    /* pointer to where to find the address */
#~ } XServerInterpretedAddress;
class XServerInterpretedAddress(Structure):
  _fields_ = [
    ('typelength', c_int),
    ('valuelength', c_int),
    ('type', c_char_p),
    ('value', c_char_p),
  ]

#/*
# * Data structure for "image" data, used by image manipulation routines.
# */
#~ typedef struct _XImage {
    #~ int width, height;    /* size of image */
    #~ int xoffset;    /* number of pixels offset in X direction */
    #~ int format;      /* XYBitmap, XYPixmap, ZPixmap */
    #~ char *data;      /* pointer to image data */
    #~ int byte_order;    /* data byte order, LSBFirst, MSBFirst */
    #~ int bitmap_unit;    /* quant. of scanline 8, 16, 32 */
    #~ int bitmap_bit_order;  /* LSBFirst, MSBFirst */
    #~ int bitmap_pad;    /* 8, 16, 32 either XY or ZPixmap */
    #~ int depth;      /* depth of image */
    #~ int bytes_per_line;    /* accelarator to next line */
    #~ int bits_per_pixel;    /* bits per pixel (ZPixmap) */
    #~ unsigned long red_mask;  /* bits in z arrangment */
    #~ unsigned long green_mask;
    #~ unsigned long blue_mask;
    #~ XPointer obdata;    /* hook for the object routines to hang on */
    #~ struct funcs {    /* image manipulation routines */
  #~ struct _XImage *(*create_image)(
    #~ struct _XDisplay* /* display */,
    #~ Visual*    /* visual */,
    #~ unsigned int  /* depth */,
    #~ int    /* format */,
    #~ int    /* offset */,
    #~ char*    /* data */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int    /* bitmap_pad */,
    #~ int    /* bytes_per_line */);
  #~ int (*destroy_image)        (struct _XImage *);
  #~ unsigned long (*get_pixel)  (struct _XImage *, int, int);
  #~ int (*put_pixel)            (struct _XImage *, int, int, unsigned long);
  #~ struct _XImage *(*sub_image)(struct _XImage *, int, int, unsigned int, unsigned int);
  #~ int (*add_pixel)            (struct _XImage *, long);
  #~ } f;
#~ } XImage;
class funcs(Structure):
  _fields_ = [
    ('create_image', c_void_p),
    ('destroy_image', c_void_p),
    ('get_pixel', c_void_p),
    ('put_pixel', c_void_p),
    ('sub_image', c_void_p),
    ('add_pixel', c_void_p),
  ]

class _XImage(Structure): pass
_XImage._fields_ = [
  ('width', c_int),
  ('height', c_int),
  ('xoffset', c_int),
  ('format', c_int),
  ('data', c_void_p),
  ('byte_order', c_int),
  ('bitmap_unit', c_int),
  ('bitmap_bit_order', c_int),
  ('bitmap_pad', c_int),
  ('depth', c_int),
  ('bytes_per_line', c_int),
  ('bits_per_pixel', c_int),
  ('red_mask', c_ulong),
  ('green_mask', c_ulong),
  ('blue_mask', c_ulong),
  ('obdata', XPointer),
  ('f', funcs),
]
XImage = _XImage

#/*
# * Data structure for XReconfigureWindow
# */
#~ typedef struct {
    #~ int x, y;
    #~ int width, height;
    #~ int border_width;
    #~ Window sibling;
    #~ int stack_mode;
#~ } XWindowChanges;
class XWindowChanges(Structure):
  _fields_ = [
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('sibling', Window),
    ('stack_mode', c_int),
  ]

#/*
# * Data structure used by color operations
# */
#~ typedef struct {
  #~ unsigned long pixel;
  #~ unsigned short red, green, blue;
  #~ char flags;  /* do_red, do_green, do_blue */
  #~ char pad;
#~ } XColor;
class XColor(Structure):
  _fields_ = [
    ('pixel', c_ulong),
    ('red', c_ushort),
    ('green', c_ushort),
    ('blue', c_ushort),
    ('flags', c_byte),
    ('pad', c_byte),
  ]

#/*
# * Data structures for graphics operations.  On most machines, these are
# * congruent with the wire protocol structures, so reformatting the data
# * can be avoided on these architectures.
# */
#~ typedef struct {
    #~ short x1, y1, x2, y2;
#~ } XSegment;
class XSegment(Structure):
  _fields_ = [
    ('x1', c_short),
    ('y1', c_short),
    ('x2', c_short),
    ('y2', c_short),
  ]

#~ typedef struct {
    #~ short x, y;
#~ } XPoint;
class XPoint(Structure):
  _fields_ = [
    ('x', c_short),
    ('y', c_short),
  ]

#~ typedef struct {
    #~ short x, y;
    #~ unsigned short width, height;
#~ } XRectangle;
class XRectangle(Structure):
  _fields_ = [
    ('x', c_short),
    ('y', c_short),
    ('width', c_ushort),
    ('height', c_ushort),
  ]

#~ typedef struct {
    #~ short x, y;
    #~ unsigned short width, height;
    #~ short angle1, angle2;
#~ } XArc;
class XArc(Structure):
  _fields_ = [
    ('x', c_short),
    ('y', c_short),
    ('width', c_ushort),
    ('height', c_ushort),
    ('angle1', c_short),
    ('angle2', c_short),
  ]

#/* Data structure for XChangeKeyboardControl */

#~ typedef struct {
        #~ int key_click_percent;
        #~ int bell_percent;
        #~ int bell_pitch;
        #~ int bell_duration;
        #~ int led;
        #~ int led_mode;
        #~ int key;
        #~ int auto_repeat_mode;   /* On, Off, Default */
#~ } XKeyboardControl;
class XKeyboardControl(Structure):
  _fields_ = [
    ('key_click_percent', c_int),
    ('bell_percent', c_int),
    ('bell_pitch', c_int),
    ('bell_duration', c_int),
    ('led', c_int),
    ('led_mode', c_int),
    ('key', c_int),
    ('auto_repeat_mode', c_int),
  ]

#/* Data structure for XGetKeyboardControl */

#~ typedef struct {
        #~ int key_click_percent;
  #~ int bell_percent;
  #~ unsigned int bell_pitch, bell_duration;
  #~ unsigned long led_mask;
  #~ int global_auto_repeat;
  #~ char auto_repeats[32];
#~ } XKeyboardState;
class XKeyboardState(Structure):
  _fields_ = [
    ('key_click_percent', c_int),
    ('bell_percent', c_int),
    ('bell_pitch', c_uint),
    ('bell_duration', c_uint),
    ('led_mask', c_ulong),
    ('global_auto_repeat', c_int),
    ('auto_repeats', c_char * 32),
  ]

#/* Data structure for XGetMotionEvents.  */

#~ typedef struct {
        #~ Time time;
  #~ short x, y;
#~ } XTimeCoord;
class XTimeCoord(Structure):
  _fields_ = [
    ('time', Time),
    ('x', c_short),
    ('y', c_short),
  ]

#/* Data structure for X{Set,Get}ModifierMapping */

#~ typedef struct {
   #~ int max_keypermod;  /* The server's max # of keys per modifier */
   #~ KeyCode *modifiermap;  /* An 8 by max_keypermod array of modifiers */
#~ } XModifierKeymap;
class XModifierKeymap(Structure):
  _fields_ = [
    ('max_keypermod', c_int),
    ('modifiermap', POINTER(KeyCode)),
  ]

#/*
# * Display datatype maintaining display specific data.
# * The contents of this structure are implementation dependent.
# * A Display should be treated as opaque by application code.
# */
#ifndef XLIB_ILLEGAL_ACCESS
#~ typedef struct _XDisplay Display;
#endif

#~ struct _XPrivate;    /* Forward declare before use for C++ */
class _XPrivate(Structure): pass

#~ struct _XrmHashBucketRec;
class _XrmHashBucketRec(Structure): pass

#~ typedef struct
#~ #ifdef XLIB_ILLEGAL_ACCESS
#~ _XDisplay
#~ #endif
#~ {
  #~ XExtData *ext_data;  /* hook for extension to hang data */
  #~ struct _XPrivate *private1;
  #~ int fd;      /* Network socket. */
  #~ int private2;
  #~ int proto_major_version;/* major version of server's X protocol */
  #~ int proto_minor_version;/* minor version of servers X protocol */
  #~ char *vendor;    /* vendor of the server hardware */
        #~ XID private3;
  #~ XID private4;
  #~ XID private5;
  #~ int private6;
  #~ XID (*resource_alloc)(  /* allocator function */
    #~ struct _XDisplay*
  #~ );
  #~ int byte_order;    /* screen byte order, LSBFirst, MSBFirst */
  #~ int bitmap_unit;  /* padding and data requirements */
  #~ int bitmap_pad;    /* padding requirements on bitmaps */
  #~ int bitmap_bit_order;  /* LeastSignificant or MostSignificant */
  #~ int nformats;    /* number of pixmap formats in list */
  #~ ScreenFormat *pixmap_format;  /* pixmap format list */
  #~ int private8;
  #~ int release;    /* release of the server */
  #~ struct _XPrivate *private9, *private10;
  #~ int qlen;    /* Length of input event queue */
  #~ unsigned long last_request_read; /* seq number of last event read */
  #~ unsigned long request;  /* sequence number of last request. */
  #~ XPointer private11;
  #~ XPointer private12;
  #~ XPointer private13;
  #~ XPointer private14;
  #~ unsigned max_request_size; /* maximum number 32 bit words in request*/
  #~ struct _XrmHashBucketRec *db;
  #~ int (*private15)(
    #~ struct _XDisplay*
    #~ );
  #~ char *display_name;  /* "host:display" string used on this connect*/
  #~ int default_screen;  /* default screen for operations */
  #~ int nscreens;    /* number of screens on this server*/
  #~ Screen *screens;  /* pointer to list of screens */
  #~ unsigned long motion_buffer;  /* size of motion buffer */
  #~ unsigned long private16;
  #~ int min_keycode;  /* minimum defined keycode */
  #~ int max_keycode;  /* maximum defined keycode */
  #~ XPointer private17;
  #~ XPointer private18;
  #~ int private19;
  #~ char *xdefaults;  /* contents of defaults from server */
  #~ /* there is more to this structure, but it is private to Xlib */
#~ }
#~ #ifdef XLIB_ILLEGAL_ACCESS
#~ Display,
#~ #endif
#~ *_XPrivDisplay;
_XDisplay._fields_ = [
  ('ext_data', POINTER(XExtData)),
  ('private1', POINTER(_XPrivate)),
  ('fd', c_int),
  ('private2', c_int),
  ('proto_major_version', c_int),
  ('proto_minor_version', c_int),
  ('vendor', c_char_p),
  ('private3', XID),
  ('private4', XID),
  ('private5', XID),
  ('private6', c_int),
  ('resource_alloc', c_void_p),
  ('byte_order', c_int),
  ('bitmap_unit', c_int),
  ('bitmap_pad', c_int),
  ('bitmap_bit_order', c_int),
  ('nformats', c_int),
  ('pixmap_format', POINTER(ScreenFormat)),
  ('private8', c_int),
  ('release', c_int),
  ('private9', POINTER(_XPrivate)),
  ('private10', POINTER(_XPrivate)),
  ('qlen', c_int),
  ('last_request_read', c_ulong),
  ('request', c_ulong),
  ('private11', XPointer),
  ('private12', XPointer),
  ('private13', XPointer),
  ('private14', XPointer),
  ('max_request_size', c_uint),
  ('db', POINTER(_XrmHashBucketRec)),
  ('private15', c_void_p),
  ('display_name', c_char_p),
  ('default_screen', c_int),
  ('nscreens', c_int),
  ('screens', POINTER(Screen)),
  ('motion_buffer', c_ulong),
  ('private16', c_ulong),
  ('min_keycode', c_int),
  ('max_keycode', c_int),
  ('private17', XPointer),
  ('private18', XPointer),
  ('private19', c_int),
  ('xdefaults', c_char_p),
]
Display = _XDisplay
_XPrivDisplay = POINTER(_XDisplay)

#undef _XEVENT_
#ifndef _XEVENT_
#/*
# * Definitions of specific events.
# */
#~ typedef struct {
  #~ int type;    /* of event */
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;          /* "event" window it is reported relative to */
  #~ Window root;          /* root window that the event occurred on */
  #~ Window subwindow;  /* child window */
  #~ Time time;    /* milliseconds */
  #~ int x, y;    /* pointer x, y coordinates in event window */
  #~ int x_root, y_root;  /* coordinates relative to root */
  #~ unsigned int state;  /* key or button mask */
  #~ unsigned int keycode;  /* detail */
  #~ Bool same_screen;  /* same screen flag */
#~ } XKeyEvent;
#~ typedef XKeyEvent XKeyPressedEvent;
#~ typedef XKeyEvent XKeyReleasedEvent;
class XKeyEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('keycode', c_uint),
    ('same_screen', Bool),
  ]
XKeyPressedEvent = XKeyEvent
XKeyReleasedEvent = XKeyEvent

#~ typedef struct {
  #~ int type;    /* of event */
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;          /* "event" window it is reported relative to */
  #~ Window root;          /* root window that the event occurred on */
  #~ Window subwindow;  /* child window */
  #~ Time time;    /* milliseconds */
  #~ int x, y;    /* pointer x, y coordinates in event window */
  #~ int x_root, y_root;  /* coordinates relative to root */
  #~ unsigned int state;  /* key or button mask */
  #~ unsigned int button;  /* detail */
  #~ Bool same_screen;  /* same screen flag */
#~ } XButtonEvent;
#~ typedef XButtonEvent XButtonPressedEvent;
#~ typedef XButtonEvent XButtonReleasedEvent;
class XButtonEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('button', c_uint),
    ('same_screen', Bool),
  ]
XButtonPressedEvent = XButtonEvent
XButtonReleasedEvent = XButtonEvent

#~ typedef struct {
  #~ int type;    /* of event */
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;          /* "event" window reported relative to */
  #~ Window root;          /* root window that the event occurred on */
  #~ Window subwindow;  /* child window */
  #~ Time time;    /* milliseconds */
  #~ int x, y;    /* pointer x, y coordinates in event window */
  #~ int x_root, y_root;  /* coordinates relative to root */
  #~ unsigned int state;  /* key or button mask */
  #~ char is_hint;    /* detail */
  #~ Bool same_screen;  /* same screen flag */
#~ } XMotionEvent;
#~ typedef XMotionEvent XPointerMovedEvent;
class XMotionEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('state', c_uint),
    ('is_hint', c_char),
    ('same_screen', Bool),
  ]
XPointerMovedEvent = XMotionEvent

#~ typedef struct {
  #~ int type;    /* of event */
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;          /* "event" window reported relative to */
  #~ Window root;          /* root window that the event occurred on */
  #~ Window subwindow;  /* child window */
  #~ Time time;    /* milliseconds */
  #~ int x, y;    /* pointer x, y coordinates in event window */
  #~ int x_root, y_root;  /* coordinates relative to root */
  #~ int mode;    /* NotifyNormal, NotifyGrab, NotifyUngrab */
  #~ int detail;
  #~ /*
   #~ * NotifyAncestor, NotifyVirtual, NotifyInferior,
   #~ * NotifyNonlinear,NotifyNonlinearVirtual
   #~ */
  #~ Bool same_screen;  /* same screen flag */
  #~ Bool focus;    /* boolean focus */
  #~ unsigned int state;  /* key or button mask */
#~ } XCrossingEvent;
#~ typedef XCrossingEvent XEnterWindowEvent;
#~ typedef XCrossingEvent XLeaveWindowEvent;
class XCrossingEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('root', Window),
    ('subwindow', Window),
    ('time', Time),
    ('x', c_int),
    ('y', c_int),
    ('x_root', c_int),
    ('y_root', c_int),
    ('mode', c_int),
    ('detail', c_int),
    ('same_screen', Bool),
    ('focus', Bool),
    ('state', c_uint),
  ]
XEnterWindowEvent = XCrossingEvent
XLeaveWindowEvent = XCrossingEvent

#~ typedef struct {
  #~ int type;    /* FocusIn or FocusOut */
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;    /* window of event */
  #~ int mode;    /* NotifyNormal, NotifyWhileGrabbed,
           #~ NotifyGrab, NotifyUngrab */
  #~ int detail;
  #~ /*
   #~ * NotifyAncestor, NotifyVirtual, NotifyInferior,
   #~ * NotifyNonlinear,NotifyNonlinearVirtual, NotifyPointer,
   #~ * NotifyPointerRoot, NotifyDetailNone
   #~ */
#~ } XFocusChangeEvent;
#~ typedef XFocusChangeEvent XFocusInEvent;
#~ typedef XFocusChangeEvent XFocusOutEvent;
class XFocusChangeEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('mode', c_int),
    ('detail', c_int),
  ]
XFocusInEvent = XFocusChangeEvent
XFocusOutEvent = XFocusChangeEvent

#/* generated on EnterWindow and FocusIn  when KeyMapState selected */
#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ char key_vector[32];
#~ } XKeymapEvent;
class XKeymapEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('key_vector', c_char * 32),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ int x, y;
  #~ int width, height;
  #~ int count;    /* if non-zero, at least this many more */
#~ } XExposeEvent;
class XExposeEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('count', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Drawable drawable;
  #~ int x, y;
  #~ int width, height;
  #~ int count;    /* if non-zero, at least this many more */
  #~ int major_code;    /* core is CopyArea or CopyPlane */
  #~ int minor_code;    /* not defined in the core */
#~ } XGraphicsExposeEvent;
class XGraphicsExposeEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('drawable', Drawable),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('count', c_int),
    ('major_code', c_int),
    ('minor_code', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Drawable drawable;
  #~ int major_code;    /* core is CopyArea or CopyPlane */
  #~ int minor_code;    /* not defined in the core */
#~ } XNoExposeEvent;
class XNoExposeEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('drawable', Drawable),
    ('major_code', c_int),
    ('minor_code', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ int state;    /* Visibility state */
#~ } XVisibilityEvent;
class XVisibilityEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('state', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window parent;    /* parent of the window */
  #~ Window window;    /* window id of window created */
  #~ int x, y;    /* window location */
  #~ int width, height;  /* size of window */
  #~ int border_width;  /* border width */
  #~ Bool override_redirect;  /* creation should be overridden */
#~ } XCreateWindowEvent;
class XCreateWindowEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('override_redirect', Bool),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
#~ } XDestroyWindowEvent;
class XDestroyWindowEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ Bool from_configure;
#~ } XUnmapEvent;
class XUnmapEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('from_configure', Bool),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ Bool override_redirect;  /* boolean, is override set... */
#~ } XMapEvent;
class XMapEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('override_redirect', Bool),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window parent;
  #~ Window window;
#~ } XMapRequestEvent;
class XMapRequestEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ Window parent;
  #~ int x, y;
  #~ Bool override_redirect;
#~ } XReparentEvent;
class XReparentEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('parent', Window),
    ('x', c_int),
    ('y', c_int),
    ('override_redirect', Bool),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ int x, y;
  #~ int width, height;
  #~ int border_width;
  #~ Window above;
  #~ Bool override_redirect;
#~ } XConfigureEvent;
class XConfigureEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('above', Window),
    ('override_redirect', Bool),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ int x, y;
#~ } XGravityEvent;
class XGravityEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ int width, height;
#~ } XResizeRequestEvent;
class XResizeRequestEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('width', c_int),
    ('height', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window parent;
  #~ Window window;
  #~ int x, y;
  #~ int width, height;
  #~ int border_width;
  #~ Window above;
  #~ int detail;    /* Above, Below, TopIf, BottomIf, Opposite */
  #~ unsigned long value_mask;
#~ } XConfigureRequestEvent;
class XConfigureRequestEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('x', c_int),
    ('y', c_int),
    ('width', c_int),
    ('height', c_int),
    ('border_width', c_int),
    ('above', Window),
    ('detail', c_int),
    ('value_mask', c_ulong),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window event;
  #~ Window window;
  #~ int place;    /* PlaceOnTop, PlaceOnBottom */
#~ } XCirculateEvent;
class XCirculateEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('event', Window),
    ('window', Window),
    ('place', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window parent;
  #~ Window window;
  #~ int place;    /* PlaceOnTop, PlaceOnBottom */
#~ } XCirculateRequestEvent;
class XCirculateRequestEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('parent', Window),
    ('window', Window),
    ('place', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ Atom atom;
  #~ Time time;
  #~ int state;    /* NewValue, Deleted */
#~ } XPropertyEvent;
class XPropertyEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('atom', Atom),
    ('time', Time),
    ('state', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ Atom selection;
  #~ Time time;
#~ } XSelectionClearEvent;
class XSelectionClearEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('selection', Atom),
    ('time', Time),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window owner;
  #~ Window requestor;
  #~ Atom selection;
  #~ Atom target;
  #~ Atom property;
  #~ Time time;
#~ } XSelectionRequestEvent;
class XSelectionRequestEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('owner', Window),
    ('requestor', Window),
    ('selection', Atom),
    ('target', Atom),
    ('property', Atom),
    ('time', Time),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window requestor;
  #~ Atom selection;
  #~ Atom target;
  #~ Atom property;    /* ATOM or None */
  #~ Time time;
#~ } XSelectionEvent;
class XSelectionEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('requestor', Window),
    ('selection', Atom),
    ('target', Atom),
    ('property', Atom),
    ('time', Time),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ Colormap colormap;  /* COLORMAP or None */
#~ #if defined(__cplusplus) || defined(c_plusplus)
  #~ Bool c_new;    /* C++ */
#~ #else
  #~ Bool new;
#~ #endif
  #~ int state;    /* ColormapInstalled, ColormapUninstalled */
#~ } XColormapEvent;
class XColormapEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('colormap', Colormap),
    ('c_new', Bool),
    ('state', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;
  #~ Atom message_type;
  #~ int format;
  #~ union {
    #~ char b[20];
    #~ short s[10];
    #~ long l[5];
    #~ } data;
#~ } XClientMessageEvent;
class _U(Union):
  _fields_ = [
    ('b', c_char * 20),
    ('s', c_short * 10),
    ('l', c_long * 5),
  ]

class XClientMessageEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('message_type', Atom),
    ('format', c_int),
    ('data', _U),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;  /* Display the event was read from */
  #~ Window window;    /* unused */
  #~ int request;    /* one of MappingModifier, MappingKeyboard,
           #~ MappingPointer */
  #~ int first_keycode;  /* first keycode */
  #~ int count;    /* defines range of change w. first_keycode*/
#~ } XMappingEvent;
class XMappingEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
    ('request', c_int),
    ('first_keycode', c_int),
    ('count', c_int),
  ]

#~ typedef struct {
  #~ int type;
  #~ Display *display;  /* Display the event was read from */
  #~ XID resourceid;    /* resource id */
  #~ unsigned long serial;  /* serial number of failed request */
  #~ unsigned char error_code;  /* error code of failed request */
  #~ unsigned char request_code;  /* Major op-code of failed request */
  #~ unsigned char minor_code;  /* Minor op-code of failed request */
#~ } XErrorEvent;
class XErrorEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('display', POINTER(Display)),
    ('resourceid', XID),
    ('serial', c_ulong),
    ('error_code', c_ubyte),
    ('request_code', c_ubyte),
    ('minor_code', c_ubyte),
  ]

#~ typedef struct {
  #~ int type;
  #~ unsigned long serial;  /* # of last request processed by server */
  #~ Bool send_event;  /* true if this came from a SendEvent request */
  #~ Display *display;/* Display the event was read from */
  #~ Window window;  /* window on which event was requested in event mask */
#~ } XAnyEvent;
class XAnyEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('window', Window),
  ]


#/***************************************************************
# *
# * GenericEvent.  This event is the standard event for all newer extensions.
# */

#~ typedef struct
    #~ {
    #~ int            type;         /* of event. Always GenericEvent */
    #~ unsigned long  serial;       /* # of last request processed */
    #~ Bool           send_event;   /* true if from SendEvent request */
    #~ Display        *display;     /* Display the event was read from */
    #~ int            extension;    /* major opcode of extension that caused the event */
    #~ int            evtype;       /* actual event type. */
    #~ } XGenericEvent;
class XGenericEvent(Structure):
  _fields_ = [
    ('type', c_int),
    ('serial', c_ulong),
    ('send_event', Bool),
    ('display', POINTER(Display)),
    ('extension', c_int),
    ('evtype', c_int),
  ]

#/*
# * this union is defined so Xlib can always use the same sized
# * event structure internally, to avoid memory fragmentation.
# */
#~ typedef union _XEvent {
        #~ int type;    /* must not be changed; first element */
  #~ XAnyEvent xany;
  #~ XKeyEvent xkey;
  #~ XButtonEvent xbutton;
  #~ XMotionEvent xmotion;
  #~ XCrossingEvent xcrossing;
  #~ XFocusChangeEvent xfocus;
  #~ XExposeEvent xexpose;
  #~ XGraphicsExposeEvent xgraphicsexpose;
  #~ XNoExposeEvent xnoexpose;
  #~ XVisibilityEvent xvisibility;
  #~ XCreateWindowEvent xcreatewindow;
  #~ XDestroyWindowEvent xdestroywindow;
  #~ XUnmapEvent xunmap;
  #~ XMapEvent xmap;
  #~ XMapRequestEvent xmaprequest;
  #~ XReparentEvent xreparent;
  #~ XConfigureEvent xconfigure;
  #~ XGravityEvent xgravity;
  #~ XResizeRequestEvent xresizerequest;
  #~ XConfigureRequestEvent xconfigurerequest;
  #~ XCirculateEvent xcirculate;
  #~ XCirculateRequestEvent xcirculaterequest;
  #~ XPropertyEvent xproperty;
  #~ XSelectionClearEvent xselectionclear;
  #~ XSelectionRequestEvent xselectionrequest;
  #~ XSelectionEvent xselection;
  #~ XColormapEvent xcolormap;
  #~ XClientMessageEvent xclient;
  #~ XMappingEvent xmapping;
  #~ XErrorEvent xerror;
  #~ XKeymapEvent xkeymap;
  #~ long pad[24];
#~ } XEvent;
#endif
class _XEvent(Union): pass
_XEvent._fields_ = [
  ('type', c_int),
  ('xany', XAnyEvent),
  ('xkey', XKeyEvent),
  ('xbutton', XButtonEvent),
  ('xmotion', XMotionEvent),
  ('xcrossing', XCrossingEvent),
  ('xfocus', XFocusChangeEvent),
  ('xexpose', XExposeEvent),
  ('xgraphicsexpose', XGraphicsExposeEvent),
  ('xnoexpose', XNoExposeEvent),
  ('xvisibility', XVisibilityEvent),
  ('xcreatewindow', XCreateWindowEvent),
  ('xdestroywindow', XDestroyWindowEvent),
  ('xunmap', XUnmapEvent),
  ('xmap', XMapEvent),
  ('xmaprequest', XMapRequestEvent),
  ('xreparent', XReparentEvent),
  ('xconfigure', XConfigureEvent),
  ('xgravity', XGravityEvent),
  ('xresizerequest', XResizeRequestEvent),
  ('xconfigurerequest', XConfigureRequestEvent),
  ('xcirculate', XCirculateEvent),
  ('xcirculaterequest', XCirculateRequestEvent),
  ('xproperty', XPropertyEvent),
  ('xselectionclear', XSelectionClearEvent),
  ('xselectionrequest', XSelectionRequestEvent),
  ('xselection', XSelectionEvent),
  ('xcolormap', XColormapEvent),
  ('xclient', XClientMessageEvent),
  ('xmapping', XMappingEvent),
  ('xerror', XErrorEvent),
  ('xkeymap', XKeymapEvent),
  ('pad', c_long * 24),
]
XEvent = _XEvent

#define XAllocID(dpy) ((*((_XPrivDisplay)dpy)->resource_alloc)((dpy)))

#/*
# * per character font metric information.
# */
#~ typedef struct {
    #~ short  lbearing;  /* origin to left edge of raster */
    #~ short  rbearing;  /* origin to right edge of raster */
    #~ short  width;    /* advance to next char's origin */
    #~ short  ascent;    /* baseline to top edge of raster */
    #~ short  descent;  /* baseline to bottom edge of raster */
    #~ unsigned short attributes;  /* per char flags (not predefined) */
#~ } XCharStruct;
class XCharStruct(Structure):
   _fields_ = [
    ('lbearing', c_short),
    ('rbearing', c_short),
    ('width', c_short),
    ('ascent', c_short),
    ('descent', c_short),
    ('attributes', c_ushort),
   ]

#/*
# * To allow arbitrary information with fonts, there are additional properties
# * returned.
# */
#~ typedef struct {
    #~ Atom name;
    #~ unsigned long card32;
#~ } XFontProp;
class XFontProp(Structure):
   _fields_ = [
    ('name', Atom),
    ('card32', c_ulong),
   ]

#~ typedef struct {
    #~ XExtData  *ext_data;  /* hook for extension to hang data */
    #~ Font        fid;            /* Font id for this font */
    #~ unsigned  direction;  /* hint about direction the font is painted */
    #~ unsigned  min_char_or_byte2;/* first character */
    #~ unsigned  max_char_or_byte2;/* last character */
    #~ unsigned  min_byte1;  /* first row that exists */
    #~ unsigned  max_byte1;  /* last row that exists */
    #~ Bool  all_chars_exist;/* flag if all characters have non-zero size*/
    #~ unsigned  default_char;  /* char to print for undefined character */
    #~ int         n_properties;   /* how many properties there are */
    #~ XFontProp  *properties;  /* pointer to array of additional properties*/
    #~ XCharStruct  min_bounds;  /* minimum bounds over all existing char*/
    #~ XCharStruct  max_bounds;  /* maximum bounds over all existing char*/
    #~ XCharStruct  *per_char;  /* first_char to last_char information */
    #~ int    ascent;    /* log. extent above baseline for spacing */
    #~ int    descent;  /* log. descent below baseline for spacing */
#~ } XFontStruct;
class XFontStruct(Structure):
   _fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('fid', Font),
    ('direction', c_uint),
    ('min_char_or_byte2', c_uint),
    ('max_char_or_byte2', c_uint),
    ('min_byte1', c_uint),
    ('max_byte1', c_uint),
    ('all_chars_exist', Bool),
    ('default_char', c_uint),
    ('n_properties', c_int),
    ('properties', POINTER(XFontProp)),
    ('min_bounds', XCharStruct),
    ('max_bounds', XCharStruct),
    ('per_char', POINTER(XCharStruct)),
    ('ascent', c_int),
    ('descent', c_int),
   ]

#/*
# * PolyText routines take these as arguments.
# */
#~ typedef struct {
    #~ char *chars;    /* pointer to string */
    #~ int nchars;      /* number of characters */
    #~ int delta;      /* delta between strings */
    #~ Font font;      /* font to print it in, None don't change */
#~ } XTextItem;
class XTextItem(Structure):
   _fields_ = [
    ('chars', c_char_p),
    ('nchars', c_int),
    ('delta', c_int),
    ('font', Font),
   ]

#~ typedef struct {    /* normal 16 bit characters are two bytes */
    #~ unsigned char byte1;
    #~ unsigned char byte2;
#~ } XChar2b;
class XChar2b(Structure):
   _fields_ = [
    ('byte1', c_ubyte),
    ('byte2', c_ubyte),
   ]

#~ typedef struct {
    #~ XChar2b *chars;    /* two byte characters */
    #~ int nchars;      /* number of characters */
    #~ int delta;      /* delta between strings */
    #~ Font font;      /* font to print it in, None don't change */
#~ } XTextItem16;
class XTextItem16(Structure):
   _fields_ = [
    ('chars', POINTER(XChar2b)),
    ('nchars', c_int),
    ('delta', c_int),
    ('font', Font),
   ]

#~ typedef union { Display *display;
    #~ GC gc;
    #~ Visual *visual;
    #~ Screen *screen;
    #~ ScreenFormat *pixmap_format;
    #~ XFontStruct *font; } XEDataObject;
class XEDataObject(Union):
   _fields_ = [
    ('display', POINTER(Display)),
    ('gc', GC),
    ('visual', POINTER(Visual)),
    ('screen', POINTER(Screen)),
    ('pixmap_format', POINTER(ScreenFormat)),
    ('font', POINTER(XFontStruct)),
   ]

#~ typedef struct {
    #~ XRectangle      max_ink_extent;
    #~ XRectangle      max_logical_extent;
#~ } XFontSetExtents;
class XFontSetExtents(Structure):
   _fields_ = [
    ('max_ink_extent', XRectangle),
    ('max_logical_extent', XRectangle),
   ]

#/* unused:
#typedef void (*XOMProc)();
# */

#~ typedef struct _XOM *XOM;
class _XOM(Structure): pass
XOM = POINTER(_XOM)

#~ typedef struct _XOC *XOC, *XFontSet;
class _XOC(Structure): pass
XOC = POINTER(_XOC)
XFontSet = POINTER(_XOC)

#~ typedef struct {
    #~ char           *chars;
    #~ int             nchars;
    #~ int             delta;
    #~ XFontSet        font_set;
#~ } XmbTextItem;
class XmbTextItem(Structure):
   _fields_ = [
    ('chars', c_char_p),
    ('nchars', c_int),
    ('delta', c_int),
    ('font_set', XFontSet),
   ]

#~ typedef struct {
    #~ wchar_t        *chars;
    #~ int             nchars;
    #~ int             delta;
    #~ XFontSet        font_set;
#~ } XwcTextItem;
class XwcTextItem(Structure):
   _fields_ = [
    ('chars', c_wchar_p),
    ('nchars', c_int),
    ('delta', c_int),
    ('font_set', XFontSet),
   ]

XNRequiredCharSet = "requiredCharSet"
XNQueryOrientation = "queryOrientation"
XNBaseFontName = "baseFontName"
XNOMAutomatic = "omAutomatic"
XNMissingCharSet = "missingCharSet"
XNDefaultString = "defaultString"
XNOrientation = "orientation"
XNDirectionalDependentDrawing = "directionalDependentDrawing"
XNContextualDrawing = "contextualDrawing"
XNFontInfo = "fontInfo"

#~ typedef struct {
    #~ int charset_count;
    #~ char **charset_list;
#~ } XOMCharSetList;
class XOMCharSetList(Structure):
   _fields_ = [
    ('charset_count', c_int),
    ('charset_list', POINTER(c_char_p)),
   ]

#~ typedef enum {
    #~ XOMOrientation_LTR_TTB,
    #~ XOMOrientation_RTL_TTB,
    #~ XOMOrientation_TTB_LTR,
    #~ XOMOrientation_TTB_RTL,
    #~ XOMOrientation_Context
#~ } XOrientation;
XOrientation = c_int
(
  XOMOrientation_LTR_TTB,
  XOMOrientation_RTL_TTB,
  XOMOrientation_TTB_LTR,
  XOMOrientation_TTB_RTL,
  XOMOrientation_Context
) = map(c_int, range(5))

#~ typedef struct {
    #~ int num_orientation;
    #~ XOrientation *orientation;  /* Input Text description */
#~ } XOMOrientation;
class XOMOrientation(Structure):
   _fields_ = [
    ('num_orientation', c_int),
    ('orientation', POINTER(XOrientation)),
   ]

#~ typedef struct {
    #~ int num_font;
    #~ XFontStruct **font_struct_list;
    #~ char **font_name_list;
#~ } XOMFontInfo;
class XOMFontInfo(Structure):
   _fields_ = [
    ('num_font', c_int),
    ('font_struct_list', POINTER(POINTER(XFontStruct))),
    ('font_name_list', POINTER(c_char_p)),
   ]

#~ typedef struct _XIM *XIM;
class _XIM(Structure): pass
XIM = POINTER(_XIM)

#~ typedef struct _XIC *XIC;
class _XIC(Structure): pass
XIC = POINTER(_XIC)

#~ typedef void (*XIMProc)(
    #~ XIM,
    #~ XPointer,
    #~ XPointer
#~ );
XIMProc = c_void_p

#~ typedef Bool (*XICProc)(
    #~ XIC,
    #~ XPointer,
    #~ XPointer
#~ );
XICProc = c_void_p

#~ typedef void (*XIDProc)(
    #~ Display*,
    #~ XPointer,
    #~ XPointer
#~ );
XIDProc = c_void_p

#~ typedef unsigned long XIMStyle;
XIMStyle = c_ulong

#~ typedef struct {
    #~ unsigned short count_styles;
    #~ XIMStyle *supported_styles;
#~ } XIMStyles;
class XIMStyles(Structure):
   _fields_ = [
    ('count_styles', c_ushort),
    ('supported_styles', POINTER(XIMStyle)),
   ]

XIMPreeditArea    = 0x0001
XIMPreeditCallbacks  = 0x0002
XIMPreeditPosition  = 0x0004
XIMPreeditNothing  = 0x0008
XIMPreeditNone    = 0x0010
XIMStatusArea    = 0x0100
XIMStatusCallbacks  = 0x0200
XIMStatusNothing  = 0x0400
XIMStatusNone    = 0x0800

XNVaNestedList = "XNVaNestedList"
XNQueryInputStyle = "queryInputStyle"
XNClientWindow = "clientWindow"
XNInputStyle = "inputStyle"
XNFocusWindow = "focusWindow"
XNResourceName = "resourceName"
XNResourceClass = "resourceClass"
XNGeometryCallback = "geometryCallback"
XNDestroyCallback = "destroyCallback"
XNFilterEvents = "filterEvents"
XNPreeditStartCallback = "preeditStartCallback"
XNPreeditDoneCallback = "preeditDoneCallback"
XNPreeditDrawCallback = "preeditDrawCallback"
XNPreeditCaretCallback = "preeditCaretCallback"
XNPreeditStateNotifyCallback = "preeditStateNotifyCallback"
XNPreeditAttributes = "preeditAttributes"
XNStatusStartCallback = "statusStartCallback"
XNStatusDoneCallback = "statusDoneCallback"
XNStatusDrawCallback = "statusDrawCallback"
XNStatusAttributes = "statusAttributes"
XNArea = "area"
XNAreaNeeded = "areaNeeded"
XNSpotLocation = "spotLocation"
XNColormap = "colorMap"
XNStdColormap = "stdColorMap"
XNForeground = "foreground"
XNBackground = "background"
XNBackgroundPixmap = "backgroundPixmap"
XNFontSet = "fontSet"
XNLineSpace = "lineSpace"
XNCursor = "cursor"

XNQueryIMValuesList = "queryIMValuesList"
XNQueryICValuesList = "queryICValuesList"
XNVisiblePosition = "visiblePosition"
XNR6PreeditCallback = "r6PreeditCallback"
XNStringConversionCallback = "stringConversionCallback"
XNStringConversion = "stringConversion"
XNResetState = "resetState"
XNHotKey = "hotKey"
XNHotKeyState = "hotKeyState"
XNPreeditState = "preeditState"
XNSeparatorofNestedList = "separatorofNestedList"

XBufferOverflow  = -1
XLookupNone = 1
XLookupChars = 2
XLookupKeySym = 3
XLookupBoth = 4

#~ typedef void *XVaNestedList;
XVaNestedList = c_void_p

#~ typedef struct {
    #~ XPointer client_data;
    #~ XIMProc callback;
#~ } XIMCallback;
class XIMCallback(Structure):
   _fields_ = [
    ('client_data', XPointer),
    ('callback', XIMProc),
   ]

#~ typedef struct {
    #~ XPointer client_data;
    #~ XICProc callback;
#~ } XICCallback;
class XICCallback(Structure):
   _fields_ = [
    ('client_data', XPointer),
    ('callback', XICProc),
   ]

#~ typedef unsigned long XIMFeedback;
XIMFeedback = c_ulong

XIMReverse = 1
XIMUnderline = (1<<1)
XIMHighlight = (1<<2)
XIMPrimary = (1<<5)
XIMSecondary = (1<<6)
XIMTertiary  = (1<<7)
XIMVisibleToForward = (1<<8)
XIMVisibleToBackword = (1<<9)
XIMVisibleToCenter = (1<<10)

#~ typedef struct _XIMText {
    #~ unsigned short length;
    #~ XIMFeedback *feedback;
    #~ Bool encoding_is_wchar;
    #~ union {
  #~ char *multi_byte;
  #~ wchar_t *wide_char;
    #~ } string;
#~ } XIMText;
class _string(Union):
   _fields_ = [
    ('multi_byte', c_char_p),
    ('wide_char', c_wchar_p),
   ]

class _XIMText(Structure):
   _fields_ = [
    ('length', c_ushort),
    ('feedback', POINTER(XIMFeedback)),
    ('encoding_is_wchar', Bool),
    ('string', _string),
   ]
XIMText = _XIMText

#~ typedef  unsigned long   XIMPreeditState;
XIMPreeditState = c_ulong

XIMPreeditUnKnown = 0
XIMPreeditEnable = 1
XIMPreeditDisable = (1<<1)

#~ typedef  struct  _XIMPreeditStateNotifyCallbackStruct {
    #~ XIMPreeditState state;
#~ } XIMPreeditStateNotifyCallbackStruct;
class _XIMPreeditStateNotifyCallbackStruct(Structure):
   _fields_ = [
    ('state', XIMPreeditState),
   ]
XIMPreeditStateNotifyCallbackStruct = _XIMPreeditStateNotifyCallbackStruct

#~ typedef  unsigned long   XIMResetState;
XIMResetState = c_ulong

XIMInitialState  = 1
XIMPreserveState = (1<<1)

#~ typedef unsigned long XIMStringConversionFeedback;
XIMStringConversionFeedback = c_ulong

XIMStringConversionLeftEdge = (0x00000001)
XIMStringConversionRightEdge = (0x00000002)
XIMStringConversionTopEdge = (0x00000004)
XIMStringConversionBottomEdge = (0x00000008)
XIMStringConversionConcealed = (0x00000010)
XIMStringConversionWrapped = (0x00000020)

#~ typedef struct _XIMStringConversionText {
    #~ unsigned short length;
    #~ XIMStringConversionFeedback *feedback;
    #~ Bool encoding_is_wchar;
    #~ union {
  #~ char *mbs;
  #~ wchar_t *wcs;
    #~ } string;
#~ } XIMStringConversionText;
class _string(Union):
   _fields_ = [
    ('mbs', c_char_p),
    ('wcs', c_wchar_p),
   ]

class _XIMStringConversionText(Structure):
  _fields_ = [
    ('length', c_ushort),
    ('feedback', POINTER(XIMStringConversionFeedback)),
    ('encoding_is_wchar', Bool),
    ('string', _string),
  ]
XIMStringConversionText = _XIMStringConversionText

#~ typedef  unsigned short  XIMStringConversionPosition;
XIMStringConversionPosition = c_ushort

#~ typedef  unsigned short  XIMStringConversionType;
XIMStringConversionType = c_ushort

XIMStringConversionBuffer =(0x0001)
XIMStringConversionLine = (0x0002)
XIMStringConversionWord = (0x0003)
XIMStringConversionChar = (0x0004)

#~ typedef  unsigned short  XIMStringConversionOperation;
XIMStringConversionOperation = c_ushort

XIMStringConversionSubstitution = (0x0001)
XIMStringConversionRetrieval = (0x0002)

#~ typedef enum {
    #~ XIMForwardChar, XIMBackwardChar,
    #~ XIMForwardWord, XIMBackwardWord,
    #~ XIMCaretUp, XIMCaretDown,
    #~ XIMNextLine, XIMPreviousLine,
    #~ XIMLineStart, XIMLineEnd,
    #~ XIMAbsolutePosition,
    #~ XIMDontChange
#~ } XIMCaretDirection;
XIMCaretDirection = c_int
(
  XIMForwardChar,
  XIMBackwardChar,
  XIMForwardWord,
  XIMBackwardWord,
  XIMCaretUp,
  XIMCaretDown,
  XIMNextLine,
  XIMPreviousLine,
  XIMLineStart,
  XIMLineEnd,
  XIMAbsolutePosition,
  XIMDontChange
) = map(c_int, range(12))

#~ typedef struct _XIMStringConversionCallbackStruct {
    #~ XIMStringConversionPosition position;
    #~ XIMCaretDirection direction;
    #~ XIMStringConversionOperation operation;
    #~ unsigned short factor;
    #~ XIMStringConversionText *text;
#~ } XIMStringConversionCallbackStruct;
class _XIMStringConversionCallbackStruct(Structure):
  _fields_ = [
    ('position', XIMStringConversionPosition),
    ('direction', XIMCaretDirection),
    ('operation', XIMStringConversionOperation),
    ('factor', c_ushort),
    ('text', POINTER(XIMStringConversionText)),
  ]
XIMStringConversionCallbackStruct = _XIMStringConversionCallbackStruct

#~ typedef struct _XIMPreeditDrawCallbackStruct {
    #~ int caret;    /* Cursor offset within pre-edit string */
    #~ int chg_first;  /* Starting change position */
    #~ int chg_length;  /* Length of the change in character count */
    #~ XIMText *text;
#~ } XIMPreeditDrawCallbackStruct;
class _XIMPreeditDrawCallbackStruct(Structure):
  _fields_ = [
    ('caret', c_int),
    ('chg_first', c_int),
    ('chg_length', c_int),
    ('text', POINTER(XIMText)),
  ]
XIMPreeditDrawCallbackStruct = _XIMPreeditDrawCallbackStruct

#~ typedef enum {
    #~ XIMIsInvisible,  /* Disable caret feedback */
    #~ XIMIsPrimary,  /* UI defined caret feedback */
    #~ XIMIsSecondary  /* UI defined caret feedback */
#~ } XIMCaretStyle;
XIMCaretStyle = c_int
(
  XIMIsInvisible,
  XIMIsPrimary,
  XIMIsSecondary
) = map(c_int, range(3))

#~ typedef struct _XIMPreeditCaretCallbackStruct {
    #~ int position;     /* Caret offset within pre-edit string */
    #~ XIMCaretDirection direction; /* Caret moves direction */
    #~ XIMCaretStyle style;   /* Feedback of the caret */
#~ } XIMPreeditCaretCallbackStruct;
class _XIMPreeditCaretCallbackStruct(Structure):
  _fields_ = [
    ('position', c_int),
    ('direction', XIMCaretDirection),
    ('style', XIMCaretStyle),
  ]
XIMPreeditCaretCallbackStruct = _XIMPreeditCaretCallbackStruct

#~ typedef enum {
    #~ XIMTextType,
    #~ XIMBitmapType
#~ } XIMStatusDataType;
XIMStatusDataType = c_int
(
  XIMTextType,
  XIMBitmapType
) = map(c_int, range(2))


#~ typedef struct _XIMStatusDrawCallbackStruct {
    #~ XIMStatusDataType type;
    #~ union {
  #~ XIMText *text;
  #~ Pixmap  bitmap;
    #~ } data;
#~ } XIMStatusDrawCallbackStruct;
class _data(Union):
  _fields_ = [
    ('text', POINTER(XIMText)),
    ('bitmap', Pixmap),
  ]

class _XIMStatusDrawCallbackStruct(Structure):
  _fields_ = [
    ('type', XIMStatusDataType),
    ('data', _data),
  ]
XIMStatusDrawCallbackStruct = _XIMStatusDrawCallbackStruct

#~ typedef struct _XIMHotKeyTrigger {
    #~ KeySym   keysym;
    #~ int     modifier;
    #~ int     modifier_mask;
#~ } XIMHotKeyTrigger;
class _XIMHotKeyTrigger(Structure):
  _fields_ = [
    ('keysym', KeySym),
    ('modifier', c_int),
    ('modifier_mask', c_int),
  ]
XIMHotKeyTrigger = _XIMHotKeyTrigger

#~ typedef struct _XIMHotKeyTriggers {
    #~ int       num_hot_key;
    #~ XIMHotKeyTrigger  *key;
#~ } XIMHotKeyTriggers;
class _XIMHotKeyTriggers(Structure):
  _fields_ = [
    ('num_hot_key', c_int),
    ('key', POINTER(XIMHotKeyTrigger)),
  ]
XIMHotKeyTriggers = _XIMHotKeyTriggers

#~ typedef  unsigned long   XIMHotKeyState;
XIMHotKeyState = c_ulong

XIMHotKeyStateON = (0x0001)
XIMHotKeyStateOFF = (0x0002)

#~ typedef struct {
    #~ unsigned short count_values;
    #~ char **supported_values;
#~ } XIMValuesList;
class XIMValuesList(Structure):
  _fields_ = [
    ('count_values', c_ushort),
    ('supported_values', POINTER(c_char_p)),
  ]

#if defined(WIN32) && !defined(_XLIBINT_)
#define _Xdebug (*_Xdebug_p)
#endif
#~ extern int _Xdebug;

#~ extern XFontStruct *XLoadQueryFont(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* name */
#~ );
XLoadQueryFont = libX11.XLoadQueryFont
XLoadQueryFont.restype = POINTER(XFontStruct)
XLoadQueryFont.argtypes = [POINTER(Display), XID]

#~ extern XFontStruct *XQueryFont(
    #~ Display*    /* display */,
    #~ XID      /* font_ID */
#~ );
XQueryFont = libX11.XQueryFont
XQueryFont.restype = POINTER(XFontStruct)
XQueryFont.argtypes = [POINTER(Display), XID]

#~ extern XTimeCoord *XGetMotionEvents(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Time    /* start */,
    #~ Time    /* stop */,
    #~ int*    /* nevents_return */
#~ );
XGetMotionEvents = libX11.XGetMotionEvents
XGetMotionEvents.restype = POINTER(XTimeCoord)
XGetMotionEvents.argtypes = [POINTER(Display), Window, Time, Time, POINTER(c_int)]

#~ extern XModifierKeymap *XDeleteModifiermapEntry(
    #~ XModifierKeymap*  /* modmap */,
#~ #if NeedWidePrototypes
    #~ unsigned int  /* keycode_entry */,
#~ #else
    #~ KeyCode    /* keycode_entry */,
#~ #endif
    #~ int      /* modifier */
#~ );
XDeleteModifiermapEntry = libX11.XDeleteModifiermapEntry
XDeleteModifiermapEntry.restype = POINTER(XModifierKeymap)
XDeleteModifiermapEntry.argtypes = [POINTER(XModifierKeymap), KeyCode, c_int]

#~ extern XModifierKeymap  *XGetModifierMapping(
    #~ Display*    /* display */
#~ );
XGetModifierMapping = libX11.XGetModifierMapping
XGetModifierMapping.restype = POINTER(XModifierKeymap)
XGetModifierMapping.argtypes = [POINTER(Display)]

#~ extern XModifierKeymap  *XInsertModifiermapEntry(
    #~ XModifierKeymap*  /* modmap */,
#~ #if NeedWidePrototypes
    #~ unsigned int  /* keycode_entry */,
#~ #else
    #~ KeyCode    /* keycode_entry */,
#~ #endif
    #~ int      /* modifier */
#~ );
XInsertModifiermapEntry = libX11.XInsertModifiermapEntry
XInsertModifiermapEntry.restype = POINTER(XModifierKeymap)
XInsertModifiermapEntry.argtypes = [POINTER(XModifierKeymap), KeyCode, c_int]

#~ extern XModifierKeymap *XNewModifiermap(
    #~ int      /* max_keys_per_mod */
#~ );
XNewModifiermap = libX11.XNewModifiermap
XNewModifiermap.restype = POINTER(XModifierKeymap)
XNewModifiermap.argtypes = [c_int]

#~ extern XImage *XCreateImage(
    #~ Display*    /* display */,
    #~ Visual*    /* visual */,
    #~ unsigned int  /* depth */,
    #~ int      /* format */,
    #~ int      /* offset */,
    #~ char*    /* data */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* bitmap_pad */,
    #~ int      /* bytes_per_line */
#~ );
XCreateImage = libX11.XCreateImage
XCreateImage.restype = POINTER(XImage)
XCreateImage.argtypes = [POINTER(Display), POINTER(Visual), c_uint, c_int, c_int, c_char_p, c_uint, c_uint, c_int, c_int]

#~ extern Status XInitImage(
    #~ XImage*    /* image */
#~ );
XInitImage = libX11.XInitImage
XInitImage.restype = Status
XInitImage.argtypes = [POINTER(XImage)]

#~ extern XImage *XGetImage(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned long  /* plane_mask */,
    #~ int      /* format */
#~ );
XGetImage = libX11.XGetImage
XGetImage.restype = POINTER(XImage)
XGetImage.argtypes = [POINTER(Display), POINTER(Display), c_int, c_int, c_uint, c_uint, c_ulong, c_int]

#~ extern XImage *XGetSubImage(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned long  /* plane_mask */,
    #~ int      /* format */,
    #~ XImage*    /* dest_image */,
    #~ int      /* dest_x */,
    #~ int      /* dest_y */
#~ );
XGetSubImage = libX11.XGetSubImage
XGetSubImage.restype = POINTER(XImage)
XGetSubImage.argtypes = [POINTER(Display), Drawable, c_int, c_int, c_uint, c_uint, c_ulong, c_int, POINTER(XImage), c_int, c_int]

#/*
# * X function declarations.
# */

#~ extern Display *XOpenDisplay(
    #~ _Xconst char*  /* display_name */
#~ );
XOpenDisplay = libX11.XOpenDisplay
XOpenDisplay.restype = POINTER(Display)
XOpenDisplay.argtypes = [c_char_p]

#~ extern void XrmInitialize(
    #~ void
#~ );
XrmInitialize = libX11.XrmInitialize

#~ extern char *XFetchBytes(
    #~ Display*    /* display */,
    #~ int*    /* nbytes_return */
#~ );
XFetchBytes = libX11.XFetchBytes
XFetchBytes.restype = c_char_p
XFetchBytes.argtypes = [POINTER(Display), POINTER(c_int)]

#~ extern char *XFetchBuffer(
    #~ Display*    /* display */,
    #~ int*    /* nbytes_return */,
    #~ int      /* buffer */
#~ );
XFetchBuffer = libX11.XFetchBuffer
XFetchBuffer.restype = c_char_p
XFetchBuffer.argtypes = [POINTER(Display), POINTER(c_int), c_int]

#~ extern char *XGetAtomName(
    #~ Display*    /* display */,
    #~ Atom    /* atom */
#~ );
XGetAtomName = libX11.XGetAtomName
XGetAtomName.restype = c_char_p
XGetAtomName.argtypes = [POINTER(Display), Atom]

#~ extern Status XGetAtomNames(
    #~ Display*    /* dpy */,
    #~ Atom*    /* atoms */,
    #~ int      /* count */,
    #~ char**    /* names_return */
#~ );
XGetAtomNames = libX11.XGetAtomNames
XGetAtomNames.restype = Status
XGetAtomNames.argtypes = [POINTER(Display), POINTER(Atom), c_int, POINTER(c_char_p)]

#~ extern char *XGetDefault(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* program */,
    #~ _Xconst char*  /* option */
#~ );
XGetDefault = libX11.XGetDefault
XGetDefault.restype = c_char_p
XGetDefault.argtypes = [POINTER(Display), c_char_p, c_char_p]

#~ extern char *XDisplayName(
    #~ _Xconst char*  /* string */
#~ );
XDisplayName = libX11.XDisplayName
XDisplayName.restype = c_char_p
XDisplayName.argtypes = [c_char_p]

#~ extern char *XKeysymToString(
    #~ KeySym    /* keysym */
#~ );
XKeysymToString = libX11.XKeysymToString
XKeysymToString.restype = c_char_p
XKeysymToString.argtypes = [KeySym]

#~ extern int (*XSynchronize(
    #~ Display*    /* display */,
    #~ Bool    /* onoff */
#~ ))(
    #~ Display*    /* display */
#~ );
XSynchronize = c_void_p

#~ extern int (*XSetAfterFunction(
    #~ Display*    /* display */
    #~ int (*) (
       #~ Display*  /* display */
            #~ )    /* procedure */
#~ ))(
    #~ Display*    /* display */
#~ );
XSetAfterFunction = c_void_p

#~ extern Atom XInternAtom(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* atom_name */,
    #~ Bool    /* only_if_exists */
#~ );
XInternAtom = libX11.XInternAtom
XInternAtom.restype = Atom
XInternAtom.argtypes = [POINTER(Display), c_char_p, Bool]

#~ extern Status XInternAtoms(
    #~ Display*    /* dpy */,
    #~ char**    /* names */,
    #~ int      /* count */,
    #~ Bool    /* onlyIfExists */,
    #~ Atom*    /* atoms_return */
#~ );
XInternAtoms = libX11.XInternAtoms
XInternAtoms.restype = Status
XInternAtoms.argtypes = [POINTER(Display), POINTER(c_char_p), c_int, Bool, POINTER(Atom)]

#~ extern Colormap XCopyColormapAndFree(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */
#~ );
XCopyColormapAndFree = libX11.XCopyColormapAndFree
XCopyColormapAndFree.restype = Colormap
XCopyColormapAndFree.argtypes = [POINTER(Display), Colormap]

#~ extern Colormap XCreateColormap(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Visual*    /* visual */,
    #~ int      /* alloc */
#~ );
XCreateColormap = libX11.XCreateColormap
XCreateColormap.restype = Colormap
XCreateColormap.argtypes = [POINTER(Display), Window, POINTER(Visual), c_int]

#~ extern Cursor XCreatePixmapCursor(
    #~ Display*    /* display */,
    #~ Pixmap    /* source */,
    #~ Pixmap    /* mask */,
    #~ XColor*    /* foreground_color */,
    #~ XColor*    /* background_color */,
    #~ unsigned int  /* x */,
    #~ unsigned int  /* y */
#~ );
XCreatePixmapCursor = libX11.XCreatePixmapCursor
XCreatePixmapCursor.restype = Cursor
XCreatePixmapCursor.argtypes = [POINTER(Display), Pixmap, Pixmap, POINTER(XColor), POINTER(XColor), c_uint, c_uint]

#~ extern Cursor XCreateGlyphCursor(
    #~ Display*    /* display */,
    #~ Font    /* source_font */,
    #~ Font    /* mask_font */,
    #~ unsigned int  /* source_char */,
    #~ unsigned int  /* mask_char */,
    #~ XColor _Xconst *  /* foreground_color */,
    #~ XColor _Xconst *  /* background_color */
#~ );
XCreateGlyphCursor = libX11.XCreateGlyphCursor
XCreateGlyphCursor.restype = Cursor
XCreateGlyphCursor.argtypes = [POINTER(Display), Font, Font, c_uint, c_uint, POINTER(XColor), POINTER(XColor)]

#~ extern Cursor XCreateFontCursor(
    #~ Display*    /* display */,
    #~ unsigned int  /* shape */
#~ );
XCreateFontCursor = libX11.XCreateFontCursor
XCreateFontCursor.restype = Cursor
XCreateFontCursor.argtypes = [POINTER(Display), c_uint]

#~ extern Font XLoadFont(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* name */
#~ );
XLoadFont = libX11.XLoadFont
XLoadFont.restype = Font
XLoadFont.argtypes = [POINTER(Display), c_char_p]

#~ extern GC XCreateGC(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ unsigned long  /* valuemask */,
    #~ XGCValues*    /* values */
#~ );
XCreateGC = libX11.XCreateGC
XCreateGC.restype = GC
XCreateGC.argtypes = [POINTER(Display), Drawable, c_ulong, POINTER(XGCValues)]

#~ extern GContext XGContextFromGC(
    #~ GC      /* gc */
#~ );
XGContextFromGC = libX11.XGContextFromGC
XGContextFromGC.restype = GContext
XGContextFromGC.argtypes = [GC]

#~ extern void XFlushGC(
    #~ Display*    /* display */,
    #~ GC      /* gc */
#~ );
XFlushGC = libX11.XFlushGC
XFlushGC.argtypes = [POINTER(Display), GC]

#~ extern Pixmap XCreatePixmap(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int  /* depth */
#~ );
XCreatePixmap = libX11.XCreatePixmap
XCreatePixmap.restype = Pixmap
XCreatePixmap.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, c_uint]

#~ extern Pixmap XCreateBitmapFromData(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ _Xconst char*  /* data */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XCreateBitmapFromData = libX11.XCreateBitmapFromData
XCreateBitmapFromData.restype = Pixmap
XCreateBitmapFromData.argtypes = [POINTER(Display), Drawable, c_char_p, c_uint, c_uint]

#~ extern Pixmap XCreatePixmapFromBitmapData(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ char*    /* data */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned long  /* fg */,
    #~ unsigned long  /* bg */,
    #~ unsigned int  /* depth */
#~ );
XCreatePixmapFromBitmapData = libX11.XCreatePixmapFromBitmapData
XCreatePixmapFromBitmapData.restype = Pixmap
XCreatePixmapFromBitmapData.argtypes = [POINTER(Display), Drawable, c_char_p, c_uint, c_uint, c_ulong, c_ulong, c_uint]

#~ extern Window XCreateSimpleWindow(
    #~ Display*    /* display */,
    #~ Window    /* parent */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int  /* border_width */,
    #~ unsigned long  /* border */,
    #~ unsigned long  /* background */
#~ );
XCreateSimpleWindow = libX11.XCreateSimpleWindow
XCreateSimpleWindow.restype = Window
XCreateSimpleWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_uint, c_ulong, c_ulong]

#~ extern Window XGetSelectionOwner(
    #~ Display*    /* display */,
    #~ Atom    /* selection */
#~ );
XGetSelectionOwner = libX11.XGetSelectionOwner
XGetSelectionOwner.restype = Window
XGetSelectionOwner.argtypes = [POINTER(Display), Atom]

#~ extern Window XCreateWindow(
    #~ Display*    /* display */,
    #~ Window    /* parent */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int  /* border_width */,
    #~ int      /* depth */,
    #~ unsigned int  /* class */,
    #~ Visual*    /* visual */,
    #~ unsigned long  /* valuemask */,
    #~ XSetWindowAttributes*  /* attributes */
#~ );
XCreateWindow = libX11.XCreateWindow
XCreateWindow.restype = Window
XCreateWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_uint, c_int, c_uint, POINTER(Visual), c_ulong, POINTER(XSetWindowAttributes)]

#~ extern Colormap *XListInstalledColormaps(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int*    /* num_return */
#~ );
XListInstalledColormaps = libX11.XListInstalledColormaps
XListInstalledColormaps.restype = POINTER(Colormap)
XListInstalledColormaps.argtypes = [POINTER(Display), Window, POINTER(c_int)]

#~ extern char **XListFonts(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* pattern */,
    #~ int      /* maxnames */,
    #~ int*    /* actual_count_return */
#~ );
XListFonts = libX11.XListFonts
XListFonts.restype = POINTER(c_char_p)
XListFonts.argtypes = [POINTER(Display), c_char_p, c_int, POINTER(c_int)]

#~ extern char **XListFontsWithInfo(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* pattern */,
    #~ int      /* maxnames */,
    #~ int*    /* count_return */,
    #~ XFontStruct**  /* info_return */
#~ );
XListFontsWithInfo = libX11.XListFontsWithInfo
XListFontsWithInfo.restype = POINTER(c_char_p)
XListFontsWithInfo.argtypes = [POINTER(Display), c_char_p, c_int, POINTER(c_int), POINTER(POINTER(XFontStruct))]

#~ extern char **XGetFontPath(
    #~ Display*    /* display */,
    #~ int*    /* npaths_return */
#~ );
XGetFontPath = libX11.XGetFontPath
XGetFontPath.restype = POINTER(c_char_p)
XGetFontPath.argtypes = [POINTER(Display), POINTER(c_int)]

#~ extern char **XListExtensions(
    #~ Display*    /* display */,
    #~ int*    /* nextensions_return */
#~ );
XListExtensions = libX11.XListExtensions
XListExtensions.restype = POINTER(c_char_p)
XListExtensions.argtypes = [POINTER(Display), POINTER(c_int)]

#~ extern Atom *XListProperties(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int*    /* num_prop_return */
#~ );
XListProperties = libX11.XListProperties
XListProperties.restype = POINTER(Atom)
XListProperties.argtypes = [POINTER(Display), Window, POINTER(c_int)]

#~ extern XHostAddress *XListHosts(
    #~ Display*    /* display */,
    #~ int*    /* nhosts_return */,
    #~ Bool*    /* state_return */
#~ );
XListHosts = libX11.XListHosts
XListHosts.restype = POINTER(XHostAddress)
XListHosts.argtypes = [POINTER(Display), POINTER(c_int), POINTER(Bool)]

#~ extern KeySym XKeycodeToKeysym(
    #~ Display*    /* display */,
#~ #if NeedWidePrototypes
    #~ unsigned int  /* keycode */,
#~ #else
    #~ KeyCode    /* keycode */,
#~ #endif
    #~ int      /* index */
#~ );
XKeycodeToKeysym = libX11.XKeycodeToKeysym
XKeycodeToKeysym.restype = KeySym
XKeycodeToKeysym.argtypes = [POINTER(Display), KeyCode, c_int]

#~ extern KeySym XLookupKeysym(
    #~ XKeyEvent*    /* key_event */,
    #~ int      /* index */
#~ );
XLookupKeysym = libX11.XLookupKeysym
XLookupKeysym.restype = KeySym
XLookupKeysym.argtypes = [POINTER(XKeyEvent), c_int]

#~ extern KeySym *XGetKeyboardMapping(
    #~ Display*    /* display */,
#~ #if NeedWidePrototypes
    #~ unsigned int  /* first_keycode */,
#~ #else
    #~ KeyCode    /* first_keycode */,
#~ #endif
    #~ int      /* keycode_count */,
    #~ int*    /* keysyms_per_keycode_return */
#~ );
XGetKeyboardMapping = libX11.XGetKeyboardMapping
XGetKeyboardMapping.restype = POINTER(KeySym)
XGetKeyboardMapping.argtypes = [POINTER(Display), KeyCode, c_int, POINTER(c_int)]

#~ extern KeySym XStringToKeysym(
    #~ _Xconst char*  /* string */
#~ );
XStringToKeysym = libX11.XStringToKeysym
XStringToKeysym.restype = KeySym
XStringToKeysym.argtypes = [c_char_p]

#~ extern long XMaxRequestSize(
    #~ Display*    /* display */
#~ );
XMaxRequestSize = libX11.XMaxRequestSize
XMaxRequestSize.restype = c_long
XMaxRequestSize.argtypes = [POINTER(Display)]

#~ extern long XExtendedMaxRequestSize(
    #~ Display*    /* display */
#~ );
XExtendedMaxRequestSize = libX11.XExtendedMaxRequestSize
XExtendedMaxRequestSize.restype = c_long
XExtendedMaxRequestSize.argtypes = [POINTER(Display)]

#~ extern char *XResourceManagerString(
    #~ Display*    /* display */
#~ );
XResourceManagerString = libX11.XResourceManagerString
XResourceManagerString.restype = c_char_p
XResourceManagerString.argtypes = [POINTER(Display)]

#~ extern char *XScreenResourceString(
  #~ Screen*    /* screen */
#~ );
XScreenResourceString = libX11.XScreenResourceString
XScreenResourceString.restype = c_char_p
XScreenResourceString.argtypes = [POINTER(Screen)]

#~ extern unsigned long XDisplayMotionBufferSize(
    #~ Display*    /* display */
#~ );
XDisplayMotionBufferSize = libX11.XDisplayMotionBufferSize
XDisplayMotionBufferSize.restype = c_ulong
XDisplayMotionBufferSize.argtypes = [POINTER(Display)]

#~ extern VisualID XVisualIDFromVisual(
    #~ Visual*    /* visual */
#~ );
XVisualIDFromVisual = libX11.XVisualIDFromVisual
XVisualIDFromVisual.restype = VisualID
XVisualIDFromVisual.argtypes = [POINTER(Visual)]

#~ /* multithread routines */

#~ extern Status XInitThreads(
    #~ void
#~ );
XInitThreads = libX11.XInitThreads

#~ extern void XLockDisplay(
    #~ Display*    /* display */
#~ );
XLockDisplay = libX11.XLockDisplay
XLockDisplay.argtypes = [POINTER(Display)]

#~ extern void XUnlockDisplay(
    #~ Display*    /* display */
#~ );
XUnlockDisplay = libX11.XUnlockDisplay
XUnlockDisplay.argtypes = [POINTER(Display)]

#~ /* routines for dealing with extensions */

#~ extern XExtCodes *XInitExtension(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* name */
#~ );
XInitExtension = libX11.XInitExtension
XInitExtension.restype = POINTER(XExtCodes)
XInitExtension.argtypes = [POINTER(Display), c_char_p]

#~ extern XExtCodes *XAddExtension(
    #~ Display*    /* display */
#~ );
XAddExtension = libX11.XAddExtension
XAddExtension.restype = POINTER(XExtCodes)
XAddExtension.argtypes = [POINTER(Display)]

#~ extern XExtData *XFindOnExtensionList(
    #~ XExtData**    /* structure */,
    #~ int      /* number */
#~ );
XFindOnExtensionList = libX11.XFindOnExtensionList
XFindOnExtensionList.restype = POINTER(XExtCodes)
XFindOnExtensionList.argtypes = [POINTER(POINTER(XExtCodes)), c_int]

#~ extern XExtData **XEHeadOfExtensionList(
    #~ XEDataObject  /* object */
#~ );
XEHeadOfExtensionList = libX11.XEHeadOfExtensionList
XEHeadOfExtensionList.restype = POINTER(POINTER(XExtCodes))
XEHeadOfExtensionList.argtypes = [XEDataObject]

#~ /* these are routines for which there are also macros */
#~ extern Window XRootWindow(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XRootWindow = libX11.XRootWindow
XRootWindow.restype = Window
XRootWindow.argtypes = [POINTER(Display), c_int]

#~ extern Window XDefaultRootWindow(
    #~ Display*    /* display */
#~ );
XDefaultRootWindow = libX11.XDefaultRootWindow
XDefaultRootWindow.restype = Window
XDefaultRootWindow.argtypes = [POINTER(Display)]

#~ extern Window XRootWindowOfScreen(
    #~ Screen*    /* screen */
#~ );
XRootWindowOfScreen = libX11.XRootWindowOfScreen
XRootWindowOfScreen.restype = Window
XRootWindowOfScreen.argtypes = [POINTER(Screen)]

#~ extern Visual *XDefaultVisual(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDefaultVisual = libX11.XDefaultVisual
XDefaultVisual.restype = POINTER(Visual)
XDefaultVisual.argtypes = [POINTER(Display), c_int]

#~ extern Visual *XDefaultVisualOfScreen(
    #~ Screen*    /* screen */
#~ );
XDefaultVisualOfScreen = libX11.XDefaultVisualOfScreen
XDefaultVisualOfScreen.restype = POINTER(Visual)
XDefaultVisualOfScreen.argtypes = [POINTER(Screen)]

#~ extern GC XDefaultGC(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDefaultGC = libX11.XDefaultGC
XDefaultGC.restype = GC
XDefaultGC.argtypes = [POINTER(Display), c_int]

#~ extern GC XDefaultGCOfScreen(
    #~ Screen*    /* screen */
#~ );
XDefaultGCOfScreen = libX11.XDefaultGCOfScreen
XDefaultGCOfScreen.restype = GC
XDefaultGCOfScreen.argtypes = [POINTER(Screen)]

#~ extern unsigned long XBlackPixel(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XBlackPixel = libX11.XBlackPixel
XBlackPixel.restype = c_ulong
XBlackPixel.argtypes = [POINTER(Display), c_int]

#~ extern unsigned long XWhitePixel(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XWhitePixel = libX11.XWhitePixel
XWhitePixel.restype = c_ulong
XWhitePixel.argtypes = [POINTER(Display), c_int]

#~ extern unsigned long XAllPlanes(
    #~ void
#~ );
XAllPlanes = libX11.XAllPlanes
XAllPlanes.restype = c_ulong
XAllPlanes.argtypes = []

#~ extern unsigned long XBlackPixelOfScreen(
    #~ Screen*    /* screen */
#~ );
XBlackPixelOfScreen = libX11.XBlackPixelOfScreen
XBlackPixelOfScreen.restype = c_ulong
XBlackPixelOfScreen.argtypes = [POINTER(Screen)]

#~ extern unsigned long XWhitePixelOfScreen(
    #~ Screen*    /* screen */
#~ );
XWhitePixelOfScreen = libX11.XWhitePixelOfScreen
XWhitePixelOfScreen.restype = c_ulong
XWhitePixelOfScreen.argtypes = [POINTER(Screen)]

#~ extern unsigned long XNextRequest(
    #~ Display*    /* display */
#~ );
XNextRequest = libX11.XNextRequest
XNextRequest.restype = c_ulong
XNextRequest.argtypes = [POINTER(Display)]

#~ extern unsigned long XLastKnownRequestProcessed(
    #~ Display*    /* display */
#~ );
XLastKnownRequestProcessed = libX11.XLastKnownRequestProcessed
XLastKnownRequestProcessed.restype = c_ulong
XLastKnownRequestProcessed.argtypes = [POINTER(Display)]

#~ extern char *XServerVendor(
    #~ Display*    /* display */
#~ );
XServerVendor = libX11.XServerVendor
XServerVendor.restype = c_char_p
XServerVendor.argtypes = [POINTER(Display)]

#~ extern char *XDisplayString(
    #~ Display*    /* display */
#~ );
XDisplayString = libX11.XDisplayString
XDisplayString.restype = c_char_p
XDisplayString.argtypes = [POINTER(Display)]

#~ extern Colormap XDefaultColormap(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDefaultColormap = libX11.XDefaultColormap
XDefaultColormap.restype = Colormap
XDefaultColormap.argtypes = [POINTER(Display), c_int]

#~ extern Colormap XDefaultColormapOfScreen(
    #~ Screen*    /* screen */
#~ );
XDefaultColormapOfScreen = libX11.XDefaultColormapOfScreen
XDefaultColormapOfScreen.restype = Colormap
XDefaultColormapOfScreen.argtypes = [POINTER(Screen)]

#~ extern Display *XDisplayOfScreen(
    #~ Screen*    /* screen */
#~ );
XDisplayOfScreen = libX11.XDisplayOfScreen
XDisplayOfScreen.restype = POINTER(Display)
XDisplayOfScreen.argtypes = [POINTER(Screen)]

#~ extern Screen *XScreenOfDisplay(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XScreenOfDisplay = libX11.XScreenOfDisplay
XScreenOfDisplay.restype = POINTER(Screen)
XScreenOfDisplay.argtypes = [POINTER(Display), c_int]

#~ extern Screen *XDefaultScreenOfDisplay(
    #~ Display*    /* display */
#~ );
XDefaultScreenOfDisplay = libX11.XDefaultScreenOfDisplay
XDefaultScreenOfDisplay.restype = POINTER(Screen)
XDefaultScreenOfDisplay.argtypes = [POINTER(Display)]

#~ extern long XEventMaskOfScreen(
    #~ Screen*    /* screen */
#~ );
XEventMaskOfScreen = libX11.XEventMaskOfScreen
XEventMaskOfScreen.restype = c_long
XEventMaskOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XScreenNumberOfScreen(
    #~ Screen*    /* screen */
#~ );
XScreenNumberOfScreen = libX11.XScreenNumberOfScreen
XScreenNumberOfScreen.restype = c_int
XScreenNumberOfScreen.argtypes = [POINTER(Screen)]

#~ typedef int (*XErrorHandler) (      /* WARNING, this type not in Xlib spec */
    #~ Display*    /* display */,
    #~ XErrorEvent*  /* error_event */
#~ );
XErrorHandler = c_void_p

#~ extern XErrorHandler XSetErrorHandler (
    #~ XErrorHandler  /* handler */
#~ );
XSetErrorHandler = libX11.XSetErrorHandler
XSetErrorHandler.restype = XErrorHandler
XSetErrorHandler.argtypes = [XErrorHandler]

#~ typedef int (*XIOErrorHandler) (    /* WARNING, this type not in Xlib spec */
    #~ Display*    /* display */
#~ );
XIOErrorHandler = c_void_p

#~ extern XIOErrorHandler XSetIOErrorHandler (
    #~ XIOErrorHandler  /* handler */
#~ );
XSetIOErrorHandler = libX11.XSetIOErrorHandler
XSetIOErrorHandler.restype = XIOErrorHandler
XSetIOErrorHandler.argtypes = [XIOErrorHandler]

#~ extern XPixmapFormatValues *XListPixmapFormats(
    #~ Display*    /* display */,
    #~ int*    /* count_return */
#~ );
XListPixmapFormats = libX11.XListPixmapFormats
XListPixmapFormats.restype = POINTER(XPixmapFormatValues)
XListPixmapFormats.argtypes = [POINTER(Display), POINTER(c_int)]

#~ extern int *XListDepths(
    #~ Display*    /* display */,
    #~ int      /* screen_number */,
    #~ int*    /* count_return */
#~ );
XListDepths = libX11.XListDepths
XListDepths.restype = POINTER(c_int)
XListDepths.argtypes = [POINTER(Display), c_int, POINTER(c_int)]

#~ #/* ICCCM routines for things that don't require special include files; */
#~ #/* other declarations are given in Xutil.h                             */
#~ extern Status XReconfigureWMWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* screen_number */,
    #~ unsigned int  /* mask */,
    #~ XWindowChanges*  /* changes */
#~ );
XReconfigureWMWindow = libX11.XReconfigureWMWindow
XReconfigureWMWindow.restype = Status
XReconfigureWMWindow.argtypes = [POINTER(Display), Window, c_int, c_uint, POINTER(XWindowChanges)]

#~ extern Status XGetWMProtocols(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom**    /* protocols_return */,
    #~ int*    /* count_return */
#~ );
XGetWMProtocols = libX11.XGetWMProtocols
XGetWMProtocols.restype = Status
XGetWMProtocols.argtypes = [POINTER(Display), Window, POINTER(POINTER(Atom)), POINTER(c_int)]

#~ extern Status XSetWMProtocols(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom*    /* protocols */,
    #~ int      /* count */
#~ );
XSetWMProtocols = libX11.XSetWMProtocols
XSetWMProtocols.restype = Status
XSetWMProtocols.argtypes = [POINTER(Display), Window, POINTER(Atom), c_int]

#~ extern Status XIconifyWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* screen_number */
#~ );
XIconifyWindow = libX11.XIconifyWindow
XIconifyWindow.restype = Status
XIconifyWindow.argtypes = [POINTER(Display), Window, c_int]

#~ extern Status XWithdrawWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* screen_number */
#~ );
XWithdrawWindow = libX11.XWithdrawWindow
XWithdrawWindow.restype = Status
XWithdrawWindow.argtypes = [POINTER(Display), Window, c_int]

#~ extern Status XGetCommand(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ char***    /* argv_return */,
    #~ int*    /* argc_return */
#~ );
XGetCommand = libX11.XGetCommand
XGetCommand.restype = Status
XGetCommand.argtypes = [POINTER(Display), Window, POINTER(POINTER(c_char_p)), POINTER(c_int)]

#~ extern Status XGetWMColormapWindows(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window**    /* windows_return */,
    #~ int*    /* count_return */
#~ );
XGetWMColormapWindows = libX11.XGetWMColormapWindows
XGetWMColormapWindows.restype = Status
XGetWMColormapWindows.argtypes = [POINTER(Display), Window, POINTER(POINTER(Window)), POINTER(c_int)]

#~ extern Status XSetWMColormapWindows(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window*    /* colormap_windows */,
    #~ int      /* count */
#~ );
XSetWMColormapWindows = libX11.XSetWMColormapWindows
XSetWMColormapWindows.restype = Status
XSetWMColormapWindows.argtypes = [POINTER(Display), Window, POINTER(Window), c_int]

#~ extern void XFreeStringList(
    #~ char**    /* list */
#~ );
XFreeStringList = libX11.XFreeStringList
XFreeStringList.argtypes = [POINTER(c_char_p)]

#~ extern int XSetTransientForHint(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window    /* prop_window */
#~ );
XSetTransientForHint = libX11.XSetTransientForHint
XSetTransientForHint.restype = c_int
XSetTransientForHint.argtypes = [POINTER(Display), Window, Window]

#~ /* The following are given in alphabetical order */

#~ extern int XActivateScreenSaver(
    #~ Display*    /* display */
#~ );
XActivateScreenSaver = libX11.XActivateScreenSaver
XActivateScreenSaver.restype = c_int
XActivateScreenSaver.argtypes = [POINTER(Display)]

#~ extern int XAddHost(
    #~ Display*    /* display */,
    #~ XHostAddress*  /* host */
#~ );
XAddHost = libX11.XAddHost
XAddHost.restype = c_int
XAddHost.argtypes = [POINTER(Display), POINTER(XHostAddress)]

#~ extern int XAddHosts(
    #~ Display*    /* display */,
    #~ XHostAddress*  /* hosts */,
    #~ int      /* num_hosts */
#~ );
XAddHosts = libX11.XAddHosts
XAddHosts.restype = c_int
XAddHosts.argtypes = [POINTER(Display), POINTER(XHostAddress), c_int]

#~ extern int XAddToExtensionList(
    #~ struct _XExtData**  /* structure */,
    #~ XExtData*    /* ext_data */
#~ );
XAddToExtensionList = libX11.XAddToExtensionList
XAddToExtensionList.restype = c_int
XAddToExtensionList.argtypes = [POINTER(POINTER(_XExtData)), POINTER(XExtData)]

#~ extern int XAddToSaveSet(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XAddToSaveSet = libX11.XAddToSaveSet
XAddToSaveSet.restype = c_int
XAddToSaveSet.argtypes = [POINTER(Display), Window]

#~ extern Status XAllocColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ XColor*    /* screen_in_out */
#~ );
XAllocColor = libX11.XAllocColor
XAllocColor.restype = Status
XAllocColor.argtypes = [POINTER(Display), Colormap,POINTER(XColor)]

#~ extern Status XAllocColorCells(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ Bool          /* contig */,
    #~ unsigned long*  /* plane_masks_return */,
    #~ unsigned int  /* nplanes */,
    #~ unsigned long*  /* pixels_return */,
    #~ unsigned int   /* npixels */
#~ );
XAllocColorCells = libX11.XAllocColorCells
XAllocColorCells.restype = Status
XAllocColorCells.argtypes = [POINTER(Display), Colormap, Bool, POINTER(c_ulong), c_int, POINTER(c_ulong), c_int]

#~ extern Status XAllocColorPlanes(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ Bool    /* contig */,
    #~ unsigned long*  /* pixels_return */,
    #~ int      /* ncolors */,
    #~ int      /* nreds */,
    #~ int      /* ngreens */,
    #~ int      /* nblues */,
    #~ unsigned long*  /* rmask_return */,
    #~ unsigned long*  /* gmask_return */,
    #~ unsigned long*  /* bmask_return */
#~ );
XAllocColorPlanes = libX11.XAllocColorPlanes
XAllocColorPlanes.restype = Status
XAllocColorPlanes.argtypes = [POINTER(Display), Colormap, Bool, POINTER(c_ulong), c_int, c_int, c_int, c_int, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]

#~ extern Status XAllocNamedColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ _Xconst char*  /* color_name */,
    #~ XColor*    /* screen_def_return */,
    #~ XColor*    /* exact_def_return */
#~ );
XAllocNamedColor = libX11.XAllocNamedColor
XAllocNamedColor.restype = Status
XAllocNamedColor.argtypes = [POINTER(Display), Colormap, c_char_p, POINTER(XColor), POINTER(XColor)]

#~ extern int XAllowEvents(
    #~ Display*    /* display */,
    #~ int      /* event_mode */,
    #~ Time    /* time */
#~ );
XAllowEvents = libX11.XAllowEvents
XAllowEvents.restype = c_int
XAllowEvents.argtypes = [POINTER(Display), c_int, Time]

#~ extern int XAutoRepeatOff(
    #~ Display*    /* display */
#~ );
XAutoRepeatOff = libX11.XAutoRepeatOff
XAutoRepeatOff.restype = c_int
XAutoRepeatOff.argtypes = [POINTER(Display)]

#~ extern int XAutoRepeatOn(
    #~ Display*    /* display */
#~ );
XAutoRepeatOn = libX11.XAutoRepeatOn
XAutoRepeatOn.restype = c_int
XAutoRepeatOn.argtypes = [POINTER(Display)]

#~ extern int XBell(
    #~ Display*    /* display */,
    #~ int      /* percent */
#~ );
XBell = libX11.XBell
XBell.restype = c_int
XBell.argtypes = [POINTER(Display), c_int]

#~ extern int XBitmapBitOrder(
    #~ Display*    /* display */
#~ );
XBitmapBitOrder = libX11.XBitmapBitOrder
XBitmapBitOrder.restype = c_int
XBitmapBitOrder.argtypes = [POINTER(Display)]

#~ extern int XBitmapPad(
    #~ Display*    /* display */
#~ );
XBitmapPad = libX11.XBitmapPad
XBitmapPad.restype = c_int
XBitmapPad.argtypes = [POINTER(Display)]

#~ extern int XBitmapUnit(
    #~ Display*    /* display */
#~ );
XBitmapUnit = libX11.XBitmapUnit
XBitmapUnit.restype = c_int
XBitmapUnit.argtypes = [POINTER(Display)]

#~ extern int XCellsOfScreen(
    #~ Screen*    /* screen */
#~ );
XCellsOfScreen = libX11.XCellsOfScreen
XCellsOfScreen.restype = c_int
XCellsOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XChangeActivePointerGrab(
    #~ Display*    /* display */,
    #~ unsigned int  /* event_mask */,
    #~ Cursor    /* cursor */,
    #~ Time    /* time */
#~ );
XChangeActivePointerGrab = libX11.XChangeActivePointerGrab
XChangeActivePointerGrab.restype = c_int
XChangeActivePointerGrab.argtypes = [POINTER(Display), c_uint, Cursor, Time]

#~ extern int XChangeGC(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long  /* valuemask */,
    #~ XGCValues*    /* values */
#~ );
XChangeGC = libX11.XChangeGC
XChangeGC.restype = c_int
XChangeGC.argtypes = [POINTER(Display), GC, c_ulong, POINTER(XGCValues)]

#~ extern int XChangeKeyboardControl(
    #~ Display*    /* display */,
    #~ unsigned long  /* value_mask */,
    #~ XKeyboardControl*  /* values */
#~ );
XChangeKeyboardControl = libX11.XChangeKeyboardControl
XChangeKeyboardControl.restype = c_int
XChangeKeyboardControl.argtypes = [POINTER(Display), c_ulong, POINTER(XKeyboardControl)]

#~ extern int XChangeKeyboardMapping(
    #~ Display*    /* display */,
    #~ int      /* first_keycode */,
    #~ int      /* keysyms_per_keycode */,
    #~ KeySym*    /* keysyms */,
    #~ int      /* num_codes */
#~ );
XChangeKeyboardMapping = libX11.XChangeKeyboardMapping
XChangeKeyboardMapping.restype = c_int
XChangeKeyboardMapping.argtypes = [POINTER(Display), c_int, c_int, POINTER(KeySym), c_int]

#~ extern int XChangePointerControl(
    #~ Display*    /* display */,
    #~ Bool    /* do_accel */,
    #~ Bool    /* do_threshold */,
    #~ int      /* accel_numerator */,
    #~ int      /* accel_denominator */,
    #~ int      /* threshold */
#~ );
XChangePointerControl = libX11.XChangePointerControl
XChangePointerControl.restype = c_int
XChangePointerControl.argtypes = [POINTER(Display), Bool, Bool, c_int, c_int, c_int]

#~ extern int XChangeProperty(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom    /* property */,
    #~ Atom    /* type */,
    #~ int      /* format */,
    #~ int      /* mode */,
    #~ _Xconst unsigned char*  /* data */,
    #~ int      /* nelements */
#~ );
XChangeProperty = libX11.XChangeProperty
XChangeProperty.restype = c_int
XChangeProperty.argtypes = [POINTER(Display), Window, Atom, Atom, c_int, c_int, c_char_p, c_int]

#~ extern int XChangeSaveSet(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* change_mode */
#~ );
XChangeSaveSet = libX11.XChangeSaveSet
XChangeSaveSet.restype = c_int
XChangeSaveSet.argtypes = [POINTER(Display), Window, c_int]

#~ extern int XChangeWindowAttributes(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned long  /* valuemask */,
    #~ XSetWindowAttributes* /* attributes */
#~ );
XChangeWindowAttributes = libX11.XChangeWindowAttributes
XChangeWindowAttributes.restype = c_int
XChangeWindowAttributes.argtypes = [POINTER(Display), Window, c_ulong, POINTER(XSetWindowAttributes)]

#~ extern Bool XCheckIfEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event_return */,
    #~ Bool (*) (
         #~ Display*      /* display */,
               #~ XEvent*      /* event */,
               #~ XPointer      /* arg */
             #~ )    /* predicate */,
    #~ XPointer    /* arg */
#~ );
XCheckIfEvent = libX11.XCheckIfEvent
XCheckIfEvent.restype = Bool
XCheckIfEvent.argtypes = [POINTER(Display), POINTER(XEvent), c_void_p]

#~ extern Bool XCheckMaskEvent(
    #~ Display*    /* display */,
    #~ long    /* event_mask */,
    #~ XEvent*    /* event_return */
#~ );
XCheckMaskEvent = libX11.XCheckMaskEvent
XCheckMaskEvent.restype = Bool
XCheckMaskEvent.argtypes = [POINTER(Display), c_long, POINTER(XEvent)]

#~ extern Bool XCheckTypedEvent(
    #~ Display*    /* display */,
    #~ int      /* event_type */,
    #~ XEvent*    /* event_return */
#~ );
XCheckTypedEvent = libX11.XCheckTypedEvent
XCheckTypedEvent.restype = Bool
XCheckTypedEvent.argtypes = [POINTER(Display), c_int, POINTER(XEvent)]

#~ extern Bool XCheckTypedWindowEvent(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* event_type */,
    #~ XEvent*    /* event_return */
#~ );
XCheckTypedWindowEvent = libX11.XCheckTypedWindowEvent
XCheckTypedWindowEvent.restype = Bool
XCheckTypedWindowEvent.argtypes = [POINTER(Display), Window, c_int, POINTER(XEvent)]

#~ extern Bool XCheckWindowEvent(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ long    /* event_mask */,
    #~ XEvent*    /* event_return */
#~ );
XCheckWindowEvent = libX11.XCheckWindowEvent
XCheckWindowEvent.restype = Bool
XCheckWindowEvent.argtypes = [POINTER(Display), Window, c_long, POINTER(XEvent)]

#~ extern int XCirculateSubwindows(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* direction */
#~ );
XCirculateSubwindows = libX11.XCirculateSubwindows
XCirculateSubwindows.restype = c_int
XCirculateSubwindows.argtypes = [POINTER(Display), Window, c_int]

#~ extern int XCirculateSubwindowsDown(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XCirculateSubwindowsDown = libX11.XCirculateSubwindowsDown
XCirculateSubwindowsDown.restype = c_int
XCirculateSubwindowsDown.argtypes = [POINTER(Display), Window]

#~ extern int XCirculateSubwindowsUp(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XCirculateSubwindowsUp = libX11.XCirculateSubwindowsUp
XCirculateSubwindowsUp.restype = c_int
XCirculateSubwindowsUp.argtypes = [POINTER(Display), Window]

#~ extern int XClearArea(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ Bool    /* exposures */
#~ );
XClearArea = libX11.XClearArea
XClearArea.restype = c_int
XClearArea.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, Bool]

#~ extern int XClearWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XClearWindow = libX11.XClearWindow
XClearWindow.restype = c_int
XClearWindow.argtypes = [POINTER(Display), Window]

#~ extern int XCloseDisplay(
    #~ Display*    /* display */
#~ );
XCloseDisplay = libX11.XCloseDisplay
XCloseDisplay.restype = c_int
XCloseDisplay.argtypes = [POINTER(Display)]

#~ extern int XConfigureWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned int  /* value_mask */,
    #~ XWindowChanges*  /* values */
#~ );
XConfigureWindow = libX11.XConfigureWindow
XConfigureWindow.restype = c_int
XConfigureWindow.argtypes = [POINTER(Display), Window, c_uint, POINTER(XWindowChanges)]

#~ extern int XConnectionNumber(
    #~ Display*    /* display */
#~ );
XConnectionNumber = libX11.XConnectionNumber
XConnectionNumber.restype = c_int
XConnectionNumber.argtypes = [POINTER(Display)]

#~ extern int XConvertSelection(
    #~ Display*    /* display */,
    #~ Atom    /* selection */,
    #~ Atom     /* target */,
    #~ Atom    /* property */,
    #~ Window    /* requestor */,
    #~ Time    /* time */
#~ );
XConvertSelection = libX11.XConvertSelection
XConvertSelection.restype = c_int
XConvertSelection.argtypes = [POINTER(Display), Atom, Atom, Atom, Window, Time]

#~ extern int XCopyArea(
    #~ Display*    /* display */,
    #~ Drawable    /* src */,
    #~ Drawable    /* dest */,
    #~ GC      /* gc */,
    #~ int      /* src_x */,
    #~ int      /* src_y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* dest_x */,
    #~ int      /* dest_y */
#~ );
XCopyArea = libX11.XCopyArea
XCopyArea.restype = c_int
XCopyArea.argtypes = [POINTER(Display), Drawable, Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]

#~ extern int XCopyGC(
    #~ Display*    /* display */,
    #~ GC      /* src */,
    #~ unsigned long  /* valuemask */,
    #~ GC      /* dest */
#~ );
XCopyGC = libX11.XCopyGC
XCopyGC.restype = c_int
XCopyGC.argtypes = [POINTER(Display), GC, c_ulong, GC]

#~ extern int XCopyPlane(
    #~ Display*    /* display */,
    #~ Drawable    /* src */,
    #~ Drawable    /* dest */,
    #~ GC      /* gc */,
    #~ int      /* src_x */,
    #~ int      /* src_y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* dest_x */,
    #~ int      /* dest_y */,
    #~ unsigned long  /* plane */
#~ );
XCopyPlane = libX11.XCopyPlane
XCopyPlane.restype = c_int
XCopyPlane.argtypes = [POINTER(Display), Drawable, Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int, c_ulong]

#~ extern int XDefaultDepth(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDefaultDepth = libX11.XDefaultDepth
XDefaultDepth.restype = c_int
XDefaultDepth.argtypes = [POINTER(Display), c_int]

#~ extern int XDefaultDepthOfScreen(
    #~ Screen*    /* screen */
#~ );
XDefaultDepthOfScreen = libX11.XDefaultDepthOfScreen
XDefaultDepthOfScreen.restype = c_int
XDefaultDepthOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XDefaultScreen(
    #~ Display*    /* display */
#~ );
XDefaultScreen = libX11.XDefaultScreen
XDefaultScreen.restype = c_int
XDefaultScreen.argtypes = [POINTER(Display)]

#~ extern int XDefineCursor(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Cursor    /* cursor */
#~ );
XDefineCursor = libX11.XDefineCursor
XDefineCursor.restype = c_int
XDefineCursor.argtypes = [POINTER(Display), Window, Cursor]

#~ extern int XDeleteProperty(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom    /* property */
#~ );
XDeleteProperty = libX11.XDeleteProperty
XDeleteProperty.restype = c_int
XDeleteProperty.argtypes = [POINTER(Display), Window, Atom]

#~ extern int XDestroyWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XDestroyWindow = libX11.XDestroyWindow
XDestroyWindow.restype = c_int
XDestroyWindow.argtypes = [POINTER(Display), Window]

#~ extern int XDestroySubwindows(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XDestroySubwindows = libX11.XDestroySubwindows
XDestroySubwindows.restype = c_int
XDestroySubwindows.argtypes = [POINTER(Display), Window]

#~ extern int XDoesBackingStore(
    #~ Screen*    /* screen */
#~ );
XDoesBackingStore = libX11.XDoesBackingStore
XDoesBackingStore.restype = c_int
XDoesBackingStore.argtypes = [POINTER(Screen)]

#~ extern Bool XDoesSaveUnders(
    #~ Screen*    /* screen */
#~ );
XDoesSaveUnders = libX11.XDoesSaveUnders
XDoesSaveUnders.restype = Bool
XDoesSaveUnders.argtypes = [POINTER(Screen)]

#~ extern int XDisableAccessControl(
    #~ Display*    /* display */
#~ );
XDisableAccessControl = libX11.XDisableAccessControl
XDisableAccessControl.restype = c_int
XDisableAccessControl.argtypes = [POINTER(Display)]

#~ extern int XDisplayCells(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayCells = libX11.XDisplayCells
XDisplayCells.restype = c_int
XDisplayCells.argtypes = [POINTER(Display), c_int]

#~ extern int XDisplayHeight(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayHeight = libX11.XDisplayHeight
XDisplayHeight.restype = c_int
XDisplayHeight.argtypes = [POINTER(Display), c_int]

#~ extern int XDisplayHeightMM(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayHeightMM = libX11.XDisplayHeightMM
XDisplayHeightMM.restype = c_int
XDisplayHeightMM.argtypes = [POINTER(Display), c_int]

#~ extern int XDisplayKeycodes(
    #~ Display*    /* display */,
    #~ int*    /* min_keycodes_return */,
    #~ int*    /* max_keycodes_return */
#~ );
XDisplayKeycodes = libX11.XDisplayKeycodes
XDisplayKeycodes.restype = c_int
XDisplayKeycodes.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]

#~ extern int XDisplayPlanes(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayPlanes = libX11.XDisplayPlanes
XDisplayPlanes.restype = c_int
XDisplayPlanes.argtypes = [POINTER(Display), c_int]

#~ extern int XDisplayWidth(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayWidth = libX11.XDisplayWidth
XDisplayWidth.restype = c_int
XDisplayWidth.argtypes = [POINTER(Display), c_int]

#~ extern int XDisplayWidthMM(
    #~ Display*    /* display */,
    #~ int      /* screen_number */
#~ );
XDisplayWidthMM = libX11.XDisplayWidthMM
XDisplayWidthMM.restype = c_int
XDisplayWidthMM.argtypes = [POINTER(Display), c_int]

#~ extern int XDrawArc(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* angle1 */,
    #~ int      /* angle2 */
#~ );
XDrawArc = libX11.XDrawArc
XDrawArc.restype = c_int
XDrawArc.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]

#~ extern int XDrawArcs(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XArc*    /* arcs */,
    #~ int      /* narcs */
#~ );
XDrawArcs = libX11.XDrawArcs
XDrawArcs.restype = c_int
XDrawArcs.argtypes = [POINTER(Display), Drawable, GC, POINTER(XArc), c_int]

#~ extern int XDrawImageString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* string */,
    #~ int      /* length */
#~ );
XDrawImageString = libX11.XDrawImageString
XDrawImageString.restype = c_int
XDrawImageString.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_char_p, c_int]

#~ extern int XDrawImageString16(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst XChar2b*  /* string */,
    #~ int      /* length */
#~ );
XDrawImageString16 = libX11.XDrawImageString16
XDrawImageString16.restype = c_int
XDrawImageString16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XChar2b), c_int]

#~ extern int XDrawLine(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x1 */,
    #~ int      /* y1 */,
    #~ int      /* x2 */,
    #~ int      /* y2 */
#~ );
XDrawLine = libX11.XDrawLine
XDrawLine.restype = c_int
XDrawLine.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_int, c_int]

#~ extern int XDrawLines(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XPoint*    /* points */,
    #~ int      /* npoints */,
    #~ int      /* mode */
#~ );
XDrawLines = libX11.XDrawLines
XDrawLines.restype = c_int
XDrawLines.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int]

#~ extern int XDrawPoint(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */
#~ );
XDrawPoint = libX11.XDrawPoint
XDrawPoint.restype = c_int
XDrawPoint.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int]

#~ extern int XDrawPoints(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XPoint*    /* points */,
    #~ int      /* npoints */,
    #~ int      /* mode */
#~ );
XDrawPoints = libX11.XDrawPoints
XDrawPoints.restype = c_int
XDrawPoints.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int]

#~ extern int XDrawRectangle(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XDrawRectangle = libX11.XDrawRectangle
XDrawRectangle.restype = c_int
XDrawRectangle.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint]

#~ extern int XDrawRectangles(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XRectangle*    /* rectangles */,
    #~ int      /* nrectangles */
#~ );
XDrawRectangles = libX11.XDrawRectangles
XDrawRectangles.restype = c_int
XDrawRectangles.argtypes = [POINTER(Display), Drawable, GC, POINTER(XRectangle), c_int]

#~ extern int XDrawSegments(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XSegment*    /* segments */,
    #~ int      /* nsegments */
#~ );
XDrawSegments = libX11.XDrawSegments
XDrawSegments.restype = c_int
XDrawSegments.argtypes = [POINTER(Display), Drawable, GC, POINTER(XSegment), c_int]

#~ extern int XDrawString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* string */,
    #~ int      /* length */
#~ );
XDrawString = libX11.XDrawString
XDrawString.restype = c_int
XDrawString.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_char_p, c_int]

#~ extern int XDrawString16(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst XChar2b*  /* string */,
    #~ int      /* length */
#~ );
XDrawString16 = libX11.XDrawString16
XDrawString16.restype = c_int
XDrawString16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XChar2b), c_int]

#~ extern int XDrawText(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ XTextItem*    /* items */,
    #~ int      /* nitems */
#~ );
XDrawText = libX11.XDrawText
XDrawText.restype = c_int
XDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XTextItem), c_int]

#~ extern int XDrawText16(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ XTextItem16*  /* items */,
    #~ int      /* nitems */
#~ );
XDrawText16 = libX11.XDrawText16
XDrawText16.restype = c_int
XDrawText16.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XTextItem), c_int]

#~ extern int XEnableAccessControl(
    #~ Display*    /* display */
#~ );
XEnableAccessControl = libX11.XEnableAccessControl
XEnableAccessControl.restype = c_int
XEnableAccessControl.argtypes = [POINTER(Display)]

#~ extern int XEventsQueued(
    #~ Display*    /* display */,
    #~ int      /* mode */
#~ );
XEventsQueued = libX11.XEventsQueued
XEventsQueued.restype = c_int
XEventsQueued.argtypes = [POINTER(Display), c_int]

#~ extern Status XFetchName(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ char**    /* window_name_return */
#~ );
XFetchName = libX11.XFetchName
XFetchName.restype = Status
XFetchName.argtypes = [POINTER(Display), Window, POINTER(c_char_p)]

#~ extern int XFillArc(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* angle1 */,
    #~ int      /* angle2 */
#~ );
XFillArc = libX11.XFillArc
XFillArc.restype = c_int
XFillArc.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint, c_int, c_int]

#~ extern int XFillArcs(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XArc*    /* arcs */,
    #~ int      /* narcs */
#~ );
XFillArcs = libX11.XFillArcs
XFillArcs.restype = c_int
XFillArcs.argtypes = [POINTER(Display), Drawable, GC, POINTER(XArc), c_int]

#~ extern int XFillPolygon(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XPoint*    /* points */,
    #~ int      /* npoints */,
    #~ int      /* shape */,
    #~ int      /* mode */
#~ );
XFillPolygon = libX11.XFillPolygon
XFillPolygon.restype = c_int
XFillPolygon.argtypes = [POINTER(Display), Drawable, GC, POINTER(XPoint), c_int, c_int, c_int]

#~ extern int XFillRectangle(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XFillRectangle = libX11.XFillRectangle
XFillRectangle.restype = c_int
XFillRectangle.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, c_uint, c_uint]

#~ extern int XFillRectangles(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XRectangle*    /* rectangles */,
    #~ int      /* nrectangles */
#~ );
XFillRectangles = libX11.XFillRectangles
XFillRectangles.restype = c_int
XFillRectangles.argtypes = [POINTER(Display), Drawable, GC, POINTER(XRectangle), c_int]

#~ extern int XFlush(
    #~ Display*    /* display */
#~ );
XFlush = libX11.XFlush
XFlush.restype = c_int
XFlush.argtypes = [POINTER(Display)]

#~ extern int XForceScreenSaver(
    #~ Display*    /* display */,
    #~ int      /* mode */
#~ );
XForceScreenSaver = libX11.XForceScreenSaver
XForceScreenSaver.restype = c_int
XForceScreenSaver.argtypes = [POINTER(Display), c_int]

#~ extern int XFree(
    #~ void*    /* data */
#~ );
XFree = libX11.XFree
XFree.restype = c_int
XFree.argtypes = [c_void_p]

#~ extern int XFreeColormap(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */
#~ );
XFreeColormap = libX11.XFreeColormap
XFreeColormap.restype = c_int
XFreeColormap.argtypes = [POINTER(Display), Colormap]

#~ extern int XFreeColors(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ unsigned long*  /* pixels */,
    #~ int      /* npixels */,
    #~ unsigned long  /* planes */
#~ );
XFreeColors = libX11.XFreeColors
XFreeColors.restype = c_int
XFreeColors.argtypes = [POINTER(Display), Colormap, POINTER(c_ulong), c_int, c_ulong]

#~ extern int XFreeCursor(
    #~ Display*    /* display */,
    #~ Cursor    /* cursor */
#~ );
XFreeCursor = libX11.XFreeCursor
XFreeCursor.restype = c_int
XFreeCursor.argtypes = [POINTER(Display), Cursor]

#~ extern int XFreeExtensionList(
    #~ char**    /* list */
#~ );
XFreeExtensionList = libX11.XFreeExtensionList
XFreeExtensionList.restype = c_int
XFreeExtensionList.argtypes = [POINTER(c_char_p)]

#~ extern int XFreeFont(
    #~ Display*    /* display */,
    #~ XFontStruct*  /* font_struct */
#~ );
XFreeFont = libX11.XFreeFont
XFreeFont.restype = c_int
XFreeFont.argtypes = [POINTER(Display), POINTER(XFontStruct)]

#~ extern int XFreeFontInfo(
    #~ char**    /* names */,
    #~ XFontStruct*  /* free_info */,
    #~ int      /* actual_count */
#~ );
XFreeFontInfo = libX11.XFreeFontInfo
XFreeFontInfo.restype = c_int
XFreeFontInfo.argtypes = [POINTER(c_char_p), POINTER(XFontStruct), c_int]

#~ extern int XFreeFontNames(
    #~ char**    /* list */
#~ );
XFreeFontNames = libX11.XFreeFontNames
XFreeFontNames.restype = c_int
XFreeFontNames.argtypes = [POINTER(c_char_p)]

#~ extern int XFreeFontPath(
    #~ char**    /* list */
#~ );
XFreeFontPath = libX11.XFreeFontPath
XFreeFontPath.restype = c_int
XFreeFontPath.argtypes = [POINTER(c_char_p)]

#~ extern int XFreeGC(
    #~ Display*    /* display */,
    #~ GC      /* gc */
#~ );
XFreeGC = libX11.XFreeGC
XFreeGC.restype = c_int
XFreeGC.argtypes = [POINTER(Display), GC]

#~ extern int XFreeModifiermap(
    #~ XModifierKeymap*  /* modmap */
#~ );
XFreeModifiermap = libX11.XFreeModifiermap
XFreeModifiermap.restype = c_int
XFreeModifiermap.argtypes = [POINTER(XModifierKeymap)]

#~ extern int XFreePixmap(
    #~ Display*    /* display */,
    #~ Pixmap    /* pixmap */
#~ );
XFreePixmap = libX11.XFreePixmap
XFreePixmap.restype = c_int
XFreePixmap.argtypes = [POINTER(Display), Pixmap]

#~ extern int XGeometry(
    #~ Display*    /* display */,
    #~ int      /* screen */,
    #~ _Xconst char*  /* position */,
    #~ _Xconst char*  /* default_position */,
    #~ unsigned int  /* bwidth */,
    #~ unsigned int  /* fwidth */,
    #~ unsigned int  /* fheight */,
    #~ int      /* xadder */,
    #~ int      /* yadder */,
    #~ int*    /* x_return */,
    #~ int*    /* y_return */,
    #~ int*    /* width_return */,
    #~ int*    /* height_return */
#~ );
XGeometry = libX11.XGeometry
XGeometry.restype = c_int
XGeometry.argtypes = [POINTER(Display), c_int, c_char_p, c_char_p, c_uint, c_uint, c_uint, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

#~ extern int XGetErrorDatabaseText(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* name */,
    #~ _Xconst char*  /* message */,
    #~ _Xconst char*  /* default_string */,
    #~ char*    /* buffer_return */,
    #~ int      /* length */
#~ );
XGetErrorDatabaseText = libX11.XGetErrorDatabaseText
XGetErrorDatabaseText.restype = c_int
XGetErrorDatabaseText.argtypes = [POINTER(Display), c_char_p, c_char_p, c_char_p, c_char_p, c_int]

#~ extern int XGetErrorText(
    #~ Display*    /* display */,
    #~ int      /* code */,
    #~ char*    /* buffer_return */,
    #~ int      /* length */
#~ );
XGetErrorText = libX11.XGetErrorText
XGetErrorText.restype = c_int
XGetErrorText.argtypes = [POINTER(Display), c_int, c_char_p, c_int]

#~ extern Bool XGetFontProperty(
    #~ XFontStruct*  /* font_struct */,
    #~ Atom    /* atom */,
    #~ unsigned long*  /* value_return */
#~ );
XGetFontProperty = libX11.XGetFontProperty
XGetFontProperty.restype = Bool
XGetFontProperty.argtypes = [POINTER(XFontStruct), Atom, POINTER(c_ulong)]

#~ extern Status XGetGCValues(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long  /* valuemask */,
    #~ XGCValues*    /* values_return */
#~ );
XGetGCValues = libX11.XGetGCValues
XGetGCValues.restype = Status
XGetGCValues.argtypes = [POINTER(Display), GC, c_ulong, POINTER(XGCValues)]

#~ extern Status XGetGeometry(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ Window*    /* root_return */,
    #~ int*    /* x_return */,
    #~ int*    /* y_return */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */,
    #~ unsigned int*  /* border_width_return */,
    #~ unsigned int*  /* depth_return */
#~ );
XGetGeometry = libX11.XGetGeometry
XGetGeometry.restype = Status
XGetGeometry.argtypes = [POINTER(Display), Drawable, POINTER(Window), POINTER(c_int), POINTER(c_int), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint)]

#~ extern Status XGetIconName(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ char**    /* icon_name_return */
#~ );
XGetIconName = libX11.XGetIconName
XGetIconName.restype = Status
XGetIconName.argtypes = [POINTER(Display), Window, POINTER(c_char_p)]

#~ extern int XGetInputFocus(
    #~ Display*    /* display */,
    #~ Window*    /* focus_return */,
    #~ int*    /* revert_to_return */
#~ );
XGetInputFocus = libX11.XGetInputFocus
XGetInputFocus.restype = c_int
XGetInputFocus.argtypes = [POINTER(Display), POINTER(Window), POINTER(c_int)]

#~ extern int XGetKeyboardControl(
    #~ Display*    /* display */,
    #~ XKeyboardState*  /* values_return */
#~ );
XGetKeyboardControl = libX11.XGetKeyboardControl
XGetKeyboardControl.restype = c_int
XGetKeyboardControl.argtypes = [POINTER(Display), POINTER(XKeyboardState)]

#~ extern int XGetPointerControl(
    #~ Display*    /* display */,
    #~ int*    /* accel_numerator_return */,
    #~ int*    /* accel_denominator_return */,
    #~ int*    /* threshold_return */
#~ );
XGetPointerControl = libX11.XGetPointerControl
XGetPointerControl.restype = c_int
XGetPointerControl.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

#~ extern int XGetPointerMapping(
    #~ Display*    /* display */,
    #~ unsigned char*  /* map_return */,
    #~ int      /* nmap */
#~ );
XGetPointerMapping = libX11.XGetPointerMapping
XGetPointerMapping.restype = c_int
XGetPointerMapping.argtypes = [POINTER(Display), c_char_p, c_int]

#~ extern int XGetScreenSaver(
    #~ Display*    /* display */,
    #~ int*    /* timeout_return */,
    #~ int*    /* interval_return */,
    #~ int*    /* prefer_blanking_return */,
    #~ int*    /* allow_exposures_return */
#~ );
XGetScreenSaver = libX11.XGetScreenSaver
XGetScreenSaver.restype = c_int
XGetScreenSaver.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

#~ extern Status XGetTransientForHint(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window*    /* prop_window_return */
#~ );
XGetTransientForHint = libX11.XGetTransientForHint
XGetTransientForHint.restype = c_int
XGetTransientForHint.argtypes = [POINTER(Display), Window, POINTER(Window)]

#~ extern int XGetWindowProperty(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom    /* property */,
    #~ long    /* long_offset */,
    #~ long    /* long_length */,
    #~ Bool    /* delete */,
    #~ Atom    /* req_type */,
    #~ Atom*    /* actual_type_return */,
    #~ int*    /* actual_format_return */,
    #~ unsigned long*  /* nitems_return */,
    #~ unsigned long*  /* bytes_after_return */,
    #~ unsigned char**  /* prop_return */
#~ );
XGetWindowProperty = libX11.XGetWindowProperty
XGetWindowProperty.restype = c_int
XGetWindowProperty.argtypes = [POINTER(Display), Window, Atom, c_long, c_long, Bool, Atom, POINTER(Atom), POINTER(c_int), POINTER(c_long), POINTER(c_long), POINTER(c_char_p)]

#~ extern Status XGetWindowAttributes(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ XWindowAttributes*  /* window_attributes_return */
#~ );
XGetWindowAttributes = libX11.XGetWindowAttributes
XGetWindowAttributes.restype = Status
XGetWindowAttributes.argtypes = [POINTER(Display), Window, POINTER(XWindowAttributes)]

#~ extern int XGrabButton(
    #~ Display*    /* display */,
    #~ unsigned int  /* button */,
    #~ unsigned int  /* modifiers */,
    #~ Window    /* grab_window */,
    #~ Bool    /* owner_events */,
    #~ unsigned int  /* event_mask */,
    #~ int      /* pointer_mode */,
    #~ int      /* keyboard_mode */,
    #~ Window    /* confine_to */,
    #~ Cursor    /* cursor */
#~ );
XGrabButton = libX11.XGrabButton
XGrabButton.restype = c_int
XGrabButton.argtypes = [POINTER(Display), c_uint, c_uint, Window, Bool, c_uint, c_int, c_int, Window, Cursor]

#~ extern int XGrabKey(
    #~ Display*    /* display */,
    #~ int      /* keycode */,
    #~ unsigned int  /* modifiers */,
    #~ Window    /* grab_window */,
    #~ Bool    /* owner_events */,
    #~ int      /* pointer_mode */,
    #~ int      /* keyboard_mode */
#~ );
XGrabKey = libX11.XGrabKey
XGrabKey.restype = c_int
XGrabKey.argtypes = [POINTER(Display), c_int, c_uint, Window, Bool, c_int, c_int]

#~ extern int XGrabKeyboard(
    #~ Display*    /* display */,
    #~ Window    /* grab_window */,
    #~ Bool    /* owner_events */,
    #~ int      /* pointer_mode */,
    #~ int      /* keyboard_mode */,
    #~ Time    /* time */
#~ );
XGrabKeyboard = libX11.XGrabKeyboard
XGrabKeyboard.restype = c_int
XGrabKeyboard.argtypes = [POINTER(Display), Window, Bool, c_int, c_int, Time]

#~ extern int XGrabPointer(
    #~ Display*    /* display */,
    #~ Window    /* grab_window */,
    #~ Bool    /* owner_events */,
    #~ unsigned int  /* event_mask */,
    #~ int      /* pointer_mode */,
    #~ int      /* keyboard_mode */,
    #~ Window    /* confine_to */,
    #~ Cursor    /* cursor */,
    #~ Time    /* time */
#~ );
XGrabPointer = libX11.XGrabPointer
XGrabPointer.restype = c_int
XGrabPointer.argtypes = [POINTER(Display), Window, Bool, c_uint, c_int, c_int, Window, Cursor, Time]

#~ extern int XGrabServer(
    #~ Display*    /* display */
#~ );
XGrabServer = libX11.XGrabServer
XGrabServer.restype = c_int
XGrabServer.argtypes = [POINTER(Display)]

#~ extern int XHeightMMOfScreen(
    #~ Screen*    /* screen */
#~ );
XHeightMMOfScreen = libX11.XHeightMMOfScreen
XHeightMMOfScreen.restype = c_int
XHeightMMOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XHeightOfScreen(
    #~ Screen*    /* screen */
#~ );
XHeightOfScreen = libX11.XHeightOfScreen
XHeightOfScreen.restype = c_int
XHeightOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XIfEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event_return */,
    #~ Bool (*) (
         #~ Display*      /* display */,
               #~ XEvent*      /* event */,
               #~ XPointer      /* arg */
             #~ )    /* predicate */,
    #~ XPointer    /* arg */
#~ );
XIfEvent = libX11.XIfEvent
XIfEvent.restype = c_int
XIfEvent.argtypes = [POINTER(Display), XEvent, c_void_p, XPointer]

#~ extern int XImageByteOrder(
    #~ Display*    /* display */
#~ );
XImageByteOrder = libX11.XImageByteOrder
XImageByteOrder.restype = c_int
XImageByteOrder.argtypes = [POINTER(Display)]

#~ extern int XInstallColormap(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */
#~ );
XInstallColormap = libX11.XInstallColormap
XInstallColormap.restype = c_int
XInstallColormap.argtypes = [POINTER(Display), Colormap]

#~ extern KeyCode XKeysymToKeycode(
    #~ Display*    /* display */,
    #~ KeySym    /* keysym */
#~ );
XKeysymToKeycode = libX11.XKeysymToKeycode
XKeysymToKeycode.restype = c_int
XKeysymToKeycode.argtypes = [POINTER(Display), KeySym]

#~ extern int XKillClient(
    #~ Display*    /* display */,
    #~ XID      /* resource */
#~ );
XKillClient = libX11.XKillClient
XKillClient.restype = c_int
XKillClient.argtypes = [POINTER(Display), XID]

#~ extern Status XLookupColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ _Xconst char*  /* color_name */,
    #~ XColor*    /* exact_def_return */,
    #~ XColor*    /* screen_def_return */
#~ );
XLookupColor = libX11.XLookupColor
XLookupColor.restype = Status
XLookupColor.argtypes = [POINTER(Display), Colormap, c_char_p, POINTER(XColor), POINTER(XColor)]

#~ extern int XLowerWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XLowerWindow = libX11.XLowerWindow
XLowerWindow.restype = c_int
XLowerWindow.argtypes = [POINTER(Display), Window]

#~ extern int XMapRaised(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XMapRaised = libX11.XMapRaised
XMapRaised.restype = c_int
XMapRaised.argtypes = [POINTER(Display), Window]

#~ extern int XMapSubwindows(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XMapSubwindows = libX11.XMapSubwindows
XMapSubwindows.restype = c_int
XMapSubwindows.argtypes = [POINTER(Display), Window]

#~ extern int XMapWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XMapWindow = libX11.XMapWindow
XMapWindow.restype = c_int
XMapWindow.argtypes = [POINTER(Display), Window]

#~ extern int XMaskEvent(
    #~ Display*    /* display */,
    #~ long    /* event_mask */,
    #~ XEvent*    /* event_return */
#~ );
XMaskEvent = libX11.XMaskEvent
XMaskEvent.restype = c_int
XMaskEvent.argtypes = [POINTER(Display), c_long, POINTER(XEvent)]

#~ extern int XMaxCmapsOfScreen(
    #~ Screen*    /* screen */
#~ );
XMaxCmapsOfScreen = libX11.XMaxCmapsOfScreen
XMaxCmapsOfScreen.restype = c_int
XMaxCmapsOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XMinCmapsOfScreen(
    #~ Screen*    /* screen */
#~ );
XMinCmapsOfScreen = libX11.XMinCmapsOfScreen
XMinCmapsOfScreen.restype = c_int
XMinCmapsOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XMoveResizeWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XMoveResizeWindow = libX11.XMoveResizeWindow
XMoveResizeWindow.restype = c_int
XMoveResizeWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint]

#~ extern int XMoveWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ int      /* x */,
    #~ int      /* y */
#~ );
XMoveWindow = libX11.XMoveWindow
XMoveWindow.restype = c_int
XMoveWindow.argtypes = [POINTER(Display), Window, c_int, c_int]

#~ extern int XNextEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event_return */
#~ );
XNextEvent = libX11.XNextEvent
XNextEvent.restype = c_int
XNextEvent.argtypes = [POINTER(Display), POINTER(XEvent)]

#~ extern int XNoOp(
    #~ Display*    /* display */
#~ );
XNoOp = libX11.XNoOp
XNoOp.restype = c_int
XNoOp.argtypes = [POINTER(Display)]

#~ extern Status XParseColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ _Xconst char*  /* spec */,
    #~ XColor*    /* exact_def_return */
#~ );
XParseColor = libX11.XParseColor
XParseColor.restype = Status
XParseColor.argtypes = [POINTER(Display), Colormap, c_char_p, POINTER(XColor)]

#~ extern int XParseGeometry(
    #~ _Xconst char*  /* parsestring */,
    #~ int*    /* x_return */,
    #~ int*    /* y_return */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */
#~ );
XParseGeometry = libX11.XParseGeometry
XParseGeometry.restype = c_int
XParseGeometry.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_uint), POINTER(c_uint)]

#~ extern int XPeekEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event_return */
#~ );
XPeekEvent = libX11.XPeekEvent
XPeekEvent.restype = c_int
XPeekEvent.argtypes = [POINTER(Display), POINTER(XEvent)]

#~ extern int XPeekIfEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event_return */,
    #~ Bool (*) (
         #~ Display*    /* display */,
               #~ XEvent*    /* event */,
               #~ XPointer    /* arg */
             #~ )    /* predicate */,
    #~ XPointer    /* arg */
#~ );
XPeekIfEvent = libX11.XPeekIfEvent
XPeekIfEvent.restype = c_int
XPeekIfEvent.argtypes = [POINTER(Display), POINTER(XEvent), c_void_p, XPointer]

#~ extern int XPending(
    #~ Display*    /* display */
#~ );
XPending = libX11.XPending
XPending.restype = c_int
XPending.argtypes = [POINTER(Display)]

#~ extern int XPlanesOfScreen(
    #~ Screen*    /* screen */
#~ );
XPlanesOfScreen = libX11.XPlanesOfScreen
XPlanesOfScreen.restype = c_int
XPlanesOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XProtocolRevision(
    #~ Display*    /* display */
#~ );
XProtocolRevision = libX11.XProtocolRevision
XProtocolRevision.restype = c_int
XProtocolRevision.argtypes = [POINTER(Display)]

#~ extern int XProtocolVersion(
    #~ Display*    /* display */
#~ );
XProtocolVersion = libX11.XProtocolVersion
XProtocolVersion.restype = c_int
XProtocolVersion.argtypes = [POINTER(Display)]

#~ extern int XPutBackEvent(
    #~ Display*    /* display */,
    #~ XEvent*    /* event */
#~ );
XPutBackEvent = libX11.XPutBackEvent
XPutBackEvent.restype = c_int
XPutBackEvent.argtypes = [POINTER(Display), POINTER(XEvent)]

#~ extern int XPutImage(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ XImage*    /* image */,
    #~ int      /* src_x */,
    #~ int      /* src_y */,
    #~ int      /* dest_x */,
    #~ int      /* dest_y */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XPutImage = libX11.XPutImage
XPutImage.restype = c_int
XPutImage.argtypes = [POINTER(Display), Drawable, GC, POINTER(XImage), c_int, c_int, c_int, c_int, c_uint, c_uint]

#~ extern int XQLength(
    #~ Display*    /* display */
#~ );
XQLength = libX11.XQLength
XQLength.restype = c_int
XQLength.argtypes = [POINTER(Display)]

#~ extern Status XQueryBestCursor(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ unsigned int        /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */
#~ );
XQueryBestCursor = libX11.XQueryBestCursor
XQueryBestCursor.restype = Status
XQueryBestCursor.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]

#~ extern Status XQueryBestSize(
    #~ Display*    /* display */,
    #~ int      /* class */,
    #~ Drawable    /* which_screen */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */
#~ );
XQueryBestSize = libX11.XQueryBestSize
XQueryBestSize.restype = Status
XQueryBestSize.argtypes = [POINTER(Display), c_int, Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]

#~ extern Status XQueryBestStipple(
    #~ Display*    /* display */,
    #~ Drawable    /* which_screen */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */
#~ );
XQueryBestStipple = libX11.XQueryBestStipple
XQueryBestStipple.restype = Status
XQueryBestStipple.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]

#~ extern Status XQueryBestTile(
    #~ Display*    /* display */,
    #~ Drawable    /* which_screen */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */
#~ );
XQueryBestTile = libX11.XQueryBestTile
XQueryBestTile.restype = Status
XQueryBestTile.argtypes = [POINTER(Display), Drawable, c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]

#~ extern int XQueryColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ XColor*    /* def_in_out */
#~ );
XQueryColor = libX11.XQueryColor
XQueryColor.restype = c_int
XQueryColor.argtypes = [POINTER(Display), Colormap, POINTER(XColor)]

#~ extern int XQueryColors(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ XColor*    /* defs_in_out */,
    #~ int      /* ncolors */
#~ );
XQueryColors = libX11.XQueryColors
XQueryColors.restype = c_int
XQueryColors.argtypes = [POINTER(Display), Colormap, POINTER(XColor), c_int]

#~ extern Bool XQueryExtension(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* name */,
    #~ int*    /* major_opcode_return */,
    #~ int*    /* first_event_return */,
    #~ int*    /* first_error_return */
#~ );
XQueryExtension = libX11.XQueryExtension
XQueryExtension.restype = Bool
XQueryExtension.argtypes = [POINTER(Display), c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

#~ extern int XQueryKeymap(
    #~ Display*    /* display */,
    #~ char [32]    /* keys_return */
#~ );
XQueryKeymap = libX11.XQueryKeymap
XQueryKeymap.restype = c_int
XQueryKeymap.argtypes = [POINTER(Display), c_char * 32]

#~ extern Bool XQueryPointer(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window*    /* root_return */,
    #~ Window*    /* child_return */,
    #~ int*    /* root_x_return */,
    #~ int*    /* root_y_return */,
    #~ int*    /* win_x_return */,
    #~ int*    /* win_y_return */,
    #~ unsigned int*       /* mask_return */
#~ );
XQueryPointer = libX11.XQueryPointer
XQueryPointer.restype = Bool
XQueryPointer.argtypes = [POINTER(Display), Window, POINTER(Window), POINTER(Window), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_uint)]

#~ extern int XQueryTextExtents(
    #~ Display*    /* display */,
    #~ XID      /* font_ID */,
    #~ _Xconst char*  /* string */,
    #~ int      /* nchars */,
    #~ int*    /* direction_return */,
    #~ int*    /* font_ascent_return */,
    #~ int*    /* font_descent_return */,
    #~ XCharStruct*  /* overall_return */
#~ );
XQueryTextExtents = libX11.XQueryTextExtents
XQueryTextExtents.restype = c_int
XQueryTextExtents.argtypes = [POINTER(Display), XID, c_char_p, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]

#~ extern int XQueryTextExtents16(
    #~ Display*    /* display */,
    #~ XID      /* font_ID */,
    #~ _Xconst XChar2b*  /* string */,
    #~ int      /* nchars */,
    #~ int*    /* direction_return */,
    #~ int*    /* font_ascent_return */,
    #~ int*    /* font_descent_return */,
    #~ XCharStruct*  /* overall_return */
#~ );
XQueryTextExtents16 = libX11.XQueryTextExtents16
XQueryTextExtents16.restype = c_int
XQueryTextExtents16.argtypes = [POINTER(Display), XID, POINTER(XChar2b), c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]

#~ extern Status XQueryTree(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window*    /* root_return */,
    #~ Window*    /* parent_return */,
    #~ Window**    /* children_return */,
    #~ unsigned int*  /* nchildren_return */
#~ );
XQueryTree = libX11.XQueryTree
XQueryTree.restype = Status
XQueryTree.argtypes = [POINTER(Display), Window, POINTER(Window), POINTER(Window), POINTER(POINTER(Window)), POINTER(c_uint)]

#~ extern int XRaiseWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XRaiseWindow = libX11.XRaiseWindow
XRaiseWindow.restype = c_int
XRaiseWindow.argtypes = [POINTER(Display), Window]

#~ extern int XReadBitmapFile(
    #~ Display*    /* display */,
    #~ Drawable     /* d */,
    #~ _Xconst char*  /* filename */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */,
    #~ Pixmap*    /* bitmap_return */,
    #~ int*    /* x_hot_return */,
    #~ int*    /* y_hot_return */
#~ );
XReadBitmapFile = libX11.XReadBitmapFile
XReadBitmapFile.restype = c_int
XReadBitmapFile.argtypes = [POINTER(Display), Drawable, c_char_p, POINTER(c_uint), POINTER(c_uint), POINTER(Pixmap), POINTER(c_int), POINTER(c_int)]

#~ extern int XReadBitmapFileData(
    #~ _Xconst char*  /* filename */,
    #~ unsigned int*  /* width_return */,
    #~ unsigned int*  /* height_return */,
    #~ unsigned char**  /* data_return */,
    #~ int*    /* x_hot_return */,
    #~ int*    /* y_hot_return */
#~ );
XReadBitmapFileData = libX11.XReadBitmapFileData
XReadBitmapFileData.restype = c_int
XReadBitmapFileData.argtypes = [c_char_p, POINTER(c_uint), POINTER(c_uint), POINTER(c_char_p), POINTER(c_int), POINTER(c_int)]

#~ extern int XRebindKeysym(
    #~ Display*    /* display */,
    #~ KeySym    /* keysym */,
    #~ KeySym*    /* list */,
    #~ int      /* mod_count */,
    #~ _Xconst unsigned char*  /* string */,
    #~ int      /* bytes_string */
#~ );
XRebindKeysym = libX11.XRebindKeysym
XRebindKeysym.restype = c_int
XRebindKeysym.argtypes = [POINTER(Display), KeySym, POINTER(KeySym), c_int, c_char_p, c_int]

#~ extern int XRecolorCursor(
    #~ Display*    /* display */,
    #~ Cursor    /* cursor */,
    #~ XColor*    /* foreground_color */,
    #~ XColor*    /* background_color */
#~ );
XRecolorCursor = libX11.XRecolorCursor
XRecolorCursor.restype = c_int
XRecolorCursor.argtypes = [POINTER(Display), Cursor, POINTER(XColor), POINTER(XColor)]

#~ extern int XRefreshKeyboardMapping(
    #~ XMappingEvent*  /* event_map */
#~ );
XRefreshKeyboardMapping = libX11.XRefreshKeyboardMapping
XRefreshKeyboardMapping.restype = c_int
XRefreshKeyboardMapping.argtypes = [POINTER(XMappingEvent)]

#~ extern int XRemoveFromSaveSet(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XRemoveFromSaveSet = libX11.XRemoveFromSaveSet
XRemoveFromSaveSet.restype = c_int
XRemoveFromSaveSet.argtypes = [POINTER(Display), Window]

#~ extern int XRemoveHost(
    #~ Display*    /* display */,
    #~ XHostAddress*  /* host */
#~ );
XRemoveHost = libX11.XRemoveHost
XRemoveHost.restype = c_int
XRemoveHost.argtypes = [POINTER(Display), POINTER(XHostAddress)]

#~ extern int XRemoveHosts(
    #~ Display*    /* display */,
    #~ XHostAddress*  /* hosts */,
    #~ int      /* num_hosts */
#~ );
XRemoveHosts = libX11.XRemoveHosts
XRemoveHosts.restype = c_int
XRemoveHosts.argtypes = [POINTER(Display), POINTER(XHostAddress), c_int]

#~ extern int XReparentWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Window    /* parent */,
    #~ int      /* x */,
    #~ int      /* y */
#~ );
XReparentWindow = libX11.XReparentWindow
XReparentWindow.restype = c_int
XReparentWindow.argtypes = [POINTER(Display), Window, Window, c_int, c_int]

#~ extern int XResetScreenSaver(
    #~ Display*    /* display */
#~ );
XResetScreenSaver = libX11.XResetScreenSaver
XResetScreenSaver.restype = c_int
XResetScreenSaver.argtypes = [POINTER(Display)]

#~ extern int XResizeWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */
#~ );
XResizeWindow = libX11.XResizeWindow
XResizeWindow.restype = c_int
XResizeWindow.argtypes = [POINTER(Display), Window, c_uint, c_uint]

#~ extern int XRestackWindows(
    #~ Display*    /* display */,
    #~ Window*    /* windows */,
    #~ int      /* nwindows */
#~ );
XRestackWindows = libX11.XRestackWindows
XRestackWindows.restype = c_int
XRestackWindows.argtypes = [POINTER(Display), POINTER(Window), c_int]

#~ extern int XRotateBuffers(
    #~ Display*    /* display */,
    #~ int      /* rotate */
#~ );
XRotateBuffers = libX11.XRotateBuffers
XRotateBuffers.restype = c_int
XRotateBuffers.argtypes = [POINTER(Display), c_int]

#~ extern int XRotateWindowProperties(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Atom*    /* properties */,
    #~ int      /* num_prop */,
    #~ int      /* npositions */
#~ );
XRotateWindowProperties = libX11.XRotateWindowProperties
XRotateWindowProperties.restype = c_int
XRotateWindowProperties.argtypes = [POINTER(Display), Window, POINTER(Atom), c_int, c_int]

#~ extern int XScreenCount(
    #~ Display*    /* display */
#~ );
XScreenCount = libX11.XScreenCount
XScreenCount.restype = c_int
XScreenCount.argtypes = [POINTER(Display)]

#~ extern int XSelectInput(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ long    /* event_mask */
#~ );
XSelectInput = libX11.XSelectInput
XSelectInput.restype = c_int
XSelectInput.argtypes = [POINTER(Display), Window, c_long]

#~ extern Status XSendEvent(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Bool    /* propagate */,
    #~ long    /* event_mask */,
    #~ XEvent*    /* event_send */
#~ );
XSendEvent = libX11.XSendEvent
XSendEvent.restype = Status
XSendEvent.argtypes = [POINTER(Display), Window, Bool, c_long, POINTER(XEvent)]

#~ extern int XSetAccessControl(
    #~ Display*    /* display */,
    #~ int      /* mode */
#~ );
XSetAccessControl = libX11.XSetAccessControl
XSetAccessControl.restype = c_int
XSetAccessControl.argtypes = [POINTER(Display), c_int]

#~ extern int XSetArcMode(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* arc_mode */
#~ );
XSetArcMode = libX11.XSetArcMode
XSetArcMode.restype = c_int
XSetArcMode.argtypes = [POINTER(Display), GC, c_int]

#~ extern int XSetBackground(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long  /* background */
#~ );
XSetBackground = libX11.XSetBackground
XSetBackground.restype = c_int
XSetBackground.argtypes = [POINTER(Display), GC, c_ulong]

#~ extern int XSetClipMask(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ Pixmap    /* pixmap */
#~ );
XSetClipMask = libX11.XSetClipMask
XSetClipMask.restype = c_int
XSetClipMask.argtypes = [POINTER(Display), GC, Pixmap]

#~ extern int XSetClipOrigin(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* clip_x_origin */,
    #~ int      /* clip_y_origin */
#~ );
XSetClipOrigin = libX11.XSetClipOrigin
XSetClipOrigin.restype = c_int
XSetClipOrigin.argtypes = [POINTER(Display), GC, c_int, c_int]

#~ extern int XSetClipRectangles(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* clip_x_origin */,
    #~ int      /* clip_y_origin */,
    #~ XRectangle*    /* rectangles */,
    #~ int      /* n */,
    #~ int      /* ordering */
#~ );
XSetClipRectangles = libX11.XSetClipRectangles
XSetClipRectangles.restype = c_int
XSetClipRectangles.argtypes = [POINTER(Display), GC, c_int, c_int, POINTER(XRectangle), c_int, c_int]

#~ extern int XSetCloseDownMode(
    #~ Display*    /* display */,
    #~ int      /* close_mode */
#~ );
XSetCloseDownMode = libX11.XSetCloseDownMode
XSetCloseDownMode.restype = c_int
XSetCloseDownMode.argtypes = [POINTER(Display), c_int]

#~ extern int XSetCommand(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ char**    /* argv */,
    #~ int      /* argc */
#~ );
XSetCommand = libX11.XSetCommand
XSetCommand.restype = c_int
XSetCommand.argtypes = [POINTER(Display), Window, POINTER(c_char_p), c_int]

#~ extern int XSetDashes(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* dash_offset */,
    #~ _Xconst char*  /* dash_list */,
    #~ int      /* n */
#~ );
XSetDashes = libX11.XSetDashes
XSetDashes.restype = c_int
XSetDashes.argtypes = [POINTER(Display), GC, c_int, c_char_p, c_int]

#~ extern int XSetFillRule(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* fill_rule */
#~ );
XSetFillRule = libX11.XSetFillRule
XSetFillRule.restype = c_int
XSetFillRule.argtypes = [POINTER(Display), GC, c_int]

#~ extern int XSetFillStyle(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* fill_style */
#~ );
XSetFillStyle = libX11.XSetFillStyle
XSetFillStyle.restype = c_int
XSetFillStyle.argtypes = [POINTER(Display), GC, c_int]

#~ extern int XSetFont(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ Font    /* font */
#~ );
XSetFont = libX11.XSetFont
XSetFont.restype = c_int
XSetFont.argtypes = [POINTER(Display), GC, Font]

#~ extern int XSetFontPath(
    #~ Display*    /* display */,
    #~ char**    /* directories */,
    #~ int      /* ndirs */
#~ );
XSetFontPath = libX11.XSetFontPath
XSetFontPath.restype = c_int
XSetFontPath.argtypes = [POINTER(Display), POINTER(c_char_p), c_int]

#~ extern int XSetForeground(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long  /* foreground */
#~ );
XSetForeground = libX11.XSetForeground
XSetForeground.restype = c_int
XSetForeground.argtypes = [POINTER(Display), GC, c_ulong]

#~ extern int XSetFunction(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* function */
#~ );
XSetFunction = libX11.XSetFunction
XSetFunction.restype = c_int
XSetFunction.argtypes = [POINTER(Display), GC, c_int]

#~ extern int XSetGraphicsExposures(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ Bool    /* graphics_exposures */
#~ );
XSetGraphicsExposures = libX11.XSetGraphicsExposures
XSetGraphicsExposures.restype = c_int
XSetGraphicsExposures.argtypes = [POINTER(Display), GC, Bool]

#~ extern int XSetIconName(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ _Xconst char*  /* icon_name */
#~ );
XSetIconName = libX11.XSetIconName
XSetIconName.restype = c_int
XSetIconName.argtypes = [POINTER(Display), Window, c_char_p]

#~ extern int XSetInputFocus(
    #~ Display*    /* display */,
    #~ Window    /* focus */,
    #~ int      /* revert_to */,
    #~ Time    /* time */
#~ );
XSetInputFocus = libX11.XSetInputFocus
XSetInputFocus.restype = c_int
XSetInputFocus.argtypes = [POINTER(Display), Window, c_int, Time]

#~ extern int XSetLineAttributes(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned int  /* line_width */,
    #~ int      /* line_style */,
    #~ int      /* cap_style */,
    #~ int      /* join_style */
#~ );
XSetLineAttributes = libX11.XSetLineAttributes
XSetLineAttributes.restype = c_int
XSetLineAttributes.argtypes = [POINTER(Display), GC, c_uint, c_int, c_int, c_int]

#~ extern int XSetModifierMapping(
    #~ Display*    /* display */,
    #~ XModifierKeymap*  /* modmap */
#~ );
XSetModifierMapping = libX11.XSetModifierMapping
XSetModifierMapping.restype = c_int
XSetModifierMapping.argtypes = [POINTER(Display), POINTER(XModifierKeymap)]

#~ extern int XSetPlaneMask(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long  /* plane_mask */
#~ );
XSetPlaneMask = libX11.XSetPlaneMask
XSetPlaneMask.restype = c_int
XSetPlaneMask.argtypes = [POINTER(Display), GC, c_ulong]

#~ extern int XSetPointerMapping(
    #~ Display*    /* display */,
    #~ _Xconst unsigned char*  /* map */,
    #~ int      /* nmap */
#~ );
XSetPointerMapping = libX11.XSetPointerMapping
XSetPointerMapping.restype = c_int
XSetPointerMapping.argtypes = [POINTER(Display), c_char_p, c_int]

#~ extern int XSetScreenSaver(
    #~ Display*    /* display */,
    #~ int      /* timeout */,
    #~ int      /* interval */,
    #~ int      /* prefer_blanking */,
    #~ int      /* allow_exposures */
#~ );
XSetScreenSaver = libX11.XSetScreenSaver
XSetScreenSaver.restype = c_int
XSetScreenSaver.argtypes = [POINTER(Display), c_int, c_int, c_int, c_int]

#~ extern int XSetSelectionOwner(
    #~ Display*    /* display */,
    #~ Atom          /* selection */,
    #~ Window    /* owner */,
    #~ Time    /* time */
#~ );
XSetSelectionOwner = libX11.XSetSelectionOwner
XSetSelectionOwner.restype = c_int
XSetSelectionOwner.argtypes = [POINTER(Display), Atom, Window, Time]

#~ extern int XSetState(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ unsigned long   /* foreground */,
    #~ unsigned long  /* background */,
    #~ int      /* function */,
    #~ unsigned long  /* plane_mask */
#~ );
XSetState = libX11.XSetState
XSetState.restype = c_int
XSetState.argtypes = [POINTER(Display), GC, c_ulong, c_ulong, c_int, c_ulong]

#~ extern int XSetStipple(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ Pixmap    /* stipple */
#~ );
XSetStipple = libX11.XSetStipple
XSetStipple.restype = c_int
XSetStipple.argtypes = [POINTER(Display), GC, Pixmap]

#~ extern int XSetSubwindowMode(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* subwindow_mode */
#~ );
XSetSubwindowMode = libX11.XSetSubwindowMode
XSetSubwindowMode.restype = c_int
XSetSubwindowMode.argtypes = [POINTER(Display), GC, c_int]

#~ extern int XSetTSOrigin(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ int      /* ts_x_origin */,
    #~ int      /* ts_y_origin */
#~ );
XSetTSOrigin = libX11.XSetTSOrigin
XSetTSOrigin.restype = c_int
XSetTSOrigin.argtypes = [POINTER(Display), GC, c_int, c_int]

#~ extern int XSetTile(
    #~ Display*    /* display */,
    #~ GC      /* gc */,
    #~ Pixmap    /* tile */
#~ );
XSetTile = libX11.XSetTile
XSetTile.restype = c_int
XSetTile.argtypes = [POINTER(Display), GC, Pixmap]

#~ extern int XSetWindowBackground(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned long  /* background_pixel */
#~ );
XSetWindowBackground = libX11.XSetWindowBackground
XSetWindowBackground.restype = c_int
XSetWindowBackground.argtypes = [POINTER(Display), Window, c_ulong]

#~ extern int XSetWindowBackgroundPixmap(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Pixmap    /* background_pixmap */
#~ );
XSetWindowBackgroundPixmap = libX11.XSetWindowBackgroundPixmap
XSetWindowBackgroundPixmap.restype = c_int
XSetWindowBackgroundPixmap.argtypes = [POINTER(Display), Window, Pixmap]

#~ extern int XSetWindowBorder(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned long  /* border_pixel */
#~ );
XSetWindowBorder = libX11.XSetWindowBorder
XSetWindowBorder.restype = c_int
XSetWindowBorder.argtypes = [POINTER(Display), Window, c_ulong]

#~ extern int XSetWindowBorderPixmap(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Pixmap    /* border_pixmap */
#~ );
XSetWindowBorderPixmap = libX11.XSetWindowBorderPixmap
XSetWindowBorderPixmap.restype = c_int
XSetWindowBorderPixmap.argtypes = [POINTER(Display), Window, Pixmap]

#~ extern int XSetWindowBorderWidth(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ unsigned int  /* width */
#~ );
XSetWindowBorderWidth = libX11.XSetWindowBorderWidth
XSetWindowBorderWidth.restype = c_int
XSetWindowBorderWidth.argtypes = [POINTER(Display), Window, c_uint]

#~ extern int XSetWindowColormap(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ Colormap    /* colormap */
#~ );
XSetWindowColormap = libX11.XSetWindowColormap
XSetWindowColormap.restype = c_int
XSetWindowColormap.argtypes = [POINTER(Display), Window, Colormap]

#~ extern int XStoreBuffer(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* bytes */,
    #~ int      /* nbytes */,
    #~ int      /* buffer */
#~ );
XStoreBuffer = libX11.XStoreBuffer
XStoreBuffer.restype = c_int
XStoreBuffer.argtypes = [POINTER(Display), c_char_p, c_int, c_int]

#~ extern int XStoreBytes(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* bytes */,
    #~ int      /* nbytes */
#~ );
XStoreBytes = libX11.XStoreBytes
XStoreBytes.restype = c_int
XStoreBytes.argtypes = [POINTER(Display), c_char_p, c_int]

#~ extern int XStoreColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ XColor*    /* color */
#~ );
XStoreColor = libX11.XStoreColor
XStoreColor.restype = c_int
XStoreColor.argtypes = [POINTER(Display), Colormap, POINTER(XColor)]

#~ extern int XStoreColors(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ XColor*    /* color */,
    #~ int      /* ncolors */
#~ );
XStoreColors = libX11.XStoreColors
XStoreColors.restype = c_int
XStoreColors.argtypes = [POINTER(Display), Colormap, POINTER(XColor), c_int]

#~ extern int XStoreName(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ _Xconst char*  /* window_name */
#~ );
XStoreName = libX11.XStoreName
XStoreName.restype = c_int
XStoreName.argtypes = [POINTER(Display), Window, c_char_p]

#~ extern int XStoreNamedColor(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */,
    #~ _Xconst char*  /* color */,
    #~ unsigned long  /* pixel */,
    #~ int      /* flags */
#~ );
XStoreNamedColor = libX11.XStoreNamedColor
XStoreNamedColor.restype = c_int
XStoreNamedColor.argtypes = [POINTER(Display), Colormap, c_char_p, c_ulong, c_int]

#~ extern int XSync(
    #~ Display*    /* display */,
    #~ Bool    /* discard */
#~ );
XSync = libX11.XSync
XSync.restype = c_int
XSync.argtypes = [POINTER(Display), Bool]

#~ extern int XTextExtents(
    #~ XFontStruct*  /* font_struct */,
    #~ _Xconst char*  /* string */,
    #~ int      /* nchars */,
    #~ int*    /* direction_return */,
    #~ int*    /* font_ascent_return */,
    #~ int*    /* font_descent_return */,
    #~ XCharStruct*  /* overall_return */
#~ );
XTextExtents = libX11.XTextExtents
XTextExtents.restype = c_int
XTextExtents.argtypes = [POINTER(XFontStruct), c_char_p, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]

#~ extern int XTextExtents16(
    #~ XFontStruct*  /* font_struct */,
    #~ _Xconst XChar2b*  /* string */,
    #~ int      /* nchars */,
    #~ int*    /* direction_return */,
    #~ int*    /* font_ascent_return */,
    #~ int*    /* font_descent_return */,
    #~ XCharStruct*  /* overall_return */
#~ );
XTextExtents16 = libX11.XTextExtents16
XTextExtents16.restype = c_int
XTextExtents16.argtypes = [POINTER(XFontStruct), POINTER(XChar2b), c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(XCharStruct)]

#~ extern int XTextWidth(
    #~ XFontStruct*  /* font_struct */,
    #~ _Xconst char*  /* string */,
    #~ int      /* count */
#~ );
XTextWidth = libX11.XTextWidth
XTextWidth.restype = c_int
XTextWidth.argtypes = [POINTER(XFontStruct),  c_char_p, c_int]

#~ extern int XTextWidth16(
    #~ XFontStruct*  /* font_struct */,
    #~ _Xconst XChar2b*  /* string */,
    #~ int      /* count */
#~ );
XTextWidth16 = libX11.XTextWidth16
XTextWidth16.restype = c_int
XTextWidth16.argtypes = [POINTER(XFontStruct), POINTER(XChar2b), c_int]

#~ extern Bool XTranslateCoordinates(
    #~ Display*    /* display */,
    #~ Window    /* src_w */,
    #~ Window    /* dest_w */,
    #~ int      /* src_x */,
    #~ int      /* src_y */,
    #~ int*    /* dest_x_return */,
    #~ int*    /* dest_y_return */,
    #~ Window*    /* child_return */
#~ );
XTranslateCoordinates = libX11.XTranslateCoordinates
XTranslateCoordinates.restype = Bool
XTranslateCoordinates.argtypes = [POINTER(Display), Window, Window, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(Window)]

#~ extern int XUndefineCursor(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XUndefineCursor = libX11.XUndefineCursor
XUndefineCursor.restype = c_int
XUndefineCursor.argtypes = [POINTER(Display), Window]

#~ extern int XUngrabButton(
    #~ Display*    /* display */,
    #~ unsigned int  /* button */,
    #~ unsigned int  /* modifiers */,
    #~ Window    /* grab_window */
#~ );
XUngrabButton = libX11.XUngrabButton
XUngrabButton.restype = c_int
XUngrabButton.argtypes = [POINTER(Display), c_uint, c_uint, Window]

#~ extern int XUngrabKey(
    #~ Display*    /* display */,
    #~ int      /* keycode */,
    #~ unsigned int  /* modifiers */,
    #~ Window    /* grab_window */
#~ );
XUngrabKey = libX11.XUngrabKey
XUngrabKey.restype = c_int
XUngrabKey.argtypes = [POINTER(Display), c_int, c_uint, Window]

#~ extern int XUngrabKeyboard(
    #~ Display*    /* display */,
    #~ Time    /* time */
#~ );
XUngrabKeyboard = libX11.XUngrabKeyboard
XUngrabKeyboard.restype = c_int
XUngrabKeyboard.argtypes = [POINTER(Display), Time]

#~ extern int XUngrabPointer(
    #~ Display*    /* display */,
    #~ Time    /* time */
#~ );
XUngrabPointer = libX11.XUngrabPointer
XUngrabPointer.restype = c_int
XUngrabPointer.argtypes = [POINTER(Display), Time]

#~ extern int XUngrabServer(
    #~ Display*    /* display */
#~ );
XUngrabServer = libX11.XUngrabServer
XUngrabServer.restype = c_int
XUngrabServer.argtypes = [POINTER(Display)]

#~ extern int XUninstallColormap(
    #~ Display*    /* display */,
    #~ Colormap    /* colormap */
#~ );
XUninstallColormap = libX11.XUninstallColormap
XUninstallColormap.restype = c_int
XUninstallColormap.argtypes = [POINTER(Display), Colormap]

#~ extern int XUnloadFont(
    #~ Display*    /* display */,
    #~ Font    /* font */
#~ );
XUnloadFont = libX11.XUnloadFont
XUnloadFont.restype = c_int
XUnloadFont.argtypes = [POINTER(Display), Font]

#~ extern int XUnmapSubwindows(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XUnmapSubwindows = libX11.XUnmapSubwindows
XUnmapSubwindows.restype = c_int
XUnmapSubwindows.argtypes = [POINTER(Display), Window]

#~ extern int XUnmapWindow(
    #~ Display*    /* display */,
    #~ Window    /* w */
#~ );
XUnmapWindow = libX11.XUnmapWindow
XUnmapWindow.restype = c_int
XUnmapWindow.argtypes = [POINTER(Display), Window]

#~ extern int XVendorRelease(
    #~ Display*    /* display */
#~ );
XVendorRelease = libX11.XVendorRelease
XVendorRelease.restype = c_int
XVendorRelease.argtypes = [POINTER(Display)]

#~ extern int XWarpPointer(
    #~ Display*    /* display */,
    #~ Window    /* src_w */,
    #~ Window    /* dest_w */,
    #~ int      /* src_x */,
    #~ int      /* src_y */,
    #~ unsigned int  /* src_width */,
    #~ unsigned int  /* src_height */,
    #~ int      /* dest_x */,
    #~ int      /* dest_y */
#~ );
XWarpPointer = libX11.XWarpPointer
XWarpPointer.restype = c_int
XWarpPointer.argtypes = [POINTER(Display), Window, Window, c_int, c_int, c_uint, c_uint, c_int, c_int]

#~ extern int XWidthMMOfScreen(
    #~ Screen*    /* screen */
#~ );
XWidthMMOfScreen = libX11.XWidthMMOfScreen
XWidthMMOfScreen.restype = c_int
XWidthMMOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XWidthOfScreen(
    #~ Screen*    /* screen */
#~ );
XWidthOfScreen = libX11.XWidthOfScreen
XWidthOfScreen.restype = c_int
XWidthOfScreen.argtypes = [POINTER(Screen)]

#~ extern int XWindowEvent(
    #~ Display*    /* display */,
    #~ Window    /* w */,
    #~ long    /* event_mask */,
    #~ XEvent*    /* event_return */
#~ );
XWindowEvent = libX11.XWindowEvent
XWindowEvent.restype = c_int
XWindowEvent.argtypes = [POINTER(Display), Window, c_long, POINTER(XEvent)]

#~ extern int XWriteBitmapFile(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* filename */,
    #~ Pixmap    /* bitmap */,
    #~ unsigned int  /* width */,
    #~ unsigned int  /* height */,
    #~ int      /* x_hot */,
    #~ int      /* y_hot */
#~ );
XWriteBitmapFile = libX11.XWriteBitmapFile
XWriteBitmapFile.restype = c_int
XWriteBitmapFile.argtypes = [POINTER(Display), c_char_p, Pixmap, c_uint, c_uint, c_int, c_int]

#~ extern Bool XSupportsLocale (void);
XSupportsLocale = libX11.XSupportsLocale
XSupportsLocale.restype = Bool
XSupportsLocale.argtypes = []

#~ extern char *XSetLocaleModifiers(
    #~ const char*    /* modifier_list */
#~ );
XSetLocaleModifiers = libX11.XSetLocaleModifiers
XSetLocaleModifiers.restype = c_char_p
XSetLocaleModifiers.argtypes = [c_char_p]

#~ extern XOM XOpenOM(
    #~ Display*      /* display */,
    #~ struct _XrmHashBucketRec*  /* rdb */,
    #~ _Xconst char*    /* res_name */,
    #~ _Xconst char*    /* res_class */
#~ );
XOpenOM = libX11.XOpenOM
XOpenOM.restype = XOM
XOpenOM.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), c_char_p, c_char_p]

#~ extern Status XCloseOM(
    #~ XOM      /* om */
#~ );
XCloseOM = libX11.XCloseOM
XCloseOM.restype = Status
XCloseOM.argtypes = [XOM]

#~ extern char *XSetOMValues(
    #~ XOM      /* om */,
    #~ ...
#~ ) _X_SENTINEL(0);
XSetOMValues = libX11.XSetOMValues
XSetOMValues.restype = c_char_p
XSetOMValues.argtypes = [XOM]

#~ extern char *XGetOMValues(
    #~ XOM      /* om */,
    #~ ...
#~ ) _X_SENTINEL(0);
XGetOMValues = libX11.XGetOMValues
XGetOMValues.restype = c_char_p
XGetOMValues.argtypes = [XOM]

#~ extern Display *XDisplayOfOM(
    #~ XOM      /* om */
#~ );
XDisplayOfOM = libX11.XDisplayOfOM
XDisplayOfOM.restype = Display
XDisplayOfOM.argtypes = [XOM]

#~ extern char *XLocaleOfOM(
    #~ XOM      /* om */
#~ );
XLocaleOfOM = libX11.XLocaleOfOM
XLocaleOfOM.restype = c_char_p
XLocaleOfOM.argtypes = [XOM]

#~ extern XOC XCreateOC(
    #~ XOM      /* om */,
    #~ ...
#~ ) _X_SENTINEL(0);
XCreateOC = libX11.XCreateOC
XCreateOC.restype = XOC
XCreateOC.argtypes = [XOM]

#~ extern void XDestroyOC(
    #~ XOC      /* oc */
#~ );
XDestroyOC = libX11.XDestroyOC
XDestroyOC.argtypes = [XOC]

#~ extern XOM XOMOfOC(
    #~ XOC      /* oc */
#~ );
XOMOfOC = libX11.XOMOfOC
XOMOfOC.restype = XOM
XOMOfOC.argtypes = [XOC]

#~ extern char *XSetOCValues(
    #~ XOC      /* oc */,
    #~ ...
#~ ) _X_SENTINEL(0);
XSetOCValues = libX11.XSetOCValues
XSetOCValues.restype = c_char_p
XSetOCValues.argtypes = [XOC]

#~ extern char *XGetOCValues(
    #~ XOC      /* oc */,
    #~ ...
#~ ) _X_SENTINEL(0);
XGetOCValues = libX11.XGetOCValues
XGetOCValues.restype = c_char_p
XGetOCValues.argtypes = [XOC]

#~ extern XFontSet XCreateFontSet(
    #~ Display*    /* display */,
    #~ _Xconst char*  /* base_font_name_list */,
    #~ char***    /* missing_charset_list */,
    #~ int*    /* missing_charset_count */,
    #~ char**    /* def_string */
#~ );
XCreateFontSet = libX11.XCreateFontSet
XCreateFontSet.restype = XFontSet
XCreateFontSet.argtypes = [POINTER(Display), c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int), POINTER(c_char_p)]

#~ extern void XFreeFontSet(
    #~ Display*    /* display */,
    #~ XFontSet    /* font_set */
#~ );
XFreeFontSet = libX11.XFreeFontSet
XFreeFontSet.argtypes = [POINTER(Display), XFontSet]

#~ extern int XFontsOfFontSet(
    #~ XFontSet    /* font_set */,
    #~ XFontStruct***  /* font_struct_list */,
    #~ char***    /* font_name_list */
#~ );
XFontsOfFontSet = libX11.XFontsOfFontSet
XFontsOfFontSet.restype = c_int
XFontsOfFontSet.argtypes = [XFontSet, POINTER(POINTER(POINTER(XFontStruct))), POINTER(POINTER(c_char_p))]

#~ extern char *XBaseFontNameListOfFontSet(
    #~ XFontSet    /* font_set */
#~ );
XBaseFontNameListOfFontSet = libX11.XBaseFontNameListOfFontSet
XBaseFontNameListOfFontSet.restype = c_char_p
XBaseFontNameListOfFontSet.argtypes = [XFontSet]

#~ extern char *XLocaleOfFontSet(
    #~ XFontSet    /* font_set */
#~ );
XLocaleOfFontSet = libX11.XLocaleOfFontSet
XLocaleOfFontSet.restype = c_char_p
XLocaleOfFontSet.argtypes = [XFontSet]

#~ extern Bool XContextDependentDrawing(
    #~ XFontSet    /* font_set */
#~ );
XContextDependentDrawing = libX11.XContextDependentDrawing
XContextDependentDrawing.restype = Bool
XContextDependentDrawing.argtypes = [XFontSet]

#~ extern Bool XDirectionalDependentDrawing(
    #~ XFontSet    /* font_set */
#~ );
XDirectionalDependentDrawing = libX11.XDirectionalDependentDrawing
XDirectionalDependentDrawing.restype = Bool
XDirectionalDependentDrawing.argtypes = [XFontSet]

#~ extern Bool XContextualDrawing(
    #~ XFontSet    /* font_set */
#~ );
XContextualDrawing = libX11.XContextualDrawing
XContextualDrawing.restype = Bool
XContextualDrawing.argtypes = [XFontSet]

#~ extern XFontSetExtents *XExtentsOfFontSet(
    #~ XFontSet    /* font_set */
#~ );
XExtentsOfFontSet = libX11.XExtentsOfFontSet
XExtentsOfFontSet.restype = POINTER(XFontSetExtents)
XExtentsOfFontSet.argtypes = [XFontSet]

#~ extern int XmbTextEscapement(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
XmbTextEscapement = libX11.XmbTextEscapement
XmbTextEscapement.restype = c_int
XmbTextEscapement.argtypes = [XFontSet, c_char_p, c_int]

#~ extern int XwcTextEscapement(
    #~ XFontSet    /* font_set */,
    #~ _Xconst wchar_t*  /* text */,
    #~ int      /* num_wchars */
#~ );
XwcTextEscapement = libX11.XwcTextEscapement
XwcTextEscapement.restype = c_int
XwcTextEscapement.argtypes = [XFontSet, c_char_p, c_int]

#~ extern int Xutf8TextEscapement(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
Xutf8TextEscapement = libX11.Xutf8TextEscapement
Xutf8TextEscapement.restype = c_int
Xutf8TextEscapement.argtypes = [XFontSet, c_char_p, c_int]

#~ extern int XmbTextExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
XmbTextExtents = libX11.XmbTextExtents
XmbTextExtents.restype = c_int
XmbTextExtents.argtypes = [XFontSet, c_char_p, c_int, POINTER(XRectangle), POINTER(XRectangle)]

#~ extern int XwcTextExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst wchar_t*  /* text */,
    #~ int      /* num_wchars */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
XwcTextExtents = libX11.XwcTextExtents
XwcTextExtents.restype = c_int
XwcTextExtents.argtypes = [XFontSet, c_wchar_p, c_int, POINTER(XRectangle), POINTER(XRectangle)]

#~ extern int Xutf8TextExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
Xutf8TextExtents = libX11.Xutf8TextExtents
Xutf8TextExtents.restype = c_int
Xutf8TextExtents.argtypes = [XFontSet, c_char_p, c_int, POINTER(XRectangle), POINTER(XRectangle)]

#~ extern Status XmbTextPerCharExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */,
    #~ XRectangle*    /* ink_extents_buffer */,
    #~ XRectangle*    /* logical_extents_buffer */,
    #~ int      /* buffer_size */,
    #~ int*    /* num_chars */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
XmbTextPerCharExtents = libX11.XmbTextPerCharExtents
XmbTextPerCharExtents.restype = Status
XmbTextPerCharExtents.argtypes = [XFontSet, c_char_p, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]

#~ extern Status XwcTextPerCharExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst wchar_t*  /* text */,
    #~ int      /* num_wchars */,
    #~ XRectangle*    /* ink_extents_buffer */,
    #~ XRectangle*    /* logical_extents_buffer */,
    #~ int      /* buffer_size */,
    #~ int*    /* num_chars */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
XwcTextPerCharExtents = libX11.XwcTextPerCharExtents
XwcTextPerCharExtents.restype = Status
XwcTextPerCharExtents.argtypes = [XFontSet, c_wchar_p, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]

#~ extern Status Xutf8TextPerCharExtents(
    #~ XFontSet    /* font_set */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */,
    #~ XRectangle*    /* ink_extents_buffer */,
    #~ XRectangle*    /* logical_extents_buffer */,
    #~ int      /* buffer_size */,
    #~ int*    /* num_chars */,
    #~ XRectangle*    /* overall_ink_return */,
    #~ XRectangle*    /* overall_logical_return */
#~ );
Xutf8TextPerCharExtents = libX11.Xutf8TextPerCharExtents
Xutf8TextPerCharExtents.restype = Status
Xutf8TextPerCharExtents.argtypes = [XFontSet, c_char_p, c_int, POINTER(XRectangle), POINTER(XRectangle), c_int, POINTER(c_int), POINTER(XRectangle), POINTER(XRectangle)]

#~ extern void XmbDrawText(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ XmbTextItem*  /* text_items */,
    #~ int      /* nitems */
#~ );
XmbDrawText = libX11.XmbDrawText
XmbDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XmbTextItem), c_int]

#~ extern void XwcDrawText(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ XwcTextItem*  /* text_items */,
    #~ int      /* nitems */
#~ );
XwcDrawText = libX11.XwcDrawText
XwcDrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XwcTextItem), c_int]

#~ extern void Xutf8DrawText(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ XmbTextItem*  /* text_items */,
    #~ int      /* nitems */
#~ );
Xutf8DrawText = libX11.Xutf8DrawText
Xutf8DrawText.argtypes = [POINTER(Display), Drawable, GC, c_int, c_int, POINTER(XmbTextItem), c_int]

#~ extern void XmbDrawString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
XmbDrawString = libX11.XmbDrawString
XmbDrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_char_p, c_int]

#~ extern void XwcDrawString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst wchar_t*  /* text */,
    #~ int      /* num_wchars */
#~ );
XwcDrawString = libX11.XwcDrawString
XwcDrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_wchar_p, c_int]

#~ extern void Xutf8DrawString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
Xutf8DrawString = libX11.Xutf8DrawString
Xutf8DrawString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_char_p, c_int]

#~ extern void XmbDrawImageString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
XmbDrawImageString = libX11.XmbDrawImageString
XmbDrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_char_p, c_int]

#~ extern void XwcDrawImageString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst wchar_t*  /* text */,
    #~ int      /* num_wchars */
#~ );
XwcDrawImageString = libX11.XwcDrawImageString
XwcDrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_wchar_p, c_int]

#~ extern void Xutf8DrawImageString(
    #~ Display*    /* display */,
    #~ Drawable    /* d */,
    #~ XFontSet    /* font_set */,
    #~ GC      /* gc */,
    #~ int      /* x */,
    #~ int      /* y */,
    #~ _Xconst char*  /* text */,
    #~ int      /* bytes_text */
#~ );
Xutf8DrawImageString = libX11.Xutf8DrawImageString
Xutf8DrawImageString.argtypes = [POINTER(Display), Drawable, XFontSet, GC, c_int, c_int, c_char_p, c_int]

#~ extern XIM XOpenIM(
    #~ Display*      /* dpy */,
    #~ struct _XrmHashBucketRec*  /* rdb */,
    #~ char*      /* res_name */,
    #~ char*      /* res_class */
#~ );
XOpenIM = libX11.XOpenIM
XOpenIM.restype = XIM
XOpenIM.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), c_char_p, c_char_p]

#~ extern Status XCloseIM(
    #~ XIM /* im */
#~ );
XCloseIM = libX11.XCloseIM
XCloseIM.restype = Status
XCloseIM.argtypes = [XIM]

#~ extern char *XGetIMValues(
    #~ XIM /* im */, ...
#~ ) _X_SENTINEL(0);
XGetIMValues = libX11.XGetIMValues
XGetIMValues.restype = c_char_p
XGetIMValues.argtypes = [XIM]

#~ extern char *XSetIMValues(
    #~ XIM /* im */, ...
#~ ) _X_SENTINEL(0);
XSetIMValues = libX11.XSetIMValues
XSetIMValues.restype = c_char_p
XSetIMValues.argtypes = [XIM]

#~ extern Display *XDisplayOfIM(
    #~ XIM /* im */
#~ );
XDisplayOfIM = libX11.XDisplayOfIM
XDisplayOfIM.restype = POINTER(Display)
XDisplayOfIM.argtypes = [XIM]

#~ extern char *XLocaleOfIM(
    #~ XIM /* im*/
#~ );
XLocaleOfIM = libX11.XLocaleOfIM
XLocaleOfIM.restype = c_char_p
XLocaleOfIM.argtypes = [XIM]

#~ extern XIC XCreateIC(
    #~ XIM /* im */, ...
#~ ) _X_SENTINEL(0);
XCreateIC = libX11.XCreateIC
XCreateIC.restype = XIC
XCreateIC.argtypes = [XIM]

#~ extern void XDestroyIC(
    #~ XIC /* ic */
#~ );
XDestroyIC = libX11.XDestroyIC
XDestroyIC.argtypes = [XIC]

#~ extern void XSetICFocus(
    #~ XIC /* ic */
#~ );
XSetICFocus = libX11.XSetICFocus
XSetICFocus.argtypes = [XIC]

#~ extern void XUnsetICFocus(
    #~ XIC /* ic */
#~ );
XUnsetICFocus = libX11.XUnsetICFocus
XUnsetICFocus.argtypes = [XIC]

#~ extern wchar_t *XwcResetIC(
    #~ XIC /* ic */
#~ );
XwcResetIC = libX11.XwcResetIC
XwcResetIC.restype = c_wchar_p
XwcResetIC.argtypes = [XIC]

#~ extern char *XmbResetIC(
    #~ XIC /* ic */
#~ );
XmbResetIC = libX11.XmbResetIC
XmbResetIC.restype = c_char_p
XmbResetIC.argtypes = [XIC]

#~ extern char *Xutf8ResetIC(
    #~ XIC /* ic */
#~ );
Xutf8ResetIC = libX11.Xutf8ResetIC
Xutf8ResetIC.restype = c_char_p
Xutf8ResetIC.argtypes = [XIC]

#~ extern char *XSetICValues(
    #~ XIC /* ic */, ...
#~ ) _X_SENTINEL(0);
XSetICValues = libX11.XSetICValues
XSetICValues.restype = c_char_p
XSetICValues.argtypes = [XIC]

#~ extern char *XGetICValues(
    #~ XIC /* ic */, ...
#~ ) _X_SENTINEL(0);
XGetICValues = libX11.XGetICValues
XGetICValues.restype = c_char_p
XGetICValues.argtypes = [XIC]

#~ extern XIM XIMOfIC(
    #~ XIC /* ic */
#~ );
XIMOfIC = libX11.XIMOfIC
XIMOfIC.restype = XIM
XIMOfIC.argtypes = [XIC]

#~ extern Bool XFilterEvent(
    #~ XEvent*  /* event */,
    #~ Window  /* window */
#~ );
XFilterEvent = libX11.XFilterEvent
XFilterEvent.restype = Bool
XFilterEvent.argtypes = [POINTER(XEvent), Window]

#~ extern int XmbLookupString(
    #~ XIC      /* ic */,
    #~ XKeyPressedEvent*  /* event */,
    #~ char*    /* buffer_return */,
    #~ int      /* bytes_buffer */,
    #~ KeySym*    /* keysym_return */,
    #~ Status*    /* status_return */
#~ );
XmbLookupString = libX11.XmbLookupString
XmbLookupString.restype = c_int
XmbLookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), c_char_p, c_int, POINTER(KeySym), POINTER(Status)]

#~ extern int XwcLookupString(
    #~ XIC      /* ic */,
    #~ XKeyPressedEvent*  /* event */,
    #~ wchar_t*    /* buffer_return */,
    #~ int      /* wchars_buffer */,
    #~ KeySym*    /* keysym_return */,
    #~ Status*    /* status_return */
#~ );
XwcLookupString = libX11.XwcLookupString
XwcLookupString.restype = c_int
XwcLookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), c_wchar_p, c_int, POINTER(KeySym), POINTER(Status)]

#~ extern int Xutf8LookupString(
    #~ XIC      /* ic */,
    #~ XKeyPressedEvent*  /* event */,
    #~ char*    /* buffer_return */,
    #~ int      /* bytes_buffer */,
    #~ KeySym*    /* keysym_return */,
    #~ Status*    /* status_return */
#~ );
Xutf8LookupString = libX11.Xutf8LookupString
Xutf8LookupString.restype = c_int
Xutf8LookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), c_char_p, c_int, POINTER(KeySym), POINTER(Status)]

#~ extern XVaNestedList XVaCreateNestedList(
    #~ int /*unused*/, ...
#~ ) _X_SENTINEL(0);
XVaCreateNestedList = libX11.XVaCreateNestedList
XVaCreateNestedList.restype = XVaNestedList
XVaCreateNestedList.argtypes = [c_int]

#~ /* internal connections for IMs */

#~ extern Bool XRegisterIMInstantiateCallback(
    #~ Display*      /* dpy */,
    #~ struct _XrmHashBucketRec*  /* rdb */,
    #~ char*      /* res_name */,
    #~ char*      /* res_class */,
    #~ XIDProc      /* callback */,
    #~ XPointer      /* client_data */
#~ );
XRegisterIMInstantiateCallback = libX11.XRegisterIMInstantiateCallback
XRegisterIMInstantiateCallback.restype = Bool
XRegisterIMInstantiateCallback.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), c_char_p, c_char_p, XIDProc, XPointer]

#~ extern Bool XUnregisterIMInstantiateCallback(
    #~ Display*      /* dpy */,
    #~ struct _XrmHashBucketRec*  /* rdb */,
    #~ char*      /* res_name */,
    #~ char*      /* res_class */,
    #~ XIDProc      /* callback */,
    #~ XPointer      /* client_data */
#~ );
XUnregisterIMInstantiateCallback = libX11.XUnregisterIMInstantiateCallback
XUnregisterIMInstantiateCallback.restype = Bool
XUnregisterIMInstantiateCallback.argtypes = [POINTER(Display), POINTER(_XrmHashBucketRec), c_char_p, c_char_p, XIDProc, XPointer]

#~ typedef void (*XConnectionWatchProc)(
    #~ Display*      /* dpy */,
    #~ XPointer      /* client_data */,
    #~ int        /* fd */,
    #~ Bool      /* opening */,   /* open or close flag */
    #~ XPointer*      /* watch_data */ /* open sets, close uses */
#~ );
XConnectionWatchProc = c_void_p

#~ extern Status XInternalConnectionNumbers(
    #~ Display*      /* dpy */,
    #~ int**      /* fd_return */,
    #~ int*      /* count_return */
#~ );
XInternalConnectionNumbers = libX11.XInternalConnectionNumbers
XInternalConnectionNumbers.restype = Status
XInternalConnectionNumbers.argtypes = [POINTER(Display), POINTER(POINTER(c_int)), POINTER(c_int)]

#~ extern void XProcessInternalConnection(
    #~ Display*      /* dpy */,
    #~ int        /* fd */
#~ );
XProcessInternalConnection = libX11.XProcessInternalConnection
XProcessInternalConnection.argtypes = [POINTER(Display), c_int]

#~ extern Status XAddConnectionWatch(
    #~ Display*      /* dpy */,
    #~ XConnectionWatchProc  /* callback */,
    #~ XPointer      /* client_data */
#~ );
XAddConnectionWatch = libX11.XAddConnectionWatch
XAddConnectionWatch.restype = Status
XAddConnectionWatch.argtypes = [POINTER(Display), XConnectionWatchProc, XPointer]

#~ extern void XRemoveConnectionWatch(
    #~ Display*      /* dpy */,
    #~ XConnectionWatchProc  /* callback */,
    #~ XPointer      /* client_data */
#~ );
XRemoveConnectionWatch = libX11.XRemoveConnectionWatch
XRemoveConnectionWatch.argtypes = [POINTER(Display), XConnectionWatchProc, XPointer]

#~ extern void XSetAuthorization(
    #~ char *      /* name */,
    #~ int        /* namelen */,
    #~ char *      /* data */,
    #~ int        /* datalen */
#~ );
XSetAuthorization = libX11.XSetAuthorization
XSetAuthorization.argtypes = [c_char_p, c_int, c_char_p, c_int]

#~ extern int _Xmbtowc(
    #~ wchar_t *      /* wstr */,
#~ #ifdef ISC
    #~ char const *    /* str */,
    #~ size_t      /* len */
#~ #else
    #~ char *      /* str */,
    #~ int        /* len */
#~ #endif
#~ );
_Xmbtowc = libX11._Xmbtowc
_Xmbtowc.restype = c_int
_Xmbtowc.argtypes = [c_wchar_p, c_char_p, c_ulong]

#~ extern int _Xwctomb(
    #~ char *      /* str */,
    #~ wchar_t      /* wc */
#~ );
_Xwctomb = libX11._Xwctomb
_Xwctomb.restype = c_int
_Xwctomb.argtypes = [c_char_p, c_wchar]
