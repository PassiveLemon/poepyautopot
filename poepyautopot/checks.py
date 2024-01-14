from .objects import Config

def meter_check(meter, screen_load):
  x_raw, y_raw = meter.pixel
  screen = screen_load[x_raw, y_raw]
  empty_min = tuple(x - Config.main_range for x in meter.empty)
  empty_max = tuple(x + Config.main_range for x in meter.empty)
  if Config.main_verbose == 3:
    print(f"{meter}-pixel[exp{meter.pixel} - act{x_raw, y_raw}]")
    print(f"{meter}-rgb[exp({meter.empty}) - act{screen}]")
  if empty_min <= screen <= empty_max:
    meter.need = False
    return False
  else:
    meter.need = True
    return True

def flask_check(flask, screen_load):
  x_raw, y_raw = flask.pixel
  x_off = (int(x_raw) + int(flask.offset_x))
  screen = screen_load[x_off, y_raw]
  empty_min = tuple(x - Config.main_range for x in flask.empty)
  empty_max = tuple(x + Config.main_range for x in flask.empty)
  if Config.main_verbose == 3:
    print(f"{flask}-pixel[exp{flask.pixel} - act{x_off, y_raw}]")
    print(f"{flask}-rgb[exp({flask.empty}) - act{screen}]")
  if empty_min <= screen <= empty_max:
    flask.valid = False
    return False
  else:
    flask.valid = True
    return True

def menu_check(menu, screen_load):
  x1_raw, y1_raw = menu.pixel1
  screen1 = screen_load[x1_raw, y1_raw]
  empty_min1 = tuple(x - Config.main_range for x in menu.color1)
  empty_max1 = tuple(x + Config.main_range for x in menu.color1)
  if empty_min1 <= screen1 <= empty_max1:
    menu1 = True
  else:
    menu1 = False

  x2_raw, y2_raw = menu.pixel2
  screen2 = screen_load[x2_raw, y2_raw]
  empty_min2 = tuple(x - Config.main_range for x in menu.color2)
  empty_max2 = tuple(x + Config.main_range for x in menu.color2)
  if empty_min2 <= screen2 <= empty_max2:
    menu2 = True
  else:
    menu2 = False
  
  x3_raw, y3_raw = menu.pixel3
  screen3 = screen_load[x3_raw, y3_raw]
  empty_min3 = tuple(x - Config.main_range for x in menu.color3)
  empty_max3 = tuple(x + Config.main_range for x in menu.color3)
  if empty_min3 <= screen3 <= empty_max3:
    menu3 = True
  else:
    menu3 = False
  if Config.main_verbose == 3:
    print(f"{menu}-pixel1[exp{menu.pixel1} - act{x1_raw, y1_raw}]")
    print(f"{menu}-rgb1[exp({menu.color1}) - act{screen1}]")
    print(f"{menu}-pixel2[exp{menu.pixel2} - act{x2_raw, y2_raw}]")
    print(f"{menu}-rgb2[exp({menu.color2}) - act{screen2}]")
    print(f"{menu}-pixel3[exp{menu.pixel3} - act{x3_raw, y3_raw}]")
    print(f"{menu}-rgb3[exp({menu.color3}) - act{screen3}]")
  # If 2 of the 3 pixels match, return True. This allows the check to still pass, in case the cursor or something is covering a pixel
  if (menu1 and menu2) or (menu2 and menu3) or (menu3 and menu1):
    menu.inside = True
    return True
  else:
    menu.inside = False
    return False

