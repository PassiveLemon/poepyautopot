import numpy as np
import pyautogui as pag
import keyboard as kb
import random as random
import time as time
from evdev import UInput, ecodes as e

# Hardware
keyboard_event = "/dev/input/event0"
# Account for the possibility of screen above or left of the game. This assumes a default 1080p for every screen.
screen_offset_x = 1920
screen_offset_y = 0

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

def init_test(saveloc):
  flask_init()
  flasks_panel.save(saveloc + "flasks_panel.jpg")

  flask1.img.save(saveloc + "flask1.jpg")
  flask2.img.save(saveloc + "flask2.jpg")
  flask3.img.save(saveloc + "flask3.jpg")
  flask4.img.save(saveloc + "flask4.jpg")
  flask5.img.save(saveloc + "flask5.jpg")

  life_init()
  life_panel.save(saveloc + "life.jpg")

  mana_init()
  mana_panel.save(saveloc + "mana_panel.jpg")

#init_test("/home/lemon/Documents/GitHub/poepyautopot/images/")

def keyboard_press():
  ui = UInput.from_device(keyboard_event)
  ui.write(e.EV_KEY, e.KEY_1, 1)
  ui.syn()

  # Apply some variation to keypress length
  random_sleep = random.randint(44, 181)
  time.sleep(random_sleep / 1000.0)

  ui.write(e.EV_KEY, e.KEY_1, 0)
  ui.syn()
  ui.close()




#runnerstate = False

#kb.add_hotkey('page up, page down', lambda: runnerstate = True)

#while kb.is_pressed('esc') == false:
#  width, height = pic.size
#
#  for x in range(0, width, 10):
#    for y in range(0, height, 10):
#      r, g, b = pic.getpixel((x,y))

#      if r == x and g == x and b == x:
