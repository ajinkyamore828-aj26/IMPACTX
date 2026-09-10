"""
Data preprocessing and feature scaling utilities for ML models.
"""

from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
from config.config import MODEL_PATH_SCALER
from src.utils.logger import get_logger

logger = get_logger("preprocessing")

class Preprocessor:
    """Scales and normalizes feature vectors using scikit-learn StandardScaler."""

    def __init__(self):
        self.scaler: Optional[StandardScaler] = None

    def fit_transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(X)

    def transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        if self.scaler is None:
            if Path(MODEL_PATH_SCALER).exists():
                self.load(MODEL_PATH_SCALER)
            else:
                return np.array(X)
        return self.scaler.transform(X)

    def save(self, file_path: str | Path = MODEL_PATH_SCALER) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, file_path)
        logger.info(f"Saved feature scaler to {file_path}")

    def load(self, file_path: str | Path = MODEL_PATH_SCALER) -> None:
        self.scaler = joblib.load(file_path)
        logger.info(f"Loaded feature scaler from {file_path}")
