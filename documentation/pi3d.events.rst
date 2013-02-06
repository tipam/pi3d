events Package
==============

This powerful package can be used to handle inputs from controllers: mouse,
keyboard, joystick, gamepad, xbox etc::

  from pi3d.events.events import InputEvents, nameOf, codeOf
  ...
  DISPLAY = Display.create(...
  ...
  inputs = InputEvents()
  inputs.get_mouse_movement()
  ...
  while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
    ...
    inputs.do_input_events()
    mx, my, mv, mh, md = inputs.get_mouse_movement()
    ...
    jx, jy = inputs.get_joystick()
    ...
    jrx, jry = inputs.get_joystickR() # gamepad
    ...
    if inputs.key_state("BTN_LEFT"):
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))

    if inputs.key_state("KEY_W"):  #key W
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))
    ...
  inputs.release()
  DISPLAY.destroy()

This is a rough outline of its use, look in some of the demos [Silo.py] for more
details.



:mod:`event_consts` Module
--------------------------

.. automodule:: pi3d.events.event_consts
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`events` Module
--------------------

.. automodule:: pi3d.events.events
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`ioctl` Module
-------------------

.. automodule:: pi3d.events.ioctl
    :members:
    :undoc-members:
    :show-inheritance:

