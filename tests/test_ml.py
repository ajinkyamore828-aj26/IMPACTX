"""
Machine Learning inference and prediction tests.
"""

from src.ml.model_loader import ModelRegistry
from src.ml.predict import PredictionEngine
from config.constants import RISK_THRESHOLDS

def test_model_loading():
    impact_model = ModelRegistry.get_impact_model()
    unused_model = ModelRegistry.get_unused_model()
    assert impact_model is not None
    assert unused_model is not None

def test_impact_prediction(mock_graph):
    res = PredictionEngine.predict_impact("database.py", "main.py", mock_graph)
    assert 0.0 <= res["probability"] <= 1.0
    assert res["risk_level"] in ("HIGH", "MEDIUM", "LOW")
    assert res["is_ml_prediction"] is True

def test_unused_prediction(mock_graph):
    res = PredictionEngine.predict_unused("dead_code.py", mock_graph)
    assert 0.0 <= res["probability"] <= 1.0
    assert res["risk_level"] in ("HIGH", "MEDIUM", "LOW")
    assert res["is_ml_prediction"] is True
