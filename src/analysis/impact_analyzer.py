"""
Impact analyzer: performs static reachability and ML change impact analysis.
"""

from typing import Dict, List, Any, Optional
import networkx as nx

from src.graph.dependency_graph import DependencyGraph
from src.features.feature_extractor import FeatureExtractor
from src.ml.predict import PredictionEngine
from src.utils.logger import get_logger

logger = get_logger("impact_analyzer")

class ImpactAnalyzer:
    """Analyzes the blast radius and downstream ripple effects when code changes."""

    def __init__(self, dep_graph: DependencyGraph):
        self.dep_graph = dep_graph
        self.fe = FeatureExtractor(dep_graph)

    def analyze_impact(self, target_entity: str, max_depth: int = 5) -> Dict[str, Any]:
        """
        Analyzes all components affected if target_entity is modified.
        Returns detailed direct & indirect impact predictions with paths and risk scores.
        """
        if not self.dep_graph.graph.has_node(target_entity):
            return {
                "source": target_entity,
                "error": f"Entity '{target_entity}' not found in dependency graph.",
                "affected_components": [],
                "summary": {},
            }

        # 1. Reachability traversal: who depends on target_entity?
        # BFS traversal on the reverse dependency graph
        transitive_dependents = self.dep_graph.get_transitive_dependents(target_entity, max_depth=max_depth)
        
        # 2. Score each reachable dependent using ML prediction engine
        results: List[Dict[str, Any]] = []
        rev_graph = self.dep_graph.graph.reverse()

        for affected_id, dist in transitive_dependents.items():
            # Get node metadata
            node_data = self.dep_graph.graph.nodes.get(affected_id, {})
            
            # Predict impact probability & risk
            pred = PredictionEngine.predict_impact(
                source=target_entity,
                target=affected_id,
                dep_graph=self.dep_graph,
                fe=self.fe,
            )

            # Get dependency path (target_entity -> ... -> affected_id in reverse graph)
            path = []
            try:
                path = nx.shortest_path(rev_graph, target_entity, affected_id)
            except Exception:
                path = [target_entity, affected_id]

            results.append({
                "component": affected_id,
                "name": node_data.get("name", affected_id),
                "type": node_data.get("type", "unknown"),
                "language": node_data.get("language", "unknown"),
                "file_path": node_data.get("file_path", affected_id),
                "distance": dist,
                "level": "Direct (Level 1)" if dist == 1 else f"Indirect (Level {dist})",
                "probability": pred["probability"],
                "risk_level": pred["risk_level"],
                "is_ml": pred["is_ml_prediction"],
                "explanations": pred["explanations"],
                "path": path,
            })

        # Sort by distance ascending, then probability descending
        results.sort(key=lambda x: (x["distance"], -x["probability"]))

        # Compute summary metrics
        direct_count = sum(1 for r in results if r["distance"] == 1)
        indirect_count = sum(1 for r in results if r["distance"] > 1)
        high_risk_count = sum(1 for r in results if r["risk_level"] == "HIGH")
        medium_risk_count = sum(1 for r in results if r["risk_level"] == "MEDIUM")
        low_risk_count = sum(1 for r in results if r["risk_level"] == "LOW")

        # 3. Upstream dependencies: what does target_entity rely on?
        raw_deps = self.dep_graph.get_dependencies(target_entity)
        upstream_deps: List[Dict[str, Any]] = []
        for dep_id in raw_deps:
            dep_node = self.dep_graph.graph.nodes.get(dep_id, {})
            edge_data = self.dep_graph.graph.get_edge_data(target_entity, dep_id) or {}
            upstream_deps.append({
                "component": dep_id,
                "name": dep_node.get("name", dep_id),
                "type": dep_node.get("type", "unknown"),
                "language": dep_node.get("language", "unknown"),
                "relationship": edge_data.get("type", "depends_on"),
            })

        return {
            "source": target_entity,
            "total_affected": len(results),
            "direct_count": direct_count,
            "indirect_count": indirect_count,
            "high_risk_count": high_risk_count,
            "medium_risk_count": medium_risk_count,
            "low_risk_count": low_risk_count,
            "max_distance": max([r["distance"] for r in results], default=0),
            "affected_components": results,
            "upstream_dependencies": upstream_deps,
            "upstream_count": len(upstream_deps),
        }

