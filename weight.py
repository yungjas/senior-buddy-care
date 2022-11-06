# run this in makecode

radio.set_group(5)

def on_button_pressed_a():
    global change, calibrated_scale
    change = change - 0.1
    calibrated_scale = 985 / change
    HX711.set_scale(calibrated_scale * 120)
    HX711.tare(1)
    serial.write_string("recalibrated")
    basic.pause(2000)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global change, calibrated_scale
    change = 7.62
    calibrated_scale = 985 / change
    HX711.set_scale(calibrated_scale * 120)
    HX711.tare(1)
    serial.write_string("recalibrated")
    basic.pause(2000)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

# def on_received_string(receivedString):
#     global signal
#     signal = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
#     basic.show_number(signal)
#     signal = 95 + signal
#     radio.send_string("" + str(signal) + "dBM")
#     radio.send_string("" + str(weight) + "g")
#     serial.write_string("One Reading: ")
#     serial.write_line("" + str((weight)))
#     serial.write_string("Signal: ")
#     serial.write_line("" + str((int(signal))))
# radio.on_received_string(on_received_string)

def on_button_pressed_b():
    global change, calibrated_scale
    change = change + 0.1
    calibrated_scale = 985 / change
    HX711.set_scale(calibrated_scale * 120)
    HX711.tare(1)
    serial.write_string("recalibrated")
    basic.pause(2000)
input.on_button_pressed(Button.B, on_button_pressed_b)

valor_string = ""
ceros = ""
valor = 0
weight = 0
signal = 0
calibrated_scale = 0
change = 0
radio.set_group(10)
HX711.SetPIN_DOUT(DigitalPin.P0)
HX711.SetPIN_SCK(DigitalPin.P8)
HX711.begin()
serial.redirect(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BAUD_RATE115200)
serial.write_line("")
serial.write_line("HX711 Initializing Scale: ")
serial.write_line("Before Setting Up the Scale: ")
serial.write_string("Read: ")
serial.write_line("" + str(HX711.read()))
serial.write_string("Read Average: ")
serial.write_line("" + str(HX711.read_average(20)))
serial.write_string("Get Value: ")
serial.write_line("" + str(HX711.get_value(5)))
serial.write_string("Get Units: ")
serial.write_line("" + str(HX711.get_units(5)))
change = 7.62
calibrated_scale = 985 / change
HX711.set_scale(calibrated_scale * 120)
HX711.tare(1)
basic.pause(1000)
serial.write_string("Read:")
serial.write_line("" + str(HX711.read()))
serial.write_string("Read Average:")
serial.write_line("" + str(HX711.read_average(20)))
serial.write_string("Get Value:")
serial.write_line("" + str(HX711.get_value(5)))
serial.write_string("Get Units")
serial.write_line("" + str(HX711.get_units(5)))
serial.write_line("")
serial.write_line("")
serial.write_line("")
serial.write_line("")
serial.write_line("Readings: ")
basic.pause(1000)

def on_forever():
    global valor, ceros, valor_string, weight
    #serial.write_string("One Reading")
    valor = HX711.get_units(1)
    ceros = ""
    #ops = "" + str(abs(Math.round((valor - int(valor)) * 100)))
    if len(str(abs(Math.round((valor - int(valor)) * 100)))) == 0:
        ceros = "00"
    elif len(str(abs(Math.round((valor - int(valor)) * 100)))) == 1:
        ceros = "0"
    valor_string = "" + str(int(valor)) + "." + ceros + ("" + str(abs(Math.round((valor - int(valor)) * 100))))
    weight = int(valor)
    radio.send_string(str(weight) + "g")
    #serial.write_line(valor_string)
    serial.write_string(str(valor) + "g")
    if int(parse_float(valor_string)) > 0:
        basic.show_icon(IconNames.SQUARE)
    else:
        basic.show_icon(IconNames.SMALL_DIAMOND)
    valor = HX711.get_units(20)
    ceros = ""
    if len(str(abs(Math.round((valor - int(valor)) * 100)))) == 0:
        ceros = "00"
    elif len(str(abs(Math.round((valor - int(valor)) * 100)))) == 1:
        ceros = "0"
    valor_string = "" + str(int(valor)) + "." + ceros + ("" + str(abs(Math.round((valor - int(valor)) * 100))))
    HX711.power_down()
    basic.pause(2000)
    HX711.power_up()
    basic.pause(100)
basic.forever(on_forever)
