-- Initialize SQLite databases for Insider Risk Management
-- This creates two databases:
-- 1. insider_risk.db - Stores individual risk events
-- 2. analytics.db - Stores aggregated analytics data

-- Database 1: insider_risk.db
-- This mirrors what would come from BigQuery/DataFlow processing

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
);

CREATE INDEX IF NOT EXISTS idx_user_id ON risk_events(user_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON risk_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_risk_level ON risk_events(risk_level);

-- Insert sample data
INSERT INTO risk_events (user_id, event_type, timestamp, risk_score, risk_level, sensitive_data_access, unusual_time, large_data_transfer, privileged_action)
VALUES 
    ('user001', 'DATA_ACCESS', '2024-01-15 10:30:00', 30.0, 'LOW', 1, 0, 0, 0),
    ('user002', 'FILE_DOWNLOAD', '2024-01-15 14:20:00', 70.0, 'HIGH', 1, 0, 1, 0),
    ('user003', 'PRIVILEGED_ACTION', '2024-01-15 22:15:00', 65.0, 'MEDIUM', 0, 1, 0, 1),
    ('user001', 'DATA_EXPORT', '2024-01-16 09:45:00', 85.0, 'HIGH', 1, 0, 1, 1),
    ('user004', 'LOGIN', '2024-01-16 11:20:00', 20.0, 'LOW', 0, 0, 0, 0);

-- Database 2: analytics.db
-- Stores aggregated analytics from BigQuery queries

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

-- Insert sample analytics data
INSERT INTO analytics_summary (date, risk_level, event_count, avg_risk_score, max_risk_score)
VALUES 
    ('2024-01-15', 'LOW', 1, 30.0, 30.0),
    ('2024-01-15', 'MEDIUM', 1, 65.0, 65.0),
    ('2024-01-15', 'HIGH', 1, 70.0, 70.0),
    ('2024-01-16', 'LOW', 1, 20.0, 20.0),
    ('2024-01-16', 'HIGH', 1, 85.0, 85.0);

