# Apache Kafka

Apache Kafka is a high-throughput, fault-tolerant, and scalable distributed streaming platform initially developed at LinkedIn. It is designed to efficiently handle real-time data streams from various sources, including applications, databases, and sensors.

Kafka operates as a **publish-subscribe messaging system**, enabling applications to seamlessly publish and consume data from topics. It is widely used for event-driven architectures, real-time analytics, and data integration due to its reliability, durability, and performance.

## Key Features
- **Scalability**: Seamlessly scales horizontally to accommodate large data volumes.
- **Fault Tolerance**: Ensures high availability through data replication across multiple brokers.
- **Low Latency**: Optimized for real-time data streaming and processing.
- **Durability**: Persistent message storage ensures data integrity and reliability.

## Architecture Overview
Kafka's architecture is built around three core components:

### 1. Producers
Producers are responsible for publishing data to Kafka topics. Messages sent by producers are distributed across partitions within a topic, ensuring load balancing and scalability.

### 2. Brokers
Brokers are Kafka servers that store and manage topics. They handle producer requests, store messages in partitions, and serve consumer read requests. Brokers work collectively to distribute workload efficiently.

### 3. Consumers
Consumers subscribe to topics and retrieve messages from Kafka brokers. They can be grouped into **consumer groups**, allowing parallel processing and efficient load distribution.

---

## Installation Guide

### Installing Kafka on Windows

Follow these steps to install Apache Kafka on Windows:

#### Step 1: Download Kafka
Download the latest version of Apache Kafka from the [official website](https://kafka.apache.org/downloads).

#### Step 2: Extract the Kafka Package
Extract the downloaded Kafka zip file to a directory of your choice (e.g., `C:\kafka`).

```sh
 tar -xvzf kafka_2.13-3.4.0.tgz
```

#### Step 3: Configure Zookeeper
Navigate to the Kafka `config` folder and edit `zookeeper.properties`. Set the `dataDir` path:

```properties
 dataDir=C:/Kafka/kafka/zookeeper-data
```

#### Step 4: Configure Kafka Server
Modify the `server.properties` file and update the log directory:

```properties
 log.dirs=C:/Kafka/kafka/kafka_logs
```

### Running Kafka Server

#### Step 1: Start Zookeeper
Kafka requires Zookeeper to manage the cluster and brokers. Open a PowerShell prompt and execute:

```sh
 .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

Zookeeper will start on port 2181.

#### Step 2: Start Kafka Server
Open another PowerShell prompt, navigate to the Kafka folder, and run:

```sh
 .\bin\windows\kafka-server-start.bat .\config\server.properties
```

Your Kafka Server is now up and running.

---

## Getting Started with Kafka

### Step 1: Create a Kafka Topic
Open a new command prompt in the `\bin\windows` directory and run:

```sh
 kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
```

### Step 2: Start a Kafka Producer
To send messages to `test` topic, run:

```sh
 kafka-console-producer.bat --broker-list localhost:9092 --topic test
```

### Step 3: Start a Kafka Consumer
To read messages from `test` topic, run:

```sh
 kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
```

### Step 4: List All Topics
Verify all created topics by running:

```sh
 .\bin\windows\kafka-topics.bat --bootstrap-server=localhost:9092 --list
```

---


## Conclusion
Apache Kafka is a robust platform for building scalable, high-performance data pipelines and real-time streaming applications. Its ability to handle large-scale event-driven architectures makes it an essential tool for modern data-driven enterprises.

---

### 📌 Additional Resources
- [Official Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka GitHub Repository](https://github.com/apache/kafka)
- [Kafka Tutorials & Guides](https://kafka.apache.org/documentation/#gettingStarted)

