from ctypes import c_byte, c_char, c_float, c_int, c_short

"""
Converts iterables of Python types into tuple of types from ctypes.

We need this because we do all our calculations in Python types but then pass
them to an external C library which wants ctypes.

"""

def c_bytes(x):
  return (c_byte * len(x))(*x)

def c_chars(x):
  return (c_char * len(x))(*x)

def c_floats(x):
  return (c_float * len(x))(*x)

def c_ints(x):
  return (c_int * len(x))(*x)

def c_shorts(x):
  return (c_short * len(x))(*x)

