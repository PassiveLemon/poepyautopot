# poepyautopot
A Python based Autopot script for Path of Exile </br>

This will constantly check your life, mana, and flasks. If your life/mana gets too low, it will determine which flasks it can use and will press that number through your keyboard's input driver. </br>

## Disclaimer
I am not responsible for any bans or data loss as a result of using this. This was a project for me to learn Python. If you are worried about getting banned, don't use it and be a legitimate player :) </br>

# Dependencies
* Linux. <b>This is not supported on Windows or MacOS</b> though it may in the future.
* X11. This is not supported on Wayland.
* Sudo. This requires access to `/dev`.
* Python packages: `colorama evdev pillow pyyaml (pynput for kp_calc.py)`
* <b>Note:</b> The game must be in fullscreen at 1920x1080p. Other methods might eventually be supported. You can always fix this yourself though.

# Usage
Clone the repo, edit the `config.yaml`, run `sudo python3 __main__.py -f <path to config file>`. Please read the configuration below. It will not work out of the box. </br>
- Arguments can be found by tacking `-h` or `--help`

The colors of the outputs in the terminal have meaning:
* For meter values like life and mana, if it is needed, it will be red. Otherwise, it's green.
* For flasks, if it's valid and not locked, it's green. If it's valid but locked, it will be yellow. If it's not valid, it will be red.
* For menus, it will be green. </br>

You can run the `kp_calc.py` script in utils to get a calculated data set for your key presses to use in the config. Just run it and follow the prompt. You can use any numbers you want, I just recommend using actual data as it represents the physical capabilities of your keyboard and should theoretically make your key presses look more human. If your keyboard key presses physically cannot be shorter than 28 ms, you shouldn't be emulating a 2 ms key press. </br>

# Configuration (config.yaml)
#### Write any time value as a whole number. Ex: for 100 milliseconds, just write 100 and for 3 seconds, just write 3. </br>
This will not work out of the box. You will need to configure it yourself. Go into the config.yaml, past the database, and edit the appropriate values under the user config section. Details are below. </br>
If it doesn't seem to work properly, please make sure your configurations are correctly set. As a last resort, open an issue in the GitHub repository. </br>
## Flask database
<b>This is still a WIP and it is not recommended to change anything unless you know what you are doing.</b> </br>

This is the database for each flask type and the pixel to detect when the flask is in the left most slot. (This gets adjusted with an X offset depending on its slot) </br>
#### Flasks
| Value | Options | Description |
| :- | :- | :- |
| `pixel(#):` | `tuple (x, y)` | The location of the pixels (x, y) coordinates on the screen. |
| `empty(#):` | `tuple r, g, b` | The color of the pixel when the flask is empty. |
| `duration:` | `number` | The duration of the flasks effect. |

#### Menus
| Value | Options | Description |
| :- | :- | :- |
| `pixel(#):` | `tuple (x, y)` | The location of the pixels (x, y) coordinates on the screen. |
| `color(#):` | `tuple r, g, b` | The color the checked pixel must match to return True. |

## User config
#### Hardware
| Value | Options | Default | Description |
| :- | :- | :- | :- |
| `keyboard_event:` | `string with path` | `/dev/input/event0` | The event device that applies to your keyboard. This is usually event0 but you should double check. |
| `screen_offset:` | `integer` | `x: 0` `y: 0` | The space of screen above and to the left of the game window. <b>This assumes the game is fullscreen at 1920x1080p!</b> Ex: If you have two horzontal 1080p monitors, and you run the game on the right one, set the X to 1920 and Y to 0. If you have 2 vertical 1080p monitors and you run the game on the bottom one, set the X to 0 and Y to 1080. |

#### Key press
| Value | Options | Default | Description |
| :- | :- | :- | :- |
| `shortest:` | `integer` | `54` | The lowest/shortest value from your data set. |
| `longest:` | `integer` | `141` |  The highest/longest value from your data set. |
| `std_dev:` | `integer` | `21` |  The standard deviation of your data set. |
| `target:` | `integer` | `110` |  The target mean length of your key press. Most of the lengths should be around this number. |

#### Flasks
| Value | Options | Default | Description |
| :- | :- | :- | :- |
| `enable:` | `boolean` | `False` | Enable the flask to be automated. |
`type:` | `yaml anchor` | `*life_hallowed` | What kind of flask it is. Ex: A sacred life flask. |
`react:` | `string` `Life` `Mana` | `Life` | This will cause the flask to react to either life or mana. This can be used to trigger utility/unique flasks.
`always:` | `boolean` | `False` | This will cause the flask to trigger every single time life/mana is needed. Flasks with this enabled are recommended to be put towards the right of your flask menu to avoid locking other flasks. |
- Tip: `react:` and `always:` can be paired to activate flasks whenever life/mana is needed regardless of priority. Useful for utility/unique flasks.

#### Main
| Value | Options | Default | Description |
| :- | :- | :- | :- |
| `life:` | `boolean` | `True` | Enable life checking. Disable if you don't want your life flasks automated. |
| `mana:` | `boolean` | `True` | Enable mana checking. Disable if you don't want your mana flasks automated. |
| `menus:` | `boolean` | `True` | Enable menu detection. Recommend to leave this on as it will prevent unnecessary key presses. |
| `rate:` | `number` | `16` | The interval of each check. Setting it to 100 will check every 100 ms. Set it to 0 to effectively disable the limit. 16 should give around 60 Hz. |
| `range:` | `integer` | `5` | The range of pixels to check. This means it will check pixels up to 5 RGB values away from the designated color. This just gives some margin. |
| `delay:` | `number` | `3` | The amount of seconds to delay the start of the program by. |
| `verbose:` | `0` `1` `2` `3` | `2` | The level of verbosity. 0 shows nothing. 1 shows the pressed keys. 2 shows 1 + every check. 3 enables 2 + verbose mode. |
- Note: The flasks have x offsets! What it actually detects is offset from what it expected based on the slot its in. Don't get confused by this when enabling verbose mode. |

Of course you can always edit the code itself to fit some of your needs. It's still very much a WIP so more is to come. There is still plenty of room for improvement and features. </br>

# Notes
I do not recommend relying on this to always keep you alive. It does a pretty good job but do not expect it to replace for your fingers. I do not think it is fast enough for that. </br>

On my system, it runs at around 60-70 Hz. This may be different based on your system hardware and configuration. Usually, the less things you enable, the faster it runs. I am trying to make this as fast as possible. </br>

I recommend to run PoE at 60 FPS. Running it too high will cause the game to get choppy and it might slow down the script. From personal experience, running at 144 FPS is way more choppy than at 60 FPS. </br>

Currently, pixel values only detect if something is empty. This works easily but it not the most customizable. This may be improved in the future. </br>

Flasks do have a lock system but its only for itself. It does not currently detect the lock of other flasks. This means that it may use other life/mana flasks almost immediately after previously using one because of delays in the life zone. Faster flask durations and slower check rates make this less noticable but it's planned to be fixed. </br>
