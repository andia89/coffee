import sqlite3
import datetime

filename = "/home/pi/coffee/scripts/coffee.db"


conn = sqlite3.connect(filename)
names = conn.execute("SELECT NAME FROM COFFEE WHERE ID > 0 AND ACTIVE=1 AND COFFEEID > 0").fetchall()

last_act = []
for name in names:
    ticks = conn.execute("SELECT DAT FROM TICKS WHERE TICKS.COFFEEID=(SELECT COFFEEID FROM COFFEE WHERE NAME='%s')"%name).fetchall()[-1][0]
    email = conn.execute("SELECT EMAIL FROM COFFEE WHERE NAME='%s'"%(name)).fetchone()[0]
    last_act.append((name[0], ticks, email))
last_act.sort(key=lambda x: x[1])
conn.close()

for i in last_act:
    print(i)
    
