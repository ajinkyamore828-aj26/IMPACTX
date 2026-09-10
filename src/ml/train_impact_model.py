"""
Training module for Change Impact Prediction model.
"""

from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
from pathlib import Path

from config.config import DATASET_PATH_IMPACT, MODEL_PATH_IMPACT, MODEL_PATH_IMPACT_SCALER
from src.features.feature_definitions import IMPACT_FEATURE_NAMES
from src.ml.evaluate import evaluate_classifier
from src.utils.logger import get_logger

logger = get_logger("train_impact_model")

def train_impact_pipeline() -> Tuple[Any, StandardScaler, Dict[str, Any]]:
    df = pd.read_csv(DATASET_PATH_IMPACT)
    X = df[IMPACT_FEATURE_NAMES].values
    y = df["affected"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
    )
    rf.fit(X_train_scaled, y_train)
    rf_metrics = evaluate_classifier(rf, X_test_scaled, y_test, IMPACT_FEATURE_NAMES)

    xgb_model = xgb.XGBClassifier(
        max_depth=6,
        learning_rate=0.08,
        n_estimators=180,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        eval_metric="logloss",
    )
    xgb_model.fit(X_train_scaled, y_train)
    xgb_metrics = evaluate_classifier(xgb_model, X_test_scaled, y_test, IMPACT_FEATURE_NAMES)

    if xgb_metrics["f1"] >= rf_metrics["f1"]:
        best_model = xgb_model
        best_metrics = xgb_metrics
        model_name = "XGBoostClassifier"
    else:
        best_model = rf
        best_metrics = rf_metrics
        model_name = "RandomForestClassifier"

    best_metrics["model_name"] = model_name
    best_metrics["dataset_samples"] = len(df)
    
    Path(MODEL_PATH_IMPACT).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH_IMPACT)
    joblib.dump(scaler, MODEL_PATH_IMPACT_SCALER)
    logger.info(f"Saved best impact model ({model_name}) to {MODEL_PATH_IMPACT}")

    return best_model, scaler, best_metrics
