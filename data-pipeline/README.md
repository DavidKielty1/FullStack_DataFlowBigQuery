# Data Pipeline (DataFlow + BigQuery)

This directory contains the data processing pipeline using Google Cloud DataFlow and BigQuery.

## Structure

- `dataflow_pipeline.py` - Apache Beam pipeline for processing risk events
- `bigquery_queries.py` - BigQuery analytics and query utilities

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

