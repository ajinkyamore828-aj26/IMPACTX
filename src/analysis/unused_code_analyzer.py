"""
Unused code analyzer: identifies dead code, unreferenced entities, and orphaned files.
"""

from typing import Dict, List, Any
from pathlib import Path

from src.graph.dependency_graph import DependencyGraph
from src.features.feature_extractor import FeatureExtractor
from src.ml.predict import PredictionEngine
from config.constants import EntityType
from src.utils.logger import get_logger

logger = get_logger("unused_code_analyzer")

class UnusedCodeAnalyzer:
    """Detects potentially unused functions, classes, and orphaned files."""

    def __init__(self, dep_graph: DependencyGraph):
        self.dep_graph = dep_graph
        self.fe = FeatureExtractor(dep_graph)

    def analyze_unused(self) -> List[Dict[str, Any]]:
        """
        Scans all nodes in the dependency graph to identify unused or orphaned code.
        Returns candidates ranked by unused probability descending.
        """
        candidates: List[Dict[str, Any]] = []

        for node_id, data in self.dep_graph.graph.nodes(data=True):
            entity_type = data.get("type", "unknown")
            name = data.get("name", node_id)
            file_path = data.get("file_path", node_id)

            # Skip test files and setup/init wrappers from dead code false alarms
            file_lower = Path(file_path).name.lower()
            if any(k in file_lower for k in ("test", "spec", "_test", "conftest")):
                continue

            # Special python dunder methods (__init__, __str__, etc.) are not unused
            if name.startswith("__") and name.endswith("__"):
                continue

            # Run ML prediction
            pred = PredictionEngine.predict_unused(
                entity_id=node_id,
                dep_graph=self.dep_graph,
                fe=self.fe,
            )

            # Heuristic booster: zero references
            refs = pred["reference_count"]
            prob = pred["probability"]
            risk = pred["risk_level"]

            candidates.append({
                "entity_id": node_id,
                "name": name,
                "type": entity_type,
                "file_path": file_path,
                "language": data.get("language", "unknown"),
                "line_start": data.get("line_start", 0),
                "line_end": data.get("line_end", 0),
                "lines_of_code": data.get("lines_of_code", 0),
                "reference_count": refs,
                "unused_probability": prob,
                "risk_level": risk,
                "is_ml": pred["is_ml_prediction"],
                "reasons": pred["reasons"],
            })

        # Sort: Highest probability first, then lowest reference count
        candidates.sort(key=lambda x: (-x["unused_probability"], x["reference_count"]))
        return candidates
