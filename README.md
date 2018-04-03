# Keyboard Mario [Abandoned]

A music program which plays a notes of a song each time a letter is placed. Currently works on Linux, though the program may need to be modified depending on where the keyboard event is being outputted to.

The input file is the song.txt, which is song written in the abc notation.

The file which the program uses to listen to keyboard events is:
    /dev/input/event0

This file may not be the location of where the keyboard event is on your specific laptop.

This program was written as a test to a later project I will call Monitype (like monitor, but monitype. get it? hahaha.... not funny anyways..), which will monitor your typing speed throught the session, and tell you your speed and accuracy based on how many keys and backspaces were pressed respectivly).

Dependencies:
evdev
pygame

# Contributing
 - Feel free to clean up my disgusting code (I believe this was the first time I wrote python code)
 - Some ideas for further development:
    -> Read from Midi files
    -> Generalize the driver files, so it works on all devices (Lookat AutoKey for reference on how to do that).
