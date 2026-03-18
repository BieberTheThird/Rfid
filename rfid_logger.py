from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time

# CONFIG
MQTT_BROKER = "10.14.213.223"
MQTT_TOPIC = "rfid/scan"

reader = SimpleMFRC522()

print("RFID logger running — Warte auf Karte...")

try:
    while True:
        uid, text = reader.read()

        if uid:
            #Read card
            uid_str = str(uid).strip()
            print(f"Karte erkannt! UID: {uid_str}")

            #MQTT Send Message
            try:
                publish.single(MQTT_TOPIC, uid_str, hostname=MQTT_BROKER)
                print(f"MQTT: '{uid_str}' an Topic '{MQTT_TOPIC}' gesendet.")
            except Exception as e:
                print(f"MQTT Fehler: {e}")

            time.sleep(2)

except KeyboardInterrupt:
    print("\nProgramm abgebrochen.")
finally:
    GPIO.cleanup()
