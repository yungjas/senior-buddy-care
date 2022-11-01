# Imports go at the top
from microbit import *
import radio

radio.on()
radio.config(group=5)

# Code in a 'while True:' loop repeats forever
while True:
    if button_a.is_pressed():
        radio.send("B")
    if button_b.was_pressed():
        radio.send("C")
    display.show("A")
    radio.send(str(accelerometer.get_values()) + " A")
