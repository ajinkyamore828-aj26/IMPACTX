"""
Security validation utilities for impactx.
"""

import os
from pathlib import Path

class SecurityError(Exception):
    """Base exception for security violations."""
    pass

class PathTraversalError(SecurityError):
    """Raised when a path tries to escape the destination directory."""
    pass

class ZipBombError(SecurityError):
    """Raised when an archive exceeds size or compression limits."""
    pass

def is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """Verify that target_path resolves strictly within base_dir."""
    try:
        resolved_base = base_dir.resolve()
        resolved_target = target_path.resolve()
        return resolved_base in resolved_target.parents or resolved_base == resolved_target
    except Exception:
        return False

def sanitize_path(path_str: str) -> str:
    """Sanitize path string by removing leading slashes and drive letters."""
    cleaned = path_str.replace("\\", "/").strip()
    while cleaned.startswith("/") or cleaned.startswith("./"):
        cleaned = cleaned.lstrip("/.")
    return cleaned

def is_binary_file(file_path: Path) -> bool:
    """Checks whether a file contains null bytes (binary indicator)."""
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except Exception:
        return True
