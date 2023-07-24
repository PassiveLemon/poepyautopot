# poepyautopot
A Python based Autopot script for Path of Exile

# WIP

This is mostly an impulse project but also an opportunity to learn some Python.

For getting the recommended timings on keypresses, go to a site like [this](https://keyboardtester.info/keyboard-latency-test/) and type around 20-30 numbers (1-5) while holding your hand how you normally would when playing the game. Using a calculator, put all of the values into a table and find the minimum, maximum, standard deviation and then either q1, mean or q3 (which ever appears to match the values in your table closest.) Next take your std dev and whatever other value you chose. range_key_press just adds/subs that amount from the shortest and longest key press. You don't really need to change that. </br>
Of course you can use any numbers you want, I just recommend using actual data as it should theoretically make your keypresses look more human, avoiding detecting from anticheats.
