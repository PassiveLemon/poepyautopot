import random
import time
import ast
import asyncio
import yaml
import pyautogui
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

  global main_enable, life_enable, mana_enable
  main = yaml_config["main"]
  main_enable = main["enable"] #g
  life_enable = main["life"] #g
  mana_enable = main["mana"] #g

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
def life_check():
  life_panel = pyautogui.screenshot(region=(100 + screen_offset_x, 875 + screen_offset_y, 2, 200))

  r, g, b = life_panel.getpixel((1, 130))

  if 101 <= r <= 111 and 9 <= g <= 19 and 15 <= b <= 25:
    life.need = False
  else:
    life.need = True

def mana_check():
  mana_panel = pyautogui.screenshot(region=(1800 + screen_offset_x, 875 + screen_offset_y, 2, 200))

  r, g, b = mana_panel.getpixel((2, 50))

  if 8 <= r <= 18 and 71 <= g <= 81 and 150 <= b <= 160:
    mana.need = False
  else:
    mana.need = True

def flask_check(flask_pixel, flask_x_offset, flask_empty, flask):
  flasks_panel = pyautogui.screenshot(region=(310 + screen_offset_x, 990 + screen_offset_y, 223, 80))

  x_raw, y_raw = ast.literal_eval(flask_pixel)
  x_off = (int(x_raw) + int(flask_x_offset))

  r, g, b = flasks_panel.getpixel((x_off, y_raw))

  r_empty, g_empty, b_empty, = ast.literal_eval(flask_empty)
  r_empty_min, r_empty_max = r_empty - 5, r_empty + 5
  g_empty_min, g_empty_max = g_empty - 5, g_empty + 5
  b_empty_min, b_empty_max = b_empty - 5, b_empty + 5

  if r_empty_min <= r <= r_empty_max and g_empty_min <= g <= g_empty_max and b_empty_min <= b <= b_empty_max:
    flask.valid = False
  else:
    flask.valid = True

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

  # Print pressed key and its length
  key_map = {
    e.KEY_1: 1,
    e.KEY_2: 2,
    e.KEY_3: 3,
    e.KEY_4: 4,
    e.KEY_5: 5,
  }
  print(f"{key_map[num]} ({random_key_press_sleep} ms)")\


# Debug
def image_save():
  life_panel = pyautogui.screenshot(region=(100 + screen_offset_x, 875 + screen_offset_y, 2, 200))
  mana_panel = pyautogui.screenshot(region=(1800 + screen_offset_x, 875 + screen_offset_y, 2, 200))
  flasks_panel = pyautogui.screenshot(region=(310 + screen_offset_x, 990 + screen_offset_y, 223, 80))

  life_panel.save(image_save_location + "life.png")
  mana_panel.save(image_save_location + "mana_panel.png")
  flasks_panel.save(image_save_location + "flasks_panel.png")


# Main
def main():
  config_init()
  flask_body_init()
  life_mana_body_init()
  key_press_init()

  while True:
    if life_enable is True:
      life_check()
    if flask1_enable is True:
      flask_check(flask1_pixel, flask1_x_offset, flask1_empty, flask1)
    if flask2_enable is True:
      flask_check(flask2_pixel, flask2_x_offset, flask2_empty, flask2)
    if flask3_enable is True:
      flask_check(flask3_pixel, flask3_x_offset, flask3_empty, flask3)
    if flask4_enable is True:
      flask_check(flask4_pixel, flask4_x_offset, flask4_empty, flask4)
    if flask5_enable is True:
      flask_check(flask5_pixel, flask5_x_offset, flask5_empty, flask5)

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
