import sqlite3
filename = "/home/pi/coffee/scripts/coffee.db"

name = ""
firstname = ""
email=""
while not name:
    name = input("Name: ")
while not firstname:
    firstname = input("First Name: ")
while not email:
    email = input("Email: ")
    if not "@" in email:
        email=""

conn = sqlite3.connect(filename)
conn.execute("UPDATE COFFEE SET EMAIL='%s' WHERE NAME='%s' AND FIRSTNAME='%s'"%(email,name, firstname))
conn.commit()
conn.close()
