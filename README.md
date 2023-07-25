# poepyautopot
A Python based Autopot script for Path of Exile

# WIP

This is mostly an impulse project but also an opportunity to learn some Python.

# Configuration
## config.yaml
`keyboard_event:` The `/dev/input/event#` that applies to your keyboard. </br>
`screen_offset:` The space of screen above and to the left of the game window. This assumes the game is fullscreen at 1080p! </br>

#### WRITE THESE IN SECONDS! They will get converted to milliseconds. </br>
These will use my data by default. </br>
`key_press: shortest:` The lowest/shortest value from your data set. </br>
`key_press: longest:` The highest/longest value from your data set. </br>
`key_press: range:` The +/- range for the randomizer. You don't really need to change this. </br>
`key_press: std_dev:` The standard deviation of your data set. </br>
`key_press: target:` The target mean length of your key press. Most of the lengths should be around this number. <br>
`key_press: test: enable:` Boolean for the key_press test. </br>
`key_press: test: delay:` Time before the test actually begins. Gives you time to move your mouse to where you want it. </br>
`key_press: test: count:` The amount of key_presses to simulate. </br>

`image_test: enable:` Boolean for the image test. </br>
`image_test: save_location:` The location where the test images are stored. Only needed if image_test is enabled.

For getting the recommended timings on key presses, go into utils and run the kp_calc.py script (requires sudo). This will provide calculated timings to use above. </br>
With that data set, find the minimum, maximum, standard deviation and then a target number. This could be something like the q1, mean or q3. </br>
Of course you can use any numbers you want, I just recommend using actual data as it represents the physical capabilities of your keyboard and should theoretically make your key presses look more human. If your keyboard key presses physically cannot be shorter than 28 ms, you shouldn't be emulating a 2 ms key press. </br>
