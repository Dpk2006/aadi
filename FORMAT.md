# IoT Data API - Request Format Guide

**Current Version: v1.1.0 (App ID Removed)**
# 📟 IoT Data API: Command Reference

**Latest Version (v2.0)**: `app_id` has been removed.

---

## 🚀 1. Register Device
Get your API Key. You only do this once per device.

```bash
curl -X POST "http://localhost:8000/api/v1/devices/register?device_id=my_device&device_name=My_Sensor&category=IOT&branch_id=lab_01"
```
✅ **Response:**
```json
{"device_id": "my_device", "api_key": "sk_device_..."}
```
**Store this API Key!** 🔑

---

## 📡 2. Send Data
Send sensor readings to the cloud.

```bash
curl -X POST "http://localhost:8000/api/v1/logs/IOT/My_Sensor" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 25.5,
      "humidity": 60.2,
      "status": "active"
    }
  }'
```
> **Note:** The `device_name` in the URL (`My_Sensor`) **MUST** match the name you registered.

---

## 📊 3. Get Data

### ➤ Get Latest Reading
Perfect for real-time status checks.
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=latest" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### ➤ Get History (JSON)
Fetch last 10 readings.
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=json&limit=10" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### ➤ Download CSV
Export data for Excel/Analysis.
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=csv&limit=1000" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -o my_data.csv
```

---

## 🛠 Troubleshooting

| Error | Meaning | Fix |
|-------|---------|-----|
| `400 Bad Request` | Device Name Mismatch | Ensure URL name matches registered name. |
| `401 Unauthorized` | Invalid Key | Check your `X-API-Key` header. |
| `404 Not Found` | No Data | Check if you have sent data yet. |

---

## ⚡ Quick Copy-Paste Test
Run these 3 lines to test the whole flow:

```bash
# 1. Register
KEY=$(curl -s -X POST "http://localhost:8000/api/v1/devices/register?device_id=test_dev&device_name=test_sens&category=TEST&branch_id=main" | jq -r .api_key)

# 2. Send
curl -X POST "http://localhost:8000/api/v1/logs/TEST/test_sens" -H "X-API-Key: $KEY" -H "Content-Type: application/json" -d '{"data":{"val":123}}'

# 3. Read
curl "http://localhost:8000/api/v1/logs/TEST/test_sens?mode=latest" -H "X-API-Key: $KEY"
```
