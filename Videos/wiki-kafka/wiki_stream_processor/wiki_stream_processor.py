import os
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import faust
from prometheus_client import start_http_server, Counter
from datetime import datetime, timezone, timedelta

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")

# Connect to Elasticsearch
es = Elasticsearch([ES_HOST])
if es.ping():
    print("✅ Connected to Elasticsearch!")
else:
    print("❌ Elasticsearch connection failed!")

# Define Faust app
app = faust.App('wikipedia-processor', broker=f'kafka://{KAFKA_BROKER}')

# Prometheus metrics
events_processed = Counter("wiki_events_processed_total", "Total events processed")
events_indexed = Counter("wiki_events_indexed_total", "Total events indexed to Elasticsearch")

# Start Prometheus metrics server on port 8001
start_http_server(8001)

# Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Faust record schema
class WikiEvent(faust.Record, serializer='json'):
    title: str
    user: str
    comment: str
    timestamp: int
    bot: bool
    wiki: str

# Topics
wiki_topic = app.topic(TOPIC_NAME, value_type=WikiEvent)
filtered_topic = app.topic(FILTERED_TOPIC_NAME, value_type=WikiEvent)

# Agent to process wiki events
@app.agent(wiki_topic)
async def process_wiki(events):
    async for event in events:
        try:
            if not event.bot:
                await filtered_topic.send(value=event)
                events_processed.inc()

                # Convert UNIX timestamp to IST 24-hour format string
                ist_time = datetime.fromtimestamp(event.timestamp, IST).strftime("%Y-%m-%d %H:%M:%S")

                doc = {
                    "title": event.title,
                    "user": event.user,
                    "comment": event.comment,
                    "timestamp": ist_time,  # ✅ Human-readable IST format
                    "wiki": event.wiki
                }

                try:
                    res = es.index(index=ES_INDEX, document=doc)
                    print(f"📡 Indexed to Elasticsearch (ID: {res['_id']}): {event.title}")
                    events_indexed.inc()
                except es_exceptions.ElasticsearchException as es_err:
                    print(f"❌ Elasticsearch indexing failed: {es_err}")
        except Exception as e:
            print(f"⚠️ Processing error: {e}")

# Run app
if __name__ == '__main__':
    app.main()
