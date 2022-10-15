# run this in makecode

radio.set_group(6)

def on_received_string(receivedString):
    serial.write_line(receivedString)
radio.on_received_string(on_received_string)

# test function
def on_button_pressed_a():
    #radio.send_string("hello")
    serial.write_line("hello")
input.on_button_pressed(Button.A, on_button_pressed_a)