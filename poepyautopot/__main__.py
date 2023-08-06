import argparse
import ast
import asyncio
from evdev import UInput, ecodes as e
import multiprocessing
from PIL import ImageGrab
import random
import time
import threading
import yaml
#import ctypes.util

#x11 = ctypes.util.find_library("X11")
#if not x11:
#  print("No X11.")
#  exit()

# Init
def config_init():
  # Turn variables from config.yaml into usable variables in the script.
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", default="./config.yaml")
  config_file = parser.parse_args().file

  yaml_config = yaml.safe_load(open(config_file))

  #g just means the variable is globally assigned. Makes reading easier.
  global life_pixel, life_empty, mana_pixel, mana_empty, flask1_offset_x, flask2_offset_x, flask3_offset_x, flask4_offset_x, flask5_offset_x
  database = yaml_config["database"]
  life = database["life"]
  life_pixel = life["pixel"] #g
  life_empty = life["empty"] #g
  mana = database["mana"]
  mana_pixel = mana["pixel"] #g
  mana_empty = mana["empty"] #g
  database_flask = database["flask"]
  flask1_offset_x = database_flask["flask1_offset_x"] #g
  flask2_offset_x = database_flask["flask2_offset_x"] #g
  flask3_offset_x = database_flask["flask3_offset_x"] #g
  flask4_offset_x = database_flask["flask4_offset_x"] #g
  flask5_offset_x = database_flask["flask5_offset_x"] #g
  global escape_pixel1, escape_color1, escape_pixel2, escape_color2, escape_pixel3, escape_color3
  global loading_pixel1, loading_color1, loading_pixel2, loading_color2, loading_pixel3, loading_color3
  global death_pixel1, death_color1, death_pixel2, death_color2, death_pixel3, death_color3
  menus = database["menus"]
  escape = menus["escape"]
  escape_pixel1 = escape["pixel1"] #g
  escape_color1 = escape["color1"] #g
  escape_pixel2 = escape["pixel2"] #g
  escape_color2 = escape["color2"] #g
  escape_pixel3 = escape["pixel3"] #g
  escape_color3 = escape["color3"] #g
  loading = menus["loading"]
  loading_pixel1 = loading["pixel1"] #g
  loading_color1 = loading["color1"] #g
  loading_pixel2 = loading["pixel2"] #g
  loading_color2 = loading["color2"] #g
  loading_pixel3 = loading["pixel3"] #g
  loading_color3 = loading["color3"] #g
  death = menus["death"]
  death_pixel1 = death["pixel1"] #g
  death_color1 = death["color1"] #g
  death_pixel2 = death["pixel2"] #g
  death_color2 = death["color2"] #g
  death_pixel3 = death["pixel3"] #g
  death_color3 = death["color3"] #g

  global keyboard_event, screen_offset_x, screen_offset_y
  hardware = yaml_config["hardware"]
  keyboard_event = hardware["keyboard_event"] #g
  screen_offset = hardware["screen_offset"]
  screen_offset_x = screen_offset["x"] #g
  screen_offset_y = screen_offset["y"] #g

  global key_press_shortest, key_press_longest, key_press_range, key_press_std_dev, key_press_target, key_press_test_enable, key_press_test_delay, key_press_test_count
  key_press = yaml_config["key_press"]
  key_press_shortest = key_press["shortest"] #g
  key_press_longest = key_press["longest"] #g
  key_press_range = key_press["range"] #g
  key_press_std_dev = key_press["std_dev"] #g
  key_press_target = key_press["target"] #g

  global flask1_enable, flask1_pixel, flask1_empty, flask1_duration, flask1_react, flask1_always
  flask1 = yaml_config["flask1"]
  flask1_enable = flask1["enable"] #g
  flask1_type = flask1["type"]
  flask1_pixel = flask1_type["pixel"] #g
  flask1_empty = flask1_type["empty"] #g
  flask1_duration = flask1_type["duration"] #g
  flask1_react = flask1["react"] #g
  flask1_always = flask1["always"] #g

  global flask2_enable, flask2_pixel, flask2_empty, flask2_duration, flask2_react, flask2_always
  flask2 = yaml_config["flask2"]
  flask2_enable = flask2["enable"] #g
  flask2_type = flask2["type"]
  flask2_pixel = flask2_type["pixel"] #g
  flask2_empty = flask2_type["empty"] #g
  flask2_duration = flask2_type["duration"] #g
  flask2_react = flask1["react"] #g
  flask2_always = flask1["always"] #g

  global flask3_enable, flask3_pixel, flask3_empty, flask3_duration, flask3_react, flask3_always
  flask3 = yaml_config["flask3"]
  flask3_enable = flask3["enable"] #g
  flask3_type = flask3["type"]
  flask3_pixel = flask3_type["pixel"] #g
  flask3_empty = flask3_type["empty"] #g
  flask3_duration = flask3_type["duration"] #g
  flask3_react = flask1["react"] #g
  flask3_always = flask1["always"] #g

  global flask4_enable, flask4_pixel, flask4_empty, flask4_duration, flask4_react, flask4_always
  flask4 = yaml_config["flask4"]
  flask4_enable = flask4["enable"] #g
  flask4_type = flask4["type"]
  flask4_pixel = flask4_type["pixel"] #g
  flask4_empty = flask4_type["empty"] #g
  flask4_duration = flask4_type["duration"] #g
  flask4_react = flask1["react"] #g
  flask4_always = flask1["always"] #g

  global flask5_enable, flask5_pixel, flask5_empty, flask5_duration, flask5_react, flask5_always
  flask5 = yaml_config["flask5"]
  flask5_enable = flask5["enable"] #g
  flask5_type = flask5["type"]
  flask5_pixel = flask5_type["pixel"] #g
  flask5_empty = flask5_type["empty"] #g
  flask5_duration = flask5_type["duration"] #g
  flask5_react = flask1["react"] #g
  flask5_always = flask1["always"] #g

  global main_enable, main_life_enable, main_mana_enable, main_flask_enable, main_menu_enable
  main = yaml_config["main"]
  main_enable = main["enable"] #g
  main_life_enable = main["life"] #g
  main_mana_enable = main["mana"] #g
  main_flask_enable = main["flask"] #g
  main_menu_enable = main["menu"] #g

  global debug_enable, debug_life_enable, debug_mana_enable, debug_flask_enable, debug_menu_enable, debug_image_save_enable, debug_image_save_location
  debug = yaml_config["debug"]
  debug_enable = debug["enable"] #g
  debug_life_enable = debug["life"] #g
  debug_mana_enable = debug["mana"] #g
  debug_flask_enable = debug["flask"] #g
  debug_menu_enable = debug["menu"] #g
  debug_image_save = debug["image_save"]
  debug_image_save_enable = debug_image_save["enable"] #g
  debug_image_save_location = debug_image_save["location"] #g

  global test_enable, key_press_test_enable, key_press_test_delay, key_press_test_count
  test = yaml_config["test"]
  test_enable = test["enable"] #g
  key_press_test = test["key_press_test"]
  key_press_test_enable = key_press_test["enable"] #g
  key_press_test_delay = key_press_test["delay"] #g
  key_press_test_count = key_press_test["count"] #g

  global life_need, mana_need, flask1_valid, flask1_lock, flask2_valid, flask2_lock, flask3_valid, flask3_lock, flask4_valid, flask4_lock, flask5_valid, flask5_lock, flask_handoff, inside_menu
  life_need = False
  mana_need = False
  flask1_valid = True
  flask1_lock = False
  flask2_valid = True
  flask2_lock = False
  flask3_valid = True
  flask3_lock = False
  flask4_valid = True
  flask4_lock = False
  flask5_valid = True
  flask5_lock = False
  flask_handoff = False
  inside_menu = False

def key_press_init():
  global key_press_shortest_low, key_press_shortest_high, key_press_longest_low, key_press_longest_high
  key_press_shortest_low = key_press_shortest - key_press_range
  key_press_shortest_high = key_press_shortest + key_press_range
  key_press_longest_low = key_press_longest - key_press_range
  key_press_longest_high = key_press_longest + key_press_range

config_init()
key_press_init()


# Utility
def key_press(num, wait, flasknum):
  global flask1_lock, flask2_lock, flask3_lock, flask4_lock, flask5_lock
  # Bell curve to more closely group presses
  def bell_curve(min, max, sig, mu):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  ui = UInput.from_device(keyboard_event)
  ui.write(e.EV_KEY, num, 1)
  ui.syn()

  # Variate key press length with random lows and highs, std dev, and target.
  random_range_low = random.randint(key_press_shortest_low, key_press_shortest_high)
  random_range_high = random.randint(key_press_longest_low, key_press_longest_high)
  random_key_press_sleep = bell_curve(random_range_low, random_range_high, key_press_std_dev, key_press_target)
  time.sleep(random_key_press_sleep / 1000.0)

  ui.write(e.EV_KEY, num, 0)
  ui.syn()
  ui.close()
  print(f"{num} ({random_key_press_sleep} ms)")
  print(f"waiting {wait} seconds")
  time.sleep(wait / 1.5)

  if flasknum == "flask1":
    flask1_lock = False
  if flasknum == "flask2":
    flask2_lock = False
  if flasknum == "flask3":
    flask3_lock = False
  if flasknum == "flask4":
    flask4_lock = False
  if flasknum == "flask5":
    flask5_lock = False

def screen_capture():
  global screen_load
  screen_capture = ImageGrab.grab(bbox=(screen_offset_x, screen_offset_y, 1920 + screen_offset_x, 1080 + screen_offset_y))
  screen_load = screen_capture.load()

  if debug_enable == True and debug_image_save_enable == True:
    screen_capture.save("./screen.png")

def life_check():
  global life_need
  xl_raw, yl_raw = ast.literal_eval(life_pixel)
  rl, gl, bl = screen_load[xl_raw, yl_raw]
  rl_empty, gl_empty, bl_empty, = ast.literal_eval(life_empty)
  rl_empty_min, rl_empty_max = rl_empty - 5, rl_empty + 5
  gl_empty_min, gl_empty_max = gl_empty - 5, gl_empty + 5
  bl_empty_min, bl_empty_max = bl_empty - 5, bl_empty + 5
  if rl_empty_min <= rl <= rl_empty_max and gl_empty_min <= gl <= gl_empty_max and bl_empty_min <= bl <= bl_empty_max:
    life_need = False
  else:
    life_need = True

  if debug_enable == True and debug_life_enable == True:
    print(f"life-pixel[exp{main_life_pixel} - act{xl_raw, yl_raw}]")
    print(f"life-rgb[exp({main_life_empty}) - act{rl, gl, bl}]")

def mana_check():
  global mana_need
  xm_raw, ym_raw = ast.literal_eval(mana_pixel)
  rm, gm, bm = screen_load[xm_raw, ym_raw]
  rm_empty, gm_empty, bm_empty, = ast.literal_eval(mana_empty)
  rm_empty_min, rm_empty_max = rm_empty - 5, rm_empty + 5
  gm_empty_min, gm_empty_max = gm_empty - 5, gm_empty + 5
  bm_empty_min, bm_empty_max = bm_empty - 5, bm_empty + 5
  if rm_empty_min <= rm <= rm_empty_max and gm_empty_min <= gm <= gm_empty_max and bm_empty_min <= bm <= bm_empty_max:
    mana_need = False
  else:
    mana_need = True

  if debug_enable == True and debug_mana_enable == True:
    print(f"mana-pixel[exp{main_mana_pixel} - act{xm_raw, ym_raw}]")
    print(f"mana-rgb[exp({main_mana_empty}) - act{rm, gm, bm}]")

def flask_check():
  global flask1_valid, flask2_valid, flask3_valid, flask4_valid, flask5_valid
  if flask1_enable == True:
    x1_raw, y1_raw = ast.literal_eval(flask1_pixel)
    x1_off = (int(x1_raw) + int(flask1_offset_x))
    r1, g1, b1 = screen_load[x1_off, y1_raw]
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask1_empty)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      flask1_valid = False
    else:
      flask1_valid = True

  if flask2_enable == True:
    x2_raw, y2_raw = ast.literal_eval(flask2_pixel)
    x2_off = (int(x2_raw) + int(flask2_offset_x))
    r2, g2, b2 = screen_load[x2_off, y2_raw]
    r2_empty, g2_empty, b2_empty, = ast.literal_eval(flask2_empty)
    r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
    g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
    b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
    if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
      flask2_valid = False
    else:
      flask2_valid = True

  if flask3_enable == True:
    x3_raw, y3_raw = ast.literal_eval(flask3_pixel)
    x3_off = (int(x3_raw) + int(flask3_offset_x))
    r3, g3, b3 = screen_load[x3_off, y3_raw]
    r3_empty, g3_empty, b3_empty, = ast.literal_eval(flask3_empty)
    r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
    g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
    b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
    if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
      flask3_valid = False
    else:
      flask3_valid = True
  
  if flask4_enable == True:
    x4_raw, y4_raw = ast.literal_eval(flask4_pixel)
    x4_off = (int(x4_raw) + int(flask4_offset_x))
    r4, g4, b4 = screen_load[x4_off, y4_raw]
    r4_empty, g4_empty, b4_empty, = ast.literal_eval(flask4_empty)
    r4_empty_min, r4_empty_max = r4_empty - 5, r4_empty + 5
    g4_empty_min, g4_empty_max = g4_empty - 5, g4_empty + 5
    b4_empty_min, b4_empty_max = b4_empty - 5, b4_empty + 5
    if r4_empty_min <= r4 <= r4_empty_max and g4_empty_min <= g4 <= g4_empty_max and b4_empty_min <= b4 <= b4_empty_max:
      flask4_valid = False
    else:
      flask4_valid = True

  if flask5_enable == True:
    x5_raw, y5_raw = ast.literal_eval(flask5_pixel)
    x5_off = (int(x5_raw) + int(flask5_offset_x))
    r5, g5, b5 = screen_load[x5_off, y5_raw]
    r5_empty, g5_empty, b5_empty, = ast.literal_eval(flask5_empty)
    r5_empty_min, r5_empty_max = r5_empty - 5, r5_empty + 5
    g5_empty_min, g5_empty_max = g5_empty - 5, g5_empty + 5
    b5_empty_min, b5_empty_max = b5_empty - 5, b5_empty + 5
    if r5_empty_min <= r5 <= r5_empty_max and g5_empty_min <= g5 <= g5_empty_max and b5_empty_min <= b5 <= b5_empty_max:
      flask5_valid = False
    else:
      flask5_valid = True

  if debug_enable == True and debug_flask_enable == True:
    if flask1_enable == True:
      print(f"flask1-pixel[exp{flask1_pixel} - act{x1_off, y1_raw}]")
      print(f"flask1-rgb[exp({flask1_empty}) - act{r1, g1, b1}]")
    if flask2_enable == True:
      print(f"flask2-pixel[exp{flask2_pixel} - act{x2_off, y2_raw}]")
      print(f"flask2-rgb[exp({flask2_empty}) - act{r2, g2, b2}]")
    if flask3_enable == True:
      print(f"flask3-pixel[exp{flask3_pixel} - act{x3_off, y3_raw}]")
      print(f"flask3-rgb[exp({flask3_empty}) - act{r3, g3, b3}]")
    if flask4_enable == True:
      print(f"flask4-pixel[exp{flask3_pixel} - act{x4_off, y4_raw}]")
      print(f"flask4-rgb[exp({flask3_empty}) - act{r4, g4, b4}]")
    if flask5_enable == True:
      print(f"flask5-pixel[exp{flask3_pixel} - act{x5_off, y5_raw}]")
      print(f"flask5-rgb[exp({flask3_empty}) - act{r5, g5, b5}]")

def escape_check():
  global escape_inside
  x1_raw, y1_raw = ast.literal_eval(escape_pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(escape_color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    escape1 = True
  else:
    escape1 = False

  x2_raw, y2_raw = ast.literal_eval(escape_pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(escape_color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    escape2 = True
  else:
    escape2 = False
  
  x3_raw, y3_raw = ast.literal_eval(escape_pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(escape_color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    escape3 = True
  else:
    escape3 = False

  if escape1 == True and escape2 == True and escape3 == True:
    escape_inside = True
  else:
    escape_inside = False

  if debug_enable == True and debug_menu_enable == True:
    print(f"escape-pixel1[exp{escape_pixel1} - act{x1_raw, y1_raw}]")
    print(f"escape-rgb1[exp({escape_color1}) - act{r1, g1, b1}]")
    print(f"escape-pixel2[exp{escape_pixel2} - act{x2_raw, y2_raw}]")
    print(f"escape-rgb2[exp({escape_color2}) - act{r2, g2, b2}]")
    print(f"escape-pixel3[exp{escape_pixel3} - act{x3_raw, y3_raw}]")
    print(f"escape-rgb3[exp({escape_color3}) - act{r3, g3, b3}]")

def loading_check():
  global loading_inside
  x1_raw, y1_raw = ast.literal_eval(loading_pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(loading_color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    loading1 = True
  else:
    loading1 = False

  x2_raw, y2_raw = ast.literal_eval(loading_pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(loading_color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    loading2 = True
  else:
    loading2 = False
  
  x3_raw, y3_raw = ast.literal_eval(loading_pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(loading_color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    loading3 = True
  else:
    loading3 = False

  if loading1 == True and loading2 == True and loading3 == True:
    loading_inside = True
  else:
    loading_inside = False
  
  if debug_enable == True and debug_menu_enable == True:
    print(f"loading-pixel1[exp{loading_pixel1} - act{x1_raw, y1_raw}]")
    print(f"loading-rgb1[exp({loading_color1}) - act{r1, g1, b1}]")
    print(f"loading-pixel2[exp{loading_pixel2} - act{x2_raw, y2_raw}]")
    print(f"loading-rgb2[exp({loading_color2}) - act{r2, g2, b2}]")
    print(f"loading-pixel3[exp{loading_pixel3} - act{x3_raw, y3_raw}]")
    print(f"loading-rgb3[exp({loading_color3}) - act{r3, g3, b3}]")

def death_check():
  global death_inside
  x1_raw, y1_raw = ast.literal_eval(death_pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(death_color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    death1 = True
  else:
    death1 = False

  x2_raw, y2_raw = ast.literal_eval(death_pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(death_color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    death2 = True
  else:
    death2 = False
  
  x3_raw, y3_raw = ast.literal_eval(death_pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(death_color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    death3 = True
  else:
    death3 = False

  if death1 == True and death2 == True and death3 == True:
    death_inside = True
  else:
    death_inside = False

  if debug_enable == True and debug_menu_enable == True:
    print(f"death-pixel1[exp{death_pixel1} - act{x1_raw, y1_raw}]")
    print(f"death-rgb1[exp({death_color1}) - act{r1, g1, b1}]")
    print(f"death-pixel2[exp{death_pixel2} - act{x2_raw, y2_raw}]")
    print(f"death-rgb2[exp({death_color2}) - act{r2, g2, b2}]")
    print(f"death-pixel3[exp{death_pixel3} - act{x3_raw, y3_raw}]")
    print(f"death-rgb3[exp({death_color3}) - act{r3, g3, b3}]")

# Main
def main():
  flask_handoff = False
  i = 0
  while True:
    global flask1_lock, flask2_lock, flask3_lock, flask4_lock, flask5_lock
    screen_capture()

    if main_menu_enable == True:
      escape_check()
      loading_check()
      death_check()

    if main_life_enable == True:
      life_check()
    if main_mana_enable == True:
      mana_check()
    if main_flask_enable == True:
      flask_check()

    if escape_inside == True or loading_inside == True or death_inside == True:
      inside_menu = True
    else:
      inside_menu = False

    if inside_menu != True or main_menu_enable == False:
      print(f"{i} life-{life_need} mana-{mana_need} 1-{flask1_valid} 2-{flask2_valid} 3-{flask3_valid} 4-{flask4_valid} 5-{flask5_valid}")

      if life_need == True:
        if (flask1_enable == True and flask1_valid == True) and (flask1_react == "Life" or flask1_always == True):
          flask1_press_life = threading.Thread(target=key_press, args=[e.KEY_1, flask1_duration, "flask1"])
          if flask1_lock == False:
            flask1_lock = True
            flask1_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask2_enable == True and flask2_valid == True) and ((flask2_react == "Life" and flask_handoff == True) or flask2_always == True):
          flask2_press_life = threading.Thread(target=key_press, args=[e.KEY_2, flask2_duration, "flask2"])
          if flask2_lock == False:
            flask2_lock = True
            flask2_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask3_enable == True and flask3_valid == True) and ((flask3_react == "Life" and flask_handoff == True) or flask3_always == True):
          flask3_press_life = threading.Thread(target=key_press, args=[e.KEY_3, flask3_duration, "flask3"])
          if flask3_lock == False:
            flask3_lock = True
            flask3_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if (flask4_enable == True and flask4_valid == True) and ((flask4_react == "Life" and flask_handoff == True) or flask4_always == True):
          flask4_press_life = threading.Thread(target=key_press, args=[e.KEY_4, flask4_duration, "flask4"])
          if flask4_lock == False:
            flask4_lock = True
            flask4_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if (flask5_enable == True and flask5_valid == True) and ((flask5_react == "Life" and flask_handoff == True) or flask5_always == True):
          flask5_press_life = threading.Thread(target=key_press, args=[e.KEY_5, flask5_duration, "flask5"])
          if flask5_lock == False:
            flask5_lock = True
            flask5_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if flask_handoff == True:
          print("Life tick not available")

      flask_handoff = False

      if mana_need == True:
        if (flask1_enable == True and flask1_valid == True) and (flask1_react == "mana" or flask1_always == True):
          flask1_press_mana = threading.Thread(target=key_press, args=[e.KEY_1, flask1_duration, "flask1"])
          if flask1_lock == False:
            flask1_lock = True
            flask1_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask2_enable == True and flask2_valid == True) and ((flask2_react == "mana" and flask_handoff == True) or flask2_always == True):
          flask2_press_mana = threading.Thread(target=key_press, args=[e.KEY_2, flask2_duration, "flask2"])
          if flask2_lock == False:
            flask2_lock = True
            flask2_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask3_enable == True and flask3_valid == True) and ((flask3_react == "mana" and flask_handoff == True) or flask3_always == True):
          flask3_press_mana = threading.Thread(target=key_press, args=[e.KEY_3, flask3_duration, "flask3"])
          if flask3_lock == False:
            flask3_lock = True
            flask3_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if (flask4_enable == True and flask4_valid == True) and ((flask4_react == "mana" and flask_handoff == True) or flask4_always == True):
          flask4_press_mana = threading.Thread(target=key_press, args=[e.KEY_4, flask4_duration, "flask4"])
          if flask4_lock == False:
            flask4_lock = True
            flask4_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if (flask5_enable == True and flask5_valid == True) and ((flask5_react == "mana" and flask_handoff == True) or flask5_always == True):
          flask5_press_mana = threading.Thread(target=key_press, args=[e.KEY_5, flask5_duration, "flask5"])
          if flask5_lock == False:
            flask5_lock = True
            flask5_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True
        if flask_handoff == True:
          print("mana tick not available")
      
      flask_handoff = False
    else:
      print(f"{i} escape-{escape_inside} loading-{loading_inside} death-{death_inside}")

    i += 1

if main_enable == True:
  main()

# Tests
def key_press_test():
  time.sleep(key_press_test_delay)
  key_map = {
    1: e.KEY_1,
    2: e.KEY_2,
    3: e.KEY_3,
    4: e.KEY_4,
    5: e.KEY_5,
  }
  i = key_press_test_count
  while i > 0:
    random_key = random.randint(1, 5)
    key_press(key_map[random_key])
    i -= 1

def test():
  if key_press_test_enable == True:
    key_press_test()

if test_enable == True:
  test()

