
# 📡 Real-Time Wikipedia Streaming Pipeline using Kafka & Elasticsearch

## 📌 Project Title
**Read streaming events as messages from a Kafka topic and sink them to Elasticsearch using Kafka Connect.**

## 🧠 Abstract
This project implements a **scalable real-time data pipeline** that:
- Ingests live events (Wikipedia edits)
- Streams them to **Apache Kafka**
- Processes the events using a **Faust Stream Processor**
- Forwards the filtered data to **Elasticsearch** via **Kafka Connect**
- Enables observability with **Prometheus** and **Grafana**

It is built using **modular microservices**, containerized with **Docker**, orchestrated with **Kubernetes (KIND)**, and monitored via **metrics exporters**.

## ⚙️ Tech Stack
| Component            | Technology Used               |
|---------------------|-------------------------------|
| Ingestion           | Python (wiki_producer.py)     |
| Stream Processing   | Faust (wiki_stream_processor) |
| Messaging Queue     | Apache Kafka + Zookeeper      |
| Data Sink           | Elasticsearch (via Kafka Connect) |
| Monitoring          | Prometheus + Exporters        |
| Visualization       | Grafana                       |
| Containerization    | Docker                        |
| Orchestration       | Kubernetes (KIND)             |

## 🏗️ Architecture

Wikipedia Events → wiki_producer.py → Kafka → wiki_stream_processor.py  
                                    ↓                    ↓  
                           filtered-wikipedia-events → Kafka Connect → Elasticsearch  
                                                      ↑  
                           Prometheus & Exporters monitor all services  
                                                      ↓  
                                            Grafana Dashboards  

## 📂 Folder Structure

📁 HPE_CTY_PROJECT
├── 📁 jmx_exporter
│
├── 📁 manifests
│   ├── elasticsearch-exporter.yaml
│   ├── elasticsearch.yaml
│   ├── grafana-deployment.yaml
│   ├── kafka-connect-exporter.yaml
│   ├── kafka-connect.yaml
│   ├── kafka-exporter.yaml
│   ├── kafka-ui.yaml
│   ├── kafka-wiki-pipeline.yaml
│   ├── kafka.yaml
│   ├── kibana.yaml
│   ├── node-exporter.yaml
│   ├── prometheus-deployment.yaml
│   ├── wiki-processor.yaml
│   ├── wiki-producer.yaml
│   └── zookeeper.yaml
│
├── 📁 wiki_producer
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wiki_producer.py
│
├── 📁 wiki_stream_processor
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wiki_processor.py
│
├── docker-compose.yml
└── Makefile

## 🛠️ Setup Instructions

### 🔁 Prerequisites
- Docker
- KIND (Kubernetes in Docker)
- kubectl
- Python 3.8+
- DockerHub account (for image push)

### 🚀 Quickstart (via Makefile)
```bash
# Step 1: Create KIND cluster
make create-cluster

# Step 2: Deploy all services
make deploy

# Step 3: (Optional) Deploy Prometheus & Grafana
make deploy-prometheus

# Step 4: Access dashboards
make port-forward-prometheus  # Opens Prometheus at http://localhost:9090
make port-forward-grafana     # Opens Grafana at http://localhost:3002
make port-forward-kafka-ui    # Kafka UI at http://localhost:9000
make port-forward-kibana      # Kibana at http://localhost:5601
```

## 📈 Monitoring Setup

### Prometheus Targets (`prometheus.yml`)
```yaml
scrape_configs:
  - job_name: 'wiki-producer'
    static_configs:
      - targets: ['wiki-producer:8001']

  - job_name: 'wiki-stream-processor'
    static_configs:
      - targets: ['wiki-processor:8001']

  - job_name: 'kafka-exporter'
    static_configs:
      - targets: ['kafka-exporter:9308']

  - job_name: 'elasticsearch-exporter'
    static_configs:
      - targets: ['elasticsearch-exporter:9114']

  - job_name: 'node-exporters'
    static_configs:
      - targets: ['<node-ip>:9100']
```

### Grafana Dashboards
- Prometheus Data Source URL: `http://prometheus:9090`
- Import dashboards using JSON or ID:
  - Kafka Overview: `7589`
  - Elasticsearch: `1860`
  - Node Exporter: `1860`

## ✅ Expected Output

- Live Wikipedia edits streamed into Kafka
- Bot edits filtered out by stream processor
- Human edits indexed into Elasticsearch
- Dashboards reflecting:
  - Kafka message rate
  - Indexing stats
  - CPU/Memory usage
  - Custom producer/processor metrics

## 👥 Contributors
- **Amith M S Gowda** - 4VV22CS013  
- **Amrutha R** - 4VV22CS015  
- **Nagapriya N** - 4VV22IS061  
- **S Vinod Raj** - 4VV22CS128  
- **Sumukha S** - 4VV22CI110  

### 🧑‍🏫 Mentors
- **HPE:** Mr. Hareesh Joshi (hareesh.joshi@hpe.com)  
- **VVCE:** Dr. Vidyashree K P, Associate Professor, Dept. of ISE  

## 📚 References
- [Apache Kafka Docs](https://kafka.apache.org/documentation/)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/index.html)
- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [Faust Stream Processing](https://faust.readthedocs.io/)

## 📅 Project Timeline (Phases)
| Phase          | Description                          |
|----------------|--------------------------------------|
| Phase 1        | Docker Desktop Kubernetes            |
| Phase 2        | Minikube Migration                   |
| Phase 3        | Final deployment with KIND           |
| Final          | Monitoring with Prometheus + Grafana |
