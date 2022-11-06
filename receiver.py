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

# makecode
radio.set_group(5)

def on_received_string(receivedString):
    serial.write_string(receivedString)
    #basic.show_string(receivedString)

def on_forever():
    radio.on_received_string(on_received_string)
basic.forever(on_forever)