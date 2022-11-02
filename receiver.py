# new code (run in micropython editor)
# Imports go at the top
from microbit import *
import radio

radio.on()
radio.config(group=5)

# Code in a 'while True:' loop repeats forever
while True:
    data = radio.receive()
    print(data)