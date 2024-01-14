import os
import random
import time

from colorama import Fore, Style, init as colorama_init
from evdev import UInput, ecodes as e
from PIL import ImageGrab

from .objects import Config

colorama_init()

def screen_capture():
  screen_capture = ImageGrab.grab(bbox=(Config.screen_offset_x, Config.screen_offset_y, 1920 + Config.screen_offset_x, 1080 + Config.screen_offset_y))
  screen_load = screen_capture.load()
  return screen_load

def key_press(flask):
  # Gaussian distribution for realism
  def gaussian(min, max, sig, mu):
    while True:
      value = int(random.gauss(mu, sig))
      if min <= value <= max:
        return value

  random_key_press_sleep = gaussian(Config.key_press_shortest, Config.key_press_longest, Config.key_press_std_dev, Config.key_press_target)

  ui = UInput.from_device(Config.keyboard_event)
  ui.write(e.EV_KEY, flask.number, 1)
  ui.syn()

  time.sleep(random_key_press_sleep / 1000)

  ui.write(e.EV_KEY, flask.number, 0)
  ui.syn()
  ui.close()
  if Config.main_verbose in [1, 2, 3]:
    print(f"flask {flask.number} ({random_key_press_sleep} ms), {flask.duration} second lock.")
  # Take off a portion of the sleep time to allow the flask to be activated slightly earlier than the duration if needed
  time.sleep(flask.duration / 1.5)

  flask.lock = False

def print_parser(i, meter_list, flasks_list, menu_list, menu_inside):
  # Assign certain properties of the objects to a color and parse them
  def pretty():
    print_list = []
    print_length = 0
    if flasks_list:
      for meter in meter_list:
        if meter.enable:
          if meter.need:
            print_list.append(f"{Fore.RED}{meter}{Style.RESET_ALL}")
          else:
            print_list.append(f"{Fore.GREEN}{meter}{Style.RESET_ALL}")
          print_length += len(meter.name) + 1
      print_list.append("|")
      print_length += 2
      for flask in flasks_list:
        if flask.enable:
          if flask.valid and not flask.lock:
            print_list.append(f"{Fore.GREEN}{flask}{Style.RESET_ALL}")
          elif flask.valid and flask.lock:
            print_list.append(f"{Fore.YELLOW}{flask}{Style.RESET_ALL}")
          elif not flask.valid:
            print_list.append(f"{Fore.RED}{flask}{Style.RESET_ALL}")
          print_length += len(flask.name) + 1

    if menu_list:
      for menu in menu_list:
        if menu_inside:
          print_list.append(f"{Fore.GREEN}{menu}{Style.RESET_ALL}")
          print_length += len(menu.name) + 1

    terminal_width = os.get_terminal_size().columns
    print_list.append(f"{Fore.BLUE}{i : >{os.get_terminal_size().columns - print_length - 1}}{Style.RESET_ALL}")

    for item in print_list:
      print(item, end=' ')
    # Print nothing to trick the for item loop into printing every single loop rather than for every key press. Not sure why that happens
    print('')

  match Config.main_verbose:
    case 0:
      pass
      # The print from the key_press should probably be managed from this function but oh well
    case 1:
      pass
    case 2:
      pretty()
    case 3:
      pretty()

def loop_rate(i, main_rate, absolute_start, relative_start):
  # Calculate the current time taken vs what the user specified and wait the difference
  time_taken = round(time.time() - relative_start, 3) * 1000
  if time_taken < main_rate:
    time.sleep((main_rate / 1000) - (time_taken / 1000))
