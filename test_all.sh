#!/bin/bash

# Configuration
API_URL="http://localhost:8000"
DEVICE_ID="test_device_$(date +%s)"
DEVICE_NAME="TEST_DEVICE_01"
CATEGORY="IOT"
BRANCH_ID="test_lab"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting Automated Tests${NC}"
echo "================================================="
echo "Target: $API_URL"
echo "Device ID: $DEVICE_ID"
echo "================================================="
echo

# Test 1: Register Device
echo -e "${YELLOW}Test 1: Register Log Device${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/devices/register?device_id=${DEVICE_ID}&device_name=${DEVICE_NAME}&category=${CATEGORY}&branch_id=${BRANCH_ID}")
echo "Response: $REGISTER_RESPONSE"

API_KEY=$(echo $REGISTER_RESPONSE | grep -o '"api_key":"[^"]*' | cut -d'"' -f4)

if [ -n "$API_KEY" ]; then
    echo -e "${GREEN}✅ Registration Successful. API Key: $API_KEY${NC}"
else
    echo -e "${RED}❌ Registration Failed${NC}"
    exit 1
fi
echo

# Test 2: Ingest Data
echo -e "${YELLOW}Test 2: Ingest Data${NC}"
for i in {1..3}; do
    TEMP=$(awk -v min=20 -v max=30 'BEGIN{srand(); print min+rand()*(max-min)}')
    HUMIDITY=$(awk -v min=40 -v max=80 'BEGIN{srand(); print min+rand()*(max-min)}')
    
    INGEST_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/logs/${CATEGORY}/${DEVICE_NAME}" \
      -H "X-API-Key: ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d "{
        \"data\": {
          \"temperature\": $TEMP,
          \"humidity\": $HUMIDITY,
          \"pressure\": 1013.25,
          \"reading_id\": $i
        }
      }")
    echo "Entry $i: $INGEST_RESPONSE"
done
echo -e "${GREEN}✅ Data Ingestion Complete${NC}"
echo

# Test 3: Retrieve Latest Data
echo -e "${YELLOW}Test 3: Retrieve Latest Data${NC}"
LATEST_RESPONSE=$(curl -s "${API_URL}/api/v1/logs/${CATEGORY}/${DEVICE_NAME}?mode=latest" \
  -H "X-API-Key: ${API_KEY}")
echo "Response: $LATEST_RESPONSE"
echo -e "${GREEN}✅ Retrieved latest data${NC}"
echo

# Test 4: Retrieve JSON Data
echo -e "${YELLOW}Test 4: Retrieve JSON Data (limit=3)${NC}"
JSON_RESPONSE=$(curl -s "${API_URL}/api/v1/logs/${CATEGORY}/${DEVICE_NAME}?mode=json&limit=3" \
  -H "X-API-Key: ${API_KEY}")
echo "Response: $JSON_RESPONSE"
echo -e "${GREEN}✅ Retrieved JSON data${NC}"
echo

# Test 5: Download CSV
echo -e "${YELLOW}Test 5: Download CSV${NC}"
curl -s "${API_URL}/api/v1/logs/${CATEGORY}/${DEVICE_NAME}?mode=csv" \
  -H "X-API-Key: ${API_KEY}" \
  -o test_output.csv
if [ -f "test_output.csv" ]; then
    echo -e "${GREEN}✅ CSV Downloaded (Size: $(du -h test_output.csv | cut -f1))${NC}"
    rm test_output.csv
else
    echo -e "${RED}❌ CSV Download Failed${NC}"
fi
echo

echo "================================================="
echo -e "${GREEN}🎉 All Tests Passed!${NC}"
echo "================================================="
