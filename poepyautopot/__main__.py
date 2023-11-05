from evdev import ecodes as e
import threading
import time

from config import config
import checks
import functions
import objects

# Init
life = objects.Meter("Life", config.main_life_enable, config.life_pixel, config.life_empty, False)
mana = objects.Meter("Mana", config.main_mana_enable, config.mana_pixel, config.mana_empty, False)

flask1 = objects.Flask("flask1", e.KEY_1, config.flask1_enable, config.flask1_offset_x, config.flask1_type, config.flask1_pixel, config.flask1_empty, config.flask1_duration, config.flask1_react, config.flask1_always, True, False)
flask2 = objects.Flask("flask2", e.KEY_2, config.flask2_enable, config.flask2_offset_x, config.flask2_type, config.flask2_pixel, config.flask2_empty, config.flask2_duration, config.flask2_react, config.flask2_always, True, False)
flask3 = objects.Flask("flask3", e.KEY_3, config.flask3_enable, config.flask3_offset_x, config.flask3_type, config.flask3_pixel, config.flask3_empty, config.flask3_duration, config.flask3_react, config.flask3_always, True, False)
flask4 = objects.Flask("flask4", e.KEY_4, config.flask4_enable, config.flask4_offset_x, config.flask4_type, config.flask4_pixel, config.flask4_empty, config.flask4_duration, config.flask4_react, config.flask4_always, True, False)
flask5 = objects.Flask("flask5", e.KEY_5, config.flask5_enable, config.flask5_offset_x, config.flask5_type, config.flask5_pixel, config.flask5_empty, config.flask5_duration, config.flask5_react, config.flask5_always, True, False)

escape = objects.Menu('Escape ', config.escape_pixel1, config.escape_pixel2, config.escape_pixel3, config.escape_color1, config.escape_color2, config.escape_color3, False)
loading = objects.Menu('Loading', config.loading_pixel1, config.loading_pixel2, config.loading_pixel3, config.loading_color1, config.loading_color2, config.loading_color3, False)
death = objects.Menu('Death  ', config.death_pixel1, config.death_pixel2, config.death_pixel3, config.death_color1, config.death_color2, config.death_color3, False)

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
    screen_load = functions.screen_capture()
    life_handoff = True
    mana_handoff = True

    if config.main_menu_enable:
      for menu in menu_list:
        checks.menu_check(menu, screen_load)

    # Check if the user is inside one of the menu screens. If so, skip the processing.
    if not escape.inside and not loading.inside and not death.inside:
      if config.main_life_enable:
        checks.meter_check(life, screen_load)
      if config.main_mana_enable:
        checks.meter_check(mana, screen_load)
      for flask in flasks_list:
        if flask.enable:
          checks.flask_check(flask, screen_load)
          flask_press = threading.Thread(target=functions.key_press, args=[flask])
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
      functions.print_parser(i, meter_list, flasks_list, None)
    else:
      functions.print_parser(i, meter_list, None, menu_list)

    functions.loop_rate(i, config.main_rate, absolute_start, relative_start)

if __name__ == "__main__":
  main()
