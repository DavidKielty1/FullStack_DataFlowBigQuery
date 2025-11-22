"""
BigQuery queries and analytics for insider risk data.
These queries can be used to generate insights and feed the Next.js API.
"""

from google.cloud import bigquery
import pandas as pd


class BigQueryAnalytics:
    """Handle BigQuery analytics queries."""
    
    def __init__(self, project_id, dataset_id):
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = dataset_id
    
    def get_risk_events(self, limit=100, risk_level=None):
        """Query risk events from BigQuery."""
        query = f"""
        SELECT 
            user_id,
            event_type,
            timestamp,
            risk_score,
            risk_level
        FROM `{self.client.project}.{self.dataset_id}.risk_events`
        WHERE 1=1
        """
        
        if risk_level:
            query += f" AND risk_level = '{risk_level}'"
        
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        return self.client.query(query).to_dataframe()
    
    def get_risk_summary(self, days=30):
        """Get aggregated risk summary."""
        query = f"""
        SELECT 
            DATE(timestamp) as date,
            risk_level,
            COUNT(*) as event_count,
            AVG(risk_score) as avg_risk_score,
            MAX(risk_score) as max_risk_score
        FROM `{self.client.project}.{self.dataset_id}.risk_events`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY date, risk_level
        ORDER BY date DESC
        """
        
        return self.client.query(query).to_dataframe()
    
    def get_user_risk_profile(self, user_id):
        """Get risk profile for a specific user."""
        query = f"""
        SELECT 
            user_id,
            COUNT(*) as total_events,
            AVG(risk_score) as avg_risk_score,
            MAX(risk_score) as max_risk_score,
            COUNTIF(risk_level = 'HIGH') as high_risk_events
        FROM `{self.client.project}.{self.dataset_id}.risk_events`
        WHERE user_id = '{user_id}'
        GROUP BY user_id
        """
        
        return self.client.query(query).to_dataframe()


if __name__ == '__main__':
    # Example usage
    analytics = BigQueryAnalytics('your-project-id', 'insider_risk')
    
    # Get recent events
    events = analytics.get_risk_events(limit=50)
    print("Recent Events:")
    print(events.head())
    
    # Get summary
    summary = analytics.get_risk_summary(days=7)
    print("\nRisk Summary:")
    print(summary)

