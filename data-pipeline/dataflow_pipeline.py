"""
DataFlow pipeline for processing insider risk data and loading into BigQuery.
This pipeline processes events, detects anomalies, and stores results.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Iterator, TYPE_CHECKING

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToBigQuery
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.options.pipeline_options import PipelineOptions

if TYPE_CHECKING:
    from apache_beam.pvalue import PCollection, PValue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessRiskEvents(beam.DoFn):
    """Process individual risk events and calculate risk scores."""

    def process(
        self, element: str | Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Process a single event and yield enriched data."""
        try:
            event = (
                json.loads(element)
                if isinstance(element, str)
                else element
            )

            # Calculate risk score (simplified example)
            risk_score = self._calculate_risk_score(event)
            event['risk_score'] = risk_score
            event['risk_level'] = self._determine_risk_level(risk_score)

            yield event
        except Exception as e:
            logger.error(f"Error processing event: {e}")

    def _calculate_risk_score(self, event: Dict[str, Any]) -> int:
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

    def _determine_risk_level(self, score: int) -> str:
        """Determine risk level based on score."""
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'


# Typed filter functions for event routing
def filter_access_events(event: Dict[str, Any]) -> bool:
    """Filter for access-related events."""
    event_type = event.get('event_type', '').lower()
    return 'access' in event_type or 'file' in event_type


def filter_data_transfer_events(event: Dict[str, Any]) -> bool:
    """Filter for data transfer events."""
    event_type = event.get('event_type', '').lower()
    return (
        'transfer' in event_type or
        'download' in event_type or
        'export' in event_type
    )


def filter_privileged_events(event: Dict[str, Any]) -> bool:
    """Filter for privileged action events."""
    event_type = event.get('event_type', '').lower()
    return 'privileged' in event_type or 'admin' in event_type


def filter_auth_events(event: Dict[str, Any]) -> bool:
    """Filter for authentication events."""
    event_type = event.get('event_type', '').lower()
    return 'authentication' in event_type or 'login' in event_type


def filter_sensitive_data_events(event: Dict[str, Any]) -> bool:
    """Filter for sensitive data access events."""
    return (
        event.get('sensitive_data_access', False) or
        'sensitive' in event.get('event_type', '').lower()
    )


def filter_other_events(event: Dict[str, Any]) -> bool:
    """Filter for events that don't match other categories."""
    event_type = event.get('event_type', '').lower()
    return not any([
        'access' in event_type,
        'transfer' in event_type,
        'download' in event_type,
        'export' in event_type,
        'privileged' in event_type,
        'admin' in event_type,
        'authentication' in event_type,
        'login' in event_type,
        event.get('sensitive_data_access', False)
    ])


def run_pipeline(
    project_id: str,
    dataset_id: str,
    input_path: str,
    output_path: str
) -> None:
    """Run the DataFlow pipeline with segmented storage by event_type."""

    # Common schema for all event tables
    event_schema = (
        'user_id:STRING,event_type:STRING,'
        'timestamp:TIMESTAMP,risk_score:FLOAT,'
        'risk_level:STRING'
    )

    pipeline_options = PipelineOptions([
        '--project', project_id,
        '--runner', 'DataflowRunner',
        '--region', 'europe-west2',
        '--temp_location', output_path,
        '--staging_location', output_path,
    ])

    with beam.Pipeline(options=pipeline_options) as pipeline:
        # PCollection of processed risk events
        processed_events: PCollection[Dict[str, Any]] = (  # type: ignore
            pipeline
            | 'ReadEvents' >> ReadFromText(input_path)
            | 'ProcessEvents' >> beam.ParDo(ProcessRiskEvents())
        )

        # Route events by event_type to separate tables
        # Each table stores events with risk_level column for clustering
        # Access events
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterAccessEvents' >> beam.Filter(  # type: ignore[arg-type]
                filter_access_events
            )
            | 'WriteAccessEvents' >> WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.access_events',
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

        # Data transfer events
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterDataTransferEvents' >> beam.Filter(  # type: ignore
                filter_data_transfer_events
            )
            | 'WriteDataTransferEvents' >> WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.data_transfer_events',
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

        # Privileged action events
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterPrivilegedEvents' >> beam.Filter(  # type: ignore
                filter_privileged_events
            )
            | 'WritePrivilegedEvents' >> WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.privileged_action_events',
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

        # Authentication events
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterAuthEvents' >> beam.Filter(  # type: ignore[arg-type]
                filter_auth_events
            )
            | 'WriteAuthEvents' >> WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.authentication_events',
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

        # Sensitive data access events
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterSensitiveDataEvents' >> beam.Filter(  # type: ignore
                filter_sensitive_data_events
            )
            | 'WriteSensitiveDataEvents' >> WriteToBigQuery(
                table=(
                    f'{project_id}:{dataset_id}.'
                    'sensitive_data_access_events'
                ),
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

        # All other events (catch-all)
        _: PValue = (  # type: ignore[assignment]
            processed_events
            | 'FilterOtherEvents' >> beam.Filter(  # type: ignore[arg-type]
                filter_other_events
            )
            | 'WriteOtherEvents' >> WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.other_events',
                schema=event_schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--dataset_id', default='insider_risk')
    parser.add_argument('--input_path', required=True)
    parser.add_argument('--output_path', required=True)

    args = parser.parse_args()

    run_pipeline(
        args.project_id,
        args.dataset_id,
        args.input_path,
        args.output_path
    )
