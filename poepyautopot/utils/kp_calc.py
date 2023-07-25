from pynput import keyboard 
import time
import os
import re
import statistics

# I do not take ownership of any of the code in this file. 90% of this was generated from ChatGPT, I just touched some of it up.

with open("key_press_data.txt", "w") as file:
  file.write(f"")

def write_to_file(key, time_taken):
  with open("key_press_data.txt", "a") as file:
    file.write(f"{key} - {time_taken:.1f} ms\n")

def on_key_press(key):
  global t
  t = time.time()
  return False

def on_key_release(key):
  time_taken = round(time.time() - t, 3) * 1000
  os.system("clear")
  print(key,time_taken,'ms')
  write_to_file(key, time_taken)

  return False

i = 20
print(f"Please press 1 number from 1-5 {i} times. Make sure to not press to quickly.")
while i > 0:
  with keyboard.Listener(on_press = on_key_press) as press_listener:
    press_listener.join()

  with keyboard.Listener(on_release = on_key_release) as release_listener:
    release_listener.join()
    i -= 1

def extract_ms(entry):
  pattern = r"\d+\.\d+"
  match = re.search(pattern, entry)
  if match:
    return float(match.group())
  else:
    return None

def main():
  file_path = "./key_press_data.txt"

  with open(file_path, "r") as file:
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

  print(f"Minimum: {minimum:.1f} ms")
  print(f"Maximum: {maximum:.1f} ms")
  print(f"Standard deviation: {standard_deviation:.1f} ms")
  print(f"Q1: {q1:.1f} ms")
  print(f"Mean: {mean:.1f} ms")
  print(f"Q3: {q3:.1f} ms")

main()