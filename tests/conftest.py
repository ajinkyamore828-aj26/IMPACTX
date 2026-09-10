"""
Pytest fixtures for impactx test suite.
"""

import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.graph.dependency_graph import DependencyGraph

@pytest.fixture
def mock_graph():
    g = DependencyGraph()
    g.add_node("main.py", "file", lines_of_code=100, language="Python")
    g.add_node("auth.py", "file", lines_of_code=50, language="Python")
    g.add_node("database.py", "file", lines_of_code=80, language="Python")
    g.add_node("dead_code.py", "file", lines_of_code=30, language="Python")

    g.add_edge("main.py", "auth.py", "imports")
    g.add_edge("auth.py", "database.py", "imports")
    g.add_edge("main.py", "database.py", "imports")
    return g
