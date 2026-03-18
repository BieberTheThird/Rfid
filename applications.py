from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("rfid.db")
    # This row_factory allows us to access columns by name like row['name']
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    db = get_db()
    cur = db.cursor()

    # Check and Reset logic
    cur.execute("SELECT MAX(DATE(timestamp)) FROM scans")
    result = cur.fetchone()
    last_entry_date = result[0] if result and result[0] else None

    if last_entry_date and last_entry_date < today_date:
        cur.execute("DELETE FROM scans")
        db.commit()
        print(f"New day ({today_date}) detected. Database cleared.")

    # Fetch data
    cur.execute("""
        SELECT u.name, s.uid, s.timestamp
        FROM scans s
        JOIN users u ON u.uid = s.uid
        ORDER BY s.uid, s.timestamp ASC
    """)
    rows = cur.fetchall()
    db.close()

    # Process data
    users = {}
    for row in rows:
        uid = row['uid']
        ts = datetime.fromisoformat(row['timestamp'])

        if uid not in users:
            users[uid] = {"name": row['name'], "times": []}
        users[uid]["times"].append(ts)

    table = []
    for uid, user in users.items():
        times = user["times"]
        anzahl_scans = len(times)


        break_is = "On Break" if anzahl_scans % 2 == 1 else "Working"

        # Time Maths
        total_seconds = 0
        for i in range(0, anzahl_scans - 1, 2):
            total_seconds += (times[i + 1] - times[i]).total_seconds()

        total_minutes = int(total_seconds // 60)
        hours, mins = divmod(total_minutes, 60)

        duration = f"{hours}h {mins}min" if hours > 0 else f"{mins}min"

        table.append({
            "name": user["name"],
            "break_time": duration,
            "status": break_is
        })

    return render_template("index.html", table=table)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
