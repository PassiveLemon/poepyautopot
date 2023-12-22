import os
import threading
import time

# This program requires access to keyboard devices (which requires root) so we exit before anything happens.
if os.geteuid() != 0:
  print("You need root priviledges to run this.")
  exit()

from evdev import ecodes as e

from .config import configs
from .objects import Meter, Flask, Menu
from .checks import menu_check, meter_check, flask_check
from .functions import screen_capture, key_press, print_parser, loop_rate

# Init
life = Meter("Life", configs.main_life_enable, configs.life_pixel, configs.life_empty, False)
mana = Meter("Mana", configs.main_mana_enable, configs.mana_pixel, configs.mana_empty, False)

flask1 = Flask("flask1", e.KEY_1, configs.flask1_enable, configs.flask1_offset_x, configs.flask1_type, configs.flask1_pixel, configs.flask1_empty, configs.flask1_duration, configs.flask1_react, configs.flask1_always, True, False)
flask2 = Flask("flask2", e.KEY_2, configs.flask2_enable, configs.flask2_offset_x, configs.flask2_type, configs.flask2_pixel, configs.flask2_empty, configs.flask2_duration, configs.flask2_react, configs.flask2_always, True, False)
flask3 = Flask("flask3", e.KEY_3, configs.flask3_enable, configs.flask3_offset_x, configs.flask3_type, configs.flask3_pixel, configs.flask3_empty, configs.flask3_duration, configs.flask3_react, configs.flask3_always, True, False)
flask4 = Flask("flask4", e.KEY_4, configs.flask4_enable, configs.flask4_offset_x, configs.flask4_type, configs.flask4_pixel, configs.flask4_empty, configs.flask4_duration, configs.flask4_react, configs.flask4_always, True, False)
flask5 = Flask("flask5", e.KEY_5, configs.flask5_enable, configs.flask5_offset_x, configs.flask5_type, configs.flask5_pixel, configs.flask5_empty, configs.flask5_duration, configs.flask5_react, configs.flask5_always, True, False)

escape = Menu('Escape ', configs.escape_pixel1, configs.escape_pixel2, configs.escape_pixel3, configs.escape_color1, configs.escape_color2, configs.escape_color3, False)
loading = Menu('Loading', configs.loading_pixel1, configs.loading_pixel2, configs.loading_pixel3, configs.loading_color1, configs.loading_color2, configs.loading_color3, False)
death = Menu('Death  ', configs.death_pixel1, configs.death_pixel2, configs.death_pixel3, configs.death_color1, configs.death_color2, configs.death_color3, False)

meter_list = [life, mana]
flasks_list = [flask1, flask2, flask3, flask4, flask5]
menu_list = [escape, loading, death]

# Main
def main():
  i = 0
  absolute_start = time.time()
  while True:
    i += 1
    relative_start = time.time()
    screen_load = screen_capture()
    life_handoff = True
    mana_handoff = True
    menu_inside = False

    if configs.main_menu_enable:
      for menu in menu_list:
        menu_check(menu, screen_load, menu_inside)

    # Check if the user is inside one of the menu screens. If so, skip the processing.
    if not menu_inside:
      if configs.main_life_enable:
        meter_check(life, screen_load)
      if configs.main_mana_enable:
        meter_check(mana, screen_load)
      for flask in flasks_list:
        if flask.enable:
          flask_check(flask, screen_load)
          flask_press = threading.Thread(target=key_press, args=[flask])
          if life.need:
            if flask.valid and ((flask.react == "Life" and life_handoff) or flask.always):
              if not flask.lock:
                flask.lock = True
                flask_press.start()
              life_handoff = False
            else:
              life_handoff = True
          if mana.need:
            if flask.valid and ((flask.react == "Mana" and mana_handoff) or flask.always):
              if not flask.lock:
                flask.lock = True
                flask_press.start()
              mana_handoff = False
            else:
              mana_handoff = True
      print_parser(i, meter_list, flasks_list, None)
    else:
      print_parser(i, meter_list, None, menu_list)

    loop_rate(i, configs.main_rate, absolute_start, relative_start)

if __name__ == "__main__":
  main()
