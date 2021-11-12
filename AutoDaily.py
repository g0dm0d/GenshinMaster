import datetime
from datetime import datetime, date, time, timezone
import time
import pytz
from pytz import UTC
import genshinstats as gs
import mysql
import mysql.connector
from mysql.connector import Error

SQLhost='localhost'
SQLuser='SA'
SQLpassword='password'
SQLdatabase='GenshinMaster'

timeserver=datetime.now(UTC) \
    .astimezone(pytz.timezone('Asia/Chongqing'))

print(f'Started: {timeserver.hour}:{timeserver.minute}:{timeserver.second}')

while True:
    if timeserver.hour == 0 and timeserver.minute == 0:
        print(f'{timeserver.hour}:{timeserver.minute}:{timeserver.second}')
        try:
            connection = mysql.connector.connect(
                host=SQLhost,
                user=SQLuser,
                password=SQLpassword,
                database=SQLdatabase
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM User WHERE daily='1'")
            rows = cursor.fetchall()
            for row in rows:
                ltuid = row[1]
                ltoken = row[2]
                gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
                reward = gs.claim_daily_reward()
                if reward is not None:
                    print(f"Claimed daily reward - {reward['cnt']}x {reward['name']}")
                else:
                    print("Could not claim daily reward")
            time.sleep(60)
        except Error as e:
            print(f"The error '{e}' occurred")
    time.sleep(1)