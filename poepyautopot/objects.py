from ast import literal_eval as le # To evaluate the tuples correctly
import os

import yaml

from .config import arguments

class Config(object):
  def __init__(self):
    yaml_config = yaml.safe_load(open(arguments.file))
    self.database = yaml_config["database"]
    self.life = self.database["life"]
    self.life_pixel = le(self.life["pixel"])
    self.life_empty = le(self.life["empty"])
    self.mana = self.database["mana"]
    self.mana_pixel = le(self.mana["pixel"])
    self.mana_empty = le(self.mana["empty"])

    self.database_flask = self.database["flask"]
    self.flask1_offset_x = self.database_flask["flask1_offset_x"]
    self.flask2_offset_x = self.database_flask["flask2_offset_x"]
    self.flask3_offset_x = self.database_flask["flask3_offset_x"]
    self.flask4_offset_x = self.database_flask["flask4_offset_x"]
    self.flask5_offset_x = self.database_flask["flask5_offset_x"]

    self.menus = self.database["menus"]
    self.escape = self.menus["escape"]
    self.escape_pixel1 = le(self.escape["pixel1"])
    self.escape_color1 = le(self.escape["color1"])
    self.escape_pixel2 = le(self.escape["pixel2"])
    self.escape_color2 = le(self.escape["color2"])
    self.escape_pixel3 = le(self.escape["pixel3"])
    self.escape_color3 = le(self.escape["color3"])
    self.loading = self.menus["loading"]
    self.loading_pixel1 = le(self.loading["pixel1"])
    self.loading_color1 = le(self.loading["color1"])
    self.loading_pixel2 = le(self.loading["pixel2"])
    self.loading_color2 = le(self.loading["color2"])
    self.loading_pixel3 = le(self.loading["pixel3"])
    self.loading_color3 = le(self.loading["color3"])
    self.death = self.menus["death"]
    self.death_pixel1 = le(self.death["pixel1"])
    self.death_color1 = le(self.death["color1"])
    self.death_pixel2 = le(self.death["pixel2"])
    self.death_color2 = le(self.death["color2"])
    self.death_pixel3 = le(self.death["pixel3"])
    self.death_color3 = le(self.death["color3"])

    self.hardware = yaml_config["hardware"]
    self.keyboard_event = self.hardware["keyboard_event"]
    self.screen_offset = self.hardware["screen_offset"]
    self.screen_offset_x = self.screen_offset["x"]
    self.screen_offset_y = self.screen_offset["y"]

    self.key_press = yaml_config["key_press"]
    self.key_press_shortest = self.key_press["shortest"]
    self.key_press_longest = self.key_press["longest"]
    self.key_press_std_dev = self.key_press["std_dev"]
    self.key_press_target = self.key_press["target"]

    self.flask1 = yaml_config["flask1"]
    self.flask1_enable = self.flask1["enable"]
    self.flask1_type = self.flask1["type"]
    self.flask1_pixel = le(self.flask1_type["pixel"])
    self.flask1_empty = le(self.flask1_type["empty"])
    self.flask1_duration = self.flask1_type["duration"]
    self.flask1_react = self.flask1["react"]
    self.flask1_always = self.flask1["always"]

    self.flask2 = yaml_config["flask2"]
    self.flask2_enable = self.flask2["enable"]
    self.flask2_type = self.flask2["type"]
    self.flask2_pixel = le(self.flask2_type["pixel"])
    self.flask2_empty = le(self.flask2_type["empty"])
    self.flask2_duration = self.flask2_type["duration"]
    self.flask2_react = self.flask2["react"]
    self.flask2_always = self.flask2["always"]

    self.flask3 = yaml_config["flask3"]
    self.flask3_enable = self.flask3["enable"]
    self.flask3_type = self.flask3["type"]
    self.flask3_pixel = le(self.flask3_type["pixel"])
    self.flask3_empty = le(self.flask3_type["empty"])
    self.flask3_duration = self.flask3_type["duration"]
    self.flask3_react = self.flask3["react"]
    self.flask3_always = self.flask3["always"]

    self.flask4 = yaml_config["flask4"]
    self.flask4_enable = self.flask4["enable"]
    self.flask4_type = self.flask4["type"]
    self.flask4_pixel = le(self.flask4_type["pixel"])
    self.flask4_empty = le(self.flask4_type["empty"])
    self.flask4_duration = self.flask4_type["duration"]
    self.flask4_react = self.flask4["react"]
    self.flask4_always = self.flask4["always"]

    self.flask5 = yaml_config["flask5"]
    self.flask5_enable = self.flask5["enable"]
    self.flask5_type = self.flask5["type"]
    self.flask5_pixel = le(self.flask5_type["pixel"])
    self.flask5_empty = le(self.flask5_type["empty"])
    self.flask5_duration = self.flask5_type["duration"]
    self.flask5_react = self.flask5["react"]
    self.flask5_always = self.flask5["always"]

    self.main = yaml_config["main"]
    self.main_life_enable = self.main["life"]
    self.main_mana_enable = self.main["mana"]
    self.main_menu_enable = self.main["menu"]
    self.main_rate = self.main["rate"]
    self.main_range = self.main["range"]
    self.main_delay = self.main["delay"]
    self.main_verbose = self.main["verbose"]

class Meter(object):
  def __init__(self, name, enable, pixel, empty, need):
    self.name = name
    self.enable = enable
    self.pixel = pixel
    self.empty = empty
    self.need = need
  def __str__(self):
    return self.name

class Flask(object):
  def __init__(self, name, number, enable, offset_x, type, pixel, empty, duration, react, always, valid, lock, last):
    self.name = name
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
    self.last = last
  def __str__(self):
    return self.name

class Menu(object):
  def __init__(self, name, pixel1, pixel2, pixel3, color1, color2, color3, inside):
    self.name = name
    self.pixel1 = pixel1
    self.pixel2 = pixel2
    self.pixel3 = pixel3
    self.color1 = color1
    self.color2 = color2
    self.color3 = color3
    self.inside = inside
  def __str__(self):
    return self.name

Config = Config()
