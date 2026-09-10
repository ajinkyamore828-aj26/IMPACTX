"""
Master model training script for impactx.
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
from datetime import datetime

from config.config import (
    DATASET_PATH_IMPACT,
    DATASET_PATH_UNUSED,
    MODEL_METADATA_PATH,
)
from training.generate_dataset import generate_impact_dataset, generate_unused_dataset
from src.ml.train_impact_model import train_impact_pipeline
from src.ml.train_unused_model import train_unused_pipeline
from src.utils.logger import get_logger

logger = get_logger("train_models")

def run_training_suite() -> None:
    print("=" * 60)
    print("impactx ML Training Suite — Generating Datasets & Training Models")
    print("=" * 60)

    if not Path(DATASET_PATH_IMPACT).exists():
        print("[1/4] Generating Impact Prediction dataset...")
        generate_impact_dataset()
    else:
        print("[1/4] Impact dataset found.")

    if not Path(DATASET_PATH_UNUSED).exists():
        print("[2/4] Generating Unused Code dataset...")
        generate_unused_dataset()
    else:
        print("[2/4] Unused Code dataset found.")

    print("[3/4] Training and validating Impact Prediction model...")
    impact_model, impact_scaler, impact_metrics = train_impact_pipeline()
    print(f"  -> Impact Model ({impact_metrics['model_name']})")
    print(f"     Accuracy: {impact_metrics['accuracy']:.4f} | F1: {impact_metrics['f1']:.4f} | ROC-AUC: {impact_metrics['roc_auc']:.4f}")

    print("[4/4] Training and validating Unused Code Detection model...")
    unused_model, unused_scaler, unused_metrics = train_unused_pipeline()
    print(f"  -> Unused Code Model ({unused_metrics['model_name']})")
    print(f"     Accuracy: {unused_metrics['accuracy']:.4f} | F1: {unused_metrics['f1']:.4f} | ROC-AUC: {unused_metrics['roc_auc']:.4f}")

    metadata = {
        "training_date": datetime.now().isoformat(),
        "impact_model": {
            "model_type": impact_metrics["model_name"],
            "dataset_samples": impact_metrics["dataset_samples"],
            "accuracy": round(impact_metrics["accuracy"], 4),
            "precision": round(impact_metrics["precision"], 4),
            "recall": round(impact_metrics["recall"], 4),
            "f1": round(impact_metrics["f1"], 4),
            "roc_auc": round(impact_metrics["roc_auc"], 4),
            "confusion_matrix": impact_metrics["confusion_matrix"],
            "roc_curve": impact_metrics["roc_curve"],
            "feature_importance": impact_metrics["feature_importance"],
        },
        "unused_model": {
            "model_type": unused_metrics["model_name"],
            "dataset_samples": unused_metrics["dataset_samples"],
            "accuracy": round(unused_metrics["accuracy"], 4),
            "precision": round(unused_metrics["precision"], 4),
            "recall": round(unused_metrics["recall"], 4),
            "f1": round(unused_metrics["f1"], 4),
            "roc_auc": round(unused_metrics["roc_auc"], 4),
            "confusion_matrix": unused_metrics["confusion_matrix"],
            "roc_curve": unused_metrics["roc_curve"],
            "feature_importance": unused_metrics["feature_importance"],
        },
    }

    Path(MODEL_METADATA_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 60)
    print(f"Training completed successfully! Metadata saved to {MODEL_METADATA_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    run_training_suite()
