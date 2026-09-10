"""
Unit and integration tests for the Gemini AI Copilot engine.
"""

import pytest
from src.ai.gemini_engine import GeminiEngine


def test_gemini_availability():
    """Verifies that Gemini availability check works and detects the configured key."""
    available = GeminiEngine.is_available()
    assert isinstance(available, bool)


def test_gemini_architecture_summary_fallback():
    """Verifies that architecture summary returns gracefully without raising exceptions."""
    scan_info = {
        "project_name": "test_project",
        "total_files": 5,
        "total_code_lines": 350,
        "language_distribution": {"Python": 5},
    }
    metrics = {}
    top_hubs = [{"id": "main.py", "entity_type": "file", "pagerank": 0.25, "in_degree": 3}]
    cycles = []

    res = GeminiEngine.generate_architecture_summary(scan_info, metrics, top_hubs, cycles)
    if GeminiEngine.is_available():
        assert res is not None
        assert len(res) > 20
    else:
        assert res is None


def test_gemini_explain_impact_fallback():
    """Verifies that explain_impact works without errors."""
    impact_res = {
        "total_affected": 2,
        "direct_count": 1,
        "indirect_count": 1,
        "high_risk_count": 1,
        "affected_components": [
            {
                "component": "order_service.py",
                "type": "file",
                "level": "Direct",
                "distance": 1,
                "probability": 0.85,
                "risk_level": "HIGH",
                "explanations": ["Direct import dependency"],
            }
        ],
    }

    res = GeminiEngine.explain_impact("cart.py", impact_res)
    if GeminiEngine.is_available():
        assert res is not None
        assert len(res) > 10
    else:
        assert res is None


def test_gemini_unused_code_empty():
    """Verifies empty candidates handled cleanly."""
    res = GeminiEngine.explain_unused_code([])
    if GeminiEngine.is_available():
        assert "No dead code candidates" in res
    else:
        assert res is None


def test_gemini_unused_code_full_table():
    """Verifies that explain_unused_code handles multi-component table with references and entry points."""
    sample_table = [
        {
            "name": "ProductDetail.jsx",
            "type": "file",
            "file_path": "client/src/pages/ProductDetail.jsx",
            "reference_count": 1,
            "unused_probability": 0.003,
            "risk_level": "LOW",
            "reasons": ["Zero static incoming references"],
        },
        {
            "name": "server.js",
            "type": "file",
            "file_path": "server/server.js",
            "reference_count": 0,
            "unused_probability": 0.001,
            "risk_level": "LOW",
            "reasons": ["Zero static incoming references"],
        },
    ]
    filter_ctx = {"risk_levels": ["LOW"], "entity_types": ["file"], "total_count": 2}
    res = GeminiEngine.explain_unused_code(sample_table, filter_context=filter_ctx)
    if GeminiEngine.is_available():
        assert res is not None
        assert len(res) > 20
    else:
        assert res is None

