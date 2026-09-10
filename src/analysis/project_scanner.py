"""
Project scanner and file system inspection.
"""

from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import fnmatch
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.constants import IGNORED_DIRECTORIES, IGNORED_FILE_PATTERNS, SUPPORTED_EXTENSIONS
from src.analysis.file_detector import FileDetector
from src.utils.file_utils import read_file_safe, count_lines, normalize_rel_path
from src.utils.security import is_binary_file
from src.utils.logger import get_logger

logger = get_logger("project_scanner")

# Skip files larger than this (bytes) — minified/generated files
_MAX_FILE_SIZE = 500_000  # 500 KB


def _is_ignored(path: Path) -> bool:
    """Fast pre-filter: ignored directory or file pattern."""
    if any(part in IGNORED_DIRECTORIES for part in path.parts):
        return True
    if any(fnmatch.fnmatch(path.name, pat) for pat in IGNORED_FILE_PATTERNS):
        return True
    return False


def _process_file(path: Path, root_dir: Path) -> Dict[str, Any] | None:
    """Process a single file and return its metadata dict, or None to skip."""
    try:
        # Fast size check before reading content
        size = path.stat().st_size
        if size == 0 or size > _MAX_FILE_SIZE:
            return None

        # Skip extensions we cannot use right away (avoid binary check cost)
        ext = path.suffix.lower()
        if ext and ext not in SUPPORTED_EXTENSIONS:
            # Still allow unknown extensions through — FileDetector may know them
            # but skip obviously binary extensions
            _BINARY_EXTS = {
                ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff",
                ".woff2", ".ttf", ".eot", ".otf", ".mp4", ".mp3", ".wav",
                ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar", ".jar",
                ".war", ".ear", ".lock",
            }
            if ext in _BINARY_EXTS:
                return None

        # Binary check (reads 1 KB)
        if is_binary_file(path):
            return None

        rel_path = normalize_rel_path(path, root_dir)
        language = FileDetector.detect_language(path)
        category = FileDetector.categorize_file(path)

        content = read_file_safe(path)
        tot, code, comm = count_lines(content)

        return {
            "path": rel_path,
            "abs_path": str(path.resolve()),
            "name": path.name,
            "language": language,
            "category": category,
            "is_supported": FileDetector.is_supported(path),
            "size_bytes": size,
            "total_lines": tot,
            "code_lines": code,
            "comment_lines": comm,
        }
    except Exception:
        return None


class ProjectScanner:
    """Scans project directory and builds inventory of files and languages."""

    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)

    def scan(self) -> Dict[str, Any]:
        """
        Recursively scans root_dir in parallel, respecting ignored dirs/patterns.
        Returns project metadata and file inventory.
        """
        # Collect candidate paths first (fast, single-threaded os.walk)
        candidates: List[Path] = []
        for path in self.root_dir.rglob("*"):
            if not path.is_file():
                continue
            if _is_ignored(path):
                continue
            candidates.append(path)

        # Process files in parallel
        files_info: List[Dict[str, Any]] = []
        lang_counts: Dict[str, int] = {}
        total_lines = 0
        total_code_lines = 0

        max_workers = min(8, len(candidates) or 1)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(_process_file, p, self.root_dir): p for p in candidates}
            for future in as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                total_lines += result["total_lines"]
                total_code_lines += result["code_lines"]
                if result["language"] != "Unknown":
                    lang_counts[result["language"]] = lang_counts.get(result["language"], 0) + 1
                files_info.append(result)

        logger.info(f"Scanned {len(files_info)} valid files across {len(lang_counts)} languages.")

        return {
            "root_path": str(self.root_dir),
            "project_name": self.root_dir.name,
            "total_files": len(files_info),
            "total_lines": total_lines,
            "total_code_lines": total_code_lines,
            "language_distribution": lang_counts,
            "files": files_info,
        }
