📊 Time Series Database (TSDB) Project

A lightweight, in-memory time series database designed for efficient storage, querying, and aggregation of time-stamped data.

Ideal for scenarios requiring high-frequency data ingestion and real-time analytics.

🚀 Overview


This project implements a custom time series database (TSDB) in Python, featuring:

In-Memory Storage: Utilizes Python's built-in data structures for fast data access.

Chunked Data Management: Supports chunked storage to optimize memory usage and query performance.

Aggregation Functions: Provides built-in support for sum and average aggregations.

Downsampling: Allows data downsampling for efficient long-term storage and analysis.

REST API: Exposes a simple HTTP API for data ingestion and retrieval.

🛠️ Architecture

Note: Replace the above URL with the actual link to your architecture diagram.

📦 Prerequisites


Ensure the following are installed:

Docker

Docker Compose

Python 3.11+

🧪 Setup and Installation

Clone the Repository:


git clone https://github.com/souvikDevloper/tsdb_project.git

cd tsdb_project

Build and Start Services:


docker-compose up --build -d

This command builds the Docker images and starts the services in detached mode.

Verify Running Services:

TSDB API: Access via http://localhost:8000

Prometheus: Access via http://localhost:9090

Grafana: Access via http://localhost:3000

Default credentials for Grafana:

Username: admin

Password: admin

🧪 Running Tests

To execute tests within the tsdb container:


docker-compose exec tsdb pytest

📡 API Endpoints

POST /data

Ingests a new data point.

Request Body:


{
  "timestamp": "2025-05-14T09:00:00Z",
  "value": 42
}

Response:


{
  "message": "Data point ingested successfully"
}

GET /metrics

Retrieves all stored metrics.

Response:


[
  {
    "metric": "m1",
    "data": [
      {"timestamp": 1684050000, "value": 42},
      {"timestamp": 1684050600, "value": 45}
    ]
  }
]
🔧 Configuration

Environment variables can be set in the docker-compose.yml file under the tsdb service:

CHUNK_SIZE: Number of data points per chunk (default: 500)

RETENTION_SECONDS: Data retention period in seconds (default: 60)

NUM_SHARDS: Number of data shards (default: 4)

🧪 Testing

Unit tests are located in the tests/ directory. To run them:

docker-compose exec tsdb pytest tests/

📚 License

This project is licensed under the MIT License - see the LICENSE file for details.

📄 Acknowledgements

pytest – Testing framework

Docker – Containerization platform

Grafana – Visualization tool

Prometheus – Monitoring system

