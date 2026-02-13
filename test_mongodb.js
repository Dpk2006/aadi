// MongoDB Test Queries for IoT Data API
// Run: mongosh centralized_data --file test_mongodb.js

print("=== IoT Data API - MongoDB Tests ===\n");

// Test 1: View all devices
print("Test 1: View All Devices");
print("------------------------");
db.devices.find().forEach(doc => printjson(doc));
print("\n");

// Test 2: Count total devices
print("Test 2: Count Total Devices");
print("---------------------------");
print("Total devices: " + db.devices.countDocuments());
print("\n");

// Test 3: View latest 5 logs
print("Test 3: Latest 5 Logs");
print("---------------------");
db.logs.find().sort({ timestamp: -1 }).limit(5).forEach(doc => printjson(doc));
print("\n");

// Test 4: Count total logs
print("Test 4: Count Total Logs");
print("------------------------");
print("Total logs: " + db.logs.countDocuments());
print("\n");

// Test 5: Find logs by specific device (replace with your device_id)
print("Test 5: Logs by Device ID");
print("-------------------------");
const deviceId = "test_device_1769620111"; // Replace with actual device_id
const deviceLogs = db.logs.find({ device_id: deviceId }).count();
print("Logs for device '" + deviceId + "': " + deviceLogs);
print("\n");

// Test 6: Find logs from last hour
print("Test 6: Logs from Last Hour");
print("---------------------------");
const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
const recentLogs = db.logs.find({ timestamp: { $gte: oneHourAgo } }).count();
print("Logs in last hour: " + recentLogs);
print("\n");

// Test 7: Average sensor values (aggregation)
print("Test 7: Average Sensor Values");
print("-----------------------------");
db.logs.aggregate([
    { $match: { device_id: deviceId } },
    {
        $group: {
            _id: null,
            avgTemp: { $avg: "$payload.temperature" },
            avgHumidity: { $avg: "$payload.humidity" },
            avgPressure: { $avg: "$payload.pressure" },
            count: { $sum: 1 }
        }
    }
]).forEach(doc => {
    print("Average Temperature: " + doc.avgTemp.toFixed(2) + "°C");
    print("Average Humidity: " + doc.avgHumidity.toFixed(2) + "%");
    print("Average Pressure: " + doc.avgPressure.toFixed(2) + " hPa");
    print("Total readings: " + doc.count);
});
print("\n");

// Test 8: Logs grouped by app_id
print("Test 8: Logs Grouped by App ID");
print("-------------------------------");
db.logs.aggregate([
    {
        $group: {
            _id: "$app_id",
            count: { $sum: 1 },
            devices: { $addToSet: "$device_id" }
        }
    },
    { $sort: { count: -1 } }
]).forEach(doc => {
    print("App ID: " + doc._id);
    print("  Count: " + doc.count);
    print("  Devices: " + doc.devices.join(", "));
    print("");
});
print("\n");

// Test 9: Find devices by category
print("Test 9: Devices by Category");
print("---------------------------");
db.devices.aggregate([
    {
        $group: {
            _id: "$category",
            count: { $sum: 1 },
            devices: { $push: "$_id" }
        }
    }
]).forEach(doc => {
    print("Category: " + doc._id);
    print("  Count: " + doc.count);
    print("  Devices: " + doc.devices.join(", "));
    print("");
});
print("\n");

// Test 10: Check indexes
print("Test 10: Database Indexes");
print("-------------------------");
print("Devices collection indexes:");
db.devices.getIndexes().forEach(idx => print("  - " + JSON.stringify(idx.key)));
print("\nLogs collection indexes:");
db.logs.getIndexes().forEach(idx => print("  - " + JSON.stringify(idx.key)));
print("\n");

print("=== All MongoDB Tests Completed ===");
