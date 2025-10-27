# consumer.py  (Kafka consumer for IoT messages)
# ------------------------------------------------
# This script connects to Kafka and listens to the topic "iotsensors".
# Whenever a new message arrives (sent by generator.py), it prints it to the console.
#
# Flow overview:
#   messages produced by generator.py ──> Kafka broker with topic "iotsensors"  ──> messages consumed here by consumer.py
#
# Think of it like a subscriber in a "publish-subscribe" system:
#   - generator.py publishes (produces) data
#   - consumer.py subscribes (consumes) data

try:
    # Import Kafka consumer library and JSON to decode messages
    from kafka import KafkaConsumer
    import json

    # 1. Create a KafkaConsumer instance
    Kafka_Consumer = KafkaConsumer(
        "iotsensors",                                                           # topic name to subscribe to
        bootstrap_servers="localhost:9092",                                     # where Kafka broker is running
        auto_offset_reset="latest",                                             # start from newest messages# (use "earliest" to read backlog)
        value_deserializer=lambda message: json.loads(message.decode("utf-8")), # convert bytes → JSON → dict
        group_id="iot group readers",                                           # consumer group name (for load balancing)
    )

    # 2. Ready to receive data
    print("[INFO] Waiting for messages...")

    # 3. Infinite loop: this waits for messages forever
    for msg in Kafka_Consumer:
        # msg.value is the actual JSON dict we produced in generator.py
        print("[CONSUMED]", msg.value)

except Exception as e:
    # If anything goes wrong (e.g., Kafka not running), print the error
    print(f"[ERROR] {e}")

# Keep window open so user can read errors/info before closing
input("Press Enter to exit...")
