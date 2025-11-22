#!/usr/bin/env python3
"""
Cross-platform script to initialize SQLite databases.
Works on Windows, Linux, and macOS.
"""

import sqlite3
import os
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent
databases_dir = script_dir

print("Initializing SQLite databases...")

# Ensure databases directory exists
databases_dir.mkdir(exist_ok=True)

# Database 1: insider_risk.db
insider_risk_db = databases_dir / "insider_risk.db"
conn1 = sqlite3.connect(insider_risk_db)

cursor1 = conn1.cursor()

# Create risk_events table
cursor1.execute("""
CREATE TABLE IF NOT EXISTS risk_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    risk_score REAL,
    risk_level TEXT,
    sensitive_data_access INTEGER DEFAULT 0,
    unusual_time INTEGER DEFAULT 0,
    large_data_transfer INTEGER DEFAULT 0,
    privileged_action INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor1.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON risk_events(user_id)")
cursor1.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON risk_events(timestamp)")
cursor1.execute("CREATE INDEX IF NOT EXISTS idx_risk_level ON risk_events(risk_level)")

# Insert sample data
cursor1.execute("""
INSERT OR IGNORE INTO risk_events 
(user_id, event_type, timestamp, risk_score, risk_level, sensitive_data_access, unusual_time, large_data_transfer, privileged_action)
VALUES 
    ('user001', 'DATA_ACCESS', '2024-01-15 10:30:00', 30.0, 'LOW', 1, 0, 0, 0),
    ('user002', 'FILE_DOWNLOAD', '2024-01-15 14:20:00', 70.0, 'HIGH', 1, 0, 1, 0),
    ('user003', 'PRIVILEGED_ACTION', '2024-01-15 22:15:00', 65.0, 'MEDIUM', 0, 1, 0, 1),
    ('user001', 'DATA_EXPORT', '2024-01-16 09:45:00', 85.0, 'HIGH', 1, 0, 1, 1),
    ('user004', 'LOGIN', '2024-01-16 11:20:00', 20.0, 'LOW', 0, 0, 0, 0)
""")

conn1.commit()
conn1.close()
print(f"✓ Created {insider_risk_db}")

# Database 2: analytics.db
analytics_db = databases_dir / "analytics.db"
conn2 = sqlite3.connect(analytics_db)

cursor2 = conn2.cursor()

# Create analytics_summary table
cursor2.execute("""
CREATE TABLE IF NOT EXISTS analytics_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    risk_level TEXT NOT NULL,
    event_count INTEGER DEFAULT 0,
    avg_risk_score REAL,
    max_risk_score REAL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, risk_level)
)
""")

cursor2.execute("CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics_summary(date)")
cursor2.execute("CREATE INDEX IF NOT EXISTS idx_analytics_risk_level ON analytics_summary(risk_level)")

# Insert sample analytics data
cursor2.execute("""
INSERT OR IGNORE INTO analytics_summary 
(date, risk_level, event_count, avg_risk_score, max_risk_score)
VALUES 
    ('2024-01-15', 'LOW', 1, 30.0, 30.0),
    ('2024-01-15', 'MEDIUM', 1, 65.0, 65.0),
    ('2024-01-15', 'HIGH', 1, 70.0, 70.0),
    ('2024-01-16', 'LOW', 1, 20.0, 20.0),
    ('2024-01-16', 'HIGH', 1, 85.0, 85.0)
""")

conn2.commit()
conn2.close()
print(f"✓ Created {analytics_db}")

print("\nDatabases initialized successfully!")
print(f"- {insider_risk_db}")
print(f"- {analytics_db}")

