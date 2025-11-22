# Database Initialization

This directory contains scripts to initialize the SQLite databases used for local development.

## Quick Start

### Windows (Recommended)
```bash
python init_databases.py
```

### Linux/macOS
```bash
# Option 1: Python (works everywhere)
python3 init_databases.py

# Option 2: Shell script (requires sqlite3 CLI)
chmod +x init_databases.sh
./init_databases.sh
```

## Databases Created

1. **insider_risk.db** - Stores individual risk events
   - Mirrors the structure of BigQuery risk_events table
   - Contains sample data for testing

2. **analytics.db** - Stores aggregated analytics summaries
   - Pre-aggregated data for faster dashboard queries
   - Contains sample analytics data

## Files

- `init_databases.py` - Cross-platform Python script (recommended)
- `init_databases.sh` - Bash script for Linux/macOS
- `init_databases.sql` - SQL schema reference

## Notes

- Databases are created in the `databases/` directory
- Existing databases will not be overwritten (uses INSERT OR IGNORE)
- Sample data is included for testing purposes
- These databases are for local development only
- Production uses BigQuery instead

