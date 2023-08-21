import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="./config.yaml")
config_file = parser.parse_args().file

yaml_config = yaml.safe_load(open(config_file))

# I hate all of this. Atleast it's somewhat hidden in here.
class Config:
  def __init__(self):
    self.database = yaml_config["database"]
    self.life = self.database["life"]
    self.life_pixel = self.life["pixel"]
    self.life_empty = self.life["empty"]
    self.mana = self.database["mana"]
    self.mana_pixel = self.mana["pixel"]
    self.mana_empty = self.mana["empty"]

    self.database_flask = self.database["flask"]
    self.flask1_offset_x = self.database_flask["flask1_offset_x"]
    self.flask2_offset_x = self.database_flask["flask2_offset_x"]
    self.flask3_offset_x = self.database_flask["flask3_offset_x"]
    self.flask4_offset_x = self.database_flask["flask4_offset_x"]
    self.flask5_offset_x = self.database_flask["flask5_offset_x"]

    self.menus = self.database["menus"]
    self.escape = self.menus["escape"]
    self.escape_pixel1 = self.escape["pixel1"]
    self.escape_color1 = self.escape["color1"]
    self.escape_pixel2 = self.escape["pixel2"]
    self.escape_color2 = self.escape["color2"]
    self.escape_pixel3 = self.escape["pixel3"]
    self.escape_color3 = self.escape["color3"]
    self.loading = self.menus["loading"]
    self.loading_pixel1 = self.loading["pixel1"]
    self.loading_color1 = self.loading["color1"]
    self.loading_pixel2 = self.loading["pixel2"]
    self.loading_color2 = self.loading["color2"]
    self.loading_pixel3 = self.loading["pixel3"]
    self.loading_color3 = self.loading["color3"]
    self.death = self.menus["death"]
    self.death_pixel1 = self.death["pixel1"]
    self.death_color1 = self.death["color1"]
    self.death_pixel2 = self.death["pixel2"]
    self.death_color2 = self.death["color2"]
    self.death_pixel3 = self.death["pixel3"]
    self.death_color3 = self.death["color3"]

    self.hardware = yaml_config["hardware"]
    self.keyboard_event = self.hardware["keyboard_event"]
    self.screen_offset = self.hardware["screen_offset"]
    self.screen_offset_x = self.screen_offset["x"]
    self.screen_offset_y = self.screen_offset["y"]

    self.key_press = yaml_config["key_press"]
    self.key_press_shortest = self.key_press["shortest"]
    self.key_press_longest = self.key_press["longest"]
    self.key_press_range = self.key_press["range"]
    self.key_press_std_dev = self.key_press["std_dev"]
    self.key_press_target = self.key_press["target"]

    self.key_press_shortest_low = self.key_press_shortest - self.key_press_range
    self.key_press_shortest_high = self.key_press_shortest + self.key_press_range
    self.key_press_longest_low = self.key_press_longest - self.key_press_range
    self.key_press_longest_high = self.key_press_longest + self.key_press_range

    self.flask1 = yaml_config["flask1"]
    self.flask1_enable = self.flask1["enable"]
    self.flask1_type = self.flask1["type"]
    self.flask1_pixel = self.flask1_type["pixel"]
    self.flask1_empty = self.flask1_type["empty"]
    self.flask1_duration = self.flask1_type["duration"]
    self.flask1_react = self.flask1["react"]
    self.flask1_always = self.flask1["always"]

    self.flask2 = yaml_config["flask2"]
    self.flask2_enable = self.flask2["enable"]
    self.flask2_type = self.flask2["type"]
    self.flask2_pixel = self.flask2_type["pixel"]
    self.flask2_empty = self.flask2_type["empty"]
    self.flask2_duration = self.flask2_type["duration"]
    self.flask2_react = self.flask2["react"]
    self.flask2_always = self.flask2["always"]

    self.flask3 = yaml_config["flask3"]
    self.flask3_enable = self.flask3["enable"]
    self.flask3_type = self.flask3["type"]
    self.flask3_pixel = self.flask3_type["pixel"]
    self.flask3_empty = self.flask3_type["empty"]
    self.flask3_duration = self.flask3_type["duration"]
    self.flask3_react = self.flask3["react"]
    self.flask3_always = self.flask3["always"]

    self.flask4 = yaml_config["flask4"]
    self.flask4_enable = self.flask4["enable"]
    self.flask4_type = self.flask4["type"]
    self.flask4_pixel = self.flask4_type["pixel"]
    self.flask4_empty = self.flask4_type["empty"]
    self.flask4_duration = self.flask4_type["duration"]
    self.flask4_react = self.flask4["react"]
    self.flask4_always = self.flask4["always"]

    self.flask5 = yaml_config["flask5"]
    self.flask5_enable = self.flask5["enable"]
    self.flask5_type = self.flask5["type"]
    self.flask5_pixel = self.flask5_type["pixel"]
    self.flask5_empty = self.flask5_type["empty"]
    self.flask5_duration = self.flask5_type["duration"]
    self.flask5_react = self.flask5["react"]
    self.flask5_always = self.flask5["always"]

    self.main = yaml_config["main"]
    self.main_enable = self.main["enable"]
    self.main_life_enable = self.main["life"]
    self.main_mana_enable = self.main["mana"]
    self.main_menu_enable = self.main["menu"]
    self.main_rate = self.main["rate"]

    self.debug = yaml_config["debug"]
    self.debug_enable = self.debug["enable"]
    self.debug_life_enable = self.debug["life"]
    self.debug_mana_enable = self.debug["mana"]
    self.debug_flask_enable = self.debug["flask"]
    self.debug_menu_enable = self.debug["menu"]
    self.debug_image_save = self.debug["image_save"]
    self.debug_image_save_enable = self.debug_image_save["enable"]
    self.debug_image_save_location = self.debug_image_save["location"]

config = Config()
