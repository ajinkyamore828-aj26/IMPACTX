"""
Dependency graph data structure and operations using NetworkX.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
import networkx as nx
from config.constants import EdgeType, EntityType
from src.utils.logger import get_logger

logger = get_logger("dependency_graph")

class DependencyGraph:
    """
    Directed dependency graph where an edge A -> B means entity A depends on entity B
    (e.g., A imports B, A calls B, A inherits from B).
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, entity_id: str, entity_type: str, **metadata) -> None:
        """Adds or updates a node in the graph."""
        self.graph.add_node(
            entity_id,
            id=entity_id,
            type=entity_type,
            **metadata
        )

    def add_edge(self, source: str, target: str, edge_type: str = EdgeType.IMPORTS, weight: float = 1.0) -> None:
        """
        Adds directed edge source -> target.
        source depends on target.
        """
        if not self.graph.has_node(source):
            self.add_node(source, EntityType.FILE, name=source)
        if not self.graph.has_node(target):
            self.add_node(target, EntityType.FILE, name=target)

        self.graph.add_edge(source, target, type=edge_type, weight=weight)

    def get_dependencies(self, node_id: str) -> List[str]:
        """Returns direct dependencies (successors) that node_id depends on."""
        if not self.graph.has_node(node_id):
            return []
        return list(self.graph.successors(node_id))

    def get_dependents(self, node_id: str) -> List[str]:
        """Returns direct dependents (predecessors) that depend on node_id."""
        if not self.graph.has_node(node_id):
            return []
        return list(self.graph.predecessors(node_id))

    def get_transitive_dependents(self, node_id: str, max_depth: int = 10) -> Dict[str, int]:
        """
        Traverses reverse graph to find all components affected by a change in node_id.
        Returns dict of {affected_node: distance}.
        """
        if not self.graph.has_node(node_id):
            return {}

        affected: Dict[str, int] = {}
        # BFS on reverse graph
        rev_graph = self.graph.reverse()
        lengths = nx.single_source_shortest_path_length(rev_graph, node_id, cutoff=max_depth)
        for target, dist in lengths.items():
            if target != node_id:
                affected[target] = dist
        return affected

    def get_shortest_dependency_path(self, source: str, target: str) -> Optional[List[str]]:
        """Returns shortest path from source to target if one exists."""
        try:
            return nx.shortest_path(self.graph, source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_file_level_graph(self) -> nx.DiGraph:
        """
        Creates a condensed file-level directed graph where nodes are files
        and edges aggregate all file, function, and class level relationships.
        """
        file_graph = nx.DiGraph()

        # Add all file nodes
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == EntityType.FILE:
                file_graph.add_node(node, **data)
            else:
                file_path = data.get("file_path")
                if file_path and not file_graph.has_node(file_path):
                    file_graph.add_node(file_path, type=EntityType.FILE, name=file_path, language=data.get("language", "Unknown"))

        # Aggregate edges
        for u, v, data in self.graph.edges(data=True):
            u_file = self.graph.nodes[u].get("file_path", u)
            v_file = self.graph.nodes[v].get("file_path", v)
            if u_file != v_file:
                if file_graph.has_edge(u_file, v_file):
                    file_graph[u_file][v_file]["weight"] += 1.0
                else:
                    file_graph.add_edge(u_file, v_file, type=data.get("type", EdgeType.IMPORTS), weight=1.0)

        return file_graph

    @property
    def number_of_nodes(self) -> int:
        return self.graph.number_of_nodes()

    @property
    def number_of_edges(self) -> int:
        return self.graph.number_of_edges()
