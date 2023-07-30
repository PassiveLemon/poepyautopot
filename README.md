# poepyautopot
A Python based Autopot script for Path of Exile

This will constantly check your life, mana, and flasks. If your life/mana gets too low, it will determine which flasks it can use and will press that number through your keyboard's input driver.

## Disclaimer
I am not responsible for any bans or data loss as a result of using this. This was a project for me to learn Python. If you are worried about getting banned, don't use it and be a legitimate player :)

# Dependencies
* Linux. <b>This does not currently support Windows or MacOS.</b>
* Sudo. This requires access to a `/dev/input` device.
* Python3. Duh.
* Python packages: `evdev pillow pyyaml`
* <b>Note:</b> The game must be in fullscreen at 1080p. Other methods might eventually be supported. You can always fix this yourself though.

# Notes and tips
I do not recommend relying on this to always keep you alive. It does not run quite fast enough for that yet. It works well for low and slow damage but getting hit too rapidly may kill you before it gets processed. I am currently working on speeding this up. </br>

Currently on my system, it runs at around 30-50 Hz. Your system may vary. Once again, I am currently working on speeding this up. 60 Hz minimum is the goal. </br>

I recommend to run PoE at a frame rate of around 60-72 Hz. Running it too high will cause the game to get choppy and slow down the script. </br>

I recommend using flasks that regenerate life as fast as possible (Ex: Sanctified, Eternal). There is no cooldown implemented yet so a slow flask may get ticked multiple times. </br>

# Usage
Clone the repo, edit the `config.yaml`, run `__main__.py`. </br>

You can run the `kp_calc.py` script in utils to get a calculated data set for your key presses to use in the config. Of course you can use any numbers you want, I just recommend using actual data as it represents the physical capabilities of your keyboard and should theoretically make your key presses look more human. If your keyboard key presses physically cannot be shorter than 28 ms, you shouldn't be emulating a 2 ms key press. </br>

# Configuration (config.yaml)
## Flask database
This is still a WIP. </br>
Duration is still an experimental variable. </br>
This is the database for each flask type and the pixel to detect in the leftmost slot. (This gets adjusted based on the slot). </br>
It is not recommended to change anything unless you know what you are doing. </br>

## User config
#### Hardware
`keyboard_event:` The `/dev/input/event#` that applies to your keyboard. </br>
`screen_offset:` The space of screen above and to the left of the game window. This assumes the game is fullscreen at 1080p! </br>

#### WRITE THESE IN SECONDS! They will get converted to milliseconds. </br>
These will use my data by default. </br>
`key_press: shortest:` The lowest/shortest value from your data set. </br>
`key_press: longest:` The highest/longest value from your data set. </br>
`key_press: range:` The +/- range for the randomizer. You don't really need to change this. </br>
`key_press: std_dev:` The standard deviation of your data set. </br>
`key_press: target:` The target mean length of your key press. Most of the lengths should be around this number. <br>

#### Flasks
`flask#: enable:` Booleam to enable the flask to be automated. </br>
`flask#: type:` What kind of flask it is. Ex: A sacred life flask. To set this, you must use the yaml anchor in the database. </br>
`flask#: x_offset:` The pixel offset of the capture. Don't change this unless you know what you are doing. </br>

#### Functions
`main: enable:` Boolean to enable the main part of the script. You should probably keep this enabled. </br>
`main: life:` Boolean to enable the life checking. Disable if you don't want your life flasks automated. </br>
`main: mana:` Same thing as `main: life:`, just for mana. </br>
`main: flasks:` Boolean to enable flask automation. You should probably also keep this enabled. </br>

`debug: enable:` Boolean to enable debugging. This just shows some extra details while running. May impact performance. Recommended to keep this off. </br>
`debug: image_save: enable:` Boolean to enable the saving of images while running. This will MASSIVELY tank performance so its HIGHLY recommend to keep this off. </br>
`debug: image_save: location:` The place you want to save the images to. </br>

`test: enable:` Boolean to enable testing functions. </br>
`test: key_press_test: enable:` Boolean to enable the key_press test. </br>
`test: key_press_test: delay:` Time before the test actually begins. Gives you time to move your cursor to where you want it. </br>
`test: key_press_test: count:` The amount of key_presses to simulate. </br>
