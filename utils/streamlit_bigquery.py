"""
===========================================================
Create the main page of the app (home page)
===========================================================
Script purpose:
    This script's purpose is to create the main page for the app;
    includes the app title, description, and others.

"""

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from utils.config import GCP_PROJECT_ID, KEY_PATH
import logging

logger = logging.getLogger(__name__)

@st.cache_resource
def get_bq_client():
    try:
        if "gcp" in st.secrets:
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp"]
            )
        else:
            from utils.config import KEY_PATH
            credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        
        client = bigquery.Client(project=GCP_PROJECT_ID, credentials=credentials)
        return client

    except Exception as e:
        logger.error(f"Failed to create a connection with BigQuery: {e}")
        raise

@st.cache_data(ttl=3600)
def run_query(query):
    client = get_bq_client()
    return client.query(query).to_dataframe()