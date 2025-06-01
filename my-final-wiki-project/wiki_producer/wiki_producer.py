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
# import os
# import json
# import time
# import requests
# from kafka import KafkaProducer, errors
# from sseclient import SSEClient

# # Environment variables with defaults
# TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

# def connect_kafka_producer(retries=5, delay=5):
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
#     producer = connect_kafka_producer()
#     if not producer:
#         return

#     print("🔄 Listening to Wikipedia events...")
#     try:
#         while True:
#             try:
#                 response = requests.get(WIKI_STREAM_URL, stream=True)
#                 if response.status_code != 200:
#                     print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
#                     time.sleep(5)
#                     continue

#                 client = SSEClient(response)

#                 for event in client.events():
#                     if event.event != "message" or not event.data.strip():
#                         continue

#                     try:
#                         change = json.loads(event.data)

#                         if change.get("type") == "edit":
#                             # Do NOT convert timestamp to IST here — send raw
#                             print(f"✍ Sending: {change.get('title')} by {change.get('user')}")
#                             future = producer.send(TOPIC_NAME, value=change)

#                             try:
#                                 metadata = future.get(timeout=10)
#                                 print(f"✅ Kafka: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
#                             except Exception as e:
#                                 print(f"❌ Kafka send error: {e}")

#                             producer.flush()

#                     except json.JSONDecodeError as e:
#                         print(f"⚠️ JSON decode error: {e} | Data: {event.data}")

#                 client.close()

#             except requests.exceptions.RequestException as e:
#                 print(f"❌ Request failed: {e}. Retrying in 5 seconds...")
#                 time.sleep(5)

#     except KeyboardInterrupt:
#         print("\n🛑 Stopped by user. Closing producer...")
#         producer.close()

# if __name__ == "__main__":
#     stream_wikipedia_events()


import os
import json
import time
import requests
from kafka import KafkaProducer, errors
from sseclient import SSEClient
from prometheus_client import start_http_server, Counter
from prometheus_client import start_http_server
start_http_server(8000)

# Metrics
events_sent = Counter('wiki_events_sent_total', 'Total Wikipedia events sent to Kafka')
errors_encountered = Counter('wiki_producer_errors_total', 'Total errors encountered in wiki producer')

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# Environment variables
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
WIKI_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

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
            errors_encountered.inc()
            time.sleep(delay)
    print("🔥 Exiting: No Kafka connection after retries.")
    return None

def stream_wikipedia_events():
    producer = connect_kafka_producer()
    if not producer:
        return

    print("🔄 Listening to Wikipedia events...")
    try:
        while True:
            try:
                response = requests.get(WIKI_STREAM_URL, stream=True)
                if response.status_code != 200:
                    print(f"❌ Failed to connect to Wikipedia stream: {response.status_code}")
                    errors_encountered.inc()
                    time.sleep(5)
                    continue

                client = SSEClient(response)

                for event in client.events():
                    if event.event != "message" or not event.data.strip():
                        continue

                    try:
                        change = json.loads(event.data)

                        if change.get("type") == "edit":
                            print(f"✍ Sending: {change.get('title')} by {change.get('user')}")
                            future = producer.send(TOPIC_NAME, value=change)
                            events_sent.inc()

                            try:
                                metadata = future.get(timeout=10)
                                print(f"✅ Kafka: {metadata.topic} | Partition: {metadata.partition} | Offset: {metadata.offset}")
                            except Exception as e:
                                print(f"❌ Kafka send error: {e}")
                                errors_encountered.inc()

                            producer.flush()

                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON decode error: {e} | Data: {event.data}")
                        errors_encountered.inc()

                client.close()

            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed: {e}. Retrying in 5 seconds...")
                errors_encountered.inc()
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user. Closing producer...")
        producer.close()

if __name__ == "__main__":
    stream_wikipedia_events()
