
import sqlite3
import paho.mqtt.client as mqtt

# CONFIG
MQTT_BROKER = "10.14.213.223"
MQTT_TOPIC = "rfid/scan"
DB_NAME = "rfid.db"

def save_to_db(uid):
    try:
        with sqlite3.connect(DB_NAME) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO scans (uid) VALUES (?)", (uid,))
            db.commit()
            print(f"Erfolg: UID {uid} in Datenbank gespeichert.")
    except Exception as e:
        print(f"Datenbankfehler: {e}")

# on Message Calllback
def on_message(client, userdata, msg):
    uid = msg.payload.decode("utf-8")
    print(f"Nachricht empfangen: {uid} auf Topic {msg.topic}")
    save_to_db(uid)

# MQTT Setup
client = mqtt.Client()
client.on_message = on_message

print("Verbinde mit Broker...")
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"Warte auf Scans auf Topic '{MQTT_TOPIC}'...")
client.loop_forever()
