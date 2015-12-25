from evdev import InputDevice
from select import select
import pygame
pygame.init()
s = pygame.mixer.Sound('Bb0.aiff')

dev = InputDevice("/dev/input/by-path/platform-i8042-serio-0-event-kbd")
count = 0
while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        code = str(event).split(" ")[4]
        current = str(event).split("val")[1]
        count += 1;
        if (code != '00,' and current == " 01"):
            print(current)
            s.play()
        if (count == 6):
            count = 0
pygame.quit()
