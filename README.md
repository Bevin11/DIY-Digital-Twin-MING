# DIY-Digital-Twin-MING
Industrial Digital Twin using MING Stack - MQTT, InfluxDB, Node-RED, Grafana


About This Project:

This project is a fully functional DIY Industrial Digital Twin built entirely using free, open-source software — no physical hardware required. A Digital Twin is a virtual representation of a real physical system that mirrors its behavior, state, and data in real time. In modern manufacturing and Industry 4.0 environments, digital twins are used to monitor equipment health, detect anomalies, predict failures before they happen, and optimize industrial processes — all from a central software dashboard.

In traditional factories, engineers physically walk to each machine, read analog gauges, and manually record values in logbooks. This process is slow, error-prone, and impossible to scale across hundreds of machines running simultaneously. A digital twin solves this completely — every machine reports its own condition automatically, continuously, and in real time to a central monitoring system. Engineers can see the live status of every sensor, every motor, and every process variable from a single screen, from anywhere.

This project replicates that exact industrial architecture using the MING stack — a widely adopted open-source IIoT pipeline consisting of MQTT, InfluxDB, Node-RED, and Grafana. A Python program simulates a factory floor temperature sensor, generating realistic temperature readings that rise and fall naturally — exactly as a real industrial sensor would behave. These readings are published every 2 seconds to a Mosquitto MQTT broker using the MQTT protocol — the global standard for IoT device communication used in factories, oil refineries, power plants, and smart buildings worldwide.

Node-RED — a visual flow programming tool — subscribes to the MQTT broker, receives every temperature reading, transforms the data into the correct format, and writes it into InfluxDB — a time-series database specifically designed for storing continuous sensor data with precise timestamps. Unlike traditional databases, InfluxDB is optimized for high-frequency time-stamped data, making it the industry standard for IoT historian systems. Finally, Grafana connects to InfluxDB and renders a live, auto-refreshing dashboard showing the temperature trend over time, complete with a threshold alarm line at 80°C — exactly as a real SCADA or HMI system would display in an industrial control room.

The purpose of this project is threefold. First, it demonstrates the complete IIoT data pipeline from data generation to visualization — the same pipeline used by companies like Siemens, Honeywell, ABB, and Emerson in their Industry 4.0 solutions. Second, it serves as a learning platform for understanding how industrial communication protocols, time-series databases, and monitoring dashboards work together as an integrated system. Third, it provides a foundation that can be extended with real hardware — replacing the Python simulator with an actual PLC or microcontroller requires only changing the data source, while the entire MQTT → Node-RED → InfluxDB → Grafana pipeline remains identical.

This project bridges the gap between traditional instrumentation engineering and modern Industry 4.0 technologies — demonstrating practical skills in IIoT architecture, industrial communication protocols, time-series data management, and real-time visualization that are directly applicable to roles in industrial automation, smart manufacturing, and digital transformation.


Live Dashboard:

![Grafana Dashboard](docs/Screenshot%202026-03-30%20093125.png)

System Architecture:

Python Simulator (temperature_sensor.py) — written in VS Code
              ↓  MQTT QoS 1 — retain=True
    Mosquitto Broker (localhost:1883)
              ↓  Subscribe
         Node-RED Flow
              ↓  Write
    InfluxDB v2.8 — ming_factory bucket
              ↓  Flux Query
    Grafana Dashboard — live graph


Tech Stack (MING):

| Letter | Tool | Version | Purpose |
|--------|------|---------|---------|
| **M** | MQTT — Mosquitto | v2.x | Real-time message transport |
| **I** | InfluxDB | v2.8.0 | Time-series data storage |
| **N** | Node-RED | v3.x | Data flow orchestration |
| **G** | Grafana | v10.x | Live monitoring dashboard |

---

Tools Used :

Visual Studio Code (VS Code)

VS Code is the code editor used to write the Python simulator in this project. It is the most widely used code editor in the world, developed by Microsoft and available for free. It provides syntax highlighting, error detection, a built-in terminal to run Python programs, and thousands of extensions. Every line of Python code in this project was written inside VS Code.

Python

Python is the programming language used to simulate the industrial temperature sensor. It is one of the most popular languages in the world for data engineering, IoT, and automation projects. In this project, Python generates realistic temperature values, packages them as JSON messages, and publishes them to the MQTT broker every 2 seconds — exactly mimicking how a real PLC or IoT sensor would behave. Two libraries are used — paho-mqtt for MQTT communication and influxdb-client for direct database writing.

MQTT — Mosquitto Broker

MQTT (Message Queuing Telemetry Transport) is the global standard protocol for IoT communication. It uses a publish-subscribe architecture — the Python sensor publishes temperature data to a topic, and Node-RED subscribes to receive it. Mosquitto is the open-source MQTT broker that sits in the middle and routes all messages. It runs as a background service on Windows and is the same broker used in real industrial IoT deployments worldwide.

Node-RED

Node-RED is a visual flow programming tool developed by IBM, now maintained by the OpenJS Foundation. Instead of writing code, you drag and drop nodes onto a canvas and connect them with wires. In this project, Node-RED subscribes to the MQTT broker, receives temperature data, transforms it using a JavaScript function node, and writes it to InfluxDB. It is widely used in Industry 4.0 for connecting industrial systems without complex programming.

nfluxDB

InfluxDB is a time-series database — specifically designed for storing data that is continuously collected over time with precise timestamps. Unlike MySQL or SQL Server, InfluxDB is optimized for sensor data, metrics, and real-time measurements. In this project, every temperature reading is stored in InfluxDB with nanosecond-precision timestamps, making it possible to query historical trends and display them in Grafana.

Grafana

Grafana is an open-source data visualization and monitoring platform. It connects to InfluxDB, queries the stored temperature data using the Flux query language, and renders a live, auto-refreshing graph on a professional dashboard. The dashboard includes a threshold line at 80°C — when temperature crosses this line, it turns red, simulating an industrial alarm condition. Grafana is used by companies like PayPal, eBay, and thousands of manufacturers for real-time monitoring.


Python Simulator — Full Code
The simulator is written in Python 3 and developed using VS Code. It uses the paho-mqtt library to publish temperature data to the MQTT broker every 2 seconds.

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
        print("Connected to MQTT Broker")
        print(f"Publishing to topic: {TOPIC}")
        print("Press Ctrl+C to stop\n")
    else:
        print(f"Connection failed. Code: {rc}")

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
        print(f"Temperature: {temp}°C  →  sent to MQTT")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSensor stopped.")
    client.loop_stop()
    client.disconnect()


What This Project Does:

- Simulates an industrial temperature sensor (20°C to 85°C)
- Publishes sensor data every 2 seconds via MQTT protocol
- Node-RED subscribes to MQTT and writes data to InfluxDB
- InfluxDB stores every reading with precise timestamps
- Grafana displays live temperature graph with 80°C threshold alert
- Full end-to-end IIoT pipeline — identical to real factory systems



Screenshots:

Python Simulator — Live MQTT Publishing
![Python Simulator](docs/Screenshot%202026-03-30%20093017.png)

Node-RED Flow — Complete Pipeline
![Node-RED Flow](docs/Screenshot%202026-03-30%20085713.png)

Node-RED Function Node — Data Transformation Logic
![Function Node](docs/Screenshot%202026-03-30%20085802.png)

InfluxDB — Time-Series Data Storage
![InfluxDB Data](docs/Screenshot%202026-03-30%20092942.png)



Project Structure:

This repository is organized into three main folders.

1.The `python-simulator` folder contains the Python script 
that simulates the industrial temperature sensor and 
publishes data to the MQTT broker. 
2.The `node-red-flows` folder will contain the exported Node-RED flow JSON file 
showing the complete data pipeline configuration. 
3.The `docs` folder holds all project screenshots and 
documentation used in this README. The root contains 
this README file describing the entire project.
```
DIY-Digital-Twin-MING/
├── python-simulator/
│   └── temperature_sensor.py    # Simulates temperature sensor
├── node-red-flows/              # Node-RED pipeline (coming soon)
├── docs/                        # Screenshots and documentation
└── README.md                    # Project documentation
```

How to Run:

Requirements
- Python 3.x with paho-mqtt and influxdb-client
- Mosquitto MQTT Broker
- InfluxDB v2.x
- Node-RED with node-red-contrib-influxdb
- Grafana

Setup Steps

# Step 1 — Install Python libraries
pip install paho-mqtt influxdb-client

# Step 2 — Start MQTT Broker
net start mosquitto

# Step 3 — Run temperature sensor simulator
cd python-simulator
py temperature_sensor.py

# Step 4 — Open Node-RED
# Browser → http://localhost:1880

# Step 5 — Open InfluxDB
# Browser → http://localhost:8086

# Step 6 — Open Grafana Dashboard
# Browser → http://localhost:3000



MQTT Message Format (JSON)

```json
{
  "sensor_id": "sensor1",
  "temperature": 45.23,
  "unit": "celsius",
  "location": "factory_floor"
}
```


**MQTT Topic:** `factory/sensor1/temperature`
**QoS Level:** 1 (At least once delivery)
**Retain:** True (last value always available)

---


InfluxDB Data Model:

* Bucket - ming_factory 
* Measurement -  temperature_data
* Field - temperature (float) 
* Tags - sensor_id/location 
* Retention - 30 days 


Grafana Flux Query:
```flux
from(bucket: "ming_factory")
  |> range(start: -15m)
  |> filter(fn: (r) => r._measurement == "temperature_data")
  |> filter(fn: (r) => r._field == "temperature")
```

---
  

About the Author:

Bevin 
Instrumentation & Control Engineer | IIoT Developer
📍 Tamil Nadu, India

Professional Background
- 3 years industrial experience — Emerson DeltaV DCS operations
- NABL Calibration Engineer — ISO/IEC 17025:2017
- Industrial protocols: Modbus TCP/IP, Profibus, HART, Fieldbus
- PLC Programming: Delta, ABB, Omron, Allen Bradley, Schneider Electric
- SCADA: Wonderware InTouch (in progress), Siemens WinCC (upcoming)

### Connect
- GitHub: [Bevin11](https://github.com/Bevin11)
- LinkedIn: [linkedin.com/in/bevin](https://linkedin.com/in/bevin)
- Email: Bevin1058@gmail.com



## ⭐ If this project helped you, please give it a star!
