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


# makecode
radio.set_group(5)

def on_forever():
    basic.show_string("Alice")
    x = str(input.acceleration(Dimension.X))
    y = str(input.acceleration(Dimension.Y))
    z = str(input.acceleration(Dimension.Z))
    acc = x + "," + y + "," + z
    #acc = str(, input.acceleration(Dimension.Y), input.acceleration(Dimension.Z)) + " A"
    #acc = str(), str(input.acceleration(Dimension.Y)), str(input.acceleration(Dimension.Z)) + " A"
    #basic.show_string(str(acc))
    radio.send_string(acc)
    
basic.forever(on_forever)
    
