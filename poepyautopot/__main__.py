import os
import threading
import time

from evdev import ecodes as e

from .objects import Config, Meter, Flask, Menu
from .checks import menu_check, meter_check, flask_check
from .functions import screen_capture, key_press, print_parser, loop_rate

life = Meter("Life", Config.main_life_enable, Config.life_pixel, Config.life_empty, False)
mana = Meter("Mana", Config.main_mana_enable, Config.mana_pixel, Config.mana_empty, False)

flask1 = Flask("flask1", e.KEY_1, Config.flask1_enable, Config.flask1_offset_x, Config.flask1_type, Config.flask1_pixel, Config.flask1_empty, Config.flask1_duration, Config.flask1_react, Config.flask1_always, True, False, None)
flask2 = Flask("flask2", e.KEY_2, Config.flask2_enable, Config.flask2_offset_x, Config.flask2_type, Config.flask2_pixel, Config.flask2_empty, Config.flask2_duration, Config.flask2_react, Config.flask2_always, True, False, None)
flask3 = Flask("flask3", e.KEY_3, Config.flask3_enable, Config.flask3_offset_x, Config.flask3_type, Config.flask3_pixel, Config.flask3_empty, Config.flask3_duration, Config.flask3_react, Config.flask3_always, True, False, None)
flask4 = Flask("flask4", e.KEY_4, Config.flask4_enable, Config.flask4_offset_x, Config.flask4_type, Config.flask4_pixel, Config.flask4_empty, Config.flask4_duration, Config.flask4_react, Config.flask4_always, True, False, None)
flask5 = Flask("flask5", e.KEY_5, Config.flask5_enable, Config.flask5_offset_x, Config.flask5_type, Config.flask5_pixel, Config.flask5_empty, Config.flask5_duration, Config.flask5_react, Config.flask5_always, True, False, None)

escape = Menu("Escape", Config.escape_pixel1, Config.escape_pixel2, Config.escape_pixel3, Config.escape_color1, Config.escape_color2, Config.escape_color3, False)
loading = Menu("Loading", Config.loading_pixel1, Config.loading_pixel2, Config.loading_pixel3, Config.loading_color1, Config.loading_color2, Config.loading_color3, False)
death = Menu("Death", Config.death_pixel1, Config.death_pixel2, Config.death_pixel3, Config.death_color1, Config.death_color2, Config.death_color3, False)

meter_list = [life, mana]
flasks_list = [flask1, flask2, flask3, flask4, flask5]
menu_list = [escape, loading, death]

def main():
  time.sleep(Config.main_delay)
  i = 0
  absolute_start = time.time()
  try:
    while True:
      i += 1
      relative_start = time.time()
      screen_load = screen_capture()
      life_handoff = True
      mana_handoff = True
      menu_inside = False

      if Config.main_menu_enable:
        for menu in menu_list:
          if menu_check(menu, screen_load):
            menu_inside = True

      # Check if the user is inside one of the menu screens. If so, skip the processing
      if not menu_inside:
        for meter in meter_list:
          if meter.enable:
            meter.need = meter_check(meter, screen_load)
        for flask in flasks_list:
          if flask.enable:
            flask.valid = flask_check(flask, screen_load)
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

      print_parser(i, meter_list, flasks_list, menu_list, menu_inside)
      loop_rate(i, Config.main_rate, absolute_start, relative_start)
  except KeyboardInterrupt:
    exit()

if __name__ == "__main__":
  main()
