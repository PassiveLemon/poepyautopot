import ast

from config import config

class Checks:
  def meter_check(self, meter, screen_load):
    # Take the pixels from the config and literally evaluate them as a tuple. Add/sub 5 from the pixels for a slight range to catch any minor pixel changes
    xl_raw, yl_raw = ast.literal_eval(meter.pixel)
    rl, gl, bl = screen_load[xl_raw, yl_raw]
    rl_empty, gl_empty, bl_empty, = ast.literal_eval(meter.empty)
    rl_empty_min, rl_empty_max = rl_empty - 5, rl_empty + 5
    gl_empty_min, gl_empty_max = gl_empty - 5, gl_empty + 5
    bl_empty_min, bl_empty_max = bl_empty - 5, bl_empty + 5
    if rl_empty_min <= rl <= rl_empty_max and gl_empty_min <= gl <= gl_empty_max and bl_empty_min <= bl <= bl_empty_max:
      meter.need = False
    else:
      meter.need = True

    if config.debug_enable == True and config.debug_life_enable == True:
      print(f"{meter}-pixel[exp{meter.pixel} - act{xl_raw, yl_raw}]")
      print(f"{meter}-rgb[exp({meter.empty}) - act{rl, gl, bl}]")

  def flask_check(self, flask, screen_load):
    if flask.enable == True:
      x1_raw, y1_raw = ast.literal_eval(flask.pixel)
      x1_off = (int(x1_raw) + int(flask.offset_x))
      r1, g1, b1 = screen_load[x1_off, y1_raw]
      r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask.empty)
      r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
      g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
      b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
      if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
        flask.valid = False
      else:
        flask.valid = True

    if config.debug_enable == True and config.debug_flask_enable == True:
      if flask.enable == True:
        print(f"{flask}-pixel[exp{flask.pixel} - act{x1_off, y1_raw}]")
        print(f"{flask}-rgb[exp({flask.empty}) - act{r1, g1, b1}]")

  def menu_check(self, menu, screen_load):
    x1_raw, y1_raw = ast.literal_eval(menu.pixel1)
    r1, g1, b1 = screen_load[x1_raw, y1_raw]
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(menu.color1)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      menu1 = True
    else:
      menu1 = False

    x2_raw, y2_raw = ast.literal_eval(menu.pixel2)
    r2, g2, b2 = screen_load[x2_raw, y2_raw]
    r2_empty, g2_empty, b2_empty, = ast.literal_eval(menu.color2)
    r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
    g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
    b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
    if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
      menu2 = True
    else:
      menu2 = False
    
    x3_raw, y3_raw = ast.literal_eval(menu.pixel3)
    r3, g3, b3 = screen_load[x3_raw, y3_raw]
    r3_empty, g3_empty, b3_empty, = ast.literal_eval(menu.color3)
    r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
    g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
    b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
    if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
      menu3 = True
    else:
      menu3 = False

    if menu1 == True and menu2 == True and menu3 == True:
      menu.inside = True
    else:
      menu.inside = False

    if config.debug_enable == True and config.debug_menu_enable == True:
      print(f"{menu}-pixel1[exp{menu.pixel1} - act{x1_raw, y1_raw}]")
      print(f"{menu}-rgb1[exp({menu.color1}) - act{r1, g1, b1}]")
      print(f"{menu}-pixel2[exp{menu.pixel2} - act{x2_raw, y2_raw}]")
      print(f"{menu}-rgb2[exp({menu.color2}) - act{r2, g2, b2}]")
      print(f"{menu}-pixel3[exp{menu.pixel3} - act{x3_raw, y3_raw}]")
      print(f"{menu}-rgb3[exp({menu.color3}) - act{r3, g3, b3}]")

checks = Checks()
