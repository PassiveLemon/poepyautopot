import random
import time

import yaml
#import numpy as np
import pyautogui as pag
#import keyboard as kb
from evdev import UInput, ecodes as e


# Init

def config_init():
  yaml_config = yaml.safe_load(open("./config.yaml"))

  global keyboard_event, screen_offset_x, screen_offset_y
  keyboard_event = yaml_config["keyboard_event"]

  screen_offset = yaml_config["screen_offset"]
  screen_offset_x = screen_offset["x"]
  screen_offset_y = screen_offset["y"]

  global key_press_shortest, key_press_longest, key_press_range, key_press_std_dev, key_press_target, key_press_test_enable, key_press_test_delay, key_press_test_count
  key_press = yaml_config["key_press"]
  key_press_shortest = key_press["shortest"]
  key_press_longest = key_press["longest"]
  key_press_range = key_press["range"]
  key_press_std_dev = key_press["std_dev"]
  key_press_target = key_press["target"]
  key_press_test = key_press["test"]
  key_press_test_enable = key_press_test["enable"]
  key_press_test_delay = key_press_test["delay"]
  key_press_test_count = key_press_test["count"]

  global image_test_enable, image_test_save_location
  image_test = yaml_config["image_test"]
  image_test_enable = image_test["enable"]
  image_test_save_location = image_test["save_location"]

def flask_body_init():
  # Template for flasks
  global flask_body
  class flask_body:
    def __init__(self, enable, use, max, cur, img):
      self.enable = enable
      self.use = use
      self.max = max
      self.cur = cur
      self.img = img

    def __str__(self):
      return f"Object(use={self.use}, max={self.max}, cur={self.cur}, img={self.img})"

  # Defining default values. Will be moved to a config file
  global flask1, flask2, flask3, flask4, flask5
  flask1 = flask_body(enable=True, use=5, max=15, cur=max, img=None)
  flask2 = flask_body(enable=True, use=5, max=15, cur=max, img=None)
  flask3 = flask_body(enable=False, use=5, max=15, cur=max, img=None)
  flask4 = flask_body(enable=False, use=5, max=15, cur=max, img=None)
  flask5 = flask_body(enable=False, use=5, max=15, cur=max, img=None)

def life_init():
  global life_panel
  life_panel = pag.screenshot(region=(100 + screen_offset_x, 875 + screen_offset_y, 2, 200))

def mana_init():
  global mana_panel
  mana_panel = pag.screenshot(region=(1800 + screen_offset_x, 875 + screen_offset_y, 2, 200))

def key_press_init():
  global key_press_shortest_low, key_press_shortest_high, key_press_longest_low, key_press_longest_high
  key_press_shortest_low = key_press_shortest - key_press_range
  key_press_shortest_high = key_press_shortest + key_press_range
  key_press_longest_low = key_press_longest - key_press_range
  key_press_longest_high = key_press_longest + key_press_range


# Utility

def flask_capture():
  # Image with panel of flasks
  global flasks_panel
  flasks_panel = pag.screenshot(region=(310 + screen_offset_x, 990 + screen_offset_y, 223, 80))

  # Indivial flasks for each slot
  flask1.img = flasks_panel.crop((1, 0, 37, 80))
  flask2.img = flasks_panel.crop((47, 0, 83, 80))
  flask3.img = flasks_panel.crop((93, 0, 129, 80))
  flask4.img = flasks_panel.crop((139, 0, 175, 80))
  flask5.img = flasks_panel.crop((185, 0, 221, 80))

def key_press(num):
  # Bell curve to more closely group presses
  def bell_curve(min, max, sig, mu):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  # Press the key
  ui = UInput.from_device(keyboard_event)
  ui.write(e.EV_KEY, num, 1)
  ui.syn()

  # Slightly variate key press length range
  random_range_low = random.randint(key_press_shortest_low, key_press_shortest_high)
  random_range_high = random.randint(key_press_longest_low, key_press_longest_high)

  # Variate key press length with random lows and highs, std dev, and target.
  random_key_press_sleep = bell_curve(random_range_low, random_range_high, key_press_std_dev, key_press_target)
  time.sleep(random_key_press_sleep / 1000.0)

  # Release key
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
  print(f"{key_map[num]} ({random_key_press_sleep} ms)")


# Main

def main():
  config_init()
  flask_body_init()
  life_init()
  mana_init()
  key_press_init()

main()


# Tests

def image_test():
  flask_capture()
  flasks_panel.save(image_test_save_location + "flasks_panel.png")

  flask1.img.save(image_test_save_location + "flask1.png")
  flask2.img.save(image_test_save_location + "flask2.png")
  flask3.img.save(image_test_save_location + "flask3.png")
  flask4.img.save(image_test_save_location + "flask4.png")
  flask5.img.save(image_test_save_location + "flask5.png")

  life_panel.save(image_test_save_location + "life.png")

  mana_panel.save(image_test_save_location + "mana_panel.png")

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
  if image_test_enable is True:
    image_test()

  if key_press_test_enable is True:
    key_press_test()

test()


#runnerstate = False

#kb.add_hotkey('page up, page down', lambda: runnerstate = True)

#while kb.is_pressed('esc') == false:
#  width, height = pic.size
#
#  for x in range(0, width, 10):
#    for y in range(0, height, 10):
#      r, g, b = pic.getpixel((x,y))

#      if r == x and g == x and b == x:
