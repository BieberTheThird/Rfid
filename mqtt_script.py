import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta

# CONFIG
MQTT_BROKER = "10.14.213.223"
MQTT_TOPIC = "rfid/scan"
DB_NAME = "rfid.db"

COOLDOWN_SECONDS = 15
last_scans = {} 

def save_to_db(uid):
    now = datetime.now()
    
    # Cooldown-Check (pro UID)

    try:
        with sqlite3.connect(DB_NAME) as db:
            cur = db.cursor()

            cur.execute("INSERT INTO scans (uid, timestamp) VALUES (?, ?)", 
                        (uid, now.strftime('%Y-%m-%d %H:%M:%S')))
            db.commit()
            last_scans[uid] = now
            print(f"Datenbank: {uid} registriert ({now.strftime('%H:%M:%S')})")
    except Exception as e:
        print(f"Datenbankfehler: {e}")

def on_message(client, userdata, msg):
    uid = msg.payload.decode("utf-8").strip()
    print(f"Nachricht empfangen: {uid}")
    save_to_db(uid)

client = mqtt.Client()
client.on_message = on_message

print("Verbinde mit MQTT Broker...")
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"Warte auf Scans auf '{MQTT_TOPIC}'...")
client.loop_forever()
