"""
===========================================================
Create connection with google BigQuery
===========================================================
Script purpose:
    Script to create a connection with google BigQuery. Gets credentials from
    config.py
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