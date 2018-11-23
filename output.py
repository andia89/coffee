import sqlite3
import datetime

filename = "/home/pi/coffee/scripts/coffee.db"


conn = sqlite3.connect(filename)
names = conn.execute("SELECT NAME FROM COFFEE WHERE ID != 0").fetchall()

sald = []
for name in names:
    total = conn.execute("SELECT SUM(MONEY) FROM INPUT").fetchone()
    inp = conn.execute("SELECT SUM(MONEY) FROM INPUT WHERE INPUT.COFFEEID=(SELECT COFFEEID FROM COFFEE WHERE NAME='%s')"%(name[0])).fetchone()[0]
    counts = conn.execute("SELECT COUNT(*) FROM TICKS WHERE TICKS.COFFEEID=(SELECT COFFEEID FROM COFFEE WHERE NAME='%s')"%(name)).fetchone()[0]
    email = conn.execute("SELECT EMAIL FROM COFFEE WHERE NAME='%s'"%(name)).fetchone()[0]
    if inp and int(inp/0.3)-counts < 0:
        sald.append((name[0], int(inp/0.3)-counts, email, round(0.3*(inp/0.3-counts),2)))
sald.sort(key=lambda x: x[1])
conn.close()

print("Total saldo:")
print("%.2f"%total)
print("")
for i in sald:
    print(i)
    
