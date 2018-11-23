import sqlite3
import shutil
import os

filename = "/home/pi/coffee/scripts/coffee.db"
filename2 = "/home/pi/coffee/scripts/temp.db"

shutil.copy2(filename, filename2)

try:
    conn = sqlite3.Connection(filename2)
    conn.execute("VACUUM")
    temp = conn.execute("SELECT COUNT(*) AS COUNT FROM TICKS WHERE DAT >= datetime('now', '-1 year')").fetchall()
    if len(temp) == 0:
        raise ValueError('This is bad. database is empty')
    shutil.copy2(filename2, filename)
    print("Everything fine")
except ValueError:
    print("ValueError - database is empty")
except sqlite3.OperationalError:
    print("sqlite error - database is corrupted")
finally:
    os.remove(filename2)
    conn.close()
    
    
