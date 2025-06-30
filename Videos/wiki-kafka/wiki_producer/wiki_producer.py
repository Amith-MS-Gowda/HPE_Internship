# wiki_producer.py

import os
import json
import time
import requests
from kafka import KafkaProducer, errors
from sseclient import SSEClient
from elasticsearch import Elasticsearch
from prometheus_client import start_http_server, Counter

TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# Prometheus metric
events_produced = Counter("wiki_events_produced_total", "Total Wikipedia events produced")

es = Elasticsearch([ES_HOST])

def connect_kafka_producer(retries=5, delay=5):
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Connected to Kafka!")
            return producer
        except errors.NoBrokersAvailable as e:
            print(f"❌ Kafka connection failed ({i+1}/{retries}): {e}")
            time.sleep(delay)
    print("🔥 Exiting: No Kafka connection after retries.")
    return None

def stream_wikipedia_events():
    producer = connect_kafka_producer()
    if not producer:
        return

    print("🔄 Listening to Wikipedia events...")
    start_http_server(8000)  # Prometheus metrics exposed on port 8000

    try:
        response = requests.get(WIKI_STREAM_URL, stream=True)
        if response.status_code != 200:
            print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
            return

        client = SSEClient(response)

        for event in client.events():
            if event.event == "message":
                try:
                    if not event.data.strip():
                        continue

                    change = json.loads(event.data)

                    if change.get("type") == "edit":
                        print(f"✍ Sending to Kafka: {change['title']} edited by {change['user']}")
                        producer.send(TOPIC_NAME, value=change)
                        events_produced.inc()
                        producer.flush()

                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON Decode Error: {e} - Data: {event.data}")
                    continue

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    stream_wikipedia_events()
