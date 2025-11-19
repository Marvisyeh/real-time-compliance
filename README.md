# 📡 Real-Time Event Monitoring Platform

A real-time data pipeline that ingests system logs, metrics, and transaction events through Kafka, performs cleaning and anomaly detection, stores cleaned data into PostgreSQL, triggers Slack alerts on anomalies, and visualizes everything in a React dashboard.

This project demonstrates an end-to-end **streaming data engineering architecture** with **real-time ETL**, **anomaly detection**, **cloud-like storage**, **API services**, and **interactive visualizations**.

---

## 🚀 Features

- **Real-time streaming pipeline** with Kafka
- **Producers** generate mock logs, metrics, and transaction events
- **Consumer A** writes raw events to S3 (raw data lake)
- **Consumer B** performs:

  - JSON parsing & data cleaning
  - Rule-based anomaly detection
  - Writes cleaned data into PostgreSQL
  - Sends Slack alerts for anomalies

- **FastAPI** backend to expose metrics, logs, anomalies, and statistics
<!-- - **React Dashboard** to visualize real-time trends and anomalies -->

---

## 🏗 Architecture Overview

```
Producers (Python)
     │
     ▼
 Kafka Topics (logs / metrics / transactions)
     │
     ├── Consumer A → S3 Raw Storage
     │
     └── Consumer B → Cleaning → Anomaly Detection → PostgreSQL → Slack Alert
                                               │
                                               ▼
                                          FastAPI API
                                               │
                                               ▼
                                       React Dashboard(planing)
```

---

## 🔧 Tech Stack

### **Backend / Data Pipeline**

- Python
- Kafka (Producers + Consumers)
- S3 (raw data storage)
- PostgreSQL (cleaned events + anomalies)
- FastAPI
- Slack Webhook for alerting

<!-- ### **Frontend** (Coming Soon)

- React + Charting Library

---

## 📁 Project Structure (Coming Soon)

```
/src
  /producers
  /consumer_a_raw_sink
  /consumer_b_etl_anomaly
  /api
  /dashboard
/infra
  /docker
  /config
/docs
  architecture-diagram.png
  anomaly-pipeline.png
README.md
```

---

## 🔥 Example Event Format

**Log Event**

```json
{
  "timestamp": "2025-01-01T10:20:30Z",
  "service": "auth-service",
  "level": "ERROR",
  "message": "User login failed",
  "user_id": 123
}
```

**Metric Event**

```json
{
  "timestamp": "2025-01-01T10:20:32Z",
  "service": "inventory-api",
  "cpu": 88.2,
  "latency_ms": 420
}
```

---

## ⚠️ Anomaly Detection Rules (Coming Soon)

- **Logs**: > 20 ERROR logs within 1 minute
- **Metrics**: CPU > 85% or Latency > 400ms
- **Transactions**: Amount > 10,000

Detected anomalies will be stored in PostgreSQL and notified via Slack.

---

## 🧪 How to Run (Coming Soon)

Documentation for running Kafka, consumers, API, and dashboard will be added as implementation progresses.

---

## 📌 Project Goals

- Build a production-style real-time data platform
- Demonstrate data pipeline & streaming engineering skills
- Show an end-to-end system: ingestion → processing → storage → API → visualization
- Serve as a portfolio project for Data / AI Engineering roles -->
