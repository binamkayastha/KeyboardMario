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

Mario = arrayCreator("song.txt")

for element in Mario:
    print(element)

#Mario=['E4','E4','E4','C4','E4','G4', 'C5', 'G4', 'E4', 'A4', 'B4', 'Bb4', 'A4', 'G4', 'C5', 'E5', 'A5', 'F5', 'G4', 'E5', 'E5', 'F5', 'D5', 'C5', 'G4', 'E4', 'A4', 'B4', 'Bb4', 'A4', 'G4', 'E4', 'D4', 'C4', 'C4', 'C4','C4','C4','C4','C4', 'D4', 'E4', 'C4', 'A3', 'G3', 'C4','C4','C4','C4', 'D4', 'E4', 'C4','C4','C4','C4', 'D4', 'E4', 'C4', 'A3', 'G3', 'E4', 'E4', 'E4', 'C4', 'E4', 'G4' ]

dev = InputDevice("/dev/input/by-path/platform-i8042-serio-0-event-kbd")
count = 0
noteNum = 0
while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        code = str(event).split(" ")[4]
        current = str(event).split("val")[1]
        count += 1
        if (code != '00,' and current == " 01"):
            print(current)
            foo = "notes/" + Mario[noteNum] + ".aiff"
            print(Mario[noteNum])
            s = pygame.mixer.Sound(foo)
            s.play()
            noteNum += 1
            if (noteNum >= len(Mario)):
                noteNum = 0; #repeat
        if (count == 6):
            count = 0
