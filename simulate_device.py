#!/usr/bin/env python3
"""
Continuous Data Sender - Simulates IoT device sending sensor data
Sends random sensor readings every 3 seconds to test live dashboard updates
"""

import requests
import time
import random
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
DEVICE_ID = "device_1"
DEVICE_NAME = "AGGRO_PCB"
CATEGORY = "IOT"
API_KEY = "sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs"

# Sensor ranges
TEMP_RANGE = (18.0, 32.0)
HUMIDITY_RANGE = (40.0, 80.0)
PRESSURE_RANGE = (990.0, 1020.0)
LIGHT_RANGE = (100, 1000)
BATTERY_RANGE = (3.0, 4.2)
RSSI_RANGE = (-90, -50)

def generate_sensor_data():
    """Generate random sensor readings"""
    return {
        "temperature": round(random.uniform(*TEMP_RANGE), 2),
        "humidity": round(random.uniform(*HUMIDITY_RANGE), 2),
        "pressure": round(random.uniform(*PRESSURE_RANGE), 2),
        "light_level": random.randint(*LIGHT_RANGE),
        "motion_detected": random.choice([True, False]),
        "battery_voltage": round(random.uniform(*BATTERY_RANGE), 2),
        "rssi": random.randint(*RSSI_RANGE)
    }

def send_data(data):
    """Send sensor data to API"""
    url = f"{API_URL}/api/v1/logs/{CATEGORY}/{DEVICE_NAME}"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"data": data}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending data: {e}")
        return False

def main():
    print("🚀 Starting Continuous Data Sender")
    print(f"📡 Target: {API_URL}")
    print(f"🔧 Device: {DEVICE_NAME} ({DEVICE_ID})")
    print(f"⏱️  Interval: 3 seconds")
    print(f"🛑 Press Ctrl+C to stop\n")
    
    count = 0
    
    try:
        while True:
            count += 1
            data = generate_sensor_data()
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Sending reading #{count}:")
            print(f"  🌡️  Temp: {data['temperature']}°C")
            print(f"  💧 Humidity: {data['humidity']}%")
            print(f"  📊 Pressure: {data['pressure']} hPa")
            print(f"  💡 Light: {data['light_level']}")
            print(f"  🔋 Battery: {data['battery_voltage']}V")
            print(f"  📶 RSSI: {data['rssi']} dBm")
            
            if send_data(data):
                print(f"  ✅ Sent successfully\n")
            else:
                print(f"  ❌ Failed to send\n")
            
            time.sleep(3)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Stopped after {count} readings")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
