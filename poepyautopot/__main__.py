import argparse
import ast
import asyncio
from evdev import UInput, ecodes as e
import multiprocessing
from PIL import ImageGrab
import random
import time
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

  global main_enable, main_life_enable, main_mana_enable, main_flask_enable
  main = yaml_config["main"]
  main_enable = main["enable"] #g
  main_life_enable = main["life"] #g
  main_mana_enable = main["mana"] #g
  main_flask_enable = main["flask"] #g

  global debug_enable, debug_life_enable, debug_life_pixel, debug_life_rgb, debug_mana_enable, debug_mana_pixel, debug_mana_rgb, debug_flask_enable, debug_image_save_enable, debug_image_save_location
  debug = yaml_config["debug"]
  debug_enable = debug["enable"] #g
  debug_life = debug["life"]
  debug_life_enable = debug_life["enable"] #g
  debug_life_pixel = debug_life["pixel"] #g
  debug_life_rgb = debug_life["rgb"] #g
  debug_mana = debug["mana"]
  debug_mana_enable = debug_mana["enable"] #g
  debug_mana_pixel = debug_mana["pixel"] #g
  debug_mana_rgb = debug_mana["rgb"] #g
  debug_flask_enable = debug["flask"]
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

  global life_need, mana_need, flask1_valid, flask2_valid, flask3_valid, flask4_valid, flask5_valid
  life_need = False
  mana_need = False
  flask1_valid = True
  flask2_valid = True
  flask3_valid = True
  flask4_valid = True
  flask5_valid = True

def key_press_init():
  global key_press_shortest_low, key_press_shortest_high, key_press_longest_low, key_press_longest_high
  key_press_shortest_low = key_press_shortest - key_press_range
  key_press_shortest_high = key_press_shortest + key_press_range
  key_press_longest_low = key_press_longest - key_press_range
  key_press_longest_high = key_press_longest + key_press_range

config_init()
key_press_init()


# Utility
def key_press(num, wait):
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
  time.sleep(wait / 1.25)

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

# Main
def main():
  i = 0
  while True:
    screen_capture()
    if main_life_enable == True:
      life_check()
    if main_mana_enable == True:
      mana_check()
    if main_flask_enable == True:
      flask_check()

    print(f"{i} life-{life_need} mana-{mana_need} 1-{flask1_valid} 2-{flask2_valid} 3-{flask3_valid} 4-{flask4_valid} 5-{flask5_valid}")

    if life_need == True:
      if (flask1_enable == True and flask1_valid == True) and (flask1_react == "Life" or flask1_always):
        key_press(e.KEY_1, flask1_duration)
      elif (flask2_enable == True and flask2_valid == True) and (flask2_react == "Life" or flask2_always):
        key_press(e.KEY_2, flask2_duration)
      elif (flask3_enable == True and flask3_valid == True) and (flask3_react == "Life" or flask3_always):
        key_press(e.KEY_3, flask3_duration)
      elif (flask4_enable == True and flask4_valid == True) and (flask4_react == "Life" or flask4_always):
        key_press(e.KEY_4, flask4_duration)
      elif (flask5_enable == True and flask5_valid == True) and (flask5_react == "Life" or flask5_always):
        key_press(e.KEY_5, flask5_duration)
      else:
        print("Life tick not available")

    if mana_need == True:
      if (flask1_valid == True and flask1_enable == True) and (flask1_react == "Mana" or flask1_always):
        key_press(e.KEY_1, flask1_duration)
      elif (flask2_valid == True and flask2_enable == True) and (flask2_react == "Mana" or flask2_always):
        key_press(e.KEY_2, flask2_duration)
      elif (flask3_valid == True and flask3_enable == True) and (flask3_react == "Mana" or flask3_always):
        key_press(e.KEY_3, flask3_duration)
      elif (flask4_valid == True and flask4_enable == True) and (flask4_react == "Mana" or flask4_always):
        key_press(e.KEY_4, flask4_duration)
      elif (flask5_valid == True and flask5_enable == True) and (flask5_react == "Mana" or flask5_always):
        key_press(e.KEY_5, flask5_duration)
      else:
        print("Mana tick not available")

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
