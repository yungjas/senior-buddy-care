import serial
import serial.tools.list_ports as list_ports
import os
import requests
import mysql.connector
# import datetime
# import time
from dotenv import load_dotenv
from datetime import date, datetime, time, timedelta

load_dotenv()

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
COM = "COM10"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# DB configs
conn = mysql.connector.connect(user="root", password="root", host="127.0.0.1", port="3316", database="senior_buddies")
cursor = conn.cursor()

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

def save_db(option, data):
    if option == "W":
        insert_query = """INSERT INTO weight (weight_data) VALUES (%s)"""
    data_db = (data,)
    cursor.execute(insert_query, data_db)
    conn.commit()

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

    send_tele_msg_complete = False
    send_tele_msg_initial = False

    while True:
        line = ser_micro.readline().decode('utf-8')
        current_time = datetime.now().time()
        set_time = time(hour = 22, minute = 50, second = 00)

        if "g" in line:
            weight = float(line.split("g")[0])
            
            if weight > 0:
                try:
                    save_db("W", weight)
                except Exception as e:
                    print(f"Error: {e}")
                
                if current_time > set_time and send_tele_msg_complete == False and send_tele_msg_initial == False:
                    print("Sending tele alert")
                    send_telegram_msg("Hi Alice, it's time to take your medication!")
                    send_tele_msg_initial = True

                #after 30 mins if user hasn't taken their meds yet
                if (send_tele_msg_initial == True) and (send_tele_msg_complete == False) and ((datetime.combine(date.today(), current_time) - datetime.combine(date.today(), set_time)) >= timedelta(minutes=1)):
                    print("Sending another tele alert")
                    send_telegram_msg("Hi Alice, it's been about a couple of minutes and you have not taken your medication yet, please remember to take them!")
                    send_tele_msg_complete = True
        
        else:
            continue
 
    ser_micro.close()

main()