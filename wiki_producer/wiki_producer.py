# # import os
# # import json
# # import time
# # import requests
# # from kafka import KafkaProducer, errors
# # from sseclient import SSEClient
# # from elasticsearch import Elasticsearch

# # # Environment variables with defaults
# # TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# # KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# # WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
# # ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# # # Optional Elasticsearch client if needed
# # es = Elasticsearch([ES_HOST])

# # def connect_kafka_producer(retries=5, delay=5):
# #     """Initialize Kafka producer with retry logic"""
# #     for i in range(retries):
# #         try:
# #             producer = KafkaProducer(
# #                 bootstrap_servers=KAFKA_BROKER,
# #                 value_serializer=lambda v: json.dumps(v).encode("utf-8")
# #             )
# #             print("✅ Connected to Kafka!")
# #             return producer
# #         except errors.NoBrokersAvailable as e:
# #             print(f"❌ Kafka connection failed ({i+1}/{retries}): {e}")
# #             time.sleep(delay)
# #     print("🔥 Exiting: No Kafka connection after retries.")
# #     return None

# # def stream_wikipedia_events():
# #     """Stream Wikipedia events and send them to Kafka"""
# #     producer = connect_kafka_producer()
# #     if not producer:
# #         return

# #     print("🔄 Listening to Wikipedia events...")
# #     try:
# #         response = requests.get(WIKI_STREAM_URL, stream=True)
# #         if response.status_code != 200:
# #             print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
# #             return

# #         client = SSEClient(response)  # <- FIXED LINE
        
# #         for event in client.events():
# #             if event.event == "message":
# #                 try:
# #                     if not event.data.strip():
# #                         continue

# #                     change = json.loads(event.data)

# #                     if change.get("type") == "edit":
# #                         print(f"✍ Sending to Kafka: {change['title']} edited by {change['user']}")
# #                         future = producer.send(TOPIC_NAME, value=change)
# #                         try:
# #                             metadata = future.get(timeout=10)
# #                             print(f"✅ Message sent: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
# #                         except Exception as e:
# #                             print(f"❌ Kafka send error: {e}")

# #                         producer.flush()

# #                 except json.JSONDecodeError as e:
# #                     print(f"⚠️ JSON Decode Error: {e} - Data: {event.data}")
# #                     continue

# #         client.close()
# #         producer.close()

# #     except requests.exceptions.RequestException as e:
# #         print(f"❌ Request failed: {e}")

# # if __name__ == "__main__":
# #     stream_wikipedia_events()

# import os
# import json
# import time
# import requests
# from kafka import KafkaProducer, errors
# from sseclient import SSEClient
# from elasticsearch import Elasticsearch

# # Environment variables with defaults
# TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
# ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# # Optional Elasticsearch client if needed
# es = Elasticsearch([ES_HOST])

# def connect_kafka_producer(retries=5, delay=5):
#     """Initialize Kafka producer with retry logic"""
#     for i in range(retries):
#         try:
#             producer = KafkaProducer(
#                 bootstrap_servers=KAFKA_BROKER,
#                 value_serializer=lambda v: json.dumps(v).encode("utf-8")
#             )
#             print("✅ Connected to Kafka!")
#             return producer
#         except errors.NoBrokersAvailable as e:
#             print(f"❌ Kafka connection failed ({i+1}/{retries}): {e}")
#             time.sleep(delay)
#     print("🔥 Exiting: No Kafka connection after retries.")
#     return None

# def stream_wikipedia_events():
#     """Stream Wikipedia events and send them to Kafka"""
#     producer = connect_kafka_producer()
#     if not producer:
#         return

#     print("🔄 Listening to Wikipedia events...")
#     while True:
#         try:
#             response = requests.get(WIKI_STREAM_URL, stream=True)
#             if response.status_code != 200:
#                 print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
#                 time.sleep(5)  # Retry after 5 seconds
#                 continue

#             client = SSEClient(response)  # <- FIXED LINE

#             for event in client.events():
#                 if event.event == "message":
#                     try:
#                         if not event.data.strip():
#                             continue

#                         change = json.loads(event.data)

#                         if change.get("type") == "edit":
#                             print(f"✍ Sending to Kafka: {change['title']} edited by {change['user']}")
#                             future = producer.send(TOPIC_NAME, value=change)
#                             try:
#                                 metadata = future.get(timeout=10)
#                                 print(f"✅ Message sent: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
#                             except Exception as e:
#                                 print(f"❌ Kafka send error: {e}")

#                             producer.flush()

#                     except json.JSONDecodeError as e:
#                         print(f"⚠️ JSON Decode Error: {e} - Data: {event.data}")
#                         continue

#             client.close()

#         except requests.exceptions.RequestException as e:
#             print(f"❌ Request failed: {e}")
#             time.sleep(5)  # Retry after 5 seconds if request fails

# if __name__ == "__main__":
#     stream_wikipedia_events()

# import os
# import json
# import time
# import requests
# from kafka import KafkaProducer, errors
# from sseclient import SSEClient
# from elasticsearch import Elasticsearch
# from datetime import datetime, timedelta

# # Environment variables with defaults
# TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
# ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# # Optional Elasticsearch client if needed
# es = Elasticsearch([ES_HOST])

# def connect_kafka_producer(retries=5, delay=5):
#     """Initialize Kafka producer with retry logic"""
#     for i in range(retries):
#         try:
#             producer = KafkaProducer(
#                 bootstrap_servers=KAFKA_BROKER,
#                 value_serializer=lambda v: json.dumps(v).encode("utf-8")
#             )
#             print("✅ Connected to Kafka!")
#             return producer
#         except errors.NoBrokersAvailable as e:
#             print(f"❌ Kafka connection failed ({i+1}/{retries}): {e}")
#             time.sleep(delay)
#     print("🔥 Exiting: No Kafka connection after retries.")
#     return None

# def convert_to_ist(timestamp):
#     """Convert UTC timestamp to IST (Indian Standard Time)"""
#     utc_time = datetime.utcfromtimestamp(timestamp)
#     ist_time = utc_time + timedelta(hours=5, minutes=30)
#     return ist_time.strftime('%Y-%m-%d %H:%M:%S')

# def stream_wikipedia_events():
#     """Stream Wikipedia events and send them to Kafka"""
#     producer = connect_kafka_producer()
#     if not producer:
#         return

#     print("🔄 Listening to Wikipedia events...")
#     while True:
#         try:
#             response = requests.get(WIKI_STREAM_URL, stream=True)
#             if response.status_code != 200:
#                 print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
#                 time.sleep(5)  # Retry after 5 seconds
#                 continue

#             client = SSEClient(response)  # <- FIXED LINE

#             for event in client.events():
#                 if event.event == "message":
#                     try:
#                         if not event.data.strip():
#                             continue

#                         change = json.loads(event.data)

#                         if change.get("type") == "edit":
#                             # Convert the timestamp to IST before sending to Kafka
#                             if "timestamp" in change:
#                                 timestamp = change["timestamp"]
#                                 ist_timestamp = convert_to_ist(timestamp)
#                                 change["timestamp"] = ist_timestamp

#                             print(f"✍ Sending to Kafka: {change['title']} edited by {change['user']}")
#                             future = producer.send(TOPIC_NAME, value=change)
#                             try:
#                                 metadata = future.get(timeout=10)
#                                 print(f"✅ Message sent: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
#                             except Exception as e:
#                                 print(f"❌ Kafka send error: {e}")

#                             producer.flush()

#                     except json.JSONDecodeError as e:
#                         print(f"⚠️ JSON Decode Error: {e} - Data: {event.data}")
#                         continue

#             client.close()

#         except requests.exceptions.RequestException as e:
#             print(f"❌ Request failed: {e}")
#             time.sleep(5)  # Retry after 5 seconds if request fails

# if __name__ == "__main__":
#     stream_wikipedia_events()
import os
import json
import time
import logging
from datetime import datetime
import requests
from kafka import KafkaProducer, errors
from sseclient import SSEClient
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wiki-producer')

# Environment variables with defaults
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
METRICS_PORT = int(os.getenv("METRICS_PORT", 8000))

# Prometheus metrics
EVENTS_SENT = Counter('wiki_producer_events_sent_total', 'Total events sent to Kafka')
SEND_ERRORS = Counter('wiki_producer_send_errors_total', 'Total event send errors')
PRODUCE_LATENCY = Histogram('wiki_producer_latency_seconds', 'Event produce latency')
EVENT_AGE = Histogram('wiki_producer_event_age_seconds', 'Age of events when received')
CONNECTION_RETRIES = Counter('wiki_producer_connection_retries_total', 'Connection retry attempts')

def connect_kafka_producer(retries=5, delay=5):
    """Connect to Kafka with retry logic"""
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks='all',
                retries=3
            )
            logger.info("Connected to Kafka at %s", KAFKA_BROKER)
            return producer
        except errors.NoBrokersAvailable as e:
            CONNECTION_RETRIES.inc()
            logger.warning("Kafka connection failed (%d/%d): %s", i+1, retries, e)
            time.sleep(delay)
    
    logger.error("Failed to connect to Kafka after %d retries", retries)
    return None

def stream_wikipedia_events():
    """Main event streaming loop"""
    # Start metrics server
    start_http_server(METRICS_PORT)
    logger.info("Metrics server started on port %d", METRICS_PORT)

    producer = connect_kafka_producer()
    if not producer:
        return

    logger.info("Listening to Wikipedia events from %s", WIKI_STREAM_URL)
    
    while True:
        try:
            response = requests.get(WIKI_STREAM_URL, stream=True, timeout=30)
            if response.status_code != 200:
                logger.error("Wikipedia stream connection failed: HTTP %d", response.status_code)
                time.sleep(5)
                continue

            client = SSEClient(response)
            
            for event in client.events():
                if event.event != "message" or not event.data.strip():
                    continue

                try:
                    change = json.loads(event.data)
                    
                    if change.get("type") == "edit":
                        # Calculate event age (current time - event timestamp)
                        event_time = datetime.fromtimestamp(change.get('timestamp', time.time()))
                        event_age = (datetime.utcnow() - event_time).total_seconds()
                        EVENT_AGE.observe(event_age)
                        
                        logger.debug("Processing edit: %s by %s", 
                                    change.get('title'), change.get('user'))
                        
                        # Send to Kafka with timing
                        start_time = time.time()
                        future = producer.send(TOPIC_NAME, value=change)
                        
                        try:
                            metadata = future.get(timeout=10)
                            PRODUCE_LATENCY.observe(time.time() - start_time)
                            EVENTS_SENT.inc()
                            
                            logger.debug("Sent to Kafka - Topic: %s, Partition: %d, Offset: %d",
                                        metadata.topic, metadata.partition, metadata.offset)
                        except Exception as e:
                            SEND_ERRORS.inc()
                            logger.error("Failed to send message to Kafka: %s", e)
                            
                        producer.flush()

                except json.JSONDecodeError as e:
                    logger.error("JSON decode error: %s - Data: %s", e, event.data[:100])
                except Exception as e:
                    logger.error("Unexpected error processing event: %s", e)

        except requests.exceptions.RequestException as e:
            logger.error("Wikipedia stream error: %s. Retrying in 5 seconds...", e)
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Shutting down producer...")
            producer.close()
            break
        except Exception as e:
            logger.error("Unexpected error: %s. Restarting stream...", e)
            time.sleep(5)

if __name__ == "__main__":
    stream_wikipedia_events()
