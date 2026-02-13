# Centralized IoT Data API

A powerful, production-ready FastAPI-based platform for collecting, storing, and visualizing IoT sensor data with real-time monitoring capabilities.

## 🌟 Features

- **Device Registration** - Web-based registration page with instant API key generation
- **Real-time Dashboard** - Live monitoring with auto-refresh, charts, and data visualization
- **Data Export** - Download sensor data as JSON or CSV (up to 1000 entries)
- **Secure Authentication** - API key-based authentication for all devices
- **Flexible Data Storage** - MongoDB for scalable data persistence
- **Multiple Retrieval Modes** - Latest, JSON array, or CSV export
- **Shareable Links** - Generate dashboard links with embedded credentials

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Register a Device](#1-register-a-device)
  - [Send Data](#2-send-data-from-your-device)
  - [View Dashboard](#3-view-live-dashboard)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Configuration](#configuration)

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
cd /home/aadi/server
source venv/bin/activate

# 2. Start the server
uvicorn app.main:app --reload

# 3. Open browser
http://localhost:8000/register  # Register your device
http://localhost:8000/dashboard # View live data
```

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- MongoDB running on localhost:27017
- pip and virtualenv

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure MongoDB is running
sudo systemctl start mongod
sudo systemctl status mongod

# 3. Start the API server
source venv/bin/activate
uvicorn app.main:app --reload
```

The server will start on `http://localhost:8000`

---

## 💡 Usage

### 1. Register a Device

**Option A: Web Interface (Recommended)**

1. Open `http://localhost:8000/register`
2. Fill in the form:
   - Device ID (unique identifier)
   - Device Name (human-readable name)
   - Category (e.g., IOT, SENSOR)
   - Branch ID (organization/location identifier)
3. Click "Register Device"
4. **Save the API key** (shown only once!)
5. Click "Go to Dashboard" to start monitoring

**Option B: API Endpoint**

```bash
curl -X POST "http://localhost:8000/api/v1/devices/register?device_id=my_device&device_name=My_Sensor&category=IOT&branch_id=lab_01"
```

Response:
```json
{
  "device_id": "my_device",
  "api_key": "sk_device_..."
}
```

---

### 2. Send Data from Your Device

**Python Example:**

```python
import requests

API_URL = "http://localhost:8000"
DEVICE_NAME = "My_Sensor"
CATEGORY = "IOT"
API_KEY = "your_api_key_here"

data = {
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25
}

response = requests.post(
    f"{API_URL}/api/v1/logs/{CATEGORY}/{DEVICE_NAME}",
    headers={"X-API-Key": API_KEY},
    json={"data": data}
)

print(response.json())  # {"status": "ok"}
```

**curl Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/logs/IOT/My_Sensor" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"data": {"temperature": 25.5, "humidity": 60.2}}'
```

---

### 3. View Live Dashboard

**Access Dashboard:**
```
http://localhost:8000/dashboard
```

**Features:**
- 📊 Real-time metrics cards
- 📈 Historical charts (Chart.js)
- 📋 Recent readings table
- 🔄 Auto-refresh every 5 seconds
- 📥 Download data as JSON/CSV
- 🔗 Generate shareable links

**With Pre-filled Credentials:**
```
http://localhost:8000/dashboard?device_id=my_device&device_name=My_Sensor&category=IOT&api_key=your_key
```

---

## 📚 API Documentation

### Endpoints

#### 1. Register Device
```
POST /api/v1/devices/register
```

**Query Parameters:**
- `device_id` (required) - Unique device identifier
- `device_name` (required) - Human-readable device name
- `category` (required) - Device category
- `branch_id` (required) - Branch/location identifier

**Response:**
```json
{
  "device_id": "string",
  "api_key": "string"
}
```

---

#### 2. Ingest Data
```
POST /api/v1/logs/{category}/{device_name}
```

**Headers:**
- `X-API-Key` (required) - Device API key
- `Content-Type: application/json`

**Body:**
```json
{
  "data": {
    "field1": "value1",
    "field2": 123,
    "field3": true
  }
}
```

**Response:**
```json
{
  "status": "ok"
}
```

---

#### 3. Retrieve Data
```
GET /api/v1/logs/{category}/{device_name}?mode={mode}&limit={limit}
```

**Headers:**
- `X-API-Key` (required)

**Query Parameters:**
- `mode` (optional) - `latest` | `json` | `csv` (default: `latest`)
- `limit` (optional) - Number of entries (1-1000, default: 10)

**Modes:**

**Latest Mode:**
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=latest" \
  -H "X-API-Key: your_key"
```

Returns single most recent entry.

**JSON Mode:**
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=json&limit=100" \
  -H "X-API-Key: your_key"
```

Returns array of entries (newest first).

**CSV Mode:**
```bash
curl "http://localhost:8000/api/v1/logs/IOT/My_Sensor?mode=csv&limit=1000" \
  -H "X-API-Key: your_key" \
  -o data.csv
```

Downloads CSV file.

---

## 🧪 Testing

### Automated Tests

```bash
# Test all endpoints
./test_all.sh

# Test MongoDB queries
mongosh centralized_data --file test_mongodb.js

# Simulate continuous data
python simulate_device.py

# Test newly registered device
python test_new_device.py
```

### Manual Testing

See [TESTING.md](TESTING.md) for comprehensive testing guide with curl commands and MongoDB queries.

---

## 📁 Project Structure

```
/home/aadi/server/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   ├── devices.py       # Device registration
│   │   └── logs.py          # Data ingestion/retrieval
│   ├── dependencies/
│   │   ├── auth.py          # API key authentication
│   │   └── payload_guard.py # Payload size validation
│   └── utils/
│       ├── csv_export.py    # CSV conversion
│       └── mongo.py         # MongoDB utilities
├── static/
│   ├── index.html           # Dashboard
│   └── register.html        # Registration page
├── test_all.sh              # Automated test script
├── test_mongodb.js          # MongoDB test queries
├── simulate_device.py       # Continuous data simulator
├── test_new_device.py       # New device test
├── requirements.txt         # Python dependencies
├── TESTING.md               # Testing documentation
├── CREDENTIALS.md           # Quick reference
└── README.md                # This file
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# MongoDB (default: localhost:27017)
MONGODB_URL=mongodb://localhost:27017

# Server (default: localhost:8000)
HOST=0.0.0.0
PORT=8000
```

### MongoDB Database

- **Database:** `centralized_data`
- **Collections:**
  - `devices` - Registered devices with API keys
  - `logs` - Sensor data entries

---

## 🔐 Security

- **API Keys:** SHA-256 hashed before storage
- **Authentication:** Required for all data operations
- **CORS:** Enabled for dashboard access
- **Payload Limits:** Configurable size restrictions

---

## 🌐 Deployment

### Local Development
```bash
uvicorn app.main:app --reload
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Remote Server (103.54.14.85)
```bash
# On remote server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Dashboard will be available at: `http://103.54.14.85:8000/dashboard`

---

### Production Setup with Systemd (Recommended)

For automatic restart and process management:

**1. Create systemd service file:**
```bash
sudo nano /etc/systemd/system/iot-api.service
```

**2. Add configuration:**
```ini
[Unit]
Description=IoT Data API
After=network.target mongod.service

[Service]
Type=simple
User=aadi
WorkingDirectory=/home/aadi/server
Environment="PATH=/home/aadi/server/venv/bin"
ExecStart=/home/aadi/server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**3. Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable iot-api
sudo systemctl start iot-api
sudo systemctl status iot-api
```

**4. Manage service:**
```bash
# View logs
sudo journalctl -u iot-api -f

# Restart
sudo systemctl restart iot-api

# Stop
sudo systemctl stop iot-api
```

---

## 📊 Dashboard Features

### Metrics Cards
- Real-time sensor values
- Auto-updating every 5 seconds
- Color-coded by data type

### Charts
- Historical trends (Chart.js)
- Multiple sensor lines
- Time-based X-axis

### Data Table
- Recent 10 readings
- Timestamp and full payload
- Sortable columns

### Export
- **Download JSON** - Up to 1000 entries
- **Download CSV** - Up to 1000 entries
- Automatic filename generation

---

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
kill -9 <PID>
```

### MongoDB connection failed
```bash
# Start MongoDB
sudo systemctl start mongod

# Check status
sudo systemctl status mongod
```

### API key not working
```bash
# Verify device exists
mongosh centralized_data --eval 'db.devices.find({_id: "your_device_id"})'
```

---

## 📝 License

This project is proprietary software.

---

## 👥 Support

For issues or questions, contact the development team.

---

## 🎯 Quick Reference

| Action | URL |
|--------|-----|
| Register Device | `http://localhost:8000/register` |
| View Dashboard | `http://localhost:8000/dashboard` |
| API Docs | `http://localhost:8000/docs` |
| Root (redirects to dashboard) | `http://localhost:8000/` |

**Happy Monitoring! 🚀**
