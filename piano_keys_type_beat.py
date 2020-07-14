"""
OVERVIEW:
This is a bot that currently holds the WR for a piano keys clone in a steam game that will remain unnamed for now.
It is a full %12 faster than the next closest bot that has been created by other players thus far.


If you plan on using this yourself, or rewriting it for use in a different pianokeys type game: 
1. measure out the area of your screen the game will appear and update np.array(ImageGrab.grab(bbox=(0,40, 1279, 1040))) accordingly.
2. use pydirectinput.position() to get and update the pixel locations
3. change x[0][2] > 240 to dectect whatever color change you need. 
    for Q_key= img[615][572], Q_key[0] will give the RGB value from the pixel provided. I only needed blue so I used x[0][2].
4. change QWOP to whatever the game uses, maybe even pydirectinput.moveTo(x,y) or pydirectinput.click() if need be.
5. run the program, use 't' to start it and '`' if you run into any problems or the program is done.

NOTES:
#Taking a screen shot of half the screen to fetch 4 pixels is shamefully inefficient, bounding box values behave oddly and I haven't fixed that yet, because it got the job done.
#Using wait_time = float(decimal.Decimal(random.randrange(80, 120))/1000) every frame is also weird, and using choose() would probably ease the burden of the CPU

"""

#IMPORTS
import numpy as np
from PIL import ImageGrab
from cv2 import cv2
from pynput.keyboard import Key, Controller
import time
import random
import pydirectinput
import decimal
from keyboard import wait, add_hotkey

#GLOBAL VARIABLES
keyboard = Controller()
detecting = False
kill_switch = False

def key_checker(img):
    global detecting
    #please note the format img uses is [Y][X], and pydirectinput.position returns [X][Y]
    Q_key= img[615][572]
    W_key= img[615][618]
    O_key= img[615][680]
    P_key= img[615][740]
    key_array=[[Q_key,'q'],[W_key,'w'],[O_key,'o'],[P_key,'p']]
    if not detecting and not Q_key[2] > 240 and not W_key[2]  > 240 and not O_key[2] > 240 and not P_key[2] > 240: #If I dont see any matches currently and I'm on wait from my last key press
        detecting = True
    for x in key_array: #check every pixel
        if x[0][2] > 240 and not detecting: #If I can hit a key, and the key I just hit has gone past...
            wait_time = float(decimal.Decimal(random.randrange(80, 120))/1000)
            detecting = True
            keyboard.press(x[1])
            time.sleep(wait_time)
            keyboard.release(x[1])
            return None
    if detecting: #if nothing else is true, I am ready to proceed
        detecting = False
    return None

def play2(input):
    global  kill_switch
    if input == '`': #wait for killswitch trigger
        kill_switch = True

wait('t') #Don't enter while loop until start ('t') is called
add_hotkey('`', play2, args=['`'])

while(True):
    if kill_switch == True: #When killswitch is called, end program.
        exit()
    screen = np.array(ImageGrab.grab(bbox=(0,40, 1279, 1040)))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    key_checker(screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
