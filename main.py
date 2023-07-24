import numpy as np
import pyautogui as pag
import keyboard as kb
import random as random
import time as time
from evdev import UInput, ecodes as e

# Custom variables

# Hardware --------------------
keyboard_event = "/dev/input/event0"
# Account for the possibility of screen above or left of the game. This assumes a default 1080p for every screen.
screen_offset_x = 1920
screen_offset_y = 0

# Keypress data ---------------
# WRITE THESE AS SECONDS. They will get converted to milliseconds.

# My shortest was 54, fastest was 141.
# My std dev was 21.
# My q3 was 110 but you can also use your q1, mean, and any other number you want really.
shortest_key_press = 54
longest_key_press = 141
range_key_press = 5
std_dev_key_press = 21
third_value_key_press = 110

# Other -----------------------
image_save_location = "/home/lemon/Documents/GitHub/poepyautopot/images/"

# -----------------------------

def flask_init():
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

  # Defining default values
  global flask1, flask2, flask3, flask4, flask5
  flask1 = flask_body(enable=True, use=5, max=15, cur=max, img=None)
  flask2 = flask_body(enable=True, use=5, max=15, cur=max, img=None)
  flask3 = flask_body(enable=False, use=5, max=15, cur=max, img=None)
  flask4 = flask_body(enable=False, use=5, max=15, cur=max, img=None)
  flask5 = flask_body(enable=False, use=5, max=15, cur=max, img=None)

def flask_capture():
  # Image with panel of flasks
  global flasks_panel
  flasks_panel = pag.screenshot(region=(310 + screen_offset_x, 990, 223, 80))

  # Indivial flasks for each slot
  flask1.img = flasks_panel.crop((1, 0, 37, 80))
  flask2.img = flasks_panel.crop((47, 0, 83, 80))
  flask3.img = flasks_panel.crop((93, 0, 129, 80))
  flask4.img = flasks_panel.crop((139, 0, 175, 80))
  flask5.img = flasks_panel.crop((185, 0, 221, 80))

def life_init():
  global life_panel
  life_panel = pag.screenshot(region=(100 + screen_offset_x, 875, 2, 200))

def mana_init():
  global mana_panel
  mana_panel = pag.screenshot(region=(1800 + screen_offset_x, 875, 2, 200))

def image_init_test(saveloc):
  flask_capture()
  flasks_panel.save(saveloc + "flasks_panel.png")

  flask1.img.save(saveloc + "flask1.png")
  flask2.img.save(saveloc + "flask2.png")
  flask3.img.save(saveloc + "flask3.png")
  flask4.img.save(saveloc + "flask4.png")
  flask5.img.save(saveloc + "flask5.png")

  life_init()
  life_panel.save(saveloc + "life.png")

  mana_init()
  mana_panel.save(saveloc + "mana_panel.png")

def key_press_init(shortest, longest, press_range):
  global key_press_short_low, key_press_short_high, key_press_long_low, key_press_long_high
  key_press_short_low = shortest - press_range
  key_press_short_high = shortest + press_range
  key_press_long_low = longest - press_range
  key_press_long_high = longest + press_range

def key_press(num):
  # Bell curve to more closely group presses
  def bell_curve(min, max, mu, sig):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  # Press the key
  ui = UInput.from_device(keyboard_event)
  ui.write(e.EV_KEY, num, 1)
  ui.syn()

  # Slightly variate keypress length range
  random_range_low = random.randint(key_press_short_low, key_press_short_high)
  random_range_high = random.randint(key_press_long_low, key_press_long_high)

  # Variate keypress length with random lows and highs, q3, and std dev.
  random_key_press_sleep = bell_curve(random_range_low, random_range_high, third_value_key_press, std_dev_key_press)
  time.sleep(random_key_press_sleep / 1000.0)

  # Release key
  ui.write(e.EV_KEY, num, 0)
  ui.syn()
  ui.close()

def key_press_test(slp, i):
  # Give time to move cursor
  time.sleep(slp)
  key_map = {
    1: e.KEY_1,
    2: e.KEY_2,
    3: e.KEY_3,
    4: e.KEY_4,
    5: e.KEY_5,
  }
  while i > 0:
    random_key = random.randint(1, 5)
    key_press(key_map[random_key])
    i -= 1

# Defaults
flask_init()
key_press_init(shortest_key_press, longest_key_press, range_key_press)
# Tests
image_init_test(image_save_location)
key_press_test(3, 20)

#runnerstate = False

#kb.add_hotkey('page up, page down', lambda: runnerstate = True)

#while kb.is_pressed('esc') == false:
#  width, height = pic.size
#
#  for x in range(0, width, 10):
#    for y in range(0, height, 10):
#      r, g, b = pic.getpixel((x,y))

#      if r == x and g == x and b == x:
