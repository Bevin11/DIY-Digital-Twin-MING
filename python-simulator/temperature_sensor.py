# ─────────────────────────────────────────────
# Simple Temperature Sensor Simulator
# Author  : Bevin I
# Stack   : Python → MQTT → Node-RED → InfluxDB → Grafana
# Topic   : factory/sensor1/temperature
# ─────────────────────────────────────────────

import paho.mqtt.client as mqtt
import json
import time
import random

# ── SETTINGS ──────────────────────────────────
BROKER = "localhost"
PORT   = 1883
TOPIC  = "factory/sensor1/temperature"

# ── TEMPERATURE SIMULATION ────────────────────
temperature = 25.0   # starting temperature in °C

def get_temperature():
    global temperature
    # slowly rise and fall like a real sensor
    temperature += random.uniform(-0.5, 0.8)
    # keep between 20°C and 85°C
    temperature = max(20.0, min(85.0, temperature))
    return round(temperature, 2)

# ── MQTT CALLBACKS ────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        print(f"📡 Publishing to topic: {TOPIC}")
        print("Press Ctrl+C to stop\n")
    else:
        print(f"❌ Connection failed. Code: {rc}")

# ── MAIN ──────────────────────────────────────
client = mqtt.Client(client_id="temp_sensor_1")
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()

time.sleep(1)

try:
    while True:
        temp = get_temperature()
        payload = {
            "sensor_id"   : "sensor1",
            "temperature" : temp,
            "unit"        : "celsius",
            "location"    : "factory_floor"
        }
        client.publish(TOPIC, json.dumps(payload), qos=1, retain=True)
        print(f"🌡 Temperature: {temp}°C  →  sent to MQTT")
        time.sleep(2)   # send every 2 seconds

except KeyboardInterrupt:
    print("\n⛔ Sensor stopped.")
    client.loop_stop()
    client.disconnect()
