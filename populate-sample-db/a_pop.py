from datetime import datetime, timedelta
import mysql.connector
import random

# DB configs
conn = mysql.connector.connect(user="root", password="root", host="127.0.0.1", port="3316", database="senior_buddies")
cursor = conn.cursor()


def save_db(option, data):
    if option == "A":
        acc = data[0]
        tilt = data[1]
        insert_query = """INSERT INTO acceleration (acc, tilt, time_created) VALUES (%s, %s, %s)"""
        data_db = (acc, tilt)
    elif option == "W":
        insert_query = """INSERT INTO weight (weight_data, time_created) VALUES (%s, %s)"""

    cursor.execute(insert_query, data)
    conn.commit()

start = datetime.strptime('Oct 20 2022  1:33PM', '%b %d %Y %I:%M%p')

for i in range(60):
    o = random.choice(["tilted", "lying down", "upright"])
    if o == "lying down":
        for _ in range(20):
            save_db("A", (random.randint(1,9), o, start))
            start = start + timedelta(minutes=10)
    elif o == "tilted":
        if random.randint(0,1) == 0:
            for _ in range(5):
                save_db("A", (random.randint(50,150), o, start))
                start = start + timedelta(minutes=10)
        else:
            for _ in range(10):
                save_db("A", (random.randint(1,9), o, start))
                start = start + timedelta(minutes=10)
    else:
        save_db("A", (random.randint(280,300), o, start))
        start = start + timedelta(minutes=10)