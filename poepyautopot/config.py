import argparse
import os

import yaml

user = os.getenv("SUDO_USER")
user_config_dir = os.getenv("XDG_CONFIG_HOME", f"/home/{user}/.config/poepyautopot")
user_config_file = os.path.join(user_config_dir, "config.yaml")
source_install_path = os.path.dirname(os.path.realpath(__file__))
source_config_file = os.path.join(source_install_path, "config.yaml")

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default=user_config_file, help="Location of configuration file.")
arguments = parser.parse_args()

try:
  yaml.safe_load(open(arguments.file))
except FileNotFoundError:
  if arguments.file is user_config_file:
    print(f"Configuration file does not exist at XDG_CONFIG: {user_config_file}, generating...")
    with open(user_config_file, 'w') as user, open (source_config_file, "r") as source:
      for line in source:
        user.write(line)
  else:
    raise Exception(f"Configuration file does not exist: {arguments.file}")
except IsADirectoryError:
  raise Exception(f"Configuration file is a directory: {arguments.file}")
except PermissionError:
  raise Exception(f"You do not have the necessary permissions to access configuration file: {arguments.file}")
except:
  raise Exception(f"Configuration file is not valid YAML: {arguments.file}")

# This program requires access to keyboard devices (which requires sudo) so we raise
if os.geteuid() != 0:
  raise Exception("This program requires sudo.")
