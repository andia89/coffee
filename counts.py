import sqlite3
import datetime

filename = "/home/pi/coffee/scripts/coffee.db"

startdate = input("Startdate (Format %yyyy-%mm-%dd %hh:%mm:%ss ")
if not startdate:
    startdate = input("Startdate (Format %yyyy-%mm-%dd %hh:%mm:%ss ")

print(startdate)
enddate = input("Enddate (Format %yyyy-%mm-%dd %hh:%mm:%ss) Hit enter for today ")
if not enddate:
    enddate = datetime.datetime.now()
    enddate = enddate.strftime("%Y-%m-%d %X")
print(enddate)

conn = sqlite3.connect(filename)
counts = conn.execute("SELECT COUNT(*) FROM TICKS WHERE '%s' < DAT AND '%s' > DAT"%(startdate, enddate)).fetchone()[0]
conn.close()

print("\n")
print("Registered ticks: %s" %(counts))
