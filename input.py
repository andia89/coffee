"""Module for parsing and testing package version predicate strings.
"""
import sqlite3
import sys
import datetime

filename = "/home/pi/coffee/scripts/coffee.db"
name = ""
firstname = ""
idi = []
money = None
date = ""
comment = ""
name2 = ""

while not name:
    name = input("Name: ")

conn = sqlite3.connect(filename)

while not len(idi):
    idi = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s'"%(name)).fetchall()
    if len(idi):
        break
    print("Name does not exist in database")
    while not name2:
        name2 = input("Name: ")
    name = str(name2)
    name2 = ""

if len(idi)>1:
    print("Name exists more than once. Try also the first name")
    idi = []

    while not firstname:
        firstname = input("First Name: ")

    while not len(idi):
        idi = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s' AND FIRSTNAME='%s'"%(name, firstname)).fetchall()
        print("First Name does not exist in database")
        while not firstname:
            firstname = input("First Name: ")

    if len(idi)>1:
        print("There are still more than one possibilities here. Try to run the script again")
        sys.exit()

while not money:
    money = input("Money: ")
    try:
        money = float(money)
    except:
        print("Put a valid number")
        money = None

while not date:
    date = input("Date (hit enter for now) -- format: %Y-%m-%d %H:%M:%S: ")
    if not date:
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except:
            print("Wrong format")
            date = None

while not comment:
    comment = input("Comment (hit enter for none): ")
    if not comment: 
        break
    else:
        comment = str(comment)

conn.execute("INSERT INTO INPUT (MONEY, DAT, COMMENT, COFFEEID) VALUES (%f, '%s', '%s', %i)"%(money, date, comment, int(idi[0][0])))

conn.commit()
conn.close()
