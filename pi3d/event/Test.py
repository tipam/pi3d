
if __name__ == "__main__":
  def mouse_handler_func(sourceType, sourceIndex, x, y, v, h):
    print("Relative[{:d}] ({:d}, {:d}), ({:d}, {:d})".format(sourceIndex, x, y, v, h))
    pass

  def joystick_handler_func(sourceType, sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty):
    print("Absolute[{:d}] ({:6.3f}, {:6.3f}, {:6.3f}), ({:6.3f}, {:6.3f}, {:6.3f}), ({:2.0f}, {:2.0f})".format(sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty))
    pass

  def unhandled_handler_func(event):
    print("Unknown: {}".format(event))
    pass

  def key_handler_func(sourceType, sourceIndex, key, value):
    print("{}[{}]={}".format(nameOf[key], sourceIndex, value))
    pass

  def syn_handler_func(sourceType, sourceIndex, code, value):
    #print("SYN {} {}".format(code,value))
    pass

  inputs = InputEvents( key_handler_func, mouse_handler_func, joystick_handler_func, syn_handler_func, unhandled_handler_func)
  #inputs = InputEvents(key_handler_func)


  while not inputs.key_state("KEY_ESC"):
    inputs.do_input_events()
    if inputs.key_state("KEY_LEFTCTRL"):
      inputs.grab_by_type("keyboard", grab=False)
      print("Name:")
      s = input()
      print("Hello {}".format(s))
      inputs.grab_by_type("keyboard", True)
    if inputs.key_state("BTN_LEFT"):
      v = inputs.get_mouse_movement()
      if v != (0,0,0,0,0):
          print(v)
    if inputs.key_state("BTN_RIGHT"):
      v = inputs.get_mouse_movement(1)
      if v != (0,0,0,0,0):
          print(v)
    if inputs.key_state("BTN_TOP2"):      #gamepad L1
      print(inputs.get_joystick())        #gamepad Left Analogue
    if inputs.key_state("BTN_BASE"):      #gamepad R1
      print(inputs.get_joystickR())      #gamepad Right Analogue
    if inputs.key_state("BTN_PINKIE"):      #gamepad L2
      v = inputs.get_hat()          #gamepad Direction pad
      if v != (0,0):
          print(v)
    if inputs.key_state("BTN_BASE2"):      #gamepad R2
      print(inputs.get_joystickR(1))      #gamepad Right Analogue (2nd device)

