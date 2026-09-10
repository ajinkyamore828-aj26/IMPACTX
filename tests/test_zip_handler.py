"""
Security and ZIP extraction tests for impactx.
"""

import zipfile
import pytest
from pathlib import Path
import tempfile

from src.utils.zip_handler import (
    safe_extract_zip,
    SecurityError,
    PathTraversalError,
    CorruptedZipError,
)

def test_safe_zip_extraction():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "valid.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("test.py", "print('hello')")
            zf.writestr("sub/utils.py", "def fn(): pass")

        dest = Path(tmp) / "extracted"
        extracted = safe_extract_zip(zip_path, extract_to=dest)
        assert (dest / "test.py").exists()
        assert (dest / "sub" / "utils.py").exists()

def test_path_traversal_prevention():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "malicious.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            # Add member with ../ path traversal
            zf.writestr("../../evil.py", "malicious_code()")

        dest = Path(tmp) / "extracted"
        with pytest.raises((PathTraversalError, SecurityError)):
            safe_extract_zip(zip_path, extract_to=dest)

def test_corrupted_zip_detection():
    with tempfile.TemporaryDirectory() as tmp:
        corrupted_path = Path(tmp) / "bad.zip"
        corrupted_path.write_bytes(b"NOT_A_ZIP_HEADER_12345")

        with pytest.raises(CorruptedZipError):
            safe_extract_zip(corrupted_path)
