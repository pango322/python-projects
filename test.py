import pyautogui
import keyboard
import time

while True:
    if keyboard.is_pressed("x"):
        pyautogui.click()
        time.sleep(0.03)
    else:
        time.sleep(0.01)