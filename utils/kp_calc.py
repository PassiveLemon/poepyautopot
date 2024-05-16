import re
import statistics
import sys
import time

from pynput import keyboard 

data_file = "./key_press_data.txt"

def write_to_file(time_taken):
  with open(data_file, "a") as file:
    file.write(f"{time_taken:.1f} \n")

def on_key_press():
  global t
  t = time.time()
  return False

def on_key_release(key):
  time_taken = (round(time.time() - t, 3) * 1000)
  print(key,time_taken,'ms')
  # Clear previous input line for neatness
  sys.stdout.write('\x1b[1A')
  sys.stdout.write('\x1b[2K')
  write_to_file(key, time_taken)
  return False

def extract_ms(entry):
  pattern = r"\d+\.\d+"
  match = re.search(pattern, entry)
  if match:
    return float(match.group())
  else:
    return None

def main():
  # Clear old data file
  with open(data_file, "w") as file:
    file.write(f"")

  i = 50
  print(f"Please press 1 number from 1-5 {i} times:")
  while i > 0:
    with keyboard.Listener(on_press = on_key_press) as press_listener:
      press_listener.join()

    with keyboard.Listener(on_release = on_key_release) as release_listener:
      release_listener.join()
      i -= 1

  with open(data_file, "r") as file:
    entries = file.read().splitlines()

  time_values = [extract_ms(entry) for entry in entries]

  if not time_values:
    print("Error with time values... Please try again.")
    return

  sorted_data = sorted(time_values)
  n = len(sorted_data)

  minimum = min(time_values)
  maximum = max(time_values)
  standard_deviation = statistics.stdev(time_values)
  q1_index = (n + 1) // 4
  q1 = sorted_data[q1_index]
  mean = statistics.mean(time_values)
  q3_index = 3 * (n + 1) // 4
  q3 = sorted_data[q3_index]

  # Clear instruction line
  sys.stdout.write('\x1b[1A')
  sys.stdout.write('\x1b[2K')

  print(f"Minimum: {minimum:.1f} ms")
  print(f"Maximum: {maximum:.1f} ms")
  print(f"Standard deviation: {standard_deviation:.1f} ms")
  print(f"Q1: {q1:.1f} ms")
  print(f"Mean: {mean:.1f} ms")
  print(f"Q3: {q3:.1f} ms")

main()
