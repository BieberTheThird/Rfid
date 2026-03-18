from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("rfid.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    db = get_db()
    cur = db.cursor()

    # Nur heutige Scans laden
    cur.execute("""
        SELECT u.name, s.uid, s.timestamp 
        FROM scans s 
        JOIN users u ON u.uid = s.uid 
        WHERE DATE(s.timestamp) = ?
        ORDER BY s.uid, s.timestamp ASC
    """, (today_date,))
    
    rows = cur.fetchall()
    db.close()

    # Daten nach User gruppieren
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
        
        # Status Logik
        is_present = (count % 2 != 0)
        status = "Anwesend" if is_present else "Abwesend"
        
        first_in = times[0].strftime("%H:%M")
        last_out = times[-1].strftime("%H:%M") if not is_present else "--:--"

        # Arbeitszeit berechnen (Intervalle 1-2, 3-4, etc.)
        total_seconds = 0
        for i in range(0, count - 1, 2):
            total_seconds += (times[i + 1] - times[i]).total_seconds()

        hours, rem = divmod(int(total_seconds), 3600)
        mins, _ = divmod(rem, 60)
        duration = f"{hours}h {mins}min"

        table_data.append({
            "name": data["name"],
            "in": first_in,
            "out": last_out,
            "duration": duration,
            "status": status,
            "class": "status-online" if is_present else "status-offline"
        })

    return render_template("index.html", table=table_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
 
