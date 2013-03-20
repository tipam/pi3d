#!/bin/bash

pushd /development/pi3d

pylint pi3d \
 --indent-string="  " \
 --include-ids=y \
 --disable=\
C0103,\
C0111,\
E0602,\
E0611,\
E1002,\
F0401,\
I0011,\
R0902,\
R0904,\
R0912,\
R0913,\
R0914,\
R0915,\
W0142,\
W0511,\
W0702\

# | /development/echomesh/code/python/experiments/FixLint.py
# FixLint is a tool of mine which fixes these outputs.

# EO602, EO611 and E1002 are very real possible errors which I've disabled
# because there are too many false positives due to Python path errors.

# Possibly useful errors that should be enabled again one day: C0111.

# TODO: figure out and fix Python path errors and re-enable "missing symbol"
# errors.

# TODO: this should probably be a pylint config file.