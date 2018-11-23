import sys
import datetime
import sqlite3

filename = "/home/pi/coffee/scripts/coffee.db"

try:
    addcount = int(sys.argv[1])
except:
    print("give valid input")
    sys.exit(1)

date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d %X")


conn = sqlite3.connect(filename)
offset_date, offset_count = conn.execute("SELECT * FROM COUNTER").fetchone()
counts = conn.execute("SELECT COUNT(*) FROM TICKS WHERE '%s' < DAT AND '%s' > DAT" % (offset_date, date)).fetchone()[0]
conn.execute("UPDATE COUNTER SET DAT='%s', COUNT=%i"%(date, int(offset_count-counts+addcount)))
conn.commit()
conn.close()


