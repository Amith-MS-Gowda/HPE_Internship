# import os
# from elasticsearch import Elasticsearch, exceptions as es_exceptions
# import faust

# # Environment variables with defaults
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
# TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
# ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")

# # Connect to Elasticsearch with retry
# es = Elasticsearch([ES_HOST])

# if es.ping():
#     print("✅ Connected to Elasticsearch!")
# else:
#     print("❌ Elasticsearch connection failed!")

# # Faust App initialization
# app = faust.App('wikipedia-processor', broker=f'kafka://{KAFKA_BROKER}')

# # Faust Record Schema
# class WikiEvent(faust.Record, serializer='json'):
#     title: str
#     user: str
#     comment: str
#     timestamp: int
#     bot: bool
#     wiki: str

# # Define topics
# wiki_topic = app.topic(TOPIC_NAME, value_type=WikiEvent)
# filtered_topic = app.topic(FILTERED_TOPIC_NAME, value_type=WikiEvent)

# @app.agent(wiki_topic)
# async def process_wiki(events):
#     async for event in events:
#         try:
#             if not event.bot:
#                 await filtered_topic.send(value=event)
#                 print(f"✅ Processed and forwarded: {event.title} by {event.user}")

#                 # Send data to Elasticsearch
#                 doc = {
#                     "title": event.title,
#                     "user": event.user,
#                     "comment": event.comment,
#                     "timestamp": event.timestamp,
#                     "wiki": event.wiki
#                 }
#                 try:
#                     res = es.index(index=ES_INDEX, document=doc)
#                     print(f"📡 Sent to Elasticsearch (ID: {res['_id']}): {event.title}")
#                 except es_exceptions.ElasticsearchException as es_err:
#                     print(f"❌ Elasticsearch indexing failed: {es_err}")

#         except Exception as e:
#             print(f"⚠️ Processing error: {e}")

# if __name__ == '__main__':
#     app.main()


# import os
# from elasticsearch import Elasticsearch, exceptions as es_exceptions
# import faust
# from datetime import datetime, timedelta

# # Environment variables with defaults
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
# TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
# FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
# ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")

# # Connect to Elasticsearch with retry
# es = Elasticsearch([ES_HOST])

# if es.ping():
#     print("✅ Connected to Elasticsearch!")
# else:
#     print("❌ Elasticsearch connection failed!")

# # Faust App initialization
# app = faust.App('wikipedia-processor', broker=f'kafka://{KAFKA_BROKER}')

# # Faust Record Schema
# class WikiEvent(faust.Record, serializer='json'):
#     title: str
#     user: str
#     comment: str
#     timestamp: int
#     bot: bool
#     wiki: str

# # Define topics
# wiki_topic = app.topic(TOPIC_NAME, value_type=WikiEvent)
# filtered_topic = app.topic(FILTERED_TOPIC_NAME, value_type=WikiEvent)

# # Helper function to convert timestamp to IST
# def convert_to_ist(timestamp):
#     """Convert UTC timestamp to IST (Indian Standard Time)"""
#     utc_time = datetime.utcfromtimestamp(timestamp)
#     ist_time = utc_time + timedelta(hours=5, minutes=30)
#     return ist_time.strftime('%Y-%m-%d %H:%M:%S')

# @app.agent(wiki_topic)
# async def process_wiki(events):
#     async for event in events:
#         try:
#             if not event.bot:
#                 await filtered_topic.send(value=event)
#                 print(f"✅ Processed and forwarded: {event.title} by {event.user}")

#                 # Convert the timestamp to IST before sending to Elasticsearch
#                 ist_timestamp = convert_to_ist(event.timestamp)

#                 # Send data to Elasticsearch with IST timestamp
#                 doc = {
#                     "title": event.title,
#                     "user": event.user,
#                     "comment": event.comment,
#                     "timestamp": ist_timestamp,  # Use converted IST timestamp
#                     "wiki": event.wiki
#                 }
#                 try:
#                     res = es.index(index=ES_INDEX, document=doc)
#                     print(f"📡 Sent to Elasticsearch (ID: {res['_id']}): {event.title}")
#                 except es_exceptions.ElasticsearchException as es_err:
#                     print(f"❌ Elasticsearch indexing failed: {es_err}")

#         except Exception as e:
#             print(f"⚠️ Processing error: {e}")

# if __name__ == '__main__':
#     app.main()
import os
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import faust
from datetime import datetime, timedelta
import time

# Environment variables with defaults
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")
APP_ID = os.getenv("FAUST_APP_ID", "wikipedia-processor")

# Connect to Elasticsearch with retry
def connect_elasticsearch(retries=5, delay=5):
    for attempt in range(retries):
        try:
            es = Elasticsearch([ES_HOST])
            if es.ping():
                print("✅ Connected to Elasticsearch!")
                return es
            else:
                print(f"❌ Elasticsearch ping failed ({attempt+1}/{retries})")
        except Exception as e:
            print(f"❌ Elasticsearch connection error: {e}")
        time.sleep(delay)
    print("🔥 Exiting: Could not connect to Elasticsearch.")
    return None

es = connect_elasticsearch()
if not es:
    exit(1)

# Faust App initialization
app = faust.App(APP_ID, broker=f'kafka://{KAFKA_BROKER}')

# Faust Record Schema
class WikiEvent(faust.Record, serializer='json'):
    title: str
    user: str
    comment: str
    timestamp: int  # Now it's a raw UNIX timestamp
    bot: bool
    wiki: str

# Define topics
wiki_topic = app.topic(TOPIC_NAME, value_type=WikiEvent)
filtered_topic = app.topic(FILTERED_TOPIC_NAME, value_type=WikiEvent)

# Convert timestamp to IST
def convert_to_ist(timestamp):
    try:
        utc_time = datetime.utcfromtimestamp(timestamp)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"⚠️ Timestamp conversion failed: {e}")
        return str(timestamp)

@app.agent(wiki_topic)
async def process_wiki(events):
    async for event in events:
        try:
            if not event.bot:
                await filtered_topic.send(value=event)
                print(f"✅ Forwarded to topic: {event.title} by {event.user}")

                # Convert to IST here
                ist_timestamp = convert_to_ist(event.timestamp)

                doc = {
                    "title": event.title,
                    "user": event.user,
                    "comment": event.comment,
                    "timestamp": ist_timestamp,
                    "wiki": event.wiki,
                }

                try:
                    res = es.index(index=ES_INDEX, document=doc)
                    print(f"📡 Indexed to Elasticsearch (ID: {res['_id']}): {event.title}")
                except es_exceptions.ElasticsearchException as es_err:
                    print(f"❌ Elasticsearch indexing error: {es_err}")

        except Exception as e:
            print(f"⚠️ Processing error: {e}")

if __name__ == '__main__':
    app.main()
