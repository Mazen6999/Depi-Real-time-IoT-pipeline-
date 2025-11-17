# generator.py (Sends to Kafka + Event Hub + CSV, and uploads CSV on exit)
# --------------------------------------------------

import os, json, time, random
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData
from azure.storage.blob import BlobServiceClient

# --- Load Environment Variables ---
load_dotenv()

# --- Kafka Configuration (Milestone 1) ---
KAFKA_TOPIC = "iotsensors"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"

# --- Azure Event Hub Configuration (Milestone 3) ---
EVENTHUB_CONNECTION_STRING = os.getenv("EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = "iot-stream"

# --- Azure Blob Storage Configuration (Milestone 2) ---
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = "raw-data"
BLOB_NAME = "sensors.csv"

# --- General Simulation Config ---
DEVICES = ["dev-1"]
INTERVAL_SEC = 5
DRAIN_PER_READ = 1
BATTERIES = {dev: random.randint(90, 100) for dev in DEVICES}
CSV_PATH = os.path.join(os.path.dirname(__file__), "sensors.csv") 

def simulate_reading(device_id, battery_pct):
    temp = round(random.uniform(18.0, 36.0), 2) if battery_pct > 0 else ''
    hum  = round(random.uniform(20.0, 90.0), 2) if battery_pct > 0 else ''
    return {
        "device_id": device_id,
        "ts": datetime.now().isoformat(), # Standard ISO format
        "temperature_c": temp,
        "humidity_pct": hum,
        "battery_pct": battery_pct,
    }

def main():
    # 1. Prepare the CSV file
    if not os.path.exists(CSV_PATH):
        open(file=CSV_PATH, mode = "w", encoding="utf-8").write(
            "device_id,ts,temperature_c,humidity_pct,battery_pct\n"
        )
    csv_file = open(file=CSV_PATH, mode="a", encoding="utf-8")

    # 2. Create the Kafka producer (Milestone 1)
    Kafka_Producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        value_serializer=lambda message: json.dumps(message).encode("utf-8"),
    )

    # 3. Create the Event Hub producer (Milestone 3)
    if not EVENTHUB_CONNECTION_STRING:
        print("[ERROR] EVENTHUB_CONNECTION_STRING environment variable not set.")
        return # <-- This 'return' is OK because it's in the 'main' function, not 'finally'
    
    EventHub_Producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STRING,
        eventhub_name=EVENTHUB_NAME
    )
    
    print(f"[INFO] Producing to Kafka: {KAFKA_TOPIC}")
    print(f"[INFO] Producing to Event Hub: {EVENTHUB_NAME}")
    print("[INFO] Press Ctrl+C to stop...")

    try:
        while True:
            for device in DEVICES:
                BATTERIES[device] = max(0, BATTERIES[device] - DRAIN_PER_READ)        
                msg = simulate_reading(device, BATTERIES[device])
                json_payload = json.dumps(msg)

                # --- Send to Kafka (Milestone 1) ---
                try:
                    Kafka_Producer.send(KAFKA_TOPIC, value=msg)
                except Exception as e:
                    print(f"[ERROR sending to Kafka] {e}")

                # --- Send to Azure Event Hub (Milestone 3) ---
                try:
                    event_data_batch = EventHub_Producer.create_batch()
                    event_data_batch.add(EventData(json_payload))
                    EventHub_Producer.send_batch(event_data_batch)
                except Exception as e:
                    print(f"[ERROR sending to Event Hub] {e}")

                # --- Save to CSV file ---
                csv_file.write(
                    f"{msg['device_id']},{msg['ts']},{msg['temperature_c']},"
                    f"{msg['humidity_pct']},{msg['battery_pct']}\n"
                )
                csv_file.flush()
                
                print("[PRODUCED]", msg)

            Kafka_Producer.flush()
            time.sleep(INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping producers...")
    finally:
        # --- Clean shutdown for ALL services ---
        print("Closing producers...")
        Kafka_Producer.close()
        EventHub_Producer.close()
        csv_file.close()

        # --- UPLOAD TO BLOB STORAGE (Milestone 2) ---
        print(f"[INFO] Uploading '{CSV_PATH}' to Azure Blob Storage...")
        
        # *** THIS IS THE FIX ***
        # We just check for the string and only try to upload if it exists.
        if AZURE_STORAGE_CONNECTION_STRING:
            try:
                blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
                blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=BLOB_NAME)
                
                with open(CSV_PATH, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                
                print("[INFO] Upload complete!")
            except Exception as e:
                print(f"[ERROR uploading to Blob] {e}")
        else:
            print(f"[ERROR] AZURE_STORAGE_CONNECTION_STRING not set. Cannot upload.")


# Run the main loop only if script is executed directly
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[Main ERROR] {e}")
    input("\nPress Enter to exit...")