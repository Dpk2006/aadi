# Testing Guide - IoT Data API

Complete testing guide for the Centralized IoT Data API with curl commands and MongoDB queries.

## Prerequisites

- API server running: `source venv/bin/activate && uvicorn app.main:app --reload`
- MongoDB running on localhost:27017
- `mongosh` installed for database queries

---

## API Testing with curl

### 1. Device Registration

Register a new device and receive an API key (shown only once).

```bash
curl -X POST "http://localhost:8000/api/v1/devices/register?device_id=device_1&device_name=AGGRO_PCB&category=IOT&branch_id=csiot"
```

**Expected Response:**
```json
{
  "device_id": "device_1",
  "api_key": "sk_device_uR_Ax2TH7LC7CwCB_YWViXIg52Hd6wxKEMi-TgEWbm0"
}
```

**⚠️ Save the API key immediately - it's only shown once!**

---

### 2. Ingest Sensor Data

Send sensor readings to the API.

```bash
curl -X POST "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "temperature": 25.5,
      "humidity": 60.2,
      "pressure": 1013.25,
      "light_level": 750,
      "motion_detected": false,
      "battery_voltage": 3.7,
      "rssi": -65
    }
  }'
```

**Expected Response:**
```json
{
  "status": "ok"
}
```

---

### 3. Retrieve Latest Data

Get the most recent sensor reading.

```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?mode=latest" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

**Expected Response:**
```json
{
  "_id": "6979aee1f3a5b47ac56f826f",
  "timestamp": "2026-01-28T06:38:25.399000",
  "category": "IOT",
  "device_name": "AGGRO_PCB",
  "device_id": "device_1",
  "branch_id": "csiot",
  "payload": {
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25,
    "light_level": 750,
    "motion_detected": false,
    "battery_voltage": 3.7,
    "rssi": -65
  }
}
```

---

### 4. Retrieve Multiple Entries (JSON)

Get the last 10 sensor readings in JSON format.

```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?mode=json&limit=10" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

**Expected Response:** Array of log entries (newest first)

---

### 5. Export Data as CSV

Download sensor data as a CSV file.

```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?mode=csv&limit=10" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -o data.csv
```

**Expected:** CSV file saved as `data.csv`

---

## MongoDB Testing with mongosh

### Connect to Database

```bash
mongosh
use centralized_data
```

### View All Devices

```javascript
db.devices.find().pretty()
```

**Expected Output:**
```javascript
{
  _id: 'device_1',
  device_name: 'AGGRO_PCB',
  category: 'IOT',
  branch_id: 'csiot',
  api_key_hash: '$2b$12$...',
  status: 'active',
  created_at: ISODate('2026-01-28T06:30:00.000Z')
}
```

---

### View Latest 5 Logs

```javascript
db.logs.find().sort({timestamp: -1}).limit(5).pretty()
```

**Expected Output:**
```javascript
{
  _id: ObjectId('6979aee1f3a5b47ac56f826f'),
  timestamp: ISODate('2026-01-28T06:38:25.399Z'),
  category: 'IOT',
  device_name: 'AGGRO_PCB',
  device_id: 'device_1',
  branch_id: 'csiot',
  payload: {
    temperature: 25.5,
    humidity: 60.2,
    pressure: 1013.25,
    light_level: 750,
    motion_detected: false,
    battery_voltage: 3.7,
    rssi: -65
  }
}
```

---

### Count Total Logs

```javascript
db.logs.countDocuments()
```

---

### Find Logs by Device

```javascript
db.logs.find({device_id: "device_1"}).count()
```

---

### Get Logs from Last Hour

```javascript
const oneHourAgo = new Date(Date.now() - 60*60*1000);
db.logs.find({timestamp: {$gte: oneHourAgo}}).count()
```

---

### Average Temperature (Aggregation)

```javascript
db.logs.aggregate([
  {$match: {device_id: "device_1"}},
  {$group: {
    _id: null,
    avgTemp: {$avg: "$payload.temperature"},
    avgHumidity: {$avg: "$payload.humidity"}
  }}
])
```

---

### Delete Test Data

```javascript
// Delete all logs for a device
db.logs.deleteMany({device_id: "device_1"})

// Delete a device
db.devices.deleteOne({_id: "device_1"})
```

---

## Error Testing

### Test Invalid API Key

```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?mode=latest" \
  -H "X-API-Key: invalid_key"
```

**Expected Response (401):**
```json
{
  "detail": "Invalid API key"
}
```

---

### Test Missing API Key

```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?mode=latest"
```

**Expected Response (403):**
```json
{
  "detail": "Not authenticated"
}
```

---

### Test No Data Found

```bash
curl "http://localhost:8000/api/v1/logs/IOT/NONEXISTENT?mode=latest" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

**Expected Response (404):**
```json
{
  "detail": "No data found"
}
```

---

## Remote Server Testing

Replace `http://localhost:8000` with `http://103.54.14.85:8000` for remote testing:

```bash
# Register device on remote server
curl -X POST "http://103.54.14.85:8000/api/v1/devices/register?device_id=device_1&device_name=AGGRO_PCB&category=IOT&branch_id=csiot"

# Ingest data to remote server
curl -X POST "http://103.54.14.85:8000/api/v1/logs/IOT/AGGRO_PCB" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{"data": {"temperature": 25.5}}'
```

---

## Dashboard Testing

1. Open `dashboard.html` in a browser
2. Enter your device credentials:
   - API URL: `http://localhost:8000`
   - Device ID: `device_1`
   - Device Name: `AGGRO_PCB`
   - Category: `IOT`
   - App ID: `sensor_app`
   - API Key: (your key from registration)
3. Click "Start Monitoring"
4. Verify:
   - ✅ Live data updates every 5 seconds
   - ✅ Metrics cards display current values
   - ✅ Chart shows historical trends
   - ✅ Table shows recent readings
5. Test "Generate Share Link" button
6. Copy link and open in new tab - should auto-load

---

## Troubleshooting

### Server won't start
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run with correct module path
uvicorn app.main:app --reload
```

### MongoDB connection failed
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod
```

### CORS errors in dashboard
- Make sure CORS middleware is added to `app/main.py`
- Check browser console for specific errors

### API key not working
- Verify you're using the exact key from registration
- Check that the device exists in MongoDB: `db.devices.find({_id: "device_1"})`
