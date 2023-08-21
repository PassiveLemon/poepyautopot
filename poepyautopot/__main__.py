from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from evdev import UInput, ecodes as e
from PIL import ImageGrab
import shutil
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

flask1 = Flask("flask1", 1, config.flask1_enable, config.flask1_offset_x, config.flask1_type, config.flask1_pixel, config.flask1_empty, config.flask1_duration, config.flask1_react, config.flask1_always, True, False)
flask2 = Flask("flask2", 2, config.flask2_enable, config.flask2_offset_x, config.flask2_type, config.flask2_pixel, config.flask2_empty, config.flask2_duration, config.flask2_react, config.flask2_always, True, False)
flask3 = Flask("flask3", 3, config.flask3_enable, config.flask3_offset_x, config.flask3_type, config.flask3_pixel, config.flask3_empty, config.flask3_duration, config.flask3_react, config.flask3_always, True, False)
flask4 = Flask("flask4", 4, config.flask4_enable, config.flask4_offset_x, config.flask4_type, config.flask4_pixel, config.flask4_empty, config.flask4_duration, config.flask4_react, config.flask4_always, True, False)
flask5 = Flask("flask5", 5, config.flask5_enable, config.flask5_offset_x, config.flask5_type, config.flask5_pixel, config.flask5_empty, config.flask5_duration, config.flask5_react, config.flask5_always, True, False)

escape = Menu('Escape ', config.escape_pixel1, config.escape_pixel2, config.escape_pixel3, config.escape_color1, config.escape_color2, config.escape_color3, False)
loading = Menu('Loading', config.loading_pixel1, config.loading_pixel2, config.loading_pixel3, config.loading_color1, config.loading_color2, config.loading_color3, False)
death = Menu('Death  ', config.death_pixel1, config.death_pixel2, config.death_pixel3, config.death_color1, config.death_color2, config.death_color3, False)

colorama_init()

def screen_capture():
  global screen_load
  screen_capture = ImageGrab.grab(bbox=(config.screen_offset_x, config.screen_offset_y, 1920 + config.screen_offset_x, 1080 + config.screen_offset_y))
  screen_load = screen_capture.load()

  if config.debug_enable == True and config.debug_image_save_enable == True:
    screen_capture.save(debug_image_save_location, "/screen.png")

# Main
def main():
  i = 0
  # Initially create the lists for the print parser
  meter_list = [life, mana]
  flasks_list = [flask1, flask2, flask3, flask4, flask5]
  menu_list = [escape, loading, death]

  test_time = time.time()
  while True:
    i += 1
    print_list = []
    print_length = 0
    life_handoff = False
    mana_handoff = False

    time_start = time.time()
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
      if flask1.enable == True:
        checks.flask_check(flask1, screen_load)
        flask1_press = threading.Thread(target=functions.key_press, args=[e.KEY_1, flask1.duration, flask1])
        if life.need == True:
          if flask1.valid == True and (flask1.react == "Life" or flask1.always == True):
            if flask1.lock == False:
              flask1.lock = True
              flask1_press.start()
            life_handoff = False
          else:
            life_handoff = True
        if mana.need == True:
          if flask1.valid == True and (flask1.react == "Mana" or flask1.always == True):
            if flask1.lock == False:
              flask1.lock = True
              flask1_press.start()
            mana_handoff = False
          else:
            mana_handoff = True

      if flask2.enable == True:
        checks.flask_check(flask2, screen_load)
        flask2_press = threading.Thread(target=functions.key_press, args=[e.KEY_2, flask2.duration, flask2])
        if life.need == True:
          if flask2.valid == True and ((flask2.react == "Life" and life_handoff == True) or flask2.always == True):
            if flask2.lock == False:
              flask2.lock = True
              flask2_press.start()
            life_handoff = False
          else:
            life_handoff = True
        if mana.need == True:
          if flask2.valid == True and ((flask2.react == "Mana" and mana_handoff == True) or flask2.always == True):
            if flask2.lock == False:
              flask2.lock = True
              flask2_press.start()
            mana_handoff = False
          else:
            mana_handoff = True

      if flask3.enable == True:
        checks.flask_check(flask3, screen_load)
        flask3_press = threading.Thread(target=functions.key_press, args=[e.KEY_3, flask3.duration, flask3])
        if life.need == True:
          if flask3.valid == True and ((flask3.react == "Life" and life_handoff == True) or flask3.always == True):
            if flask3.lock == False:
              flask3.lock = True
              flask3_press.start()
            life_handoff = False
          else:
            life_handoff = True
        if mana.need == True:
          if flask3.valid == True and ((flask3.react == "Mana" and mana_handoff == True) or flask3.always == True):
            if flask3.lock == False:
              flask3.lock = True
              flask3_press.start()
            mana_handoff = False
          else:
            mana_handoff = True

      if flask4.enable == True:
        checks.flask_check(flask4, screen_load)
        flask4_press = threading.Thread(target=functions.key_press, args=[e.KEY_4, flask4.duration, flask4])
        if life.need == True:
          if flask4.valid == True and ((flask4.react == "Life" and life_handoff == True) or flask4.always == True):
            if flask4.lock == False:
              flask4.lock = True
              flask4_press.start()
            life_handoff = False
          else:
            life_handoff = True
        if mana.need == True:
          if flask4.valid == True and ((flask4.react == "Mana" and mana_handoff == True) or flask4.always == True):
            if flask4.lock == False:
              flask4.lock = True
              flask4_press.start()
            mana_handoff = False
          else:
            mana_handoff = True

      if flask5.enable == True:
        checks.flask_check(flask5, screen_load)
        flask5_press = threading.Thread(target=functions.key_press, args=[e.KEY_5, flask5.duration, flask5])
        if life.need == True:
          if flask5.valid == True and ((flask5.react == "Life" and life_handoff == True) or flask5.always == True):
            if flask5.lock == False:
              flask5.lock = True
              flask5_press.start()
            life_handoff = False
        if mana.need == True:
          if flask5.valid == True and ((flask5.react == "Mana" and mana_handoff == True) or flask5.always == True):
            if flask5.lock == False:
              flask5.lock = True
              flask5_press.start()
            mana_handoff = False

      # Assign certain properties of the objects to a color and parse them
      for meter in meter_list:
        if meter.enable == True:
          if meter.need == True:
            print_list.append(f"{Fore.RED}{meter}{Style.RESET_ALL}")
          else:
            print_list.append(f"{Fore.GREEN}{meter}{Style.RESET_ALL}")
          print_length += 4
      print_list.append("|")
      for flask in flasks_list:
        if flask.enable == True:
          if flask.valid == True and flask.lock == False:
            print_list.append(f"{Fore.GREEN}{flask}{Style.RESET_ALL}")
          elif flask.valid == True and flask.lock == True:
            print_list.append(f"{Fore.YELLOW}{flask}{Style.RESET_ALL}")
          elif flask.valid == False:
            print_list.append(f"{Fore.RED}{flask}{Style.RESET_ALL}")
          print_length += 6
    else:
      for menu in menu_list:
        if menu.inside == True:
          print_list.append(f"{Fore.GREEN}{menu}{Style.RESET_ALL}")
          print_length += 7

    # Attempt to align the loop count to the right. Doesn't properly work but it's good enough I guess
    terminal_width = shutil.get_terminal_size().columns
    print_list.append(f"{Fore.BLUE}{i}{Style.RESET_ALL}".rjust(terminal_width - print_length))

    for item in print_list:
      print(item, end=' ')
    # Print nothing to trick the for item loop into printing every single loop rather than for every key press. Not sure why that happens
    print('')

    # Calculate the current time taken vs what the user specified and wait the difference
    time_taken = round(time.time() - time_start, 3) * 1000
    if time_taken < config.main_rate:
      time.sleep((config.main_rate / 1000) - (time_taken / 1000))

    # Calculate loop rate
    if i == 60:
      final_time = round(i / round(time.time() - test_time, 3), 1)
      print(f"About {final_time} Hz")

if __name__ == "__main__":
  if config.main_enable == True:
    main()
