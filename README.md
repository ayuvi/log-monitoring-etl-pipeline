# 📊 Log Monitoring Data Pipeline (Docker + Python + PostgreSQL + Grafana)

End-to-end data engineering project simulating real production log monitoring system used in enterprise applications (Shipping / Logistics environment).

---

## 🧠 Problem

In operational systems, application errors are often detected too late because logs are only stored as raw files.

This project transforms raw logs into analytical data and monitoring dashboards with alerting capability.

---

## 🏗 Architecture

Log Generator → ETL (Python) → PostgreSQL (DWH) → Grafana Dashboard → Alerting

---

## ⚙️ Tech Stack

* Python (ETL processing)
* PostgreSQL (Data Warehouse)
* Docker Compose (Orchestration)
* Grafana (Monitoring Dashboard)
* SQL (Transformation & Mart Layer)

---

## 🚀 Features

* Automated log ingestion
* Data warehouse modeling (raw → staging → mart)
* Error monitoring dashboard
* Alert when error threshold exceeded
* Fully containerized environment

---

## ▶️ How to Run

```bash
docker compose up --build
```

Open Grafana:

```
http://localhost:3000
user: admin
pass: admin
```

---

## 📊 Example Dashboard

Tracks:

* Error trend over time
* Service error distribution
* Hourly failure pattern

---

## 💼 Real World Relevance

Simulates monitoring system for enterprise applications such as:

* Shipping Management System
* Booking & Billing Service
* API Gateway
* Authentication Service

---

## 👤 Author

Muhammad Ayuvi Laksana Putra
