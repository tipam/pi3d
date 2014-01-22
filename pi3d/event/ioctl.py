#define _ASM_GENERIC_IOCTL_H
# I'm not claiming any copyright for transforming this from the above header file
# Copyright is with the original, so it's probably GPLv2.
#
# ioctl command encoding: 32 bits total, command in lower 16 bits,
# size of the parameter structure in the lower 14 bits of the
# upper 16 bits.
# Encoding the size of the parameter structure in the ioctl request
# is useful for catching programs compiled with old versions
# and to avoid overwriting user space outside the user buffer area.
# The highest 2 bits are reserved for indicating the ``access mode''.
# NOTE: This limits the max parameter size to 16kB -1 !
#
#
#
# The following is for compatibility across the various Linux
# platforms.  The generic ioctl numbering scheme doesn't really enforce
# a type field.  De facto, however, the top 8 bits of the lower 16
# bits are indeed used as a type field, so we might just as well make
# this explicit here.  Please be sure to use the decoding macros
# below from now on.
#

import struct
sizeof = struct.calcsize
_IOC_TYPECHECK = sizeof

_IOC_NRBITS	= 8
_IOC_TYPEBITS = 8

# 
# Let any architecture override either of the following before
# including this file.
# 

_IOC_SIZEBITS =	14
_IOC_DIRBITS = 2

_IOC_NRMASK	= ((1 << _IOC_NRBITS)-1)
_IOC_TYPEMASK =	((1 << _IOC_TYPEBITS)-1)
_IOC_SIZEMASK =	((1 << _IOC_SIZEBITS)-1)
_IOC_DIRMASK =	((1 << _IOC_DIRBITS)-1)

_IOC_NRSHIFT	= 0
_IOC_TYPESHIFT	= (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT	= (_IOC_TYPESHIFT+_IOC_TYPEBITS)
_IOC_DIRSHIFT	= (_IOC_SIZESHIFT+_IOC_SIZEBITS)

# 
# Direction bits, which any architecture can choose to override
# before including this file.
# 

_IOC_NONE	= 0
_IOC_WRITE	= 1
_IOC_READ	= 2

def _IOC(dir, type, nr, size):
 return int(((dir)  << _IOC_DIRSHIFT) |
        ((type) << _IOC_TYPESHIFT) |
        ((nr)   << _IOC_NRSHIFT) |
        ((size) << _IOC_SIZESHIFT))

# used to create numbers */
def _IO(type,nr):
  return _IOC(_IOC_NONE,(type),(nr),0)
def _IOR(type,nr,format):
  return _IOC(_IOC_READ,(type),(nr),(_IOC_TYPECHECK(format)))
def _IOW(type,nr,format):
  return _IOC(_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(format)))
def _IOWR(type,nr,format):
  return _IOC(_IOC_READ|_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(format)))
def _IOR_BAD(type,nr,format):
  return _IOC(_IOC_READ,(type),(nr),sizeof(format))
def _IOW_BAD(type,nr,format):
  return _IOC(_IOC_WRITE,(type),(nr),sizeof(format))
def _IOWR_BAD(type,nr,format):
  return _IOC(_IOC_READ|_IOC_WRITE,(type),(nr),sizeof(format))

# used to decode ioctl numbers.. */
def _IOC_DIR(nr):
  return (((nr) >> _IOC_DIRSHIFT) & _IOC_DIRMASK)
def _IOC_TYPE(nr):
  return (((nr) >> _IOC_TYPESHIFT) & _IOC_TYPEMASK)
def _IOC_NR(nr):
  return (((nr) >> _IOC_NRSHIFT) & _IOC_NRMASK)
def _IOC_SIZE(nr):
  return (((nr) >> _IOC_SIZESHIFT) & _IOC_SIZEMASK)

# ...and for the drivers/sound files... */

IOC_IN = (_IOC_WRITE << _IOC_DIRSHIFT)
IOC_OUT = (_IOC_READ << _IOC_DIRSHIFT)
IOC_INOUT = ((_IOC_WRITE|_IOC_READ) << _IOC_DIRSHIFT)
IOCSIZE_MASK = (_IOC_SIZEMASK << _IOC_SIZESHIFT)
IOCSIZE_SHIFT = (_IOC_SIZESHIFT)

#endif /* _ASM_GENERIC_IOCTL_H */
