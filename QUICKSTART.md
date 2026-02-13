# Quick Start Guide - IoT Data API

## 🚀 Getting Started in 3 Steps

### 1. Register Your Device
Visit: `http://localhost:8000/register`

Fill in:
- Device ID: `my_device`
- Device Name: `My_Sensor`
- Category: `IOT`
- Branch ID: `lab_01`

**Save your API key!** (shown only once)

---

### 2. Send Data

**Python:**
```python
import requests

requests.post(
    "http://localhost:8000/api/v1/logs/IOT/My_Sensor",
    headers={"X-API-Key": "your_api_key"},
    json={"data": {"temperature": 25.5, "humidity": 60}}
)
```

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/logs/IOT/My_Sensor" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"data": {"temperature": 25.5}}'
```

---

### 3. View Dashboard
Visit: `http://localhost:8000/dashboard`

Enter your credentials and click "Start Monitoring"

---

## 📊 URLs

| Page | URL |
|------|-----|
| Registration | `http://localhost:8000/register` |
| Dashboard | `http://localhost:8000/dashboard` |
| API Docs | `http://localhost:8000/docs` |

---

## 🧪 Test Scripts

```bash
# Simulate continuous data
python simulate_device.py

# Run all tests
./test_all.sh

# Test MongoDB
mongosh centralized_data --file test_mongodb.js
```

---

## 📝 Full Documentation

See [README.md](README.md) for complete documentation.

---

## 🆘 Troubleshooting

**Server won't start:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**MongoDB not running:**
```bash
sudo systemctl start mongod
```

**API key not working:**
- Make sure you copied the entire key
- Check device exists: `mongosh centralized_data --eval 'db.devices.find()'`
