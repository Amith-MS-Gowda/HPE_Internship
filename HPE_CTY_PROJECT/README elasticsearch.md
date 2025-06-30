# Elasticsearch

Elasticsearch is a powerful, distributed search and analytics engine designed for real-time data indexing and querying. It is part of the **Elastic Stack (ELK)**, commonly used for full-text search, log analysis, and distributed data processing.

## Key Features
- **Scalability**: Supports horizontal scaling with multiple nodes.
- **Full-Text Search**: Uses **Lucene** for efficient search and ranking.
- **High Availability**: Replication and sharding ensure fault tolerance.
- **Real-Time Analytics**: Enables fast queries over large datasets.
- **Integration**: Works seamlessly with **Kibana**, **Logstash**, and **Beats**.

## Architecture Overview
Elasticsearch follows a **distributed architecture** consisting of the following core components:

### 1. **Nodes & Clusters**
A **node** is a single Elasticsearch instance, and multiple nodes form a **cluster** for load balancing and redundancy.

### 2. **Indexes & Documents**
- **Index**: A logical namespace holding related documents (like a database).
- **Document**: A JSON object representing a data entry (like a record).

### 3. **Shards & Replicas**
- **Shards**: Split data across nodes for parallel processing.
- **Replicas**: Ensure high availability and fault tolerance.

## Installation Guide
### **Installing Elasticsearch on Windows**
Follow these steps to install and run Elasticsearch on Windows:

### **Step 1: Download Elasticsearch**
Download the latest version from the [official Elasticsearch website](https://www.elastic.co/downloads/elasticsearch).

### **Step 2: Extract & Configure Elasticsearch**
Extract the downloaded **ZIP file** to a directory (e.g., `C:\elasticsearch`).

Edit the `elasticsearch.yml` configuration file (located in `config` folder):
```yaml
cluster.name: my-cluster
node.name: node-1
network.host: 0.0.0.0
http.port: 9200
```

### **Step 3: Start Elasticsearch**
Open **PowerShell** or **Command Prompt** and navigate to the Elasticsearch `bin` folder:
```sh
cd C:\elasticsearch\bin
elasticsearch.bat
```

Elasticsearch will start and listen on port **9200**.

## Getting Started with Elasticsearch
### **Step 1: Verify Installation**
Check if Elasticsearch is running by executing:
```sh
curl -X GET "http://localhost:9200"
```
If running successfully, you'll see a JSON response with cluster details.

### **Step 2: Create an Index**
```sh
curl -X PUT "http://localhost:9200/test-index"
```

### **Step 3: Index a Document**
```sh
curl -X POST "http://localhost:9200/test-index/_doc/1" -H "Content-Type: application/json" -d '{"name": "Elasticsearch", "type": "Search Engine"}'
```

### **Step 4: Retrieve a Document**
```sh
curl -X GET "http://localhost:9200/test-index/_doc/1"
```

### **Step 5: Search Data**
```sh
curl -X GET "http://localhost:9200/test-index/_search?q=name:Elasticsearch"
```

## Securing Elasticsearch
To enable authentication and TLS encryption, modify `elasticsearch.yml`:
```yaml
xpack.security.enabled: true
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.certificate: certs/http.pem
xpack.security.http.ssl.key: certs/http-key.pem
xpack.security.http.ssl.certificate_authorities: certs/ca.pem
```
Then, restart Elasticsearch and use:
```sh
curl -X GET "https://localhost:9200" --cacert config/certs/ca.crt
```

## Managing Elasticsearch
### **List All Indexes**
```sh
curl -X GET "http://localhost:9200/_cat/indices?v"
```
### **Delete an Index**
```sh
curl -X DELETE "http://localhost:9200/test-index"
```
### **Check Cluster Health**
```sh
curl -X GET "http://localhost:9200/_cluster/health"
```

## Conclusion
Elasticsearch is a powerful search and analytics engine for handling real-time data at scale. Its integration with the **Elastic Stack** makes it an essential tool for modern applications requiring fast search, logging, and analytics capabilities.

## 📌 Additional Resources
- [Official Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/index.html)
- [Elasticsearch GitHub Repository](https://github.com/elastic/elasticsearch)
- [Elasticsearch Tutorials](https://www.elastic.co/learn)

