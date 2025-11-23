# Data Pipeline (DataFlow + BigQuery)

This directory contains the data processing pipeline using Google Cloud DataFlow and BigQuery, along with educational content on data analysis, AI/ML, and insider threat frameworks.

## Structure

- `dataflow_pipeline.py` - Apache Beam pipeline for processing risk events
- `bigquery_queries.py` - BigQuery analytics and query utilities
- `ml_anomaly_detection.py` - Simple ML-based anomaly detection example

## Documentation

- **[DATAFLOW_BIGQUERY_BASICS.md](./DATAFLOW_BIGQUERY_BASICS.md)** - Introduction to DataFlow and BigQuery
- **[AI_ML_INSIDER_RISK.md](./AI_ML_INSIDER_RISK.md)** - AI/ML concepts for insider risk detection
- **[INSIDER_THREAT_FRAMEWORKS.md](./INSIDER_THREAT_FRAMEWORKS.md)** - Frameworks and methodologies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up GCP credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Running the Pipeline

```bash
python dataflow_pipeline.py \
  --project_id your-gcp-project \
  --input_path gs://your-bucket/input/events.json \
  --output_path gs://your-bucket/temp/
```

## BigQuery Schema

The pipeline creates tables with the following schema:
- `user_id` (STRING)
- `event_type` (STRING)
- `timestamp` (TIMESTAMP)
- `risk_score` (FLOAT)
- `risk_level` (STRING)

