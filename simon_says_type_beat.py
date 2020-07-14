#This is a simon says bot that records the machine blinking from any angle  and prints out the new pattern automatically.
#I wanted to fully automate this and call a method that would move the mouse to enter the pattern but DirectX blocks mouse input,
# and I'm really not about to put hooks in DirectX to move a mouse, when I could just tell it I got the high score with hooks, so, here's the dumb baby
# version of something that was supposed to be really cool. Might rewrite for a flash game later. We'll see.

#IMPORTS
import numpy as np
from PIL import ImageGrab
from cv2 import cv2
import time
counter=1
BlinkLook=1
BlinkIgnore=2
blinkarray = []


#GLOBAL VARIABLES
frame_counter=10
detecting = False

def good_blink_recorder(img):
    global detecting
    global BlinkLook
    global BlinkIgnore
    global blinkarray
    global counter
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #blue_blink
    BL_range = np.array([77,230,230])
    BU_range = np.array([128,255,255])
    #yellow_blink
    YL_range = np.array([235,235,102])
    YU_range = np.array([255,255,128])
    #red_blink
    RL_range = np.array([235,102,102])
    RU_range = np.array([[255,128,128]])
    #green
    GL_range = np.array([235,235,235])
    GU_range = np.array([255,255,255])

    Ymask = cv2.inRange(hsv, YL_range, YU_range)
    Rmask = cv2.inRange(hsv, RL_range, RU_range)
    Bmask = cv2.inRange(hsv, BL_range, BU_range)
    Gmask = cv2.inRange(hsv, GL_range, GU_range)
    BGmask = Bmask + Gmask
    #green. Note that green uses Blues mask and simply checks to see the size of the rectangle, counting as green if it's small enough. 
    #This is because Blue and Greens blink looks identicaly when seen through RGB, but the bounding rectangle size is so different size became the determining factor.
    cnts = cv2.findContours(Bmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w>200 and 70>h>0 and detecting:
            return None
        if w>200 and 70>h>0 and not detecting:
            detecting = True
            if BlinkLook <= 0 and BlinkIgnore > 0:
                BlinkIgnore -= 1
                if BlinkIgnore == 0:
                    counter += 1
                    BlinkLook = 1
                    BlinkIgnore = counter*2
            elif BlinkLook>0:
                blinkarray.append("G")
                BlinkLook -= 1
            return None
    #blue
    cnts = cv2.findContours(Bmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w > 100 and h>80 and detecting:
            return None
        if w > 100 and h>80 and not detecting:
            detecting = True
            if BlinkLook <= 0 and BlinkIgnore > 0:
                BlinkIgnore -= 1
                if BlinkIgnore == 0:
                    counter += 1
                    BlinkLook = 1
                    BlinkIgnore = counter*2
            elif BlinkLook>0:
                blinkarray.append("B")
                BlinkLook -= 1
            return None
    #red
    cnts = cv2.findContours(Rmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w > 100 and h>80 and detecting:
            return None
        if w > 100 and h>80 and not detecting:
            detecting = True
            if BlinkLook <= 0 and BlinkIgnore > 0:
                BlinkIgnore -= 1
                if BlinkIgnore == 0:
                    counter += 1
                    BlinkLook = 1
                    BlinkIgnore = counter*2
            elif BlinkLook>0:
                blinkarray.append("R")
                BlinkLook -= 1
            return None

    #yellow
    cnts = cv2.findContours(Ymask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w > 100 and h>80 and detecting:
            return None
        if w > 100 and h>80 and not detecting:
            detecting = True
            if BlinkLook <= 0 and BlinkIgnore > 0:
                BlinkIgnore -= 1
                if BlinkIgnore == 0:
                    counter += 1
                    BlinkLook = 1
                    BlinkIgnore = counter*2
            elif BlinkLook>0:
                blinkarray.append("Y")
                BlinkLook -= 1
            return None
    if detecting:
        detecting = False
    return None

def consec(lst):
    it = iter(lst)
    prev = next(it)
    tmp = [prev]
    for ele in it:
        if prev != ele:
            yield tmp
            tmp = [ele]
        else:
            tmp.append(ele)
        prev = ele
    yield tmp

while(True):
    screen = np.array(ImageGrab.grab(bbox=(0,40, 1279, 1040)))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    good_blink_recorder(screen)
    if frame_counter>0:
        frame_counter -=1
    else:
        print("XXX", end= " ")
        for x in blinkarray:
            print(x,end="-")
        print("XXX\n\n")
        frame_counter = 10
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
