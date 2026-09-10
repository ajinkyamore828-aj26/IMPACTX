"""
Cycle detection engine for identifying circular dependencies.
"""

from typing import List
import networkx as nx
from src.graph.dependency_graph import DependencyGraph
from src.utils.logger import get_logger

logger = get_logger("cycle_detector")

class CycleDetector:
    """Detects cycles and circular dependencies in directed dependency graphs."""

    @classmethod
    def find_cycles(cls, dep_graph: DependencyGraph, max_cycles: int = 50) -> List[List[str]]:
        """
        Finds circular dependency chains up to max_cycles.
        Returns a list of cycles, where each cycle is a list of node IDs.
        """
        G = dep_graph.graph
        cycles: List[List[str]] = []
        try:
            for cycle in nx.simple_cycles(G):
                cycles.append(cycle)
                if len(cycles) >= max_cycles:
                    break
        except Exception as e:
            logger.warning(f"Cycle detection error: {e}")

        return cycles

    @classmethod
    def has_cycles(cls, dep_graph: DependencyGraph) -> bool:
        """Returns True if the dependency graph contains any directed cycle."""
        try:
            return not nx.is_directed_acyclic_graph(dep_graph.graph)
        except Exception:
            return False
