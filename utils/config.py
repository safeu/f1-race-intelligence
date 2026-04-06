"""
===========================================================
Loading secret variables
===========================================================
Script purpose:
    Script to fetch/load .env variables 
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


KEY_PATH = os.getenv("KEY_PATH")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")

if not KEY_PATH:
    raise ValueError("KEY_PATH is not set in .env")
if not GCP_PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID is not set in .env")
if not BQ_DATASET:
    raise ValueError("BQ_DATASET is not set in .env")

