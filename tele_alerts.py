import flask
import serial
import serial.tools.list_ports as list_ports
import requests
import time
import os
import sys
import subprocess
import re

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
BAUDRATE = 115200

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = flask.Flask(__name__)
app.debug = True

# Handles the case when the serial port can't be found
def handle_missing_serial_port() -> None:
    print("Couldn't connect to the micro:bit. Try these steps:")
    print("1. Unplug your micro:bit")
    print("2. Close Tera Term, PuTTY, and all other apps using the micro:bit")
    print("3. Close all MakeCode browser tabs using the micro:bit")
    print("4. Plug the micro:bit in")
    print("5. Run this app again")
    exit()


def find_comport(pid, vid, baud):
    if "win32" in sys.platform.lower():
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
                return ser_port.port
    
    elif "microsoft" in os.uname().release.lower():
        # List the serial devices available
        try:
            stdout = subprocess.check_output("/mnt/c/windows/system32/WindowsPowerShell/v1.0/powershell.exe -Command '[System.IO.Ports.SerialPort]::getportnames()'", shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError as e:
            print(f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        stdout = stdout.splitlines()[-1]
        ser_port = re.search("COM([0-9]*)", stdout)
        if ser_port:
            ser_port = f"/dev/ttyS{ser_port.group(1)}"
            return ser_port
    
    elif "linux" in sys.platform.lower():
        # List the serial devices available
        try:
            stdout = subprocess.check_output("ls /dev/ttyACM*", stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError as e:
            print(f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        ser_port = re.search("(/dev/ttyACM[0-9]*)", stdout)
        if ser_port:
            ser_port = ser_port.group(1)
            return ser_port
    
    elif "darwin" in sys.platform:

        # List the serial devices available
        try:
            stdout = subprocess.check_output("ls /dev/cu.usbmodem*", stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError:
            print(f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        ser_port = re.search("(/dev/cu.usbmodem[0-9]*)", stdout)
        if ser_port:
            ser_port = ser_port.group(1)
            return ser_port
    
    else:
        print(f"Unknown platform: {sys.platform}")
        exit()


def handle_incoming_serial_data(s):
    #s = "hello" # for testing purpose
    print(f"{s.readline().decode('utf-8').strip()}")
    s = s.readline().decode('utf-8').strip()
    print(f"text s: {s}")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={s}"
    requests.get(url = url)


def tele_alert():
    serial_port = find_comport(PID_MICROBIT, VID_MICROBIT, BAUDRATE)
    
    with serial.Serial(port=serial_port, baudrate=BAUDRATE, timeout=10) as s:
        # Sleep a while to make sure serial port is open before doing anything else
        time.sleep(1) 

        # Reset the input and output buffers in case there is leftover data
        s.reset_input_buffer()
        s.reset_output_buffer()

        while True:
            # Commenting this out for now to test telebot alerts
            # Get the number of characters ready to be read
            if s.in_waiting > 0:
                handle_incoming_serial_data(s)
            
            # for testing
            #handle_incoming_serial_data(s)


@app.route("/tele_alert")
def tele():
    try:
        flask.Response(tele_alert(), mimetype="text/event-stream")
    except Exception as e:
        return flask.jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(port=8080, debug=True)
