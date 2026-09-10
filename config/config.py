"""
Central configuration settings for impactx.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLES_DIR = BASE_DIR / "sample_projects"
TRAINING_DIR = BASE_DIR / "training"
DATASETS_DIR = TRAINING_DIR / "datasets"

# Security & Limits
MAX_UPLOAD_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", 500 * 1024 * 1024))
MAX_EXTRACTED_SIZE_BYTES = int(os.getenv("MAX_EXTRACTED_SIZE_BYTES", 1500 * 1024 * 1024))
MAX_FILE_COUNT = int(os.getenv("MAX_FILE_COUNT", 10_000))
MAX_ZIP_RATIO = 100
MAX_GRAPH_NODES_VISUALIZE = 500

# Model Paths
MODEL_PATH_IMPACT = MODELS_DIR / "impact_model.pkl"
MODEL_PATH_UNUSED = MODELS_DIR / "unused_code_model.pkl"
MODEL_PATH_IMPACT_SCALER = MODELS_DIR / "impact_scaler.pkl"
MODEL_PATH_UNUSED_SCALER = MODELS_DIR / "unused_scaler.pkl"
MODEL_PATH_SCALER = MODEL_PATH_IMPACT_SCALER
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"

# Datasets
DATASET_PATH_IMPACT = DATASETS_DIR / "impact_dataset.csv"
DATASET_PATH_UNUSED = DATASETS_DIR / "unused_code_dataset.csv"

# Cache & Runtime Settings
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_THEME = "dark"
