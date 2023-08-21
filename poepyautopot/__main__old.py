import ast
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from evdev import UInput, ecodes as e
from PIL import ImageGrab
import random
import time
import threading

from config import config

# Objects
class Meter(object):
  def __init__(self, enable, pixel, empty, need):
    self.enable = enable
    self.pixel = pixel
    self.empty = empty
    self.need = need

class Flask(object):
  def __init__(self, number, enable, offset_x, type, pixel, empty, duration, react, always, valid, lock):
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

class Menu(object):
  def __init__(self, pixel1, pixel2, pixel3, color1, color2, color3, inside):
    self.pixel1 = pixel1
    self.pixel2 = pixel2
    self.pixel3 = pixel3
    self.color1 = color1
    self.color2 = color2
    self.color3 = color3
    self.inside = inside

# Init
life = Meter(config.main_life_enable, config.life_pixel, config.life_empty, False)
mana = Meter(config.main_mana_enable, config.mana_pixel, config.mana_empty, False)

flask1 = Flask(1, config.flask1_enable, config.flask1_offset_x, config.flask1_type, config.flask1_pixel, config.flask1_empty, config.flask1_duration, config.flask1_react, config.flask1_always, True, False)
flask2 = Flask(2, config.flask2_enable, config.flask2_offset_x, config.flask2_type, config.flask2_pixel, config.flask2_empty, config.flask2_duration, config.flask2_react, config.flask2_always, True, False)
flask3 = Flask(3, config.flask3_enable, config.flask3_offset_x, config.flask3_type, config.flask3_pixel, config.flask3_empty, config.flask3_duration, config.flask3_react, config.flask3_always, True, False)
flask4 = Flask(4, config.flask4_enable, config.flask4_offset_x, config.flask4_type, config.flask4_pixel, config.flask4_empty, config.flask4_duration, config.flask4_react, config.flask4_always, True, False)
flask5 = Flask(5, config.flask5_enable, config.flask5_offset_x, config.flask5_type, config.flask5_pixel, config.flask5_empty, config.flask5_duration, config.flask5_react, config.flask5_always, True, False)

escape = Menu(config.escape_pixel1, config.escape_pixel2, config.escape_pixel3, config.escape_color1, config.escape_color2, config.escape_color3, False)
loading = Menu(config.loading_pixel1, config.loading_pixel2, config.loading_pixel3, config.loading_color1, config.loading_color2, config.loading_color3, False)
death = Menu(config.death_pixel1, config.death_pixel2, config.death_pixel3, config.death_color1, config.death_color2, config.death_color3, False)

colorama_init()

# Utility
def key_press(num, wait, flasknum):
  global flask1, flask2, flask3, flask4, flask5
  # Bell curve to more closely group presses
  def bell_curve(min, max, sig, mu):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  # Variate key press length with random lows and highs, std dev, and target.
  random_range_low = random.randint(config.key_press_shortest_low, config.key_press_shortest_high)
  random_range_high = random.randint(config.key_press_longest_low, config.key_press_longest_high)
  random_key_press_sleep = bell_curve(random_range_low, random_range_high, config.key_press_std_dev, config.key_press_target)

  ui = UInput.from_device(config.keyboard_event)
  ui.write(e.EV_KEY, num, 1)
  ui.syn()

  time.sleep(random_key_press_sleep / 1000.0)

  ui.write(e.EV_KEY, num, 0)
  ui.syn()
  ui.close()
  print(f"\n flask {num} ({random_key_press_sleep} ms), {wait} second lock.")
  time.sleep(wait / 1.5)

  if flasknum == "flask1":
    flask1.lock = False
  if flasknum == "flask2":
    flask2.lock = False
  if flasknum == "flask3":
    flask3.lock = False
  if flasknum == "flask4":
    flask4.lock = False
  if flasknum == "flask5":
    flask5.lock = False

def screen_capture():
  global screen_load
  screen_capture = ImageGrab.grab(bbox=(config.screen_offset_x, config.screen_offset_y, 1920 + config.screen_offset_x, 1080 + config.screen_offset_y))
  screen_load = screen_capture.load()

  if config.debug_enable == True and config.debug_image_save_enable == True:
    screen_capture.save("./screen.png")

def life_check():
  global life
  xl_raw, yl_raw = ast.literal_eval(life.pixel)
  rl, gl, bl = screen_load[xl_raw, yl_raw]
  rl_empty, gl_empty, bl_empty, = ast.literal_eval(life.empty)
  rl_empty_min, rl_empty_max = rl_empty - 5, rl_empty + 5
  gl_empty_min, gl_empty_max = gl_empty - 5, gl_empty + 5
  bl_empty_min, bl_empty_max = bl_empty - 5, bl_empty + 5
  if rl_empty_min <= rl <= rl_empty_max and gl_empty_min <= gl <= gl_empty_max and bl_empty_min <= bl <= bl_empty_max:
    life.need = False
  else:
    life.need = True

  if config.debug_enable == True and config.debug_life_enable == True:
    print(f"life-pixel[exp{life.pixel} - act{xl_raw, yl_raw}]")
    print(f"life-rgb[exp({life.empty}) - act{rl, gl, bl}]")

def mana_check():
  global mana
  xm_raw, ym_raw = ast.literal_eval(mana.pixel)
  rm, gm, bm = screen_load[xm_raw, ym_raw]
  rm_empty, gm_empty, bm_empty, = ast.literal_eval(mana.empty)
  rm_empty_min, rm_empty_max = rm_empty - 5, rm_empty + 5
  gm_empty_min, gm_empty_max = gm_empty - 5, gm_empty + 5
  bm_empty_min, bm_empty_max = bm_empty - 5, bm_empty + 5
  if rm_empty_min <= rm <= rm_empty_max and gm_empty_min <= gm <= gm_empty_max and bm_empty_min <= bm <= bm_empty_max:
    mana.need = False
  else:
    mana.need = True

  if config.debug_enable == True and config.debug_mana_enable == True:
    print(f"mana-pixel[exp{mana.pixel} - act{xm_raw, ym_raw}]")
    print(f"mana-rgb[exp({mana.empty}) - act{rm, gm, bm}]")

def flask_check_ind(flask):
  if flask.enable == True:
    x1_raw, y1_raw = ast.literal_eval(flask.pixel)
    x1_off = (int(x1_raw) + int(flask.offset_x))
    r1, g1, b1 = screen_load[x1_off, y1_raw]
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask.empty)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      flask.valid = False
    else:
      flask.valid = True

def flask_check():
  global flask1, flask2, flask3, flask4, flask5
  if flask1.enable == True:
    x1_raw, y1_raw = ast.literal_eval(flask1.pixel)
    x1_off = (int(x1_raw) + int(flask1.offset_x))
    r1, g1, b1 = screen_load[x1_off, y1_raw]
    r1_empty, g1_empty, b1_empty, = ast.literal_eval(flask1.empty)
    r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
    g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
    b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
    if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
      flask1.valid = False
    else:
      flask1.valid = True

  if flask2.enable == True:
    x2_raw, y2_raw = ast.literal_eval(flask2.pixel)
    x2_off = (int(x2_raw) + int(flask2.offset_x))
    r2, g2, b2 = screen_load[x2_off, y2_raw]
    r2_empty, g2_empty, b2_empty, = ast.literal_eval(flask2.empty)
    r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
    g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
    b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
    if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
      flask2.valid = False
    else:
      flask2.valid = True

  if flask3.enable == True:
    x3_raw, y3_raw = ast.literal_eval(flask3.pixel)
    x3_off = (int(x3_raw) + int(flask3.offset_x))
    r3, g3, b3 = screen_load[x3_off, y3_raw]
    r3_empty, g3_empty, b3_empty, = ast.literal_eval(flask3.empty)
    r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
    g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
    b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
    if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
      flask3.valid = False
    else:
      flask3.valid = True
  
  if flask4.enable == True:
    x4_raw, y4_raw = ast.literal_eval(flask4.pixel)
    x4_off = (int(x4_raw) + int(flask4.offset_x))
    r4, g4, b4 = screen_load[x4_off, y4_raw]
    r4_empty, g4_empty, b4_empty, = ast.literal_eval(flask4.empty)
    r4_empty_min, r4_empty_max = r4_empty - 5, r4_empty + 5
    g4_empty_min, g4_empty_max = g4_empty - 5, g4_empty + 5
    b4_empty_min, b4_empty_max = b4_empty - 5, b4_empty + 5
    if r4_empty_min <= r4 <= r4_empty_max and g4_empty_min <= g4 <= g4_empty_max and b4_empty_min <= b4 <= b4_empty_max:
      flask4.valid = False
    else:
      flask4.valid = True

  if flask5.enable == True:
    x5_raw, y5_raw = ast.literal_eval(flask5.pixel)
    x5_off = (int(x5_raw) + int(flask5.offset_x))
    r5, g5, b5 = screen_load[x5_off, y5_raw]
    r5_empty, g5_empty, b5_empty, = ast.literal_eval(flask5.empty)
    r5_empty_min, r5_empty_max = r5_empty - 5, r5_empty + 5
    g5_empty_min, g5_empty_max = g5_empty - 5, g5_empty + 5
    b5_empty_min, b5_empty_max = b5_empty - 5, b5_empty + 5
    if r5_empty_min <= r5 <= r5_empty_max and g5_empty_min <= g5 <= g5_empty_max and b5_empty_min <= b5 <= b5_empty_max:
      flask5.valid = False
    else:
      flask5.valid = True

  if config.debug_enable == True and config.debug_flask_enable == True:
    if flask1.enable == True:
      print(f"flask1-pixel[exp{flask1.pixel} - act{x1_off, y1_raw}]")
      print(f"flask1-rgb[exp({flask1.empty}) - act{r1, g1, b1}]")
    if flask2.enable == True:
      print(f"flask2-pixel[exp{flask2.pixel} - act{x2_off, y2_raw}]")
      print(f"flask2-rgb[exp({flask2.empty}) - act{r2, g2, b2}]")
    if flask3.enable == True:
      print(f"flask3-pixel[exp{flask3.pixel} - act{x3_off, y3_raw}]")
      print(f"flask3-rgb[exp({flask3.empty}) - act{r3, g3, b3}]")
    if flask4.enable == True:
      print(f"flask4-pixel[exp{flask3.pixel} - act{x4_off, y4_raw}]")
      print(f"flask4-rgb[exp({flask3.empty}) - act{r4, g4, b4}]")
    if flask5.enable == True:
      print(f"flask5-pixel[exp{flask3.pixel} - act{x5_off, y5_raw}]")
      print(f"flask5-rgb[exp({flask3.empty}) - act{r5, g5, b5}]")

def escape_check():
  global escape
  x1_raw, y1_raw = ast.literal_eval(escape.pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(escape.color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    escape1 = True
  else:
    escape1 = False

  x2_raw, y2_raw = ast.literal_eval(escape.pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(escape.color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    escape2 = True
  else:
    escape2 = False
  
  x3_raw, y3_raw = ast.literal_eval(escape.pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(escape.color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    escape3 = True
  else:
    escape3 = False

  if escape1 == True and escape2 == True and escape3 == True:
    escape.inside = True
  else:
    escape.inside = False

  if config.debug_enable == True and config.debug_menu_enable == True:
    print(f"escape-pixel1[exp{escape.pixel1} - act{x1_raw, y1_raw}]")
    print(f"escape-rgb1[exp({escape.color1}) - act{r1, g1, b1}]")
    print(f"escape-pixel2[exp{escape.pixel2} - act{x2_raw, y2_raw}]")
    print(f"escape-rgb2[exp({escape.color2}) - act{r2, g2, b2}]")
    print(f"escape-pixel3[exp{escape.pixel3} - act{x3_raw, y3_raw}]")
    print(f"escape-rgb3[exp({escape.color3}) - act{r3, g3, b3}]")

def loading_check():
  global loading
  x1_raw, y1_raw = ast.literal_eval(loading.pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(loading.color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    loading1 = True
  else:
    loading1 = False

  x2_raw, y2_raw = ast.literal_eval(loading.pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(loading.color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    loading2 = True
  else:
    loading2 = False
  
  x3_raw, y3_raw = ast.literal_eval(loading.pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(loading.color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    loading3 = True
  else:
    loading3 = False

  if loading1 == True and loading2 == True and loading3 == True:
    loading.inside = True
  else:
    loading.inside = False

  if config.debug_enable == True and config.debug_menu_enable == True:
    print(f"loading-pixel1[exp{loading.pixel1} - act{x1_raw, y1_raw}]")
    print(f"loading-rgb1[exp({loading.color1}) - act{r1, g1, b1}]")
    print(f"loading-pixel2[exp{loading.pixel2} - act{x2_raw, y2_raw}]")
    print(f"loading-rgb2[exp({loading.color2}) - act{r2, g2, b2}]")
    print(f"loading-pixel3[exp{loading.pixel3} - act{x3_raw, y3_raw}]")
    print(f"loading-rgb3[exp({loading.color3}) - act{r3, g3, b3}]")

def death_check():
  global death
  x1_raw, y1_raw = ast.literal_eval(death.pixel1)
  r1, g1, b1 = screen_load[x1_raw, y1_raw]
  r1_empty, g1_empty, b1_empty, = ast.literal_eval(death.color1)
  r1_empty_min, r1_empty_max = r1_empty - 5, r1_empty + 5
  g1_empty_min, g1_empty_max = g1_empty - 5, g1_empty + 5
  b1_empty_min, b1_empty_max = b1_empty - 5, b1_empty + 5
  if r1_empty_min <= r1 <= r1_empty_max and g1_empty_min <= g1 <= g1_empty_max and b1_empty_min <= b1 <= b1_empty_max:
    death1 = True
  else:
    death1 = False

  x2_raw, y2_raw = ast.literal_eval(death.pixel2)
  r2, g2, b2 = screen_load[x2_raw, y2_raw]
  r2_empty, g2_empty, b2_empty, = ast.literal_eval(death.color2)
  r2_empty_min, r2_empty_max = r2_empty - 5, r2_empty + 5
  g2_empty_min, g2_empty_max = g2_empty - 5, g2_empty + 5
  b2_empty_min, b2_empty_max = b2_empty - 5, b2_empty + 5
  if r2_empty_min <= r2 <= r2_empty_max and g2_empty_min <= g2 <= g2_empty_max and b2_empty_min <= b2 <= b2_empty_max:
    death2 = True
  else:
    death2 = False
  
  x3_raw, y3_raw = ast.literal_eval(death.pixel3)
  r3, g3, b3 = screen_load[x3_raw, y3_raw]
  r3_empty, g3_empty, b3_empty, = ast.literal_eval(death.color3)
  r3_empty_min, r3_empty_max = r3_empty - 5, r3_empty + 5
  g3_empty_min, g3_empty_max = g3_empty - 5, g3_empty + 5
  b3_empty_min, b3_empty_max = b3_empty - 5, b3_empty + 5
  if r3_empty_min <= r3 <= r3_empty_max and g3_empty_min <= g3 <= g3_empty_max and b3_empty_min <= b3 <= b3_empty_max:
    death3 = True
  else:
    death3 = False

  if death1 == True and death2 == True and death3 == True:
    death.inside = True
  else:
    death.inside = False

  if config.debug_enable == True and config.debug_menu_enable == True:
    print(f"death-pixel1[exp{death.pixel1} - act{x1_raw, y1_raw}]")
    print(f"death-rgb1[exp({death.color1}) - act{r1, g1, b1}]")
    print(f"death-pixel2[exp{death.pixel2} - act{x2_raw, y2_raw}]")
    print(f"death-rgb2[exp({death.color2}) - act{r2, g2, b2}]")
    print(f"death-pixel3[exp{death.pixel3} - act{x3_raw, y3_raw}]")
    print(f"death-rgb3[exp({death.color3}) - act{r3, g3, b3}]")

# Main
def main():
  global life_need, mana_need
  global inside_menu
  life_need = False
  mana_need = False
  inside_menu = False
  i = 0
  while True:
    time_start = time.time()
    screen_capture()

    if config.main_menu_enable == True:
      escape_check()
      loading_check()
      death_check()

    if config.main_life_enable == True:
      life_check()
    if config.main_mana_enable == True:
      mana_check()
    if config.main_flask_enable == True:
      #flask_check()
      flask_check_ind(flask1)
      flask_check_ind(flask2)

    print_list = []
    i += 1
    print_list.append(f"{Fore.CYAN}{i}{Style.RESET_ALL}")

    if escape.inside == True or loading.inside == True or death.inside == True:
      extra = True
      #print(f"{Fore.CYAN}{i}{Style.RESET_ALL} escape-{escape_inside} loading-{loading_inside} death-{death_inside}")
    else:
      #print(f"life-{life_need} mana-{mana_need} 1-{flask1_valid} 2-{flask2_valid} 3-{flask3_valid} 4-{flask4_valid} 5-{flask5_valid}")
      flask_handoff = False
      if life.need == True:
        if (flask1.enable == True and flask1.valid == True) and (flask1.react == "Life" or flask1.always == True):
          flask1_press_life = threading.Thread(target=key_press, args=[e.KEY_1, flask1.duration, "flask1"])
          if flask1.lock == False:
            flask1.lock = True
            flask1_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask2.enable == True and flask2.valid == True) and ((flask2.react == "Life" and flask_handoff == True) or flask2.always == True):
          flask2_press_life = threading.Thread(target=key_press, args=[e.KEY_2, flask2.duration, "flask2"])
          if flask2.lock == False:
            flask2.lock = True
            flask2_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask3.enable == True and flask3.valid == True) and ((flask3.react == "Life" and flask_handoff == True) or flask3.always == True):
          flask3_press_life = threading.Thread(target=key_press, args=[e.KEY_3, flask3.duration, "flask3"])
          if flask3.lock == False:
            flask3.lock = True
            flask3_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask4.enable == True and flask4.valid == True) and ((flask4.react == "Life" and flask_handoff == True) or flask4.always == True):
          flask4_press_life = threading.Thread(target=key_press, args=[e.KEY_4, flask4.duration, "flask4"])
          if flask4.lock == False:
            flask4.lock = True
            flask4_press_life.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask5.enable == True and flask5.valid == True) and ((flask5.react == "Life" and flask_handoff == True) or flask5.always == True):
          flask5_press_life = threading.Thread(target=key_press, args=[e.KEY_5, flask5.duration, "flask5"])
          if flask5.lock == False:
            flask5.lock = True
            flask5_press_life.start()
          flask_handoff = False

      flask_handoff = False
      if mana_need == True:
        if (flask1_enable == True and flask1_valid == True) and (flask1_react == "mana" or flask1_always == True):
          flask1_press_mana = threading.Thread(target=key_press, args=[e.KEY_1, flask1_duration, "flask1"])
          if flask1_lock == False:
            flask1_lock = True
            flask1_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask2_enable == True and flask2_valid == True) and ((flask2_react == "mana" and flask_handoff == True) or flask2_always == True):
          flask2_press_mana = threading.Thread(target=key_press, args=[e.KEY_2, flask2_duration, "flask2"])
          if flask2_lock == False:
            flask2_lock = True
            flask2_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask3_enable == True and flask3_valid == True) and ((flask3_react == "mana" and flask_handoff == True) or flask3_always == True):
          flask3_press_mana = threading.Thread(target=key_press, args=[e.KEY_3, flask3_duration, "flask3"])
          if flask3_lock == False:
            flask3_lock = True
            flask3_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask4_enable == True and flask4_valid == True) and ((flask4_react == "mana" and flask_handoff == True) or flask4_always == True):
          flask4_press_mana = threading.Thread(target=key_press, args=[e.KEY_4, flask4_duration, "flask4"])
          if flask4_lock == False:
            flask4_lock = True
            flask4_press_mana.start()
          flask_handoff = False
        else:
          flask_handoff = True

        if (flask5_enable == True and flask5_valid == True) and ((flask5_react == "mana" and flask_handoff == True) or flask5_always == True):
          flask5_press_mana = threading.Thread(target=key_press, args=[e.KEY_5, flask5_duration, "flask5"])
          if flask5_lock == False:
            flask5_lock = True
            flask5_press_mana.start()
          flask_handoff = False

    if flask1.valid == True and flask1.lock == False:
      print_list.append(f"{Fore.GREEN}flask1{Style.RESET_ALL}")
    elif flask1.valid == True and flask1.lock == True:
      print_list.append(f"{Fore.YELLOW}flask1{Style.RESET_ALL}")
    elif flask1.valid == False:
      print_list.append(f"{Fore.RED}flask1{Style.RESET_ALL}")

    if flask2.valid == True and flask2.lock == False:
      print_list.append(f"{Fore.GREEN}flask2{Style.RESET_ALL}")
    elif flask2.valid == True and flask2.lock == True:
      print_list.append(f"{Fore.YELLOW}flask2{Style.RESET_ALL}")
    elif flask2.valid == False:
      print_list.append(f"{Fore.RED}flask2{Style.RESET_ALL}")

    time_taken = round(time.time() - time_start, 3) * 1000
    if time_taken < config.main_rate:
      time.sleep((config.main_rate / 1000) - (time_taken / 1000))

    for item in print_list:
      print(item, end=' ')
    print('')

if config.main_enable == True:
  main()
