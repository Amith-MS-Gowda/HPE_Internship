
import json
import requests
from kafka import KafkaProducer, errors
from sseclient import SSEClient

TOPIC_NAME = "wikipedia-events"
KAFKA_BROKER = "localhost:9092"
WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

def connect_kafka_producer():
    """Initialize Kafka producer with error handling"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print(" Connected to Kafka!")
        return producer
    except errors.NoBrokersAvailable as e:
        print(f" Kafka connection failed: {e}")
        return None

def stream_wikipedia_events():
    """Stream Wikipedia events and send them to Kafka"""
    producer = connect_kafka_producer()
    if not producer:
        print(" Exiting: No Kafka connection.")
        return

    print("Listening to Wikipedia events...")
    try:
        response = requests.get(WIKI_STREAM_URL, stream=True)
        if response.status_code != 200:
            print(f" Failed to connect to Wikipedia stream: {response.status_code}")
            return
        client = SSEClient(response)
        for event in client.events():
            if event.event == "message":
                try:
                    if not event.data.strip():
                        print(" Received empty data, skipping...")
                        continue

                    change = json.loads(event.data)
                    print(f" Received: {change}")  # Debugging

                    if change.get("type") == "edit":
                        print(f" Sending to Kafka: {change['title']} edited by {change['user']}")
                        # producer.send(TOPIC_NAME, value=change)
                        future = producer.send(TOPIC_NAME, value=change)
                        try:
                            metadata = future.get(timeout=10)  # Wait for confirmation
                            print(f"✅ Message sent: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
                        except Exception as e:
                            print(f"❌ Kafka send error: {e}")

                        producer.flush()  # Ensure messages are sent immediately

                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e} - Data: {event.data}")
                    continue
        client.close()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    stream_wikipedia_events()
