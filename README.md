# Insider Risk Management Platform

A comprehensive platform for detecting and managing insider risk events, built with Next.js, Java Spring Boot, Google Cloud DataFlow, and BigQuery.

## Architecture Overview

This repository demonstrates a microservices architecture for insider risk detection:

- **Next.js Frontend/API**: React-based UI with API routes that can query both SQLite (for local dev) and integrate with BigQuery results
- **Java Backend Service**: Spring Boot REST API for handling complex business logic and data processing
- **Data Pipeline**: Apache Beam (DataFlow) pipelines for processing and analyzing risk events
- **BigQuery**: Cloud data warehouse for storing and querying processed risk data
- **SQLite Databases**: Two local databases for development and testing:
  - `insider_risk.db`: Stores individual risk events
  - `analytics.db`: Stores aggregated analytics summaries

## Project Structure

```
DataFlowBigQuery/
├── nextjs-app/              # Next.js application (frontend + API routes)
│   ├── app/                 # Next.js 14 App Router
│   │   ├── api/            # API routes
│   │   └── page.tsx        # Home page
│   ├── package.json
│   └── Dockerfile
│
├── java-backend/            # Java Spring Boot backend service
│   ├── src/main/java/
│   │   └── com/lloyds/insiderrisk/
│   │       ├── controller/ # REST controllers
│   │       ├── service/    # Business logic
│   │       └── repository/ # Data access
│   ├── pom.xml
│   └── Dockerfile
│
├── data-pipeline/          # DataFlow and BigQuery code
│   ├── dataflow_pipeline.py    # Apache Beam pipeline
│   ├── bigquery_queries.py     # BigQuery analytics
│   └── requirements.txt
│
├── databases/              # SQLite databases
│   ├── init_databases.sql # Database schema
│   └── init_databases.sh  # Initialization script
│
├── kubernetes/            # Kubernetes deployment manifests
│   ├── namespace.yaml
│   ├── nextjs-deployment.yaml
│   ├── java-backend-deployment.yaml
│   ├── configmap.yaml
│   └── persistent-volume.yaml
│
├── docker-compose.yml     # Docker Compose for local development
└── README.md
```

## Quick Start

### Prerequisites

- Node.js 18+
- Java 17+
- Maven 3.9+
- Python 3.9+ (for data pipeline)
- Docker & Docker Compose (for containerized deployment)
- SQLite3 (or use Python script instead)

**Note**: See [DOCKER_SETUP.md](DOCKER_SETUP.md) for Docker installation and troubleshooting.

### 1. Initialize Databases

**Option 1: Using Python (Recommended - Cross-platform)**
```bash
cd databases
python init_databases.py
```

**Option 2: Using SQLite3 command line (Linux/macOS)**
```bash
cd databases
chmod +x init_databases.sh
./init_databases.sh
```

**Option 3: Manual SQLite commands**
```bash
sqlite3 databases/insider_risk.db < databases/init_databases.sql
sqlite3 databases/analytics.db < databases/init_databases.sql
```

**Note for Windows users**: If `sqlite3` command is not available, use the Python script (Option 1) which works on all platforms.

### 2. Run with Docker Compose

**Important**: Make sure Docker Desktop is running before executing this command.

```bash
docker-compose up --build
```

This will start:
- Next.js app on http://localhost:3000
- Java backend on http://localhost:8080

**Troubleshooting Docker on Windows**:
- Ensure Docker Desktop is installed and running
- Check Docker Desktop status in system tray
- Verify Docker is accessible: `docker --version`
- If you see connection errors, restart Docker Desktop

### 3. Run Locally (Development)

#### Next.js App
```bash
cd nextjs-app
npm install
npm run dev
```

#### Java Backend
```bash
cd java-backend
mvn clean install
mvn spring-boot:run
```

## API Endpoints

### Next.js API Routes
- `GET /api/events` - Get risk events (queries SQLite)
- `GET /api/analytics` - Get analytics data
- `GET /api/health` - Health check

### Java Backend API
- `GET /api/v1/events` - Get risk events
- `GET /api/v1/events/{id}` - Get event by ID
- `POST /api/v1/events` - Create new risk event

## Data Pipeline

The data pipeline processes events using Apache Beam and stores results in BigQuery.

### Setup GCP Credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

### Run DataFlow Pipeline
```bash
cd data-pipeline
pip install -r requirements.txt

python dataflow_pipeline.py \
  --project_id your-gcp-project \
  --input_path gs://your-bucket/input/events.json \
  --output_path gs://your-bucket/temp/
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (local: minikube/kind, or GKE)
- kubectl configured

### Deploy
```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Create ConfigMap
kubectl apply -f kubernetes/configmap.yaml

# Create PersistentVolumeClaim
kubectl apply -f kubernetes/persistent-volume.yaml

# Deploy services
kubectl apply -f kubernetes/java-backend-deployment.yaml
kubectl apply -f kubernetes/nextjs-deployment.yaml
```

### Access Services
```bash
# Port forward to access locally
kubectl port-forward -n insider-risk svc/nextjs-app 3000:80
kubectl port-forward -n insider-risk svc/java-backend 8080:8080
```

## Database Schema

### insider_risk.db
Stores individual risk events with:
- User ID, event type, timestamp
- Risk score and risk level (LOW/MEDIUM/HIGH)
- Event flags (sensitive_data_access, unusual_time, etc.)

### analytics.db
Stores aggregated analytics:
- Daily summaries by risk level
- Average and max risk scores
- Event counts

## Architecture Decisions

### Why Two Databases?
- **insider_risk.db**: Mirrors BigQuery event data for local development
- **analytics.db**: Stores pre-aggregated analytics to reduce query load

### Next.js vs Java Backend?
- **Next.js API Routes**: Lightweight endpoints, good for simple CRUD and frontend integration
- **Java Backend**: Better for complex business logic, enterprise patterns, and integration with existing Java systems

Both can coexist:
- Next.js handles frontend and simple queries
- Java backend handles complex processing and integrations

## Development Notes

- SQLite databases are stored in `databases/` directory
- In production, these would be replaced by BigQuery queries
- Docker volumes mount the databases directory for persistence
- Kubernetes uses PersistentVolumeClaims for database storage

## Technologies Used

- **Frontend**: Next.js 14, React, TypeScript
- **Backend**: Java 17, Spring Boot 3.1
- **Data Processing**: Apache Beam (DataFlow), Python
- **Data Warehouse**: Google BigQuery
- **Databases**: SQLite (dev), BigQuery (prod)
- **Containers**: Docker, Kubernetes
- **Cloud**: Google Cloud Platform

## License

This is a demonstration project for technical assessment purposes.

