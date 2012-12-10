#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

SUFFIX = '.py'

USE_TK = True

def tk_demo(demos, message):
  import Tkinter

  root = Tkinter.Tk()
  root.title('pi3d demos')

  menubar = Tkinter.Menu(root)
  def make_menu(label):
    menu = Tkinter.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=menu, label=label)
    return menu

  def quit():
    root.destroy()

  file_menu = make_menu('File')
  file_menu.add_command(label='Quit', command=quit, accelerator='Ctrl+Q')
  root.bind_all('<Control-Q>', quit)

  demo_menu = make_menu('Demo')

  result = ['']
  def demo_runner(demo):
    def runner():
      result[0] = demo
      quit()
    return runner

  last_key = ''
  for demo in demos:
    runner = demo_runner(demo)
    extra = {}
    if demo[0] != last_key:
      last_key = demo[0].upper()
      extra['accelerator'] = last_key
      root.bind_all('<%s>' % last_key, runner)
    demo_menu.add_command(label=demo, command=runner, **extra)

  root.config(menu=menubar)

  label = Tkinter.Label(root, text='\n' + message + '\n')
  label.pack()
  root.mainloop()
  return result[0]

def get_demo_list():
  home = os.getcwd()
  demodir = os.path.join(home, 'demos')
  if not os.path.isdir(demodir):
    print('%s must be called from the root directory of pi3d' % sys.argv[0])
    return

  def is_demo(f):
    return f[0].isupper() and f.endswith(SUFFIX)

  demofiles = [f for f in os.listdir(demodir) if is_demo(f)]
  if not demofiles:
    print('There are no files in the demo directory')
    return

  demos = sorted([f[:-len(SUFFIX)] for f in demofiles])
  return ', '.join(demos)

def prefix():
  print('(Any prefix also works)')

def usage():
  print('Usage: %s [%s]' % demo_list)
  print()
  prefix()

def run_demo(demo):
  demo = demo.lower()
  for d in demos:
    if d.lower().startswith(demo):
      if not USE_TK:
        print()
        print('Running demo', d)
        print()
      __import__('demos.' + d)
      return True
  else:
    return False

def select_demo(demo_list)
  if len(sys.argv) is 1:
    if not USE_TK:
      print('Demos are:', demo_list)
    prefix()
    while True:
      d = tk_demo(demo_list) if USE_TK else raw_input('Enter demo name: ')
      if not d:
        break
      elif not run_demo(d):
        print("Didn't understand demo '%s'" % d)

  elif len(sys.argv) is 2:
    d = sys.argv[1]
    if not run_demo(d):
      print("Didn't understand command %s" % d)
      usage()
      exit(-1)

  else:
    print('Too many arguments to %s' % sys.argv[0])

if __name__ == '__main__':
  select_demo(get_demo_list())
