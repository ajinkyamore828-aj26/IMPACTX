"""
Constants and static configurations for impactx.
"""

from typing import Set, Dict

SUPPORTED_EXTENSIONS: Set[str] = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".html",
    ".htm",
    ".css",
}

IGNORED_DIRECTORIES: Set[str] = {
    ".git",
    ".github",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".env",
    ".cache",
    "target",
    "coverage",
    ".nyc_output",
    ".idea",
    ".vscode",
    "out",
    ".system_generated",
    ".gemini",
}

IGNORED_FILE_PATTERNS: Set[str] = {
    "*.pyc",
    "*.pyo",
    "*.class",
    "*.o",
    "*.so",
    "*.dll",
    "*.exe",
    "*.bin",
    ".DS_Store",
    "Thumbs.db",
    "*.min.js",
    "*.min.css",
    "package-lock.json",
    "yarn.lock",
}

class EdgeType:
    IMPORTS = "imports"
    CALLS = "calls"
    INHERITS = "inherits"
    REFERENCES = "references"
    INCLUDES = "includes"

class EntityType:
    FILE = "file"
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"

RISK_THRESHOLDS: Dict[str, tuple[float, float]] = {
    "LOW": (0.00, 0.3999),
    "MEDIUM": (0.40, 0.6999),
    "HIGH": (0.70, 1.0000),
}

def get_risk_level(prob: float) -> str:
    """Return risk category string given probability [0.0, 1.0]."""
    if prob >= 0.70:
        return "HIGH"
    elif prob >= 0.40:
        return "MEDIUM"
    return "LOW"
