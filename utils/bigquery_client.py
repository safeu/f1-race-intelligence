"""
===========================================================
BigQuery related tasks
===========================================================
Script purpose:
    Script to create a connection with google BigQuery. Gets credentials from
    config.py

    Now contains a script to load flattened data from jolpica and transforms files
    to BigQuery.

Functions present:
    get_bigquery_client()
        - get bigquery client credentials from utils config
    load_to_bigquery()
        - load data to bigquery (as seen in ingestion/run_ingestion.py)

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



def load_to_bigquery(rows, table_name, write_mode="WRITE_TRUNCATE"):
    try:
        if not rows:
            logger.info(f"No rows to load for {table_name}, skipping.")
            return

        client = get_bigquery_client()
        table_ref = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{table_name}"

        if write_mode not in ["WRITE_APPEND", "WRITE_TRUNCATE"]:
            raise ValueError(f"Invalid write mode: {write_mode}")

        job_config = bigquery.LoadJobConfig(
            write_disposition=getattr(bigquery.WriteDisposition, write_mode)
        )
        
        load_job = client.load_table_from_json(rows, table_ref, job_config=job_config)
        load_job.result()
        logger.info(f"Total of {len(rows)} rows loaded to BigQuery!")
    
    except Exception as e:
        logger.error(f"Failed to load data to BigQuery: {e}")
        raise
