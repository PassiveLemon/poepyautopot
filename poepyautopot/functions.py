from evdev import UInput, ecodes as e
import random
import time

from config import config

class Functions:
  def key_press(self, num, wait, flask):
    # Gaussian distribution for realism
    def gaussian(min, max, sig, mu):
      while True:
        value = int(random.gauss(mu, sig))
        if min <= value <= max:
          return value

    # Variate key press length with random lows and highs, std dev, and target.
    # From testing and visualizing the data, it doesn't really look like how the human inputs would. Doing it this way gets it to look a little better sometimes?
    random_range_low = random.randint(config.key_press_shortest_low, config.key_press_shortest_high)
    random_range_high = random.randint(config.key_press_longest_low, config.key_press_longest_high)
    random_key_press_sleep = gaussian(random_range_low, random_range_high, config.key_press_std_dev, config.key_press_target)

    ui = UInput.from_device(config.keyboard_event)
    ui.write(e.EV_KEY, num, 1)
    ui.syn()

    time.sleep(random_key_press_sleep / 1000.0)

    ui.write(e.EV_KEY, num, 0)
    ui.syn()
    ui.close()
    print(f"\n flask {num} ({random_key_press_sleep} ms), {wait} second lock.")
    time.sleep(wait / 1.5)

    flask.lock = False

functions = Functions()
