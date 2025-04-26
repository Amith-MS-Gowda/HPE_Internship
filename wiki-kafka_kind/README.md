# 📚 Wiki_Kafka_Kind Pipeline Project
This project implements a real-time streaming pipeline using Kafka to ingest and process Wikipedia edit events. The processed data is streamed into Elasticsearch for indexing and visualized via Kibanadashboards. The entire system is containerized using Docker and deployed locally using KIND (Kubernetes in Docker) for orchestration.

## 🏗️ Features

- Kafka Producer for streaming Wikipedia edit events  
- Kafka Stream Processor for transforming and filtering events  
- Kafka Connect to integrate with Elasticsearch  
- Elasticsearch for data indexing  
- Kibana dashboard for visualizing Wikipedia edits  
- Kubernetes manifests for end-to-end deployment  
- Kafka UI for topic monitoring  
- Scalable and cloud-ready deployment pipeline  
- Prometheus and Grafana integration for real-time monitoring  
- JMX Exporter sidecar container added to Kafka Connect for exposing metrics  

## 🚀 Setup Instructions

Follow these steps to set up and run the project locally using KIND and Docker.

### ✅ Prerequisites

Ensure the following tools are installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [KIND](https://kind.sigs.k8s.io/)
- [Helm](https://helm.sh/docs/intro/install/) *(optional)*
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 📁 Step 1: Clone Repository & Set up KIND Cluster

Clone the repository:

```bash
git clone <url>
cd wiki-kafka_kind
```

### 🧱 Step 2: Set up the KIND Cluster

If KIND isn't installed, follow the KIND installation guide.

Create a Kubernetes cluster:

```bash
kind create cluster --name wiki-kafka-cluster
```

### 📦 Step 3: Deploy Kubernetes Resources

Apply the Kubernetes manifests to deploy all services:

```bash
kubectl apply -f manifests/
```


Ensure your kubectl context is pointing to the KIND cluster.

### 🔍 Step 4: Check Pod Status

Check the status of the pods:

```bash
kubectl get pods
```

Make sure all pods are in the `Running` state.

### 📄 Step 5: Verify Logs

Check logs to ensure the Kafka producer and stream processor are working:

```bash
kubectl logs -f deployment/wiki-producer
kubectl logs -f deployment/wiki-processor
```

### 📊 Step 6: Access Kibana Dashboard

Port-forward the Kibana service:

```bash
kubectl port-forward service/kibana 5601:5601
```

Open your browser and go to: [http://localhost:5601](http://localhost:5601)

### 📈 Step 7: Access Kafka UI 

Port-forward the Kafka UI:

```bash
kubectl port-forward service/kafka-ui 9000:9000
```

Visit: [http://localhost:9000](http://localhost:9000)

