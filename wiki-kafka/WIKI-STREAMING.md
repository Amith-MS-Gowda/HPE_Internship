# 📰 Wiki-Kafka Pipeline Project

## 📖 Overview

This project implements a real-time streaming pipeline using Kafka to ingest and process Wikipedia edit events. The processed data is streamed into Elasticsearch for indexing and visualized via Kibana dashboards. The whole system is containerized using Docker and deployed on Kubernetes.

## 🏗️ Features

- Kafka Producer for streaming Wikipedia edit events
- Kafka Stream Processor for transforming and filtering events
- Kafka Connect to integrate with Elasticsearch
- Elasticsearch for data indexing
- Kibana dashboard for visualizing Wikipedia edits
- Kubernetes manifests for end-to-end deployment
- Kafka UI for topic monitoring
- Scalable and cloud-ready deployment pipeline

---

## 📂 Project Structure

```
wiki-kafka/
├── .idea/                           # IDE config files
├── docker-compose.yml               # Docker Compose to bootstrap services
├── k8s/                             # Kubernetes deployment YAMLs
│   ├── elasticsearch.yaml
│   ├── kafka.yaml
│   ├── zookeeper.yaml
│   ├── kafka-connect.yaml
│   ├── kafka-ui.yaml
│   ├── kibana.yaml
│   ├── wiki-producer.yaml
│   ├── wiki-processor.yaml
│   └── kafka-wiki-pipeline.yaml     # Optional full pipeline orchestration
├── wiki_producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wiki_producer.py
├── wiki_stream_processor/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── wiki_stream_processor.py
└── .gitignore
```

---

## 🚀 Workflow Steps

1. **Developed Kafka producer** to stream Wikipedia events using Python.
2. **Created Kafka stream processor** using Faust to filter and enrich events.
3. **Built Docker images** for both producer and stream processor.
4. **Defined Kubernetes manifests** for:
    - Kafka, Zookeeper, Kafka Connect, Kafka UI
    - Elasticsearch and Kibana
    - Custom Wiki producer and processor
5. **Pushed all files via GitHub Pull Request** to the `HPE_Internship` repository.
6. **Merged PR** to the main repo after code review.
7. **Next step (Planned):**
    - Integrate Twitter streaming with Kafka (via a Twitter producer).
    - Deploy the full pipeline to a cloud provider (e.g., AWS, GCP, Azure).
  
---

## 📦 Technologies Used

- **Kafka & Zookeeper** (Streaming backbone)
- **Faust (Python)** (Stream processing)
- **Kafka Connect** (Data sink to Elasticsearch)
- **Elasticsearch & Kibana** (Search & visualization)
- **Kubernetes** (Orchestration)
- **Docker** (Containerization)
- **Kafka UI** (Kafka topics monitoring)
- **GitHub** (Version control & PR management)

---
## 🐳 Docker Build & Push Commands

### 🔹 Producer Service

```bash
cd wiki_producer/
docker build -t amithgowda/wiki-producer:latest .
docker push amithgowda/wiki-producer:latest
```

### 🔹 Processor Service

```bash
cd wiki_stream_processor/
docker build -t amithgowda/wiki-processor:latest .
docker push amithgowda/wiki-processor:latest
```

⚠️ Replace `amithgowda` with your DockerHub username.

---

## ✅ Kubernetes Deployment (K8s)

```bash
kubectl apply -f k8s/zookeeper.yaml
kubectl apply -f k8s/kafka.yaml
kubectl apply -f k8s/kafka-connect.yaml
kubectl apply -f k8s/kafka-ui.yaml
kubectl apply -f k8s/elasticsearch.yaml
kubectl apply -f k8s/kibana.yaml
kubectl apply -f k8s/wiki-producer.yaml
kubectl apply -f k8s/wiki-processor.yaml

TO APPLY EVERYTHING USING SINGLE COMMAND USE:  kubectl apply -f .
```

---

## 🩺 Check Deployment Status

### 🔸 Check all Pods status:

```bash
kubectl get pods
```

---

## 📜 View Logs in Terminal

### 🔹 Producer Logs:

```bash
kubectl logs -f deployment/wiki-producer
```

### 🔹 Processor Logs:

```bash
kubectl logs -f deployment/wiki-processor
```

---

## 🔍 Access Kibana Dashboard

Once Kibana is running, forward the port to access the UI locally:

```bash
kubectl port-forward service/kibana 5601:5601
```

👉 Open [http://localhost:5601](http://localhost:5601) to visualize Wikipedia edit events in real-time.

---

## 🗺️ Next Milestone

- Integrate Twitter streaming as another Kafka producer.
- Deploy the entire architecture to the cloud.
- Implement autoscaling and CI/CD pipelines.

---

## 🤝 Contribution

Feel free to fork, improve, or open PRs. This is an internal internship project under active development.
