import os
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import faust

# Environment variables with defaults
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
TOPIC_NAME = os.getenv("TOPIC_NAME", "wikipedia-events")
FILTERED_TOPIC_NAME = os.getenv("FILTERED_TOPIC_NAME", "filtered-wikipedia-events")
ES_INDEX = os.getenv("ES_INDEX", "filtered-wikipedia-events")

# Connect to Elasticsearch with retry
es = Elasticsearch([ES_HOST])

if es.ping():
    print("✅ Connected to Elasticsearch!")
else:
    print("❌ Elasticsearch connection failed!")

# Faust App initialization
app = faust.App('wikipedia-processor', broker=f'kafka://{KAFKA_BROKER}')

# Faust Record Schema
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

@app.agent(wiki_topic)
async def process_wiki(events):
    async for event in events:
        try:
            if not event.bot:
                await filtered_topic.send(value=event)
                print(f"✅ Processed and forwarded: {event.title} by {event.user}")

                # Send data to Elasticsearch
                doc = {
                    "title": event.title,
                    "user": event.user,
                    "comment": event.comment,
                    "timestamp": event.timestamp,
                    "wiki": event.wiki
                }
                try:
                    res = es.index(index=ES_INDEX, document=doc)
                    print(f"📡 Sent to Elasticsearch (ID: {res['_id']}): {event.title}")
                except es_exceptions.ElasticsearchException as es_err:
                    print(f"❌ Elasticsearch indexing failed: {es_err}")

        except Exception as e:
            print(f"⚠️ Processing error: {e}")

if __name__ == '__main__':
    app.main()
