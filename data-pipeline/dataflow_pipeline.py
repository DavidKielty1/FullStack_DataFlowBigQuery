"""
DataFlow pipeline for processing insider risk data and loading into BigQuery.
This pipeline processes events, detects anomalies, and stores results.
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessRiskEvents(beam.DoFn):
    """Process individual risk events and calculate risk scores."""
    
    def process(self, element):
        """Process a single event and yield enriched data."""
        try:
            event = json.loads(element) if isinstance(element, str) else element
            
            # Calculate risk score (simplified example)
            risk_score = self._calculate_risk_score(event)
            event['risk_score'] = risk_score
            event['risk_level'] = self._determine_risk_level(risk_score)
            
            yield event
        except Exception as e:
            logger.error(f"Error processing event: {e}")
    
    def _calculate_risk_score(self, event):
        """Calculate risk score based on event attributes."""
        # Simplified risk scoring logic
        base_score = 0
        if event.get('sensitive_data_access', False):
            base_score += 30
        if event.get('unusual_time', False):
            base_score += 20
        if event.get('large_data_transfer', False):
            base_score += 40
        if event.get('privileged_action', False):
            base_score += 25
        
        return min(base_score, 100)
    
    def _determine_risk_level(self, score):
        """Determine risk level based on score."""
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'


def run_pipeline(project_id, dataset_id, table_id, input_path, output_path):
    """Run the DataFlow pipeline."""
    
    pipeline_options = PipelineOptions([
        '--project', project_id,
        '--runner', 'DataflowRunner',
        '--region', 'europe-west2',
        '--temp_location', output_path,
        '--staging_location', output_path,
    ])
    
    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | 'ReadEvents' >> beam.io.ReadFromText(input_path)
            | 'ProcessEvents' >> beam.ParDo(ProcessRiskEvents())
            | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.{table_id}',
                schema='user_id:STRING,event_type:STRING,timestamp:TIMESTAMP,risk_score:FLOAT,risk_level:STRING',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--dataset_id', default='insider_risk')
    parser.add_argument('--table_id', default='risk_events')
    parser.add_argument('--input_path', required=True)
    parser.add_argument('--output_path', required=True)
    
    args = parser.parse_args()
    
    run_pipeline(
        args.project_id,
        args.dataset_id,
        args.table_id,
        args.input_path,
        args.output_path
    )

