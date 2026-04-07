"""
===========================================================
BigQuery related tasks
===========================================================
Script purpose:
    Script to create a connection with google BigQuery. Gets credentials from
    config.py

    Now contains a script to load flattened data from jolpica and transforms files
    to BigQuery.
"""

from utils.config import KEY_PATH, GCP_PROJECT_ID, BQ_DATASET
from google.cloud import bigquery
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)


def get_bigquery_client():
    try:
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        client = bigquery.Client(project=GCP_PROJECT_ID, credentials=credentials)
        return client
    except Exception as e:
        logger.error(f"Failed to create a connection with BigQuery: {e}")
        raise



def load_to_bigquery(rows, table_name):
    try:
        client = get_bigquery_client()
        table_ref = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )
        
        load_job = client.load_table_from_json(rows, table_ref, job_config=job_config)
        load_job.result()
        logger.info(f"Total of {len(rows)} rows loaded to BigQuery!")
    
    except Exception as e:
        logger.error(f"Failed to load data to BigQuery: {e}")
        raise
