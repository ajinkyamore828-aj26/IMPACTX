"""
Model loader and memory cache for trained models and metadata.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import joblib

from config.config import (
    MODEL_PATH_IMPACT,
    MODEL_PATH_UNUSED,
    MODEL_PATH_IMPACT_SCALER,
    MODEL_PATH_UNUSED_SCALER,
    MODEL_METADATA_PATH,
)
from src.utils.logger import get_logger

logger = get_logger("model_loader")

class ModelRegistry:
    """Singleton loader for impactx ML models and artifacts."""
    _impact_model: Optional[Any] = None
    _unused_model: Optional[Any] = None
    _impact_scaler: Optional[Any] = None
    _unused_scaler: Optional[Any] = None
    _metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def get_impact_model(cls) -> Optional[Any]:
        if cls._impact_model is None and Path(MODEL_PATH_IMPACT).exists():
            try:
                cls._impact_model = joblib.load(MODEL_PATH_IMPACT)
                logger.info(f"Loaded impact model from {MODEL_PATH_IMPACT}")
            except Exception as e:
                logger.error(f"Failed to load impact model: {e}")
        return cls._impact_model

    @classmethod
    def get_unused_model(cls) -> Optional[Any]:
        if cls._unused_model is None and Path(MODEL_PATH_UNUSED).exists():
            try:
                cls._unused_model = joblib.load(MODEL_PATH_UNUSED)
                logger.info(f"Loaded unused code model from {MODEL_PATH_UNUSED}")
            except Exception as e:
                logger.error(f"Failed to load unused code model: {e}")
        return cls._unused_model

    @classmethod
    def get_impact_scaler(cls) -> Optional[Any]:
        if cls._impact_scaler is None and Path(MODEL_PATH_IMPACT_SCALER).exists():
            try:
                cls._impact_scaler = joblib.load(MODEL_PATH_IMPACT_SCALER)
            except Exception as e:
                logger.error(f"Failed to load impact scaler: {e}")
        return cls._impact_scaler

    @classmethod
    def get_unused_scaler(cls) -> Optional[Any]:
        if cls._unused_scaler is None and Path(MODEL_PATH_UNUSED_SCALER).exists():
            try:
                cls._unused_scaler = joblib.load(MODEL_PATH_UNUSED_SCALER)
            except Exception as e:
                logger.error(f"Failed to load unused scaler: {e}")
        return cls._unused_scaler

    @classmethod
    def get_scaler(cls) -> Optional[Any]:
        return cls.get_impact_scaler()

    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        if cls._metadata is None and Path(MODEL_METADATA_PATH).exists():
            try:
                with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as f:
                    cls._metadata = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load model metadata: {e}")
                cls._metadata = {}
        return cls._metadata or {}

    @classmethod
    def reload(cls) -> None:
        cls._impact_model = None
        cls._unused_model = None
        cls._impact_scaler = None
        cls._unused_scaler = None
        cls._metadata = None
