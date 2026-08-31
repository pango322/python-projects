#sudo modprobe uinput
#sudo .venv/bin/python test.py
import time
import keyboard
from evdev import UInput, ecodes 

mouse = UInput({
    ecodes.EV_KEY: [ecodes.BTN_LEFT],
    ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y]
}, name="Python Virtual Mouse") #creates a virtual mouse that can be controlled by python

while True:
    if keyboard.is_pressed("x"):
        mouse.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
        mouse.syn()

        mouse.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
        mouse.syn()

        time.sleep(0.005) #5 milliseconds
    else:
        time.sleep(0.01)