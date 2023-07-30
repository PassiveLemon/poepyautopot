import random
import time
import ast
import asyncio
import yaml
import pyautogui
import mss
import mss.tools
from PIL import ImageGrab
from evdev import UInput, ecodes as e


# Init
def config_init():
  yaml_config = yaml.safe_load(open("./config.yaml"))

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

  global flask1_enable, flask1_pixel, flask1_empty, flask1_duration, flask1_x_offset
  flask1 = yaml_config["flask1"]
  flask1_enable = flask1["enable"] #g
  flask1_type = flask1["type"]
  flask1_pixel = flask1_type["pixel"] #g
  flask1_empty = flask1_type["empty"] #g
  flask1_duration = flask1_type["duration"] #g
  flask1_x_offset = flask1["x_offset"] #g

  global flask2_enable, flask2_pixel, flask2_empty, flask2_duration, flask2_x_offset
  flask2 = yaml_config["flask2"]
  flask2_enable = flask2["enable"] #g
  flask2_type = flask2["type"]
  flask2_pixel = flask2_type["pixel"] #g
  flask2_empty = flask2_type["empty"] #g
  flask2_duration = flask2_type["duration"] #g
  flask2_x_offset = flask2["x_offset"] #g

  global flask3_enable, flask3_pixel, flask3_empty, flask3_duration, flask3_x_offset
  flask3 = yaml_config["flask3"]
  flask3_enable = flask3["enable"] #g
  flask3_type = flask3["type"]
  flask3_pixel = flask3_type["pixel"] #g
  flask3_empty = flask3_type["empty"] #g
  flask3_duration = flask3_type["duration"] #g
  flask3_x_offset = flask3["x_offset"] #g

  global flask4_enable, flask4_pixel, flask4_empty, flask4_duration, flask4_x_offset
  flask4 = yaml_config["flask4"]
  flask4_enable = flask4["enable"] #g
  flask4_type = flask4["type"]
  flask4_pixel = flask4_type["pixel"] #g
  flask4_empty = flask4_type["empty"] #g
  flask4_duration = flask4_type["duration"] #g
  flask4_x_offset = flask4["x_offset"] #g

  global flask5_enable, flask5_pixel, flask5_empty, flask5_duration, flask5_x_offset
  flask5 = yaml_config["flask5"]
  flask5_enable = flask5["enable"] #g
  flask5_type = flask5["type"]
  flask5_pixel = flask5_type["pixel"] #g
  flask5_empty = flask5_type["empty"] #g
  flask5_duration = flask5_type["duration"] #g
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

  global key_press_test_enable, key_press_test_delay, key_press_test_count
  test = yaml_config["test"]
  test_enable = test["enable"] #g
  key_press_test = test["key_press_test"]
  key_press_test_enable = key_press_test["enable"] #g
  key_press_test_delay = key_press_test["delay"] #g
  key_press_test_count = key_press_test["count"] #g

config_init()

def life_mana_body_init():
  class life_mana_body:
    def __init__(self, enable, need):
      self.enable = enable
      self.need = need

    def __str__(self):
      return f"Object(enable={self.enable}, need={self.need})"

  global life, mana
  life = life_mana_body(enable=life_enable, need=False)
  mana = life_mana_body(enable=mana_enable, need=False)

def flask_body_init():
  class flask_body:
    def __init__(self, enable, valid, pixel, duration, img):
      self.enable = enable
      self.valid = valid
      self.pixel = pixel
      self.duration = duration
      self.img = img

    def __str__(self):
      return f"Object(enable={self.enable}, valid={self.valid}, pixel={self.pixel}, duration={self.duration}, img={self.img})"

  global flask1, flask2, flask3, flask4, flask5
  flask1 = flask_body(enable=flask1_enable, valid=True, pixel=flask1_pixel, duration=flask1_duration, img=None)
  flask2 = flask_body(enable=flask2_enable, valid=True, pixel=flask2_pixel, duration=flask2_duration, img=None)
  flask3 = flask_body(enable=False, valid=True, pixel=None, duration=None, img=None)
  flask4 = flask_body(enable=False, valid=True, pixel=None, duration=None, img=None)
  flask5 = flask_body(enable=False, valid=True, pixel=None, duration=None, img=None)

def key_press_init():
  global key_press_shortest_low, key_press_shortest_high, key_press_longest_low, key_press_longest_high
  key_press_shortest_low = key_press_shortest - key_press_range
  key_press_shortest_high = key_press_shortest + key_press_range
  key_press_longest_low = key_press_longest - key_press_range
  key_press_longest_high = key_press_longest + key_press_range


# Utility
#def image_capture():
#  global life_panel, mana_panel, flasks_panel
#  life_panel = pyautogui.screenshot(region=(101 + screen_offset_x, 875 + screen_offset_y, 1, 200))
#  mana_panel = pyautogui.screenshot(region=(1800 + screen_offset_x, 875 + screen_offset_y, 1, 200))
#  flasks_panel = pyautogui.screenshot(region=(310 + screen_offset_x, 990 + screen_offset_y, 223, 80))

def image_capture():
  global life_panel, mana_panel, flasks_panel
  life_panel = ImageGrab.grab(bbox=(101 + screen_offset_x, 875 + screen_offset_y, 102 + screen_offset_x, 1075 + screen_offset_y))
  mana_panel = ImageGrab.grab(bbox=(1801 + screen_offset_x, 875 + screen_offset_y, 1802 + screen_offset_x, 1075 + screen_offset_y))
  flasks_panel = ImageGrab.grab(bbox=(310 + screen_offset_x, 990 + screen_offset_y, 533 + screen_offset_x, 1070 + screen_offset_y))

def life_check():
  r, g, b = life_panel.getpixel((0, 130))
  if 101 <= r <= 111 and 9 <= g <= 19 and 15 <= b <= 25:
    life.need = False
  else:
    life.need = True

def mana_check():
  r, g, b = mana_panel.getpixel((0, 130))
  if 8 <= r <= 18 and 71 <= g <= 81 and 150 <= b <= 160:
    mana.need = False
  else:
    mana.need = True

def flask_check():
  if flask1_enable is True:
    x1_raw, y1_raw = ast.literal_eval(flask1_pixel)
    x1_off = (int(x1_raw) + int(flask1_x_offset))
    r1, g1, b1 = flasks_panel.getpixel((x1_off, y1_raw))
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask1_empty)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      flask1.valid = False
    else:
      flask1.valid = True

  if flask2_enable is True:
    x2_raw, y2_raw = ast.literal_eval(flask2_pixel)
    x2_off = (int(x2_raw) + int(flask2_x_offset))
    r2, g2, b2 = flasks_panel.getpixel((x2_off, y2_raw))
    r2_empty, g2_empty, b2_empty, = ast.literal_eval(flask2_empty)
    r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
    g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
    b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
    if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
      flask2.valid = False
    else:
      flask2.valid = True

  if flask3_enable is True:
    x3_raw, y3_raw = ast.literal_eval(flask3_pixel)
    x3_off = (int(x3_raw) + int(flask3_x_offset))
    r3, g3, b3 = flasks_panel.getpixel((x3_off, y3_raw))
    r3_empty, g3_empty, b3_empty, = ast.literal_eval(flask3_empty)
    r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
    g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
    b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
    if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
      flask3.valid = False
    else:
      flask3.valid = True
  
  if flask4_enable is True:
    x4_raw, y4_raw = ast.literal_eval(flask4_pixel)
    x4_off = (int(x4_raw) + int(flask4_x_offset))
    r4, g4, b4 = flasks_panel.getpixel((x4_off, y4_raw))
    r4_empty, g4_empty, b4_empty, = ast.literal_eval(flask4_empty)
    r4_empty_min, r4_empty_max = r4_empty - 5, r4_empty + 5
    g4_empty_min, g4_empty_max = g4_empty - 5, g4_empty + 5
    b4_empty_min, b4_empty_max = b4_empty - 5, b4_empty + 5
    if r4_empty_min <= r4 <= r4_empty_max and g4_empty_min <= g4 <= g4_empty_max and b4_empty_min <= b4 <= b4_empty_max:
      flask4.valid = False
    else:
      flask4.valid = True

  if flask5_enable is True:
    x5_raw, y5_raw = ast.literal_eval(flask5_pixel)
    x5_off = (int(x5_raw) + int(flask5_x_offset))
    r5, g5, b5 = flasks_panel.getpixel((x5_off, y5_raw))
    r5_empty, g5_empty, b5_empty, = ast.literal_eval(flask5_empty)
    r5_empty_min, r5_empty_max = r5_empty - 5, r5_empty + 5
    g5_empty_min, g5_empty_max = g5_empty - 5, g5_empty + 5
    b5_empty_min, b5_empty_max = b5_empty - 5, b5_empty + 5
    if r5_empty_min <= r5 <= r5_empty_max and g5_empty_min <= g5 <= g5_empty_max and b5_empty_min <= b5 <= b5_empty_max:
      flask5.valid = False
    else:
      flask5.valid = True

def key_press(num):
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
  print(f"{num} ({random_key_press_sleep} ms)")\


# Debug
def image_save():
  image_capture()
  life_panel.save(image_save_location + "life.png")
  mana_panel.save(image_save_location + "mana_panel.png")
  flasks_panel.save(image_save_location + "flasks_panel.png")

# Main
def main():
  config_init()
  flask_body_init()
  life_mana_body_init()
  key_press_init()

  i = 0
  while True:
    image_capture()
    if life_enable is True:
      life_check()
    if mana_enable is True:
      mana_check()
    if flask_enable is True:
      flask_check()
    if debug_enable is True:
      image_save()
    print(f"life-{life.need} mana-{mana.need} 1-{flask1.valid} 2-{flask2.valid} 3-{flask3.valid} 4-{flask4.valid} 5-{flask5.valid}")

    if life.need is True:
      if flask1.valid is True and flask1.enable is True:
        key_press(e.KEY_1)
      elif flask2.valid is True and flask2.enable is True:
        key_press(e.KEY_2)
      elif flask3.valid is True and flask3.enable is True:
        key_press(e.KEY_3)
      elif flask4.valid is True and flask4.enable is True:
        key_press(e.KEY_4)
      elif flask5.valid is True and flask5.enable is True:
        key_press(e.KEY_5)
      else:
        print("Life tick not available")
    i += 1

    print(i)

if main_enable is True:
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
  if key_press_test_enable is True:
    key_press_test()

if test_enable is True:
  test()
