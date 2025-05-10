# kafka-demo

## Overview

* A **Kafka Producer** generates mock events.
* A **Kafka Consumer** listens to those events and logs them into a **MySQL database**.
* Kafka is deployed in **KRaft mode** (Zookeeper-less).

---

## Structure

```
.
├── consumer/
│   ├── app.py              # Kafka Consumer that inserts to MySQL
│   └── Dockerfile
├── producer/
│   ├── app.py              # Kafka Producer that produces events
│   └── Dockerfile
├── mysql-init/
│   └── init.sql            # Auto-creates the insurance_applications table
├── docker-compose.yml      # To start all services
├── requirements.txt
└── README.md
```

---

## Quickstart

### Requirements

* Docker
* Docker Compose

### Setup & Run

```bash
git clone https://github.com/uuboyscy/kafka-demo.git
cd kafka-demo
docker compose up --build
```

* The producer will keep sending mock events.
* The consumer will receive and log these into the MySQL `kafka_demo.insurance_applications` table.

---

## Example Kafka Event

```json
{
  "application_id": "AP123456",
  "agent_id": "AG9876",
  "customer_name": "Alice",
  "plan": "Whole Life",
  "timestamp": "2025-05-10T08:22:31.123Z"
}
```

---

## Database Schema

The table `insurance_applications` is created automatically at startup via the `mysql-init/init.sql` script:

```sql
CREATE TABLE insurance_applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  application_id VARCHAR(50),
  agent_id VARCHAR(50),
  customer_name VARCHAR(100),
  plan VARCHAR(50),
  timestamp DATETIME
);
```

You can access the database using:

```bash
docker exec -it kafka-demo-mysql-1 mysql -u root -p
# Password: example
```
