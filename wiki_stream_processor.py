from elasticsearch import Elasticsearch
import  faust

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

app = faust.App('wikipedia-processor', broker='kafka://localhost:9092')

class WikiEvent(faust.Record, serializer='json'):
    title: str
    user: str
    comment: str
    timestamp: int
    bot: bool
    wiki: str

wiki_topic = app.topic('wikipedia-events', value_type=WikiEvent)
filtered_topic = app.topic('filtered-wikipedia-events', value_type=WikiEvent)

@app.agent(wiki_topic)
async def process_wiki(events):
    async for event in events:
        if not event.bot:
            await filtered_topic.send(value=event)
            print(f"✅ Processed: {event}")

            # Send data to Elasticsearch
            es.index(index="filtered-wikipedia-events", body={
                "title": event.title,
                "user": event.user,
                "comment": event.comment,
                "timestamp": event.timestamp,
                "wiki": event.wiki
            })
            print(f"📡 Sent to Elasticsearch: {event.title}")

if __name__ == '__main__':
    app.main()
