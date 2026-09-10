"""
Graph metrics engine for centrality, degrees, PageRank, and hub identification.
Uses approximations for large graphs to stay fast.
"""

from typing import Dict, Any, List
import networkx as nx
from src.graph.dependency_graph import DependencyGraph
from src.utils.logger import get_logger

logger = get_logger("graph_metrics")

# Thresholds for approximation mode
_APPROX_THRESHOLD = 500   # nodes; above this use sampled betweenness
_BETWEENNESS_K = 100      # sample size for betweenness approximation
_SKIP_CLOSENESS_THRESHOLD = 1000  # skip closeness entirely above this


class GraphMetricsEngine:
    """Calculates structural and centrality metrics for dependency graphs."""

    @classmethod
    def compute_all_metrics(cls, dep_graph: DependencyGraph) -> Dict[str, Dict[str, Any]]:
        """
        Computes all metrics for all nodes in the graph.
        Uses approximations for large graphs to stay fast.
        Returns: {node_id: {metric_name: value}}
        """
        G = dep_graph.graph
        n = G.number_of_nodes()
        if n == 0:
            return {}

        metrics: Dict[str, Dict[str, Any]] = {}

        # Degrees — O(V+E), always fast
        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())

        # PageRank — faster convergence with looser tolerance
        try:
            pageranks = nx.pagerank(G, alpha=0.85, max_iter=100, tol=1e-4)
        except Exception as e:
            logger.warning(f"PageRank fallback due to: {e}")
            pageranks = {node: 1.0 / n for node in G.nodes()}

        # Betweenness Centrality — approximate on large graphs
        try:
            if n > _APPROX_THRESHOLD:
                k = min(_BETWEENNESS_K, n)
                betweenness = nx.betweenness_centrality(G, normalized=True, k=k)
            else:
                betweenness = nx.betweenness_centrality(G, normalized=True)
        except Exception:
            betweenness = {node: 0.0 for node in G.nodes()}

        # Closeness Centrality — skip on very large graphs
        try:
            if n > _SKIP_CLOSENESS_THRESHOLD:
                closeness = {node: 0.0 for node in G.nodes()}
            else:
                closeness = nx.closeness_centrality(G)
        except Exception:
            closeness = {node: 0.0 for node in G.nodes()}

        # Clustering — skip on very large graphs (undirected conversion is costly)
        try:
            if n > _SKIP_CLOSENESS_THRESHOLD:
                clustering = {node: 0.0 for node in G.nodes()}
            else:
                undirected = G.to_undirected()
                clustering = nx.clustering(undirected)
        except Exception:
            clustering = {node: 0.0 for node in G.nodes()}

        for node in G.nodes():
            node_data = G.nodes[node]
            metrics[node] = {
                "in_degree": in_degrees.get(node, 0),
                "out_degree": out_degrees.get(node, 0),
                "pagerank": float(pageranks.get(node, 0.0)),
                "betweenness": float(betweenness.get(node, 0.0)),
                "closeness": float(closeness.get(node, 0.0)),
                "clustering": float(clustering.get(node, 0.0)),
                "dependents_count": in_degrees.get(node, 0),
                "dependencies_count": out_degrees.get(node, 0),
                "entity_type": node_data.get("type", "unknown"),
                "language": node_data.get("language", "unknown"),
                "lines_of_code": node_data.get("lines_of_code", 0),
            }

        return metrics

    @classmethod
    def get_top_hubs(cls, dep_graph: DependencyGraph, top_n: int = 10) -> List[Dict[str, Any]]:
        """Returns the top N architectural hub components ranked by PageRank & In-Degree."""
        metrics = cls.compute_all_metrics(dep_graph)
        ranked = sorted(
            [{"id": node, **data} for node, data in metrics.items()],
            key=lambda x: (x["pagerank"], x["in_degree"]),
            reverse=True
        )
        return ranked[:top_n]
