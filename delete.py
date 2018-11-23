import sqlite3

filename = "/home/pi/coffee/scripts/coffee.db"
conn = sqlite3.connect(filename)
name = ""
while not name:
    name = input("Name: ")

idname = []
while not idname:
    idname = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s'"%(name)).fetchall()
    if not idname:
        print("This name does not exist in the database, please check!")
        name = ""
        while not name:
            name = input("Name: ")

while len(idname) > 1:
    print("Last name is ambigous, please give first name")
    firstname = input("Firstname: ")
    while not firstname:
        firstname = input("Firstname: ")
    idname = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s' AND FIRSTNAME='%s'"%(name, firstname)).fetchall()
    while not idname:
        print("This name / firstname combination does not exist in the database, please check!")
        firstname = ""
        while not firstname:
            firstname = input("Firstname: ")
        idname = conn.execute("SELECT COFFEEID FROM COFFEE WHERE NAME='%s' AND FIRSTNAME='%s'"%(name, firstname)).fetchall()

#print(idname[0][0])

conn.execute("UPDATE COFFEE SET ACTIVE=0 WHERE COFFEEID=%i"%(idname[0][0]))
conn.execute("UPDATE COFFEE SET ID=-1 WHERE COFFEEID=%i"%(idname[0][0]))
conn.commit()
conn.close()
