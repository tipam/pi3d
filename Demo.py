#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

from pi3d.constants import STARTUP_MESSAGE

SUFFIX = '.py'

USE_TK = not True

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

  return sorted([f[:-len(SUFFIX)] for f in demofiles])

def prefix():
  print('(Any prefix also works)')

def usage(demo_list):
  print('Usage: %s [%s]' % (sys.argv[0], ', '.join(demo_list)))
  print()
  prefix()

def run_one_demo(demo):
  if not USE_TK:
    print()
    print('Running demo', demo)
    print()
  __import__('demos.' + demo)


def run_demo(demo, demo_list):
  demo = demo.lower()
  for d in demo_list:
    if d.lower().startswith(demo):
      run_one_demo(d)
  else:
    print("Didn't understand demo '%s'" % demo)
    usage(demo_list)

def select_demo(demo_list):
  if not USE_TK:
    print('Demos are:', ', '.join(demo_list))
    prefix()

  while True:
    if USE_TK:
      d = tk_demo(demo_list, STARTUP_MESSAGE)
    else:
      d = raw_input('Enter demo name: ')
    if not d:
      break
    elif not run_demo(d, demo_list):
      print("Didn't understand demo '%s'" % d)


if __name__ == '__main__':
  demo_list = get_demo_list()
  if len(sys.argv) is 1:
    select_demo(demo_list)

  elif len(sys.argv) is 2:
    run_demo(sys.argv[1], demo_list)

  else:
    print('Too many arguments to %s' % sys.argv[0])

