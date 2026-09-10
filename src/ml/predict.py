"""
ML Prediction and inference engine for impact and unused code analysis.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from src.graph.dependency_graph import DependencyGraph
from src.features.feature_extractor import FeatureExtractor
from src.ml.model_loader import ModelRegistry
from config.constants import get_risk_level
from src.utils.logger import get_logger

logger = get_logger("predict")

class PredictionEngine:
    """Provides inference and explainability for change impact and unused code."""

    @classmethod
    def predict_impact(
        cls,
        source: str,
        target: str,
        dep_graph: DependencyGraph,
        fe: Optional[FeatureExtractor] = None,
    ) -> Dict[str, Any]:
        if fe is None:
            fe = FeatureExtractor(dep_graph)

        features_dict = fe.extract_impact_features(source, target)
        df_features = pd.DataFrame([features_dict])

        model = ModelRegistry.get_impact_model()
        scaler = ModelRegistry.get_impact_scaler()

        if model is not None:
            try:
                X = scaler.transform(df_features.values) if scaler is not None else df_features.values
                if hasattr(model, "predict_proba"):
                    prob = float(model.predict_proba(X)[0][1])
                else:
                    prob = float(model.predict(X)[0])
                is_ml = True
            except Exception as e:
                logger.warning(f"ML inference error for impact, falling back to static heuristic: {e}")
                prob = cls._static_impact_heuristic(features_dict)
                is_ml = False
        else:
            prob = cls._static_impact_heuristic(features_dict)
            is_ml = False

        prob = max(0.01, min(0.99, prob))
        risk = get_risk_level(prob)

        explanations = []
        if features_dict.get("direct_dependency", 0) == 1.0:
            explanations.append("Direct syntactic dependency (distance = 1)")
        elif features_dict.get("dependency_distance", 99) <= 2:
            explanations.append(f"Transitive dependency within {int(features_dict['dependency_distance'])} hops")
        
        if features_dict.get("same_module", 0) == 1.0:
            explanations.append("Co-located in same directory/package")
        if features_dict.get("shared_dependencies_count", 0) > 0:
            explanations.append(f"Shares {int(features_dict['shared_dependencies_count'])} common dependencies")

        return {
            "source": source,
            "target": target,
            "probability": round(prob, 4),
            "risk_level": risk,
            "is_ml_prediction": is_ml,
            "distance": features_dict.get("dependency_distance", 99),
            "explanations": explanations,
            "features": features_dict,
        }

    @classmethod
    def predict_unused(
        cls,
        entity_id: str,
        dep_graph: DependencyGraph,
        fe: Optional[FeatureExtractor] = None,
    ) -> Dict[str, Any]:
        if fe is None:
            fe = FeatureExtractor(dep_graph)

        features_dict = fe.extract_entity_features(entity_id)
        df_features = pd.DataFrame([features_dict])

        model = ModelRegistry.get_unused_model()
        scaler = ModelRegistry.get_unused_scaler()

        if model is not None:
            try:
                X = scaler.transform(df_features.values) if scaler is not None else df_features.values
                if hasattr(model, "predict_proba"):
                    prob = float(model.predict_proba(X)[0][1])
                else:
                    prob = float(model.predict(X)[0])
                is_ml = True
            except Exception as e:
                logger.warning(f"ML inference error for unused, falling back to static heuristic: {e}")
                prob = cls._static_unused_heuristic(features_dict)
                is_ml = False
        else:
            prob = cls._static_unused_heuristic(features_dict)
            is_ml = False

        prob = max(0.01, min(0.99, prob))
        risk = get_risk_level(prob)

        reasons = []
        if features_dict.get("reference_count", 0) == 0:
            reasons.append("Zero static incoming references")
        if features_dict.get("is_entry_point", 0) == 1.0:
            reasons.append("Recognized entry point module")
        if features_dict.get("is_test_file", 0) == 1.0:
            reasons.append("Test suite code")
        if features_dict.get("is_private", 0) == 1.0:
            reasons.append("Private/internal naming convention")

        return {
            "entity_id": entity_id,
            "probability": round(prob, 4),
            "risk_level": risk,
            "is_ml_prediction": is_ml,
            "reference_count": int(features_dict.get("reference_count", 0)),
            "reasons": reasons,
            "features": features_dict,
        }

    @staticmethod
    def _static_impact_heuristic(f: Dict[str, float]) -> float:
        dist = f.get("dependency_distance", 99.0)
        if dist == 1.0:
            return 0.88
        elif dist == 2.0:
            return 0.62
        elif dist <= 4.0:
            return 0.35
        elif f.get("same_module", 0) == 1.0:
            return 0.25
        return 0.05

    @staticmethod
    def _static_unused_heuristic(f: Dict[str, float]) -> float:
        if f.get("is_entry_point", 0) == 1.0:
            return 0.02
        if f.get("is_test_file", 0) == 1.0:
            return 0.05
        refs = f.get("reference_count", 0)
        if refs == 0:
            return 0.85
        elif refs == 1:
            return 0.30
        return 0.05
