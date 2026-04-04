import paho.mqtt.client as mqtt
import json
import joblib
import numpy as np
from tensorflow.keras.models import load_model

print("Loading AI Model and Scaler...")
model = load_model('desk_buddy_fatigue_model.h5')
scaler = joblib.load('sensor_scaler.save')

# HiveMQ Setup
broker = "7e790fa080b94fa5b2cc5991533287b3.s1.eu.hivemq.cloud"
port = 8883 # Python uses the standard secure port, not the WebSocket port
client_id = "Python_AI_Brain"
username = "roboism"
password = "@Roboism123"

# Topics
SUBSCRIBE_TOPIC = "deskbuddy/telemetry"
PUBLISH_TOPIC = "deskbuddy/ai_prediction"

# 1. What to do when connected
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ! Listening for ESP32 data...")
        client.subscribe(SUBSCRIBE_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

# 2. What to do when a message arrives from the ESP32
def on_message(client, userdata, msg):
    try:
        # 1. Decode the JSON from the ESP32
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        # Extract individual values
        temp = data.get('temperature', 25)
        hum = data.get('humidity', 50)
        co2 = data.get('co2', 400)
        lux = data.get('lux', 500)

        alert_msg = "none"
        productivity_score = 0.0

        # 2. HARDWARE GUARDRAILS (The Sanity Checks)
        if temp < 5 or temp > 60:
            alert_msg = f"⚠️ Extreme Temp ({temp}°C)! Productivity is 0%."
        elif co2 < 300 or co2 > 10000:
            alert_msg = f"⚠️ Hazardous Air ({co2} ppm)! Productivity is 0%."
        elif hum < 0 or hum > 100:
            alert_msg = f"⚠️ Sensor Error (Humidity {hum}%)! Productivity is 0%."
        elif lux < 0:
            alert_msg = f"⚠️ Sensor Error (Lux {lux})! Productivity is 0%."
        
        # 3. If the room is safe, ask the AI!
        else:
            raw_values = np.array([[ temp, hum, co2, lux ]])
            scaled_values = scaler.transform(raw_values)
            
            # The model predicts productivity natively (0.0 to 1.0)
            productivity_prob = model.predict(scaled_values, verbose=0)[0][0]
            productivity_score = round(productivity_prob * 100, 1)

            # Optional: Add a soft warning if productivity is just naturally low
            if productivity_score < 40:
                alert_msg = "⚠️ Low Productivity Environment"

        print(f"Data Received | Productivity: {productivity_score}% | Alert: {alert_msg}")
        
        # 4. Package and publish to the Dashboard
        ai_payload = json.dumps({
            "productivity_score": float(productivity_score), 
            "alert": alert_msg
        })
        
        client.publish(PUBLISH_TOPIC, ai_payload)
        
   
    except Exception as e:
        print("Waiting for valid sensor data...", e)

# Setup MQTT Client
client = mqtt.Client(client_id)
client.tls_set() # Enable secure connection
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

# Connect and run forever
client.connect(broker, port)
client.loop_forever()