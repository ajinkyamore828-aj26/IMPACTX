"""
File detector and language classification.
"""

from pathlib import Path
from typing import Dict, Optional
from config.constants import SUPPORTED_EXTENSIONS

EXT_TO_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
}

class FileDetector:
    @staticmethod
    def detect_language(file_path: str | Path) -> str:
        """Determines programming or markup language from file extension."""
        ext = Path(file_path).suffix.lower()
        return EXT_TO_LANGUAGE.get(ext, "Unknown")

    @staticmethod
    def is_supported(file_path: str | Path) -> bool:
        ext = Path(file_path).suffix.lower()
        return ext in SUPPORTED_EXTENSIONS

    @staticmethod
    def categorize_file(file_path: str | Path) -> str:
        """Categorizes file into 'source', 'test', 'config', or 'documentation'."""
        name = Path(file_path).name.lower()
        if any(k in name for k in ("test", "spec", "_test")):
            return "test"
        if any(k in name for k in ("config", "setting", "constant", "setup", ".env", "yaml", "json")):
            return "config"
        if any(k in name for k in ("readme", "license", "contributing", "docs")):
            return "documentation"
        return "source"
