from evdev import InputDevice
from select import select
from numbers import Number
import pygame
import re

def arrayCreator(filename):
    f = open(filename, "r") #Readonly
    end = False
    pattern = re.compile("K:*")
    while(not end):
        if(pattern.match(f.readline())):
            end = True
    #Next readline will read the notes of measures.
    nextLine = f.readline()
    flat = False
    sharp = False
    song = []
    while(nextLine != ""):
        for c in nextLine:

            if(flat == True):
                song.append(c + "b")
                flat = False
            elif(sharp == True):
                song.append(c + "sharp")
                sharp = False
            elif(c.isdigit() or c==' ' or c=='\n' or c=='/' or c=='=' or c=="|" or c=="_" or c=="^" or c=="(" or c=="'" or c=="z"):
                pass
            else:
                song.append(c)


            if(c == "_"): #Flat
                flat = True
            elif(c == "^"):
                sharp = True

        nextLine = f.readline()

    return song


def playNote(string):
    #s = pygame.mixer.Sound("notes/" + string + ".aiff")
    s = pygame.mixer.Sound("notes/C4.aiff")
    s.play

pygame.init()
pygame.mixer.init()

song = arrayCreator("song.txt")

#Input from keyboard event. This is why this program needs root permissions
dev = InputDevice("/dev/input/by-path/platform-i8042-serio-0-event-kbd")

noteNum = 0
while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        #Next two lines take neccessary info from the event. To see more info from event, print event.
        code = str(event).split(" ")[4]
        current = str(event).split("val")[1]
        if (code != '00,' and current == " 01"):
            foo = "notes/" + song[noteNum] + ".aiff"
            s = pygame.mixer.Sound(foo)
            s.play()
            noteNum += 1
            if (noteNum >= len(song)):
                noteNum = 0; #repeat
