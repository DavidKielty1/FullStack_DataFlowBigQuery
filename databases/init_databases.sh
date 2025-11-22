#!/bin/bash

# Script to initialize SQLite databases
# This creates two separate database files

echo "Initializing SQLite databases..."

# Create databases directory if it doesn't exist
mkdir -p databases

# Initialize insider_risk.db
sqlite3 databases/insider_risk.db <<EOF
.read init_databases.sql
EOF

# Initialize analytics.db (extract only analytics table creation)
sqlite3 databases/analytics.db <<EOF
CREATE TABLE IF NOT EXISTS analytics_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    risk_level TEXT NOT NULL,
    event_count INTEGER DEFAULT 0,
    avg_risk_score REAL,
    max_risk_score REAL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, risk_level)
);

CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics_summary(date);
CREATE INDEX IF NOT EXISTS idx_analytics_risk_level ON analytics_summary(risk_level);

INSERT INTO analytics_summary (date, risk_level, event_count, avg_risk_score, max_risk_score)
VALUES 
    ('2024-01-15', 'LOW', 1, 30.0, 30.0),
    ('2024-01-15', 'MEDIUM', 1, 65.0, 65.0),
    ('2024-01-15', 'HIGH', 1, 70.0, 70.0),
    ('2024-01-16', 'LOW', 1, 20.0, 20.0),
    ('2024-01-16', 'HIGH', 1, 85.0, 85.0);
EOF

echo "Databases initialized successfully!"
echo "- databases/insider_risk.db"
echo "- databases/analytics.db"

