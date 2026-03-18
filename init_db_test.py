import sqlite3

def init_db():
    db = sqlite3.connect("rfid.db")
    cur = db.cursor()

    #Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        uid TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    #Scans Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uid) REFERENCES users (uid)
    )
    """)

    db.commit()
    db.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
