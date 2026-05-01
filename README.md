🧠 Desk Buddy

IoT-Based Workspace Monitoring System with ML-Assisted Insights

🚀 Overview

Desk Buddy is a smart workspace monitoring system that uses IoT sensors and Machine Learning to track environmental conditions and provide real-time insights.
The system measures temperature, humidity, CO₂ levels, and light intensity (lux) using an ESP32-based node. Data is transmitted via MQTT to a local Python workstation, where it is processed for analysis, alerting, and visualization.
Instead of directly predicting productivity, the system estimates environmental comfort and fatigue risk based on predefined thresholds and a trained ML model.

⚙️ System Architecture
Edge Device (ESP32):
Collects environmental data and publishes it via MQTT.
Communication Layer (MQTT):
Handles lightweight, real-time data transfer using HiveMQ.
Processing Layer (Python):
Performs data processing and ML inference
Applies rule-based safety thresholds (e.g., high CO₂ alerts)
Generates insights and warnings
Visualization Layer (Web Dashboard):
Displays real-time data through an interactive dashboard (WebGL-based), acting as a digital representation of the workspace.

📊 Features
Real-time monitoring of workspace conditions
Environmental comfort and fatigue risk estimation
Rule-based safety alerts (e.g., CO₂, temperature limits)
MQTT-based scalable data pipeline
Interactive dashboard for live visualization
🛠️ Tech Stack
Hardware: ESP32
Protocol: MQTT (HiveMQ)
Backend: Python
Frontend: WebGL + JavaScript
ML Model: Pre-trained Neural Network
