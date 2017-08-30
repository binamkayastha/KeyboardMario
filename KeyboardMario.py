from evdev import InputDevice
from select import select
from numbers import Number
import sys
import pygame
import re

def arrayCreator(filename):
    f = open(filename, "r") #Readonly
    end = False
    pattern = re.compile("K:*") #Pattern will store Key (Musical) value
    while(not end): #Ignore all lines uptil K:
        if(pattern.match(f.readline())):
            end = True

    #Next readline will read the notes of measures.
    nextLine = f.readline()
    flat = sharp = isCord =  False

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
            elif(c.isdigit() or isCord or (c in [' ', '\n' ,'/' ,'=' ,"|" ,"_" ,"^" ,"(" ,"'" ,"z" ,"m"])):
                pass
            else:
                song.append(c)


            if(c == "_"): #Flat
                flat = True
            elif(c == "^"):
                sharp = True

        nextLine = f.readline()

    return song

def isModifier(key): #passed in parameter is keycode
    key = key[0:len(key)-1]  #get rid of ',' at end of key
    key = int(key)
    #L/R,on/off Shift, Ctrl,   Alt,     Win, Esc, Caps
    if(key in [42, 54, 29, 97, 56, 100, 125, 0, 4, 1, 58]):
        return True
    else:
        return False


#Starts here
pygame.init()
pygame.mixer.init()

if len(sys.argv) > 1:
    song = arrayCreator(sys.argv[1])
else:
    song = arrayCreator("song.txt")

#Input from keyboard event. This is why this program needs root permissions
#dev = InputDevice("/dev/input/by-path/platform-i8042-serio-0-event-kbd")
dev = InputDevice("/dev/input/event0")

noteNum = 0
while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        #Next two lines take neccessary info from the event. To see more info from event, print event.
        code = str(event).split(" ")[4]
        keydown = str(event).split("val")[1] #Value 01 if KeyDown.
        if ((not isModifier(code)) and code != '00,' and keydown == " 01"):
            foo = "notes/" + song[noteNum] + ".aiff"
            s = pygame.mixer.Sound(foo)
            s.play() #Play note
            noteNum += 1
            if (noteNum >= len(song)): #If song has reached the end
                noteNum = 0; #repeat
