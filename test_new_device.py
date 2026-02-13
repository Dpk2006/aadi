#!/usr/bin/env python3
"""
Test script for newly registered device
Tests the complete registration -> data ingestion -> dashboard flow
"""

import requests
import time
import random
from datetime import datetime

# Use the newly registered device from the registration page
API_URL = "http://localhost:8000"
DEVICE_ID = "test_device_new"
DEVICE_NAME = "TEST_SENSOR"
CATEGORY = "IOT"
API_KEY = "sk_device_Yac-dk4puc1jFoevNvXzoGBMdwAloL98RMEzczVZbu0"

def generate_sensor_data():
    """Generate random sensor readings"""
    return {
        "temperature": round(random.uniform(18.0, 32.0), 2),
        "humidity": round(random.uniform(40.0, 80.0), 2),
        "pressure": round(random.uniform(990.0, 1020.0), 2),
        "light_level": random.randint(100, 1000),
        "motion_detected": random.choice([True, False]),
        "battery_voltage": round(random.uniform(3.0, 4.2), 2),
        "rssi": random.randint(-90, -50)
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
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 Testing Newly Registered Device")
    print("=" * 50)
    print(f"Device ID: {DEVICE_ID}")
    print(f"Device Name: {DEVICE_NAME}")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 50)
    print()
    
    # Send 5 test readings
    for i in range(1, 6):
        data = generate_sensor_data()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"[{timestamp}] Sending reading #{i}:")
        print(f"  🌡️  Temp: {data['temperature']}°C")
        print(f"  💧 Humidity: {data['humidity']}%")
        print(f"  📊 Pressure: {data['pressure']} hPa")
        
        if send_data(data):
            print(f"  ✅ Success!\n")
        else:
            print(f"  ❌ Failed!\n")
            break
        
        time.sleep(2)
    
    print("=" * 50)
    print("✅ Test Complete!")
    print()
    print("📊 View data on dashboard:")
    dashboard_url = f"{API_URL}/dashboard?device_id={DEVICE_ID}&device_name={DEVICE_NAME}&category={CATEGORY}&api_key={API_KEY}"
    print(dashboard_url)

if __name__ == "__main__":
    main()
