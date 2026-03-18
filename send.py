import paho.mqtt.client as mqtt

# --- KONFIGURATION ---
MQTT_BROKER = "192.168.2.67"
MQTT_PORT = 1883
MQTT_TOPIC = "rfid/scan"

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.publish(MQTT_TOPIC, "2")
    print(" Nachricht '2' gesendet")

    client.disconnect()

except KeyboardInterrupt:
    print("\nProgramm abgebrochen.")
