"""
File operation utilities for impactx.
"""

from pathlib import Path
from typing import Tuple

def read_file_safe(file_path: Path) -> str:
    """Reads file text safely trying utf-8, then latin-1 with error replacement."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1", errors="replace") as f:
                return f.read()
        except Exception:
            with open(file_path, "r", errors="ignore") as f:
                return f.read()

def count_lines(content: str) -> Tuple[int, int, int]:
    """
    Returns (total_lines, code_lines, comment_or_blank_lines).
    """
    lines = content.splitlines()
    total = len(lines)
    code = 0
    blank_or_comment = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "//", "/*", "*")):
            blank_or_comment += 1
        else:
            code += 1
    return total, code, blank_or_comment

def normalize_rel_path(file_path: Path, base_dir: Path) -> str:
    """Returns normalized relative path string with forward slashes."""
    try:
        rel = file_path.relative_to(base_dir)
        return rel.as_posix()
    except Exception:
        return file_path.as_posix()
