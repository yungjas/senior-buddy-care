import serial
import serial.tools.list_ports as list_ports
import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
COM = "COM10"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def find_comport(pid, vid, baud, com):
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
        if (p.pid == pid) and (p.vid == vid) and (p.name == com):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None

def send_telegram_msg(s):
    global BOT_TOKEN
    global CHAT_ID
    print(BOT_TOKEN)
    print(CHAT_ID)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={s}"
    requests.get(url = url)

def main():
    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200, COM)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    
    while True:
        line = ser_micro.readline().decode('utf-8')
        current_time = datetime.datetime.now().time()

        if "g" in line:
            if current_time:
                send_telegram_msg(line)
    
    ser_micro.close()

main()