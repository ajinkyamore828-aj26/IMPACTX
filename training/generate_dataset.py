"""
Dataset generator for Impact Prediction and Unused Code Detection.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd

from config.config import DATASET_PATH_IMPACT, DATASET_PATH_UNUSED
from src.features.feature_definitions import ENTITY_FEATURE_NAMES, IMPACT_FEATURE_NAMES
from src.utils.logger import get_logger

logger = get_logger("generate_dataset")

def generate_impact_dataset(num_samples: int = 3000, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)

    source_loc = np.random.exponential(scale=80, size=num_samples) + 10
    source_complexity = np.random.gamma(shape=2, scale=2, size=num_samples) + 1
    source_out_degree = np.random.poisson(lam=4, size=num_samples)
    source_pagerank = np.random.beta(a=1, b=20, size=num_samples) * 0.1
    source_betweenness = np.random.beta(a=1, b=50, size=num_samples) * 0.05
    source_is_entry = np.random.choice([0.0, 1.0], size=num_samples, p=[0.9, 0.1])

    target_loc = np.random.exponential(scale=60, size=num_samples) + 5
    target_complexity = np.random.gamma(shape=2, scale=1.5, size=num_samples) + 1
    target_in_degree = np.random.poisson(lam=3, size=num_samples)
    target_out_degree = np.random.poisson(lam=3, size=num_samples)
    target_pagerank = np.random.beta(a=1, b=20, size=num_samples) * 0.1
    target_betweenness = np.random.beta(a=1, b=50, size=num_samples) * 0.05
    target_is_test = np.random.choice([0.0, 1.0], size=num_samples, p=[0.85, 0.15])

    distances = np.random.choice([1.0, 2.0, 3.0, 4.0, 99.0], size=num_samples, p=[0.25, 0.25, 0.20, 0.10, 0.20])
    direct_dep = np.where(distances == 1.0, 1.0, 0.0)
    shared_deps = np.where(distances <= 2.0, np.random.poisson(lam=2, size=num_samples), 0.0)
    shared_dependents = np.where(distances <= 2.0, np.random.poisson(lam=1.5, size=num_samples), 0.0)
    same_mod = np.where(distances == 1.0, np.random.choice([0.0, 1.0], size=num_samples, p=[0.4, 0.6]),
               np.where(distances == 2.0, np.random.choice([0.0, 1.0], size=num_samples, p=[0.7, 0.3]), 0.0))

    logits = (
        3.2 * direct_dep
        + 1.8 * (distances == 2.0)
        + 0.8 * (distances == 3.0)
        - 3.5 * (distances >= 99.0)
        + 1.2 * same_mod
        + 0.3 * shared_deps
        + 0.2 * target_in_degree
        + 0.8 * target_is_test * (distances <= 2.0)
        + np.random.normal(0, 0.6, size=num_samples)
    )

    probs = 1 / (1 + np.exp(-logits))
    labels = (probs > 0.5).astype(int)

    df = pd.DataFrame({
        "source_loc": source_loc,
        "source_complexity": source_complexity,
        "source_out_degree": source_out_degree,
        "source_pagerank": source_pagerank,
        "source_betweenness": source_betweenness,
        "source_is_entry": source_is_entry,
        "target_loc": target_loc,
        "target_complexity": target_complexity,
        "target_in_degree": target_in_degree,
        "target_out_degree": target_out_degree,
        "target_pagerank": target_pagerank,
        "target_betweenness": target_betweenness,
        "target_is_test": target_is_test,
        "dependency_distance": distances,
        "direct_dependency": direct_dep,
        "shared_dependencies_count": shared_deps,
        "shared_dependents_count": shared_dependents,
        "same_module": same_mod,
        "affected": labels,
    })

    Path(DATASET_PATH_IMPACT).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH_IMPACT, index=False)
    logger.info(f"Generated impact dataset: {df.shape[0]} rows")
    return df

def generate_unused_dataset(num_samples: int = 2500, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)

    lines_of_code = np.random.exponential(scale=45, size=num_samples) + 5
    function_count = np.random.poisson(lam=3, size=num_samples)
    class_count = np.random.choice([0, 1, 2], size=num_samples, p=[0.7, 0.25, 0.05])
    import_count = np.random.poisson(lam=4, size=num_samples)
    
    is_zero_ref = np.random.choice([0, 1], size=num_samples, p=[0.75, 0.25])
    in_degree = np.where(is_zero_ref == 1, 0, np.random.geometric(p=0.3, size=num_samples))
    out_degree = np.random.poisson(lam=3, size=num_samples)
    reference_count = in_degree.copy()
    call_count = np.random.poisson(lam=5, size=num_samples)
    complexity = np.random.gamma(shape=2, scale=1.5, size=num_samples) + 1

    pagerank = np.where(in_degree == 0, np.random.uniform(0.0001, 0.001, size=num_samples), np.random.beta(a=1, b=15, size=num_samples) * 0.1)
    betweenness = np.where(in_degree == 0, 0.0, np.random.beta(a=1, b=40, size=num_samples) * 0.05)
    closeness = np.random.uniform(0.01, 0.5, size=num_samples)

    is_entry = np.random.choice([0.0, 1.0], size=num_samples, p=[0.92, 0.08])
    is_test = np.random.choice([0.0, 1.0], size=num_samples, p=[0.85, 0.15])
    is_config = np.random.choice([0.0, 1.0], size=num_samples, p=[0.90, 0.10])
    is_private = np.random.choice([0.0, 1.0], size=num_samples, p=[0.80, 0.20])
    min_path_len = np.where(in_degree == 0, 99.0, np.random.choice([1.0, 2.0, 3.0], size=num_samples))
    num_ext_deps = np.random.poisson(lam=2, size=num_samples)

    logits = (
        3.5 * (reference_count == 0)
        - 4.0 * is_entry
        - 3.0 * is_test
        - 2.5 * is_config
        - 1.5 * (reference_count >= 2)
        - 2.0 * (pagerank > 0.02)
        + 0.8 * is_private * (reference_count == 0)
        + np.random.normal(0, 0.5, size=num_samples)
    )

    probs = 1 / (1 + np.exp(-logits))
    labels = (probs > 0.5).astype(int)

    df = pd.DataFrame({
        "lines_of_code": lines_of_code,
        "function_count": function_count,
        "class_count": class_count,
        "import_count": import_count,
        "dependency_count": out_degree,
        "dependent_count": in_degree,
        "in_degree": in_degree,
        "out_degree": out_degree,
        "reference_count": reference_count,
        "call_count": call_count,
        "complexity_score": complexity,
        "pagerank": pagerank,
        "betweenness_centrality": betweenness,
        "closeness_centrality": closeness,
        "is_entry_point": is_entry,
        "is_test_file": is_test,
        "is_config_file": is_config,
        "is_private": is_private,
        "min_path_length": min_path_len,
        "num_external_deps": num_ext_deps,
        "unused": labels,
    })

    Path(DATASET_PATH_UNUSED).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH_UNUSED, index=False)
    logger.info(f"Generated unused code dataset: {df.shape[0]} rows")
    return df

if __name__ == "__main__":
    generate_impact_dataset()
    generate_unused_dataset()
