#systemctl --user enable --now ydotool.service
import time
import keyboard
import subprocess

while True:
    if keyboard.is_pressed("x"):
        subprocess.run(["ydotool", "click", "0xC0"])
        time.sleep(0.03)
    else:
        time.sleep(0.01)