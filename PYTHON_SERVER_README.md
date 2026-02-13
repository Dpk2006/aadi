# Python Server Overview

## What is this server?
This is a **backend API server** written in **Python** using the **FastAPI** framework.
Its main purpose is to **collect data** from IoT devices (sensors) and **store it** in a database.

## How it works
1.  **Receives Data**: Devices send data (like temperature, humidity) to this server via HTTP POST requests.
    -   *URL*: `http://.../api/v1/logs/{category}/{device_name}`
2.  **Validates Security**: It checks an `X-API-Key` to make sure the device is allowed to send data.
3.  **Stores Data**: It saves the data into a **MongoDB** database running on your computer.
4.  **Shows Data**: It provides a web dashboard (`/dashboard`) where humans can view charts and live data.

## Key Technologies
-   **Language**: Python 3.8+
-   **Web Framework**: FastAPI (handles the web requests)
-   **Database**: MongoDB (stores the data)
-   **Server**: Uvicorn (runs the Python application)

## Important Files
If you need to edit the code, look at these files:

-   `app/main.py`: **Start here.** This is the entry point that sets up the server and routes.
-   `app/routes/`: Contains the logic for the URL endpoints.
    -   `devices.py`: Logic for registering new devices.
    -   `logs.py`: Logic for receiving and saving sensor data.
-   `app/database.py`: Code that connects to MongoDB.
-   `requirements.txt`: List of Python libraries needed to run this.

## How to Run It

1.  **Install Requirements** (only need to do this once):
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Database**:
    Make sure MongoDB is running.
    ```bash
    # On Windows often runs as a service automatically, or:
    mongod
    ```

3.  **Start the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The server will be live at: `http://localhost:8000`

## APIs at a Glance
-   `POST /api/v1/devices/register`: Create a new device ID and get an API key.
-   `POST /api/v1/logs/...`: Send sensor data.
-   `GET /dashboard`: View the data in your browser.
