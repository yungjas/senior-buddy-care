import flask
import serial
import serial.tools.list_ports as list_ports
import requests
import time
import os

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
BAUDRATE = 115200

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = flask.Flask(__name__)
app.debug = True


def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None


def incoming_message(s):
    # print(f"{s.readline().decode('utf-8').strip()}")
    # s = s.readline().decode('utf-8').strip()
    # print(f"text s: {s}")
    s = "hello" # for testing purpose
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={s}"
    requests.get(url = url)


def tele_alert():
    serial_port = find_comport(PID_MICROBIT, VID_MICROBIT, BAUDRATE)
    
    with serial.Serial(port=serial_port.port, baudrate=BAUDRATE, timeout=10) as s:
        # Sleep a while to make sure serial port is open before doing anything else
        time.sleep(1) 

        # Reset the input and output buffers in case there is leftover data
        s.reset_input_buffer()
        s.reset_output_buffer()

        while True:
            # Commenting this out for now to test telebot alerts
            # Get the number of characters ready to be read
            # if s.in_waiting > 0:
            #     incoming_message(s)
            incoming_message(s)


@app.route("/tele_alert")
def tele():
    flask.Response(tele_alert(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(port=8080, debug=True)
