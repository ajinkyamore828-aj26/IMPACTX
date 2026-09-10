"""
Feature extraction tests.
"""

from src.features.feature_extractor import FeatureExtractor
from src.features.feature_definitions import ENTITY_FEATURE_NAMES, IMPACT_FEATURE_NAMES

def test_feature_extraction(mock_graph):
    fe = FeatureExtractor(mock_graph)

    entity_features = fe.extract_entity_features("main.py")
    assert len(entity_features) == len(ENTITY_FEATURE_NAMES)
    assert entity_features["is_entry_point"] == 1.0

    impact_features = fe.extract_impact_features("database.py", "main.py")
    assert len(impact_features) == len(IMPACT_FEATURE_NAMES)
    assert impact_features["dependency_distance"] == 1.0

def test_dataframe_conversion(mock_graph):
    fe = FeatureExtractor(mock_graph)
    df_e = fe.to_entity_dataframe(["main.py", "auth.py"])
    assert df_e.shape == (2, len(ENTITY_FEATURE_NAMES))

    df_i = fe.to_impact_dataframe([("database.py", "main.py")])
    assert df_i.shape == (1, len(IMPACT_FEATURE_NAMES))
