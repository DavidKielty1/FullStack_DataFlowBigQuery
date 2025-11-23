"""
Simple ML-based anomaly detection for insider risk events.
This demonstrates basic ML concepts for interview discussion.
"""

import numpy as np
from typing import List, Dict
import json


class SimpleAnomalyDetector:
    """
    Simple anomaly detector using statistical methods.
    Demonstrates ML concepts without requiring scikit-learn.
    """
    
    def __init__(self):
        self.baselines = {}  # Store baseline statistics per user
    
    def train(self, historical_events: List[Dict]):
        """
        Train on historical events to establish baseline behavior.
        This is a simplified version - real ML would use more sophisticated algorithms.
        """
        # Group events by user
        user_events = {}
        for event in historical_events:
            user_id = event.get('user_id', 'unknown')
            if user_id not in user_events:
                user_events[user_id] = []
            user_events[user_id].append(event)
        
        # Calculate baseline statistics for each user
        for user_id, events in user_events.items():
            self.baselines[user_id] = self._calculate_baseline(events)
    
    def _calculate_baseline(self, events: List[Dict]) -> Dict:
        """Calculate baseline statistics for a user."""
        access_counts = [e.get('file_access_count', 0) for e in events]
        transfer_sizes = [e.get('data_transfer_size_mb', 0) for e in events]
        hours = [e.get('hour_of_day', 12) for e in events]
        
        return {
            'mean_access_count': np.mean(access_counts) if access_counts else 0,
            'std_access_count': np.std(access_counts) if access_counts else 0,
            'mean_transfer_size': np.mean(transfer_sizes) if transfer_sizes else 0,
            'std_transfer_size': np.std(transfer_sizes) if transfer_sizes else 0,
            'normal_hours': set(hours),  # Hours when user typically accesses
        }
    
    def predict_anomaly(self, event: Dict) -> Dict:
        """
        Predict if an event is anomalous based on learned baselines.
        Returns anomaly score and reasons.
        """
        user_id = event.get('user_id', 'unknown')
        
        # If user not in training data, use default baseline
        if user_id not in self.baselines:
            return {
                'is_anomaly': False,
                'anomaly_score': 0.0,
                'reasons': ['User not in training data']
            }
        
        baseline = self.baselines[user_id]
        anomaly_score = 0.0
        reasons = []
        
        # Check access count anomaly (using z-score)
        access_count = event.get('file_access_count', 0)
        if baseline['std_access_count'] > 0:
            z_score = abs((access_count - baseline['mean_access_count']) / baseline['std_access_count'])
            if z_score > 2:  # More than 2 standard deviations
                anomaly_score += 0.3
                reasons.append(f"Unusual access volume (z-score: {z_score:.2f})")
        
        # Check data transfer anomaly
        transfer_size = event.get('data_transfer_size_mb', 0)
        if baseline['std_transfer_size'] > 0:
            z_score = abs((transfer_size - baseline['mean_transfer_size']) / baseline['std_transfer_size'])
            if z_score > 2:
                anomaly_score += 0.4
                reasons.append(f"Unusual data transfer (z-score: {z_score:.2f})")
        
        # Check time anomaly
        hour = event.get('hour_of_day', 12)
        if hour not in baseline['normal_hours']:
            anomaly_score += 0.2
            reasons.append(f"Access outside normal hours (hour: {hour})")
        
        # Check sensitive data access
        if event.get('sensitive_data_access', False):
            anomaly_score += 0.1
            reasons.append("Sensitive data access")
        
        is_anomaly = anomaly_score > 0.5  # Threshold for anomaly
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_score': min(anomaly_score, 1.0),  # Cap at 1.0
            'reasons': reasons
        }


def enhance_event_with_ml(event: Dict, detector: SimpleAnomalyDetector) -> Dict:
    """
    Enhance an event with ML-based anomaly detection.
    This could be integrated into the DataFlow pipeline.
    """
    anomaly_result = detector.predict_anomaly(event)
    
    enhanced_event = event.copy()
    enhanced_event['ml_anomaly_score'] = anomaly_result['anomaly_score']
    enhanced_event['ml_is_anomaly'] = anomaly_result['is_anomaly']
    enhanced_event['ml_reasons'] = anomaly_result['reasons']
    
    # Combine ML score with rule-based score
    rule_based_score = event.get('risk_score', 0) / 100.0  # Normalize to 0-1
    combined_score = (anomaly_result['anomaly_score'] * 0.6) + (rule_based_score * 0.4)
    enhanced_event['combined_risk_score'] = combined_score
    
    return enhanced_event


# Example usage
if __name__ == '__main__':
    # Sample historical events (normal behavior)
    historical_events = [
        {'user_id': 'user1', 'file_access_count': 10, 'data_transfer_size_mb': 5, 'hour_of_day': 9},
        {'user_id': 'user1', 'file_access_count': 12, 'data_transfer_size_mb': 7, 'hour_of_day': 10},
        {'user_id': 'user1', 'file_access_count': 8, 'data_transfer_size_mb': 3, 'hour_of_day': 14},
        {'user_id': 'user2', 'file_access_count': 50, 'data_transfer_size_mb': 20, 'hour_of_day': 11},
        {'user_id': 'user2', 'file_access_count': 45, 'data_transfer_size_mb': 18, 'hour_of_day': 12},
    ]
    
    # Train detector
    detector = SimpleAnomalyDetector()
    detector.train(historical_events)
    
    # Test with new event (potentially anomalous)
    new_event = {
        'user_id': 'user1',
        'file_access_count': 500,  # Much higher than normal (10-12)
        'data_transfer_size_mb': 1000,  # Much higher than normal (3-7)
        'hour_of_day': 2,  # Outside normal hours (9, 10, 14)
        'sensitive_data_access': True,
        'risk_score': 75  # Rule-based score
    }
    
    result = detector.predict_anomaly(new_event)
    print("Anomaly Detection Result:")
    print(f"  Is Anomaly: {result['is_anomaly']}")
    print(f"  Anomaly Score: {result['anomaly_score']:.2f}")
    print(f"  Reasons: {result['reasons']}")
    
    # Enhance event with ML
    enhanced = enhance_event_with_ml(new_event, detector)
    print("\nEnhanced Event:")
    print(f"  ML Anomaly Score: {enhanced['ml_anomaly_score']:.2f}")
    print(f"  Combined Risk Score: {enhanced['combined_risk_score']:.2f}")
    print(f"  ML Reasons: {enhanced['ml_reasons']}")

