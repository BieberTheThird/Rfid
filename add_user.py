import sqlite3

uid = input("Enter card UID: ")
print(uid)
name = input("Enter name: ")
print(name)
db = sqlite3.connect("rfid.db")
cur = db.cursor()

cur.execute(
    "INSERT OR REPLACE INTO users (uid, name) VALUES (?, ?)",
    (uid, name)
)

db.commit()
db.close()

print("User added")
