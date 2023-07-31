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
  parser.add_argument("-f", "--file", required=True)
  config_file = parser.parse_args().file

  yaml_config = yaml.safe_load(open(config_file))

  global keyboard_event, screen_offset_x, screen_offset_y
  keyboard_event = yaml_config["keyboard_event"] #g

  screen_offset = yaml_config["screen_offset"]
  screen_offset_x = screen_offset["x"] #g
  screen_offset_y = screen_offset["y"] #g

  global key_press_shortest, key_press_longest, key_press_range, key_press_std_dev, key_press_target, key_press_test_enable, key_press_test_delay, key_press_test_count
  key_press = yaml_config["key_press"]
  key_press_shortest = key_press["shortest"] #g
  key_press_longest = key_press["longest"] #g
  key_press_range = key_press["range"] #g
  key_press_std_dev = key_press["std_dev"] #g
  key_press_target = key_press["target"] #g

  global flask1_enable, flask1_pixel, flask1_empty, flask1_duration, flask1_react, flask1_x_offset
  flask1 = yaml_config["flask1"]
  flask1_enable = flask1["enable"] #g
  flask1_type = flask1["type"]
  flask1_pixel = flask1_type["pixel"] #g
  flask1_empty = flask1_type["empty"] #g
  flask1_duration = flask1_type["duration"] #g
  flask1_react = flask1["react"] #g
  flask1_x_offset = flask1["x_offset"] #g

  global flask2_enable, flask2_pixel, flask2_empty, flask2_duration, flask2_react, flask2_x_offset
  flask2 = yaml_config["flask2"]
  flask2_enable = flask2["enable"] #g
  flask2_type = flask2["type"]
  flask2_pixel = flask2_type["pixel"] #g
  flask2_empty = flask2_type["empty"] #g
  flask2_duration = flask2_type["duration"] #g
  flask2_react = flask1["react"] #g
  flask2_x_offset = flask2["x_offset"] #g

  global flask3_enable, flask3_pixel, flask3_empty, flask3_duration, flask3_react, flask3_x_offset
  flask3 = yaml_config["flask3"]
  flask3_enable = flask3["enable"] #g
  flask3_type = flask3["type"]
  flask3_pixel = flask3_type["pixel"] #g
  flask3_empty = flask3_type["empty"] #g
  flask3_duration = flask3_type["duration"] #g
  flask3_react = flask1["react"] #g
  flask3_x_offset = flask3["x_offset"] #g

  global flask4_enable, flask4_pixel, flask4_empty, flask4_duration, flask4_react, flask4_x_offset
  flask4 = yaml_config["flask4"]
  flask4_enable = flask4["enable"] #g
  flask4_type = flask4["type"]
  flask4_pixel = flask4_type["pixel"] #g
  flask4_empty = flask4_type["empty"] #g
  flask4_duration = flask4_type["duration"] #g
  flask4_react = flask1["react"] #g
  flask4_x_offset = flask4["x_offset"] #g

  global flask5_enable, flask5_pixel, flask5_empty, flask5_duration, flask5_react, flask5_x_offset
  flask5 = yaml_config["flask5"]
  flask5_enable = flask5["enable"] #g
  flask5_type = flask5["type"]
  flask5_pixel = flask5_type["pixel"] #g
  flask5_empty = flask5_type["empty"] #g
  flask5_duration = flask5_type["duration"] #g
  flask5_react = flask1["react"] #g
  flask5_x_offset = flask5["x_offset"] #g

  global main_enable, life_enable, mana_enable, flask_enable
  main = yaml_config["main"]
  main_enable = main["enable"] #g
  life_enable = main["life"] #g
  mana_enable = main["mana"] #g
  flask_enable = main["flask"] #g

  global debug_enable, image_save_enable, image_save_location
  debug = yaml_config["debug"]
  debug_enable = debug["enable"] #g
  image_save = debug["image_save"]
  image_save_enable = image_save["enable"] #g
  image_save_location = image_save["location"] #g

  global test_enable, key_press_test_enable, key_press_test_delay, key_press_test_count
  test = yaml_config["test"]
  test_enable = test["enable"] #g
  key_press_test = test["key_press_test"]
  key_press_test_enable = key_press_test["enable"] #g
  key_press_test_delay = key_press_test["delay"] #g
  key_press_test_count = key_press_test["count"] #g

config_init()

def key_press_init():
  global key_press_shortest_low, key_press_shortest_high, key_press_longest_low, key_press_longest_high
  key_press_shortest_low = key_press_shortest - key_press_range
  key_press_shortest_high = key_press_shortest + key_press_range
  key_press_longest_low = key_press_longest - key_press_range
  key_press_longest_high = key_press_longest + key_press_range


# Utility
async def key_press(num, wait):
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

  if debug_enable is True and image_save_enable is True:
    screen_capture.save("./screen.png")

def life_check(life_need):
  r, g, b = screen_load[101, 1005]
  if 101 <= r <= 111 and 9 <= g <= 19 and 15 <= b <= 25:
    life_need.value = False
  else:
    life_need.value = True

def mana_check(mana_need):
  r, g, b = screen_load[1801, 1005]
  if 8 <= r <= 18 and 71 <= g <= 81 and 150 <= b <= 160:
    mana_need.value = False
  else:
    mana_need.value = True

def flask_check(flask1_valid, flask2_valid, flask3_valid, flask4_valid, flask5_valid):
  if flask1_enable is True:
    x1_raw, y1_raw = ast.literal_eval(flask1_pixel)
    x1_off = (int(x1_raw) + int(flask1_x_offset))
    r1, g1, b1 = screen_load[x1_off, y1_raw]
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask1_empty)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      flask1_valid.value = False
    else:
      flask1_valid.value = True

  if flask2_enable is True:
    x2_raw, y2_raw = ast.literal_eval(flask2_pixel)
    x2_off = (int(x2_raw) + int(flask2_x_offset))
    r2, g2, b2 = screen_load[x2_off, y2_raw]
    r2_empty, g2_empty, b2_empty, = ast.literal_eval(flask2_empty)
    r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
    g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
    b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
    if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
      flask2_valid.value = False
    else:
      flask2_valid.value = True

  if flask3_enable is True:
    x3_raw, y3_raw = ast.literal_eval(flask3_pixel)
    x3_off = (int(x3_raw) + int(flask3_x_offset))
    r3, g3, b3 = screen_load[x3_off, y3_raw]
    r3_empty, g3_empty, b3_empty, = ast.literal_eval(flask3_empty)
    r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
    g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
    b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
    if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
      flask3_valid.value = False
    else:
      flask3_valid.value = True
  
  if flask4_enable is True:
    x4_raw, y4_raw = ast.literal_eval(flask4_pixel)
    x4_off = (int(x4_raw) + int(flask4_x_offset))
    r4, g4, b4 = screen_load[x4_off, y4_raw]
    r4_empty, g4_empty, b4_empty, = ast.literal_eval(flask4_empty)
    r4_empty_min, r4_empty_max = r4_empty - 5, r4_empty + 5
    g4_empty_min, g4_empty_max = g4_empty - 5, g4_empty + 5
    b4_empty_min, b4_empty_max = b4_empty - 5, b4_empty + 5
    if r4_empty_min <= r4 <= r4_empty_max and g4_empty_min <= g4 <= g4_empty_max and b4_empty_min <= b4 <= b4_empty_max:
      flask4_valid.value = False
    else:
      flask4_valid.value = True

  if flask5_enable is True:
    x5_raw, y5_raw = ast.literal_eval(flask5_pixel)
    x5_off = (int(x5_raw) + int(flask5_x_offset))
    r5, g5, b5 = screen_load[x5_off, y5_raw]
    r5_empty, g5_empty, b5_empty, = ast.literal_eval(flask5_empty)
    r5_empty_min, r5_empty_max = r5_empty - 5, r5_empty + 5
    g5_empty_min, g5_empty_max = g5_empty - 5, g5_empty + 5
    b5_empty_min, b5_empty_max = b5_empty - 5, b5_empty + 5
    if r5_empty_min <= r5 <= r5_empty_max and g5_empty_min <= g5 <= g5_empty_max and b5_empty_min <= b5 <= b5_empty_max:
      flask5_valid.value = False
    else:
      flask5_valid.value = True

# Main
async def main():
  key_press_init()

  manager = multiprocessing.Manager()
  life_need = manager.Value('b', False)
  mana_need = manager.Value('b', False)
  flask1_valid = manager.Value('b', True)
  flask2_valid = manager.Value('b', True)
  flask3_valid = manager.Value('b', True)
  flask4_valid = manager.Value('b', True)
  flask5_valid = manager.Value('b', True)
  
  i = 0
  while True:
    screen_capture()

    check_processes = []
    if life_enable is True:
      life_check_process = multiprocessing.Process(target=life_check, args=[life_need])
      check_processes.append(life_check_process)
    if mana_enable is True:
      mana_check_process = multiprocessing.Process(target=mana_check, args=[mana_need])
      check_processes.append(mana_check_process)
    if flask_enable is True:
      flask_check_process = multiprocessing.Process(target=flask_check, args=[flask1_valid, flask2_valid, flask3_valid, flask4_valid, flask5_valid])
      check_processes.append(flask_check_process)

    for process in check_processes:
      process.start()
    for process in check_processes:
      process.join()

    print(f"{i} life-{life_need.value} mana-{mana_need.value} 1-{flask1_valid.value} 2-{flask2_valid.value} 3-{flask3_valid.value} 4-{flask4_valid.value} 5-{flask5_valid.value}")

    key_press_threads = []
    if life_need.value is True:
      if flask1_valid.value is True and flask1_enable is True and flask1_react == "Life":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_1, flask1_duration)))
      elif flask2_valid.value is True and flask2_enable is True and flask2_react == "Life":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_2, flask2_duration)))
      elif flask3_valid.value is True and flask3_enable is True and flask3_react == "Life":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_3, flask3_duration)))
      elif flask4_valid.value is True and flask4_enable is True and flask4_react == "Life":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_4, flask4_duration)))
      elif flask5_valid.value is True and flask5_enable is True and flask5_react == "Life":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_5, flask5_duration)))
      else:
        print("Life tick not available")

    if mana_need.value is True:
      if flask1_valid.value is True and flask1_enable is True and flask1_react == "Mana":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_1, flask1_duration)))
      elif flask2_valid.value is True and flask2_enable is True and flask2_react == "Mana":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_2, flask2_duration)))
      elif flask3_valid.value is True and flask3_enable is True and flask3_react == "Mana":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_3, flask3_duration)))
      elif flask4_valid.value is True and flask4_enable is True and flask4_react == "Mana":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_4, flask4_duration)))
      elif flask5_valid.value is True and flask5_enable is True and flask5_react == "Mana":
        key_press_threads.append(asyncio.ensure_future(key_press(e.KEY_5, flask5_duration)))
      else:
        print("Mana tick not available")
    
    await asyncio.gather(*key_press_threads)

    i += 1

if main_enable is True:
  asyncio.run(main())
  #screen_capture()

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
  if key_press_test_enable is True:
    key_press_test()

if test_enable is True:
  test()
