""" simple utility search program to find libegl.dll and libglesv2.dll
on windows systems. These library files are used by various applications
such as the chrome or firefox browsers to provide OpenGL ES 2.0 emulation.

If this application doesn't find a location you should try the general
windows search (which will take a while if you search the whole disk from
the root). If that doesn't find anything you will have to install chrome
or firefox (which is probably worth doing anyway!)

You then need to change the file:
  pi3d/constants/__init__.py
lines c. 87 and 88 to match the path where the files can be found

You might find that pi3d doesn't work with all the version on your computer
i.e. on this one (cheap packard bell windows 8) there were six directories
containing the dll files, four worked and two didn't. 
"""

import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
      f_count = 0
      for name in files:
        if fnmatch.fnmatch(name, pattern[0]):
          f_count |= 1
        if fnmatch.fnmatch(name, pattern[1]):
          f_count |= 2
        if f_count == 3:
          result.append(root)
          break
    return result

path_list = ["\Program Files (x86)", "\Users\patrick\AppData", 
             "\Users\Default\AppData", "\OEM\Preload"]
results_list = []
for path in path_list:
  results_list.extend(find(['libegl.dll', 'libglesv2.dll'], path))

for r in results_list:
  print(r)



