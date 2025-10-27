# generator.py  (Kafka + CSV + simple battery drain)
# --------------------------------------------------
# This script pretends to be IoT devices sending sensor data.
# Each device produces readings (temperature, humidity, battery) once per second.
# The readings are:
#   1. Sent as JSON messages to a Kafka topic (iotsensors).
#   2. Saved locally into a CSV file (sensors.csv) for later inspection.

import os, json, time, random
from datetime import datetime
from kafka import KafkaProducer

# Kafka topic name where messages will be published
TOPIC = "iotsensors"

# List of devices to simulate. Right now only one device: "dev-1"
DEVICES = ["dev-1"]

# Interval in seconds between each round of sending data
INTERVAL_SEC = 1

# How much the battery drains every time we send a reading
DRAIN_PER_READ = 1

# Dictionary that stores the battery % for each device.
# Example: {"dev-1": 17}
BATTERIES = {dev: random.randint(10, 20) for dev in DEVICES}

# Path of the CSV file where readings will be saved
CSV_PATH = os.path.join(os.path.dirname(__file__), "sensors.csv") 


def simulate_reading(device_id, battery_pct):
    """
    Simulate one sensor reading for a device.
    If battery is 0, no temperature/humidity data will be generated (set to None).
    Returns a dictionary representing the data.
    """
    temp = round(random.uniform(18.0, 36.0), 2) if battery_pct > 0 else None
    hum  = round(random.uniform(20.0, 90.0), 2) if battery_pct > 0 else None
    return {
        "device_id": device_id,                               # which device sent it
        "ts": datetime.now().strftime("%d/%m/%Y - %H:%M:%S"), # timestamp in local time
        "temperature_c": temp,                                # temperature in Celsius
        "humidity_pct": hum,                                  # humidity percentage
        "battery_pct": battery_pct,                           # battery left
        # "Alerts": Alerts(battery_pct,temp,hum)                # warnings (battery low, etc.)
    }

# def Alerts(battery_pct, temp, hum):
#     """
#     Create alert messages based on battery, temperature, and humidity.
#     Returns a single string with alerts separated by semicolons.
#     """
#     alerts = []

#     # Battery checks
#     if battery_pct == 0:
#         alerts.append("NO POWER")            # device is completely dead
#     elif battery_pct < 10:
#         alerts.append("LOW BATTERY")

#     # Temperature checks (only if we have a reading)
#     if temp is not None:
#         if temp < 21:
#             alerts.append("TEMP LOW")
#         elif temp > 30:
#             alerts.append("TEMP HIGH")

#     # Humidity checks (only if we have a reading)
#     if hum is not None:
#         if hum < 35:
#             alerts.append("HUMIDITY LOW")
#         elif hum > 75:
#             alerts.append("HUMIDITY HIGH")

#     return " ; ".join(alerts)   # join all alerts in one string


def main():
    # 1. Prepare the CSV file
    if not os.path.exists(CSV_PATH):
        # If file doesn’t exist, create it and write the header row
        open(file=CSV_PATH, mode = "w", encoding="utf-8").write(
            "device_id,ts,temperature_c,humidity_pct,battery_pct\n"
        )

    # Open CSV file in append mode so new readings are added at the bottom
    csv_file = open(file=CSV_PATH, mode="a", encoding="utf-8")

    # 2. Create the Kafka producer (connection to Kafka broker)
    Kafka_Producer = KafkaProducer(
        bootstrap_servers="localhost:9092",                 # Kafka is expected on this address
        value_serializer=lambda message: json.dumps(message).encode("utf-8"),  # convert dict → JSON → bytes
    )

    print(f"[INFO] Producing to {TOPIC} @ localhost:9092 | CSV: {CSV_PATH} | Devices: {DEVICES}")

    try:
        # Infinite loop: keep sending readings until user stops program
        while True:
            for device in DEVICES:
                # Drain battery for this device
                BATTERIES[device] = max(0, BATTERIES[device] - DRAIN_PER_READ)        

                # Generate one reading (dict)
                msg = simulate_reading(device, BATTERIES[device])

                # --- Send to Kafka ---
                Kafka_Producer.send(TOPIC, value=msg)

                # --- Save to CSV file ---
                csv_file.write(
                    f"{msg['device_id']},{msg['ts']},{msg['temperature_c']},"
                    f"{msg['humidity_pct']},{msg['battery_pct']}\n"
                )
                csv_file.flush()                # push to OS buffer
                os.fsync(csv_file.fileno())     # force write to disk
                print("[PRODUCED]", msg)        # show message in terminal for debugging

            # Ensure Kafka actually delivers messages
            Kafka_Producer.flush()

            # Wait before sending next batch
            time.sleep(INTERVAL_SEC)

    except KeyboardInterrupt:
        # Happens when user presses Ctrl+C
        print("\n[INFO] Stopping producer...")
    finally:
        # Clean shutdown: close both Kafka connection and CSV file
        Kafka_Producer.close()
        csv_file.close()


# Run the main loop only if script is executed directly
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
    input("Press Enter to exit...")
