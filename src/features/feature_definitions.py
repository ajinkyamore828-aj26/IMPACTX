"""
Feature definitions and schema for impactx ML models.
"""

from typing import List

# Features used for single-entity analysis (Unused Code Detector)
ENTITY_FEATURE_NAMES: List[str] = [
    "lines_of_code",
    "function_count",
    "class_count",
    "import_count",
    "dependency_count",
    "dependent_count",
    "in_degree",
    "out_degree",
    "reference_count",
    "call_count",
    "complexity_score",
    "pagerank",
    "betweenness_centrality",
    "closeness_centrality",
    "is_entry_point",
    "is_test_file",
    "is_config_file",
    "is_private",
    "min_path_length",
    "num_external_deps",
]

# Features used for pairwise analysis (Impact Predictor: Source A -> Target B)
IMPACT_FEATURE_NAMES: List[str] = [
    # Source properties
    "source_loc",
    "source_complexity",
    "source_out_degree",
    "source_pagerank",
    "source_betweenness",
    "source_is_entry",
    # Target properties
    "target_loc",
    "target_complexity",
    "target_in_degree",
    "target_out_degree",
    "target_pagerank",
    "target_betweenness",
    "target_is_test",
    # Relational properties
    "dependency_distance",       # Shortest path in graph (or 99 if unreachable)
    "direct_dependency",         # 1 if direct edge, 0 otherwise
    "shared_dependencies_count", # Common downstream components
    "shared_dependents_count",   # Common upstream callers
    "same_module",               # 1 if in same directory/package, 0 otherwise
]
