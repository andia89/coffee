import sqlite3
import shutil
import os

filename = "/home/pi/coffee/scripts/training.db"

conn = sqlite3.Connection(filename)
conn.execute("DELETE FROM STOLEN")
conn.execute("VACUUM")
conn.commit()
conn.close()
