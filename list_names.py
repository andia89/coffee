import sqlite3
import datetime

filename = "/home/pi/coffee/scripts/coffee.db"


conn = sqlite3.connect(filename)
vals = conn.execute("SELECT COFFEEID, NAME FROM COFFEE WHERE ID != 0 AND ACTIVE=1").fetchall()

sald = []
for val in vals:
    name = val[1]
    ids = val[0]
    inp = conn.execute("SELECT SUM(MONEY) FROM INPUT WHERE COFFEEID=%i"%(ids)).fetchone()[0]
    #counts = conn.execute("SELECT COUNT(*) FROM TICKS WHERE NAME='%s'"%(name)).fetchone()[0]
    fname = conn.execute("SELECT FIRSTNAME FROM COFFEE WHERE COFFEEID=%i"%(ids)).fetchone()[0]
    email = conn.execute("SELECT EMAIL FROM COFFEE WHERE COFFEEID=%i"%(ids)).fetchone()[0]
    ide = conn.execute("SELECT ID FROM COFFEE WHERE COFFEEID=%i"%(ids)).fetchone()[0]
    coffeeid = conn.execute("SELECT COFFEEID FROM COFFEE WHERE COFFEEID=%i"%(ids)).fetchone()[0]
    sald.append((name, fname, email,ide, coffeeid))
sald.sort(key=lambda x: x[0])
conn.close()

for i in sald:
    print(i)
    
