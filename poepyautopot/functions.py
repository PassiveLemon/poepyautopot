from colorama import Fore, Style, init as colorama_init
from evdev import UInput, ecodes as e
from PIL import ImageGrab
import random
import shutil
import time

from config import config

colorama_init()

def screen_capture():
  screen_capture = ImageGrab.grab(bbox=(config.screen_offset_x, config.screen_offset_y, 1920 + config.screen_offset_x, 1080 + config.screen_offset_y))
  screen_load = screen_capture.load()

  if config.debug_enable and config.debug_image_save_enable:
    screen_capture.save(debug_image_save_location, "/screen.png")

  return screen_load

def key_press(flask):
  # Gaussian distribution for realism
  def gaussian(min, max, sig, mu):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  random_key_press_sleep = gaussian(config.key_press_shortest, config.key_press_longest, config.key_press_std_dev, config.key_press_target)

  ui = UInput.from_device(config.keyboard_event)
  ui.write(e.EV_KEY, flask.number, 1)
  ui.syn()

  time.sleep(random_key_press_sleep / 1000)

  ui.write(e.EV_KEY, flask.number, 0)
  ui.syn()
  ui.close()
  print(f"\n flask {flask.number} ({random_key_press_sleep} ms), {flask.duration} second lock.")
  # Take off a portion of the sleep time to allow the flask to be activated slightly earlier than the duration if needed
  time.sleep(flask.duration / 1.5)

  flask.lock = False

def print_parser(i, meter_list, flasks_list, menu_list):
  # Assign certain properties of the objects to a color and parse them
  print_list = []
  print_length = 0
  if flasks_list:
    for meter in meter_list:
      if meter.enable:
        if meter.need:
          print_list.append(f"{Fore.RED}{meter}{Style.RESET_ALL}")
        else:
          print_list.append(f"{Fore.GREEN}{meter}{Style.RESET_ALL}")
        print_length += 4
    print_list.append("|")
    for flask in flasks_list:
      if flask.enable:
        if flask.valid and not flask.lock:
          print_list.append(f"{Fore.GREEN}{flask}{Style.RESET_ALL}")
        elif flask.valid and flask.lock:
          print_list.append(f"{Fore.YELLOW}{flask}{Style.RESET_ALL}")
        elif not flask.valid:
          print_list.append(f"{Fore.RED}{flask}{Style.RESET_ALL}")
        print_length += 6

  if menu_list:
    for menu in menu_list:
      if menu.inside:
        print_list.append(f"{Fore.GREEN}{menu}{Style.RESET_ALL}")
        print_length += 7

  # Attempt to align the loop count to the right. Doesn't properly work but it's good enough I guess
  terminal_width = shutil.get_terminal_size().columns
  print_list.append(f"{Fore.BLUE}{i}{Style.RESET_ALL}".rjust(terminal_width - print_length))

  for item in print_list:
    print(item, end=' ')
  # Print nothing to trick the for item loop into printing every single loop rather than for every key press. Not sure why that happens
  print('')

def loop_rate(i, main_rate, absolute_start, relative_start):
  # Calculate the current time taken vs what the user specified and wait the difference
  time_taken = round(time.time() - relative_start, 3) * 1000
  if time_taken < main_rate:
    time.sleep((main_rate / 1000) - (time_taken / 1000))
