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
import time
import logging
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import faust
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wiki-processor')

# Environment variables with defaults
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")
APP_ID = os.getenv("FAUST_APP_ID", "wikipedia-processor")
METRICS_PORT = int(os.getenv("METRICS_PORT", 8001))

# Prometheus metrics
EVENTS_PROCESSED = Counter('wiki_processor_events_processed_total', 'Total events processed')
PROCESSING_ERRORS = Counter('wiki_processor_processing_errors_total', 'Total processing errors')
ES_INDEX_DURATION = Histogram('wiki_processor_es_index_duration_seconds', 'Elasticsearch indexing duration')
EVENT_LAG = Histogram('wiki_processor_event_lag_seconds', 'Event processing lag')
ES_CONNECTION_RETRIES = Counter('wiki_processor_es_connection_retries', 'ES connection retries')

# Faust App initialization
app = faust.App(
    APP_ID,
    broker=f'kafka://{KAFKA_BROKER}',
    web_port=METRICS_PORT,
    web_enabled=True
)

class WikiEvent(faust.Record, serializer='json'):
    title: str
    user: str
    comment: str
    timestamp: int
    bot: bool
    wiki: str

# Define topics
wiki_topic = app.topic(TOPIC_NAME, value_type=WikiEvent)
filtered_topic = app.topic(FILTERED_TOPIC_NAME, value_type=WikiEvent)

def connect_elasticsearch(retries=5, delay=5):
    """Connect to Elasticsearch with retry logic"""
    for attempt in range(retries):
        try:
            es = Elasticsearch(
                [ES_HOST],
                sniff_on_start=True,
                sniff_on_connection_fail=True,
                sniffer_timeout=60
            )
            if es.ping():
                logger.info("Connected to Elasticsearch at %s", ES_HOST)
                return es
            else:
                ES_CONNECTION_RETRIES.inc()
                logger.warning("Elasticsearch ping failed (%d/%d)", attempt+1, retries)
        except Exception as e:
            logger.error("Elasticsearch connection error: %s", e)
        time.sleep(delay)
    
    logger.error("Failed to connect to Elasticsearch after %d retries", retries)
    return None

def ensure_index_exists(es):
    """Ensure Elasticsearch index exists with proper mapping"""
    if not es.indices.exists(index=ES_INDEX):
        try:
            es.indices.create(
                index=ES_INDEX,
                body={
                    "mappings": {
                        "properties": {
                            "title": {"type": "text"},
                            "user": {"type": "keyword"},
                            "comment": {"type": "text"},
                            "timestamp": {"type": "date"},
                            "wiki": {"type": "keyword"}
                        }
                    }
                }
            )
            logger.info("Created Elasticsearch index: %s", ES_INDEX)
        except es_exceptions.ElasticsearchException as e:
            logger.error("Failed to create index: %s", e)

@app.agent(wiki_topic)
async def process_wiki(events):
    es = connect_elasticsearch()
    if not es:
        logger.error("Cannot start processing without Elasticsearch connection")
        return
    
    ensure_index_exists(es)
    
    async for event in events:
        try:
            if event.bot:
                logger.debug("Skipping bot edit: %s", event.title)
                continue

            # Calculate processing lag
            event_time = datetime.fromtimestamp(event.timestamp)
            processing_lag = (datetime.utcnow() - event_time).total_seconds()
            EVENT_LAG.observe(processing_lag)

            # Forward to filtered topic
            await filtered_topic.send(value=event)
            logger.debug("Forwarded: %s by %s", event.title, event.user)

            # Convert timestamp to IST
            ist_timestamp = event_time + timedelta(hours=5, minutes=30)
            
            # Prepare document
            doc = {
                "title": event.title,
                "user": event.user,
                "comment": event.comment,
                "timestamp": ist_timestamp,
                "wiki": event.wiki,
                "processing_lag_seconds": processing_lag
            }

            # Index to Elasticsearch with timing
            start_time = time.time()
            try:
                res = es.index(index=ES_INDEX, document=doc)
                ES_INDEX_DURATION.observe(time.time() - start_time)
                EVENTS_PROCESSED.inc()
                
                logger.debug("Indexed to ES (ID: %s): %s", 
                            res['_id'], event.title)
            except es_exceptions.ElasticsearchException as e:
                PROCESSING_ERRORS.inc()
                logger.error("ES indexing error: %s", e)

        except Exception as e:
            PROCESSING_ERRORS.inc()
            logger.error("Processing error: %s", e)

@app.timer(interval=60.0)
async def health_check():
    """Periodic health check"""
    try:
        # Test Kafka connection
        await app.producer.client.list_topics()
        
        # Test Elasticsearch connection
        es = connect_elasticsearch(retries=1, delay=0)
        if not es or not es.ping():
            raise RuntimeError("Elasticsearch connection failed")
            
        logger.info("Health check passed")
    except Exception as e:
        logger.error("Health check failed: %s", e)

if __name__ == '__main__':
    app.main()
