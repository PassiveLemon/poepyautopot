# poepyautopot
A Python based Autopot script for Path of Exile

This will constantly check your life, mana, and flasks. If your life/mana gets too low, it will determine which flasks it can use and will press that number through your keyboard's input driver.

## Disclaimer
I am not responsible for any bans or data loss as a result of using this. This was a project for me to learn Python. If you are worried about getting banned, don't use it and be a legitimate player :)

# Dependencies
* Linux. <b>This does not currently support Windows or MacOS.</b>
* Sudo. This requires access to a `/dev/input` device.
* Python3. Duh.
* Python packages: `evdev pillow(-simd) pyyaml`
* <b>Note:</b> The game must be in fullscreen at 1080p. Other methods might eventually be supported. You can always fix this yourself though.

# Notes and tips
I do not recommend relying on this to always keep you alive. It does a pretty good job but do not expect it to replace for your fingers. I do not think it is fast enough for that. </br>

On my system, it runs at around 55-65 Hz. Your system may vary. I am trying to make this as fast as possible. </br>

I recommend to run PoE at 60 FPS. Running it too high will cause the game to get choppy and it might slow down the script. From personal experience, running at 144 FPS is way more choppy than at 60 FPS. </br>

Currently, pixel values only detect if something is empty. This works easily but it not the most customizable. This may be improved in the future. </br>

Flasks do have a lock system but its only for itself. It does not currently detect the lock of other flasks. This means that it may use other life/mana flasks when it just used on in that check. I am working on this.

# Usage
Clone the repo, edit the `config.yaml`, run `sudo python3 __main__.py -f <path to config file>`. </br>

`-f | --file:` The location of your config.yaml. You can use relative paths like ~ . Will default to the included one if not set. Ex: `~/.config/poepyautopot/config.yaml`

You can run the `kp_calc.py` script in utils to get a calculated data set for your key presses to use in the config. Just run it and follow the prompt. You can use any numbers you want, I just recommend using actual data as it represents the physical capabilities of your keyboard and should theoretically make your key presses look more human. If your keyboard key presses physically cannot be shorter than 28 ms, you shouldn't be emulating a 2 ms key press. </br>

# Configuration (config.yaml)
If it doesn't seem to work properly, please make sure your configurations are correctly set. As a last resort, open an issue on the GitHub.
## Flask database
This is still a WIP. </br>
This is the database for each flask type and the pixel to detect in the leftmost slot. (This gets adjusted based on the slot). </br>
It is not recommended to change anything unless you know what you are doing. </br>

## User config
#### Hardware
`keyboard_event:` The `/dev/input/event#` that applies to your keyboard. </br>
`screen_offset:` The space of screen above and to the left of the game window. This assumes the game is fullscreen at 1080p! Ex: If you have two horzontal 1080p monitors, and you run the game on the right one, set the X to 1920 and Y to 0. If you have 2 vertical 1080p monitors and you run the game on the bottom one, set the X to 0 and Y to 1080. </br>

#### WRITE THESE IN SECONDS! They will get converted to milliseconds. </br>
These will use my data by default. </br>
`key_press: shortest:` The lowest/shortest value from your data set. </br>
`key_press: longest:` The highest/longest value from your data set. </br>
`key_press: range:` The +/- range for the randomizer. You don't really need to change this. </br>
`key_press: std_dev:` The standard deviation of your data set. </br>
`key_press: target:` The target mean length of your key press. Most of the lengths should be around this number. <br>

#### Flasks
`flask#: enable:` Boolean to enable the flask to be automated. </br>
`flask#: type:` What kind of flask it is. Ex: A sacred life flask. To set this, you must use the yaml anchor from the database. </br>
`flask#: react:` This will cause the flask to react to either life or mana. This can be used to trigger utility/unique flasks. </br>
`flask#: always:` This will cause the flask to trigger every single time life/mana is needed. Flasks with this enabled should be put towards the right of your flask menu. Useful with utility/unique flasks. </br>

#### Functions
`main: enable:` Boolean to enable the main part of the script. You should probably keep this enabled. </br>
`main: life:` Boolean to enable the life checking. Disable if you don't want your life flasks automated. </br>
`main: mana:` Same thing as `main: life:`, just for mana. </br>
`main: flasks:` Boolean to enable flask automation. You should probably also keep this enabled. Why else would you be using this script? </br>
`main: menus:` Boolean to enable menu detection. I recommend to leave this on. It will prevent unnecessary key presses. </br>
`main: rate:` Set the interval of each check. Setting it to 100 will check every 100 ms. Set it to 0 to disable the limit. </br>

`debug: enable:` Boolean to enable debugging. This just shows some extra details while running. May impact performance. Recommended to keep this off. </br>
`debug: life: enable:` Boolean to enable life specific debugging. </br>
`debug: life: pixel:` Boolean to enable pixel detection debugging. Shows what pixel it expected to detect and what it actually detected. </br>
`debug: life: rgb:` Boolean to enable RGB debugging. Shows what RGB value it expected to detect and what it actually detected. </br>
`debug: mana:` Exact same as life. </br>
`debug: flask:` Exact same as life. </br>
* Note: The flasks have x offsets! What it actually detects is offset from what it expected based on the slot its in. Don't get confused by this. </br>
`debug: menu:` Exact same as life. </br>
`debug: image_save: enable:` Boolean to enable the saving of images while running. This will MASSIVELY tank performance so its HIGHLY recommend to keep this off. </br>
`debug: image_save: location:` The place you want to save the images to. </br>

`test: enable:` Boolean to enable testing functions. You should disable `main: enable:` when using this. </br>
`test: key_press_test: enable:` Boolean to enable the key_press test. </br>
`test: key_press_test: delay:` Time before the test actually begins. Gives you time to move your cursor to where you want it. </br>
`test: key_press_test: count:` The amount of key_presses to simulate. </br>

Of course you can always edit the code itself to fit some of your needs. It's still very much a WIP so more is to come. There is still plenty of room for improvement and features. </br>

