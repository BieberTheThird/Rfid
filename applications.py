
from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("rfid.db")
    conn.row_factory = sqlite3.Row
    return conn

def format_duration(seconds):
    hours, rem = divmod(int(seconds), 3600)
    mins, _ = divmod(rem, 60)
    if hours > 0:
        return f"{hours}h {mins}min"
    return f"{mins}min"

@app.route("/")
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT u.name, s.uid, s.timestamp
        FROM scans s
        JOIN users u ON u.uid = s.uid
        WHERE DATE(s.timestamp) = ?
        ORDER BY s.uid, s.timestamp ASC
    """, (today_date,))

    rows = cur.fetchall()
    db.close()

    user_logins = {}
    for row in rows:
        uid = row['uid']
        ts = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        if uid not in user_logins:
            user_logins[uid] = {"name": row['name'], "times": []}
        user_logins[uid]["times"].append(ts)

    table_data = []
    for uid, data in user_logins.items():
        times = data["times"]
        count = len(times)

        # Arbeitszeit & Pausenzeit Logik
        work_sec = 0
        break_sec = 0

        # Arbeitszeit: 1-2, 3-4, 5-6...
        for i in range(0, count - 1, 2):
            work_sec += (times[i + 1] - times[i]).total_seconds()

        # Pausenzeit: 2-3, 4-5, 6-7...
        for i in range(1, count - 1, 2):
            break_sec += (times[i + 1] - times[i]).total_seconds()

        is_present = (count % 2 != 0)

        table_data.append({
            "name": data["name"],
            "in": times[0].strftime("%H:%M"),
            "out": times[-1].strftime("%H:%M") if not is_present else "--:--",
            "work_time": format_duration(work_sec),
            "break_time": format_duration(break_sec),
            "status": "Anwesend" if is_present else "Abwesend",
            "class": "status-online" if is_present else "status-offline"
        })

    return render_template("index.html", table=table_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
