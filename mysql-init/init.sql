CREATE DATABASE IF NOT EXISTS kafka_demo;

USE kafka_demo;

CREATE TABLE IF NOT EXISTS insurance_applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  application_id VARCHAR(50),
  agent_id VARCHAR(50),
  customer_name VARCHAR(100),
  plan VARCHAR(50),
  timestamp DATETIME
);
