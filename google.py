#!/usr/bin/python

import datetime 
import sqlite3

filename = "/home/pi/coffee/scripts/coffee.db"
amount = 18
numberpeople = 6

price = amount/numberpeople

members = ["Pigneur","Astner", "Sabino", "Kanagin", "Leveque"] 

conn = sqlite3.connect(filename)
date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d")
myid = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='Angerer'").fetchall()
conn.execute("INSERT INTO INPUT (MONEY, DAT, COMMENT, COFFEEID) VALUES (%f, '%s', '%s', %i)"%(amount-price, date, "Google", myid[0][0]))
for name in members:
    idname = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s'"%(name)).fetchall()   
    conn.execute("INSERT INTO INPUT (MONEY, DAT, COMMENT, COFFEEID) VALUES (%f, '%s', '%s', %i)"%(-price, date, "Google", idname[0][0]))
   
conn.commit()
conn.close()
