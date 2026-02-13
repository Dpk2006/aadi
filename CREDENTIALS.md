# Quick Reference - IoT API Credentials

## 🔑 Current Active Device

**Device Information:**
- **Device ID:** `device_1`
- **Device Name:** `AGGRO_PCB`
- **Category:** `IOT`
- **Branch ID:** `csiot`
- **App ID:** `sensor_app`

**API Key:**
```
sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs
```

---

## 🚀 Quick Commands

### Ingest Data
```bash
curl -X POST "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?app_id=sensor_app" \
  -H "X-API-Key: sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs" \
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

### Get Latest Data
```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?app_id=sensor_app&mode=latest" \
  -H "X-API-Key: sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs"
```

### Get JSON Data
```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?app_id=sensor_app&mode=json&limit=10" \
  -H "X-API-Key: sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs"
```

### Export CSV
```bash
curl "http://localhost:8000/api/v1/logs/IOT/AGGRO_PCB?app_id=sensor_app&mode=csv&limit=100" \
  -H "X-API-Key: sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs" \
  -o data.csv
```

---

## 🌐 Dashboard Access

**Web Dashboard URL:**
```
http://localhost:8000/dashboard
```

**Or for remote server:**
```
http://103.54.14.85:8000/dashboard
```

**Direct Link (with credentials embedded):**
```
http://localhost:8000/dashboard?api_url=http://localhost:8000&device_id=device_1&device_name=AGGRO_PCB&category=IOT&app_id=sensor_app&api_key=sk_device_aKFIn7MHERxAwEs0XQOabOSJTiujepG24a2YRg_Lhgs
```

**Features:**
- 📊 Real-time monitoring (auto-refresh every 5 seconds)
- 📈 Interactive charts with historical data
- 📥 **Download JSON** - Export up to 1000 entries as JSON
- 📥 **Download CSV** - Export up to 1000 entries as CSV
- 🔗 Generate shareable links with embedded credentials

**To access:**
1. Open `http://localhost:8000/dashboard` in your browser
2. Fill in the credentials above
3. Click "Start Monitoring"
4. Use download buttons to export data anytime

---

## 🗄️ MongoDB Queries

```bash
# View all devices
mongosh centralized_data --eval 'db.devices.find().pretty()'

# View latest logs
mongosh centralized_data --eval 'db.logs.find().sort({timestamp: -1}).limit(5).pretty()'

# Count logs
mongosh centralized_data --eval 'db.logs.countDocuments()'
```

---

## 🧹 Reset Database

```bash
mongosh centralized_data --eval 'db.devices.deleteMany({}); db.logs.deleteMany({})'
```

---

## 📊 Test Everything

```bash
./test_all.sh
```

## mADE BY 
HITARTH SHARMA
