from evdev import UInput, ecodes as e
from PIL import ImageGrab
import threading
import time

from config import config
from checks import checks
from functions import functions

# Objects
class Meter(object):
  def __init__(self, name, enable, pixel, empty, need):
    self.name = name
    self.enable = enable
    self.pixel = pixel
    self.empty = empty
    self.need = need
  def __str__(self):
    return self.name

class Flask(object):
  def __init__(self, name, number, enable, offset_x, type, pixel, empty, duration, react, always, valid, lock):
    self.name = name
    self.number = number
    self.enable = enable
    self.offset_x = offset_x
    self.type = type
    self.pixel = pixel
    self.empty = empty
    self.duration = duration
    self.react = react
    self.always = always
    self.valid = valid
    self.lock = lock
  def __str__(self):
    return self.name

class Menu(object):
  def __init__(self, name, pixel1, pixel2, pixel3, color1, color2, color3, inside):
    self.name = name
    self.pixel1 = pixel1
    self.pixel2 = pixel2
    self.pixel3 = pixel3
    self.color1 = color1
    self.color2 = color2
    self.color3 = color3
    self.inside = inside
  def __str__(self):
    return self.name

# Init
life = Meter("Life", config.main_life_enable, config.life_pixel, config.life_empty, False)
mana = Meter("Mana", config.main_mana_enable, config.mana_pixel, config.mana_empty, False)

flask1 = Flask("flask1", e.KEY_1, config.flask1_enable, config.flask1_offset_x, config.flask1_type, config.flask1_pixel, config.flask1_empty, config.flask1_duration, config.flask1_react, config.flask1_always, True, False)
flask2 = Flask("flask2", e.KEY_2, config.flask2_enable, config.flask2_offset_x, config.flask2_type, config.flask2_pixel, config.flask2_empty, config.flask2_duration, config.flask2_react, config.flask2_always, True, False)
flask3 = Flask("flask3", e.KEY_3, config.flask3_enable, config.flask3_offset_x, config.flask3_type, config.flask3_pixel, config.flask3_empty, config.flask3_duration, config.flask3_react, config.flask3_always, True, False)
flask4 = Flask("flask4", e.KEY_4, config.flask4_enable, config.flask4_offset_x, config.flask4_type, config.flask4_pixel, config.flask4_empty, config.flask4_duration, config.flask4_react, config.flask4_always, True, False)
flask5 = Flask("flask5", e.KEY_5, config.flask5_enable, config.flask5_offset_x, config.flask5_type, config.flask5_pixel, config.flask5_empty, config.flask5_duration, config.flask5_react, config.flask5_always, True, False)

escape = Menu('Escape ', config.escape_pixel1, config.escape_pixel2, config.escape_pixel3, config.escape_color1, config.escape_color2, config.escape_color3, False)
loading = Menu('Loading', config.loading_pixel1, config.loading_pixel2, config.loading_pixel3, config.loading_color1, config.loading_color2, config.loading_color3, False)
death = Menu('Death  ', config.death_pixel1, config.death_pixel2, config.death_pixel3, config.death_color1, config.death_color2, config.death_color3, False)

meter_list = [life, mana]
flasks_list = [flask1, flask2, flask3, flask4, flask5]
menu_list = [escape, loading, death]

def screen_capture():
  global screen_load
  screen_capture = ImageGrab.grab(bbox=(config.screen_offset_x, config.screen_offset_y, 1920 + config.screen_offset_x, 1080 + config.screen_offset_y))
  screen_load = screen_capture.load()

  if config.debug_enable == True and config.debug_image_save_enable == True:
    screen_capture.save(debug_image_save_location, "/screen.png")

# Main
def main():
  i = 0

  absolute_start = time.time()
  while True:
    i += 1
    relative_start = time.time()
    life_handoff = True
    mana_handoff = True

    screen_capture()

    if config.main_menu_enable == True:
      checks.menu_check(escape, screen_load)
      checks.menu_check(loading, screen_load)
      checks.menu_check(death, screen_load)

    # Check if the user is inside one of the menu screens. If so, skip the processing
    if escape.inside == False and loading.inside == False and death.inside == False:
      if config.main_life_enable == True:
        checks.meter_check(life, screen_load)
      if config.main_mana_enable == True:
        checks.meter_check(mana, screen_load)
      for flask in flasks_list:
        if flask.enable == True:
          checks.flask_check(flask, screen_load)
          flask_press = threading.Thread(target=functions.key_press, args=[flask])
          if life.need == True:
            if flask.valid == True and ((flask.react == "Life" and life_handoff == True) or flask.always == True):
              if flask.lock == False:
                flask.lock = True
                flask_press.start()
              life_handoff = False
            else:
              life_handoff = True
          if mana.need == True:
            if flask.valid == True and ((flask.react == "Mana" and mana_handoff == True) or flask.always == True):
              if flask.lock == False:
                flask.lock = True
                flask_press.start()
              mana_handoff = False
            else:
              mana_handoff = True
      functions.print_parser(i, meter_list, flasks_list, None)
    else:
      functions.print_parser(i, meter_list, None, menu_list)

    functions.loop_rate(i, config.main_rate, absolute_start, relative_start)

if __name__ == "__main__":
  main()
