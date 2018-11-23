import sqlite3

filename = "/home/pi/coffee/scripts/coffee.db"

name = ""
firstname = ""
email=""
experi=""
ident = None
coffeeid = None
while not name:
    name = input("Name: ")
while not firstname:
    firstname = input("First Name: ")
while not email:
    email = input("Email: ")
    if not "@" in email:
        email=""

while not experi:
    experi = input("Experiment: ")
    
while not ident:
    ident = input("ID: ")
    try:
        ident = int(ident)
    except:
        ident = None

conn = sqlite3.connect(filename)

largest_id_input = conn.execute("SELECT MAX(COFFEEID) FROM INPUT").fetchone()[0]
largest_id_coffee = conn.execute("SELECT MAX(COFFEEID) FROM COFFEE").fetchone()[0]

maxid = max(largest_id_input, largest_id_coffee)

conn.execute("INSERT INTO COFFEE (ID, NAME, FIRSTNAME, EMAIL, EXPERIMENT, COFFEEID, ACTIVE) VALUES (%i, '%s', '%s', '%s', '%s', %i, 1)"%(ident, name, firstname, email, experi, maxid+1))
conn.commit()
conn.close()
