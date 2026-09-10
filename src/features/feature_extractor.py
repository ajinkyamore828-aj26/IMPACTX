"""
Feature extractor for generating ML feature matrices.
"""

from typing import Dict, Any, List, Optional
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path

from src.graph.dependency_graph import DependencyGraph
from src.graph.graph_metrics import GraphMetricsEngine
from src.features.feature_definitions import ENTITY_FEATURE_NAMES, IMPACT_FEATURE_NAMES
from src.utils.logger import get_logger

logger = get_logger("feature_extractor")

class FeatureExtractor:
    """Extracts structural, lexical, and graph-theoretic features from code entities."""

    def __init__(self, dep_graph: DependencyGraph):
        self.dep_graph = dep_graph
        self.metrics = GraphMetricsEngine.compute_all_metrics(dep_graph)

    def extract_entity_features(self, entity_id: str, node_data: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """Extracts numerical features for a single entity (for Unused Code Detection)."""
        if node_data is None:
            node_data = self.dep_graph.graph.nodes.get(entity_id, {})

        metrics = self.metrics.get(entity_id, {})
        
        name_lower = str(entity_id).lower()
        file_name = Path(node_data.get("file_path", entity_id)).name.lower()

        is_entry = 1.0 if any(k in file_name for k in ("main", "index", "app", "server", "cli", "__main__")) else 0.0
        is_test = 1.0 if any(k in file_name for k in ("test", "spec", "_test", "tests")) else 0.0
        is_config = 1.0 if any(k in file_name for k in ("config", "setting", "constant", "setup")) else 0.0
        is_private = 1.0 if Path(entity_id).stem.startswith("_") or entity_id.split("/")[-1].startswith("_") else 0.0

        # Calculate min distance to any entry point
        min_path_len = 99.0
        try:
            entry_points = [
                n for n in self.dep_graph.graph.nodes()
                if any(k in str(n).lower() for k in ("main", "index", "app"))
            ]
            if entry_points:
                paths = [
                    nx.shortest_path_length(self.dep_graph.graph, ep, entity_id)
                    for ep in entry_points
                    if nx.has_path(self.dep_graph.graph, ep, entity_id)
                ]
                if paths:
                    min_path_len = float(min(paths))
        except Exception:
            pass

        return {
            "lines_of_code": float(node_data.get("lines_of_code", 10)),
            "function_count": float(node_data.get("function_count", 0)),
            "class_count": float(node_data.get("class_count", 0)),
            "import_count": float(node_data.get("import_count", metrics.get("out_degree", 0))),
            "dependency_count": float(metrics.get("out_degree", 0)),
            "dependent_count": float(metrics.get("in_degree", 0)),
            "in_degree": float(metrics.get("in_degree", 0)),
            "out_degree": float(metrics.get("out_degree", 0)),
            "reference_count": float(metrics.get("in_degree", 0)),
            "call_count": float(node_data.get("call_count", 0)),
            "complexity_score": float(node_data.get("complexity_score", 1.0)),
            "pagerank": float(metrics.get("pagerank", 0.001)),
            "betweenness_centrality": float(metrics.get("betweenness", 0.0)),
            "closeness_centrality": float(metrics.get("closeness", 0.0)),
            "is_entry_point": is_entry,
            "is_test_file": is_test,
            "is_config_file": is_config,
            "is_private": is_private,
            "min_path_length": min_path_len,
            "num_external_deps": float(node_data.get("num_external_deps", 0)),
        }

    def extract_impact_features(self, source_id: str, target_id: str) -> Dict[str, float]:
        """Extracts pairwise relational features (for Impact Prediction: source -> target)."""
        src_data = self.dep_graph.graph.nodes.get(source_id, {})
        tgt_data = self.dep_graph.graph.nodes.get(target_id, {})
        src_met = self.metrics.get(source_id, {})
        tgt_met = self.metrics.get(target_id, {})

        # Relational metrics
        # Shortest distance in directed graph (does target depend on source, or source depend on target)
        dist = 99.0
        try:
            # Does target depend on source? i.e. target -> ... -> source
            if nx.has_path(self.dep_graph.graph, target_id, source_id):
                dist = float(nx.shortest_path_length(self.dep_graph.graph, target_id, source_id))
            elif nx.has_path(self.dep_graph.graph, source_id, target_id):
                dist = float(nx.shortest_path_length(self.dep_graph.graph, source_id, target_id))
        except Exception:
            pass

        direct_dep = 1.0 if (self.dep_graph.graph.has_edge(target_id, source_id) or self.dep_graph.graph.has_edge(source_id, target_id)) else 0.0

        # Shared neighbors
        src_succ = set(self.dep_graph.graph.successors(source_id)) if self.dep_graph.graph.has_node(source_id) else set()
        tgt_succ = set(self.dep_graph.graph.successors(target_id)) if self.dep_graph.graph.has_node(target_id) else set()
        shared_deps = float(len(src_succ.intersection(tgt_succ)))

        src_pred = set(self.dep_graph.graph.predecessors(source_id)) if self.dep_graph.graph.has_node(source_id) else set()
        tgt_pred = set(self.dep_graph.graph.predecessors(target_id)) if self.dep_graph.graph.has_node(target_id) else set()
        shared_dependents = float(len(src_pred.intersection(tgt_pred)))

        # Check if same directory
        same_mod = 1.0 if Path(source_id).parent == Path(target_id).parent else 0.0

        src_file = Path(source_id).name.lower()
        tgt_file = Path(target_id).name.lower()
        src_is_entry = 1.0 if any(k in src_file for k in ("main", "index", "app")) else 0.0
        tgt_is_test = 1.0 if any(k in tgt_file for k in ("test", "spec")) else 0.0

        return {
            "source_loc": float(src_data.get("lines_of_code", 20)),
            "source_complexity": float(src_data.get("complexity_score", 1.0)),
            "source_out_degree": float(src_met.get("out_degree", 0)),
            "source_pagerank": float(src_met.get("pagerank", 0.001)),
            "source_betweenness": float(src_met.get("betweenness", 0.0)),
            "source_is_entry": src_is_entry,
            "target_loc": float(tgt_data.get("lines_of_code", 20)),
            "target_complexity": float(tgt_data.get("complexity_score", 1.0)),
            "target_in_degree": float(tgt_met.get("in_degree", 0)),
            "target_out_degree": float(tgt_met.get("out_degree", 0)),
            "target_pagerank": float(tgt_met.get("pagerank", 0.001)),
            "target_betweenness": float(tgt_met.get("betweenness", 0.0)),
            "target_is_test": tgt_is_test,
            "dependency_distance": dist,
            "direct_dependency": direct_dep,
            "shared_dependencies_count": shared_deps,
            "shared_dependents_count": shared_dependents,
            "same_module": same_mod,
        }

    def to_entity_dataframe(self, entities: List[str]) -> pd.DataFrame:
        """Converts a list of entities to a DataFrame with ENTITY_FEATURE_NAMES."""
        rows = [self.extract_entity_features(e) for e in entities]
        df = pd.DataFrame(rows)
        for col in ENTITY_FEATURE_NAMES:
            if col not in df.columns:
                df[col] = 0.0
        return df[ENTITY_FEATURE_NAMES]

    def to_impact_dataframe(self, pairs: List[tuple[str, str]]) -> pd.DataFrame:
        """Converts a list of (source, target) pairs to a DataFrame with IMPACT_FEATURE_NAMES."""
        rows = [self.extract_impact_features(s, t) for s, t in pairs]
        df = pd.DataFrame(rows)
        for col in IMPACT_FEATURE_NAMES:
            if col not in df.columns:
                df[col] = 0.0
        return df[IMPACT_FEATURE_NAMES]
