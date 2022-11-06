import serial
import serial.tools.list_ports as list_ports
import time
import math
import requests
import os
import mysql.connector
import datetime
from dotenv import load_dotenv
from ast import literal_eval as make_tuple

load_dotenv()

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1
COM = "COM8"

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

def get_tilt(ax,ay,az):
    yaw = math.atan(ay / (math.sqrt(ax**2 + az**2)))
    yaw = yaw * 180 / math.pi
    if( yaw < 0 ):
        yaw += 360;
    if 60 <= yaw <= 90:
        return "upright"
    elif 45 <= yaw < 60:
        return "tilted"
    else:
        return "lying down"

def send_telegram_msg(s):
    global BOT_TOKEN
    global CHAT_ID
    print(BOT_TOKEN)
    print(CHAT_ID)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={s}"
    requests.get(url = url)

def save_db(option, data):
    if option == "A":
        acc = data[0]
        tilt = data[1]
        insert_query = """INSERT INTO acceleration (acc, tilt) VALUES (%s, %s)"""
        data_db = (acc, tilt)
    # elif option == "W":
    #     insert_query = """INSERT INTO weight (weight_data) VALUES (%s)"""
    
    #data_db = (data)
    cursor.execute(insert_query, data_db)
    conn.commit()


def most_frequent(List):
    return max(set(List), key = List.count)    

def main():
    global a
    global x
    global y
    global z
    global ma20
    global ma250
    global diffma
    global avgA
    global last_fall
    global timestamp
    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200, COM)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    fall_tilt = []
    tilts = []
    activites = []
    while True:
        line = ser_micro.readline().decode('utf-8')
        if len(line) == 0:
            continue
        if "C" in line:
            break
        if "B" in line:
            break
        if "A" in line:
            #print(f"line:{line}")
            line = line.split(" A")[0]
            if time.time() - timestamp > 5:
                    timestamp = time.time()
                    # =================================INSERT ACCELERATOR DATA HERE=================================
                    if tilts:
                        acc_data = (sum(avgA)/len(avgA), most_frequent(tilts))
                    else:
                        continue
                    save_db("A", acc_data) 
                    print("clearin")
                    x = x[-300:]
                    y = y[-300:]
                    z = z[-300:]
                    a = a[-300:]
                    ma20 = ma20[-300:]
                    ma250 = ma250[-300:]
                    diffma = diffma[-300:]
                    avgA = avgA[-300:]

            try:
                #acc = line.split(",")
                #print(f"acc: {acc}")
                acc = make_tuple(line)
                ax = int(acc[0])
                ay = int(acc[1])
                az = int(acc[2])
                total_acc = math.sqrt(ax**2 + ay**2 + az**2)
                a.append(total_acc)
                if len(a) >= 20:
                    d20 = sum(a[len(a)-20:])/20
                    ma20.append(d20)
                
                if len(a) >= 250:
                    d250 = sum(a[len(a)-250:])/250
                    ma250.append(d250)
                    d2f250 = abs(d250-d20)
                    diffma.append(d2f250)
                    avgA.append(sum(diffma[len(diffma)-20:])/20)
                    
                if len(a) >= 300:

                    averageOf30diff = sum(diffma[len(diffma)-300:])/300
                    if averageOf30diff > 150:  
                        #======================== FALLING ======================================================
                        fall_tilt.append(get_tilt(ax,ay,az))
                    else:
                        if len(fall_tilt) > 0: 
                            #====================================FALL ENDED==========================================
                            #trigger alert
                            if last_fall == 0 or time.time() - last_fall > 59:
                                last_fall = time.time()
                                print("ALERT")
                                send_telegram_msg(f"Fall detected at Alice's house. \nPlease send help immediately.")
                            
                            #use fall_tilt[-1] to retrieve last tilt position
                            acc_data = (averageOf30diff, fall_tilt[-1])
                            save_db("A", acc_data) 
                            fall_tilt.clear()
                        if averageOf30diff > 20:
                            continue
                            # activites.append("Walking")
                        else:
                            continue
                            # activites.append("Resting")
                    tilts.append(get_tilt(ax,ay,az))
            except Exception as e: 
                print(e)
        
        # add checks for weight and proximity here
        # if 
        if "g" in line:
            print(f"weight:{line}")

    ser_micro.close()

x = []
y = []
z = []
a = []
ma20 = [1000 for i in range(19)]
ma250 = [1000 for i in range(249)]
diffma = [0 for i in range(249)]
avgA = [0 for i in range(249)]
last_fall = 0
timestamp = time.time()
main()