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
        insert_query = """INSERT INTO acceleration (acc, tilt) VALUES (%s, %s)"""
        data_db = (acc, tilt)
    elif option == "W":
        insert_query = """INSERT INTO weight (weight_data, time_created) VALUES (%s, %s)"""

    cursor.execute(insert_query, data)
    conn.commit()

start = datetime.strptime('Oct 20 2022  1:33PM', '%b %d %Y %I:%M%p')

for i in range(600):
    c = i % 280
    x = 100
    if 50 < c < 80:
        x = 0
    save_db("W", (x, start))
    start = start + timedelta(minutes=5)