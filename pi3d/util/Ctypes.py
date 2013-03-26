from ctypes import c_byte, c_char, c_float, c_int, c_short

"""
Converts iterables of Python types into tuple of types from ctypes.

We need this because we do all our calculations in Python types but then pass
them to an external C library which wants ctypes.

"""

def c_bytes(x):
  """Return a tuple of c_byte, converted from a list of Python variables."""
  return (c_byte * len(x))(*x)

def c_chars(x):
  """Return a tuple of c_char, converted from a list of Python variables."""
  return (c_char * len(x))(*x)

def c_floats(x):
  return (c_float * len(x))(*x)
  """Return a tuple of c_float, converted from a list of Python variables."""

def c_ints(x):
  """Return a tuple of c_int, converted from a list of Python variables."""
  return (c_int * len(x))(*x)

def c_shorts(x):
  """Return a tuple of c_short, converted from a list of Python variables."""
  return (c_short * len(x))(*x)

