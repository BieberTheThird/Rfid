import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import paho.mqtt.publish as publish
import time

# --- CONFIG ---
MQTT_BROKER = "10.14.213.223"
MQTT_TOPIC = "rfid/scan"

# LED Pins
LED_RED = 11
LED_GREEN = 13
LED_BLUE = 15

# SETUP-
reader = SimpleMFRC522()

GPIO.setup([LED_RED, LED_GREEN, LED_BLUE], GPIO.OUT)

def set_led(r, g, b):
    GPIO.output(LED_RED, r)
    GPIO.output(LED_GREEN, g)
    GPIO.output(LED_BLUE, b)

print("Scanner bereit. LED ist Blau.")

try:
    while True:
        # Permanent Blue light while waiting
        set_led(0, 0, 1)

        # This blocks until a card is present
        uid, text = reader.read()

        if uid:
            uid_str = str(uid).strip()
            print(f"Karte erkannt: {uid_str}")

            try:
                publish.single(MQTT_TOPIC, uid_str, hostname=MQTT_BROKER)
                # Success = Green Light
                set_led(0, 1, 0)
                time.sleep(1.0)
            except Exception as e:
                print(f"MQTT Fehler: {e}")
                # Error = Red Light
                set_led(1, 0, 0)
                time.sleep(1.0)

except KeyboardInterrupt:
    print("\nBeende Programm...")
finally:
    # Turn off LEDs and cleanup
    set_led(0, 0, 0)
    GPIO.cleanup()
