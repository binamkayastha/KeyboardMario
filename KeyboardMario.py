from evdev import InputDevice
from select import select
from numbers import Number
import sys
import pygame
import re

def arrayCreator(filename):
    f = open(filename, "r") #Readonly
    end = False
    pattern = re.compile("K:*") #Pattern will store the Key value
    while(not end):
        if(pattern.match(f.readline())):
            end = True
    #Next readline will read the notes of measures.
    nextLine = f.readline()
    flat = False
    sharp = False
    isCord = False
    song = []
    while(nextLine != ""):
        for c in nextLine:
            if(c == '"'): #Either the beging or end of Cord
                if(isCord == True): #End of Cord
                    isCord = False;
                else:               #Begnning of Cord
                    isCord = True;
            elif(flat == True):
                song.append(c + "b")
                flat = False
            elif(sharp == True):
                song.append(c + "sharp")
                sharp = False
            elif(c.isdigit() or isCord or c==' ' or c=='\n' or c=='/' or c=='=' or c=="|" or c=="_" or c=="^" or c=="(" or c=="'" or c=="z" or c=="m"):
                pass
            else:
                song.append(c)


            if(c == "_"): #Flat
                flat = True
            elif(c == "^"):
                sharp = True

        nextLine = f.readline()

    return song

def isModifier(key):
    key = key[0:2]  #get rid of ',' at end of key
    key = int(key)
    #L and R        Shift, Ctrl,   Alt,     Win, Caps on/off
    if(key in [42, 54, 29, 97, 56, 100, 125, 1, 58]):
        return True
    else:
        return False

def playNote(string):
    #s = pygame.mixer.Sound("notes/" + string + ".aiff")
    s = pygame.mixer.Sound("notes/C4.aiff")
    s.play

pygame.init()
pygame.mixer.init()

if len(sys.argv) > 1:
    song = arrayCreator(sys.argv[1])
else:
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
        if ((not isModifier(code)) and code != '00,' and current == " 01"):
            foo = "notes/" + song[noteNum] + ".aiff"
            s = pygame.mixer.Sound(foo)
            s.play()
            noteNum += 1
            if (noteNum >= len(song)):
                noteNum = 0; #repeat
