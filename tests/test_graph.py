"""
Dependency graph and metrics engine unit tests.
"""

from src.graph.dependency_graph import DependencyGraph
from src.graph.graph_metrics import GraphMetricsEngine
from src.graph.cycle_detector import CycleDetector

def test_dependency_graph_traversal(mock_graph):
    # main -> auth -> database, main -> database
    dependents = mock_graph.get_dependents("database.py")
    assert "auth.py" in dependents
    assert "main.py" in dependents

    transitive = mock_graph.get_transitive_dependents("database.py")
    assert "main.py" in transitive
    assert "auth.py" in transitive

def test_graph_metrics(mock_graph):
    metrics = GraphMetricsEngine.compute_all_metrics(mock_graph)
    assert "database.py" in metrics
    assert metrics["database.py"]["in_degree"] == 2
    assert metrics["main.py"]["out_degree"] == 2
    assert metrics["database.py"]["pagerank"] > 0

def test_cycle_detector():
    g = DependencyGraph()
    g.add_edge("a.py", "b.py", "imports")
    g.add_edge("b.py", "c.py", "imports")
    g.add_edge("c.py", "a.py", "imports")

    assert CycleDetector.has_cycles(g)
    cycles = CycleDetector.find_cycles(g)
    assert len(cycles) >= 1
