"""
Secure ZIP extraction handler for impactx.
"""

import os
import zipfile
import tempfile
from pathlib import Path
from typing import Optional, List

from config.config import (
    MAX_UPLOAD_SIZE_BYTES,
    MAX_EXTRACTED_SIZE_BYTES,
    MAX_FILE_COUNT,
    MAX_ZIP_RATIO,
)
from src.utils.security import (
    SecurityError,
    PathTraversalError,
    ZipBombError,
    is_safe_path,
)
from src.utils.logger import get_logger

logger = get_logger("zip_handler")

ZIP_MAGIC_BYTES = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")

class CorruptedZipError(Exception):
    """Raised when the zip file is invalid or corrupted."""
    pass

def validate_zip_header(zip_path: Path) -> None:
    """Validate ZIP magic bytes signature."""
    if not zip_path.exists():
        raise FileNotFoundError(f"File not found: {zip_path}")
    if zip_path.stat().st_size < 4:
        raise CorruptedZipError("File is too small to be a valid ZIP archive.")
    with open(zip_path, "rb") as f:
        header = f.read(4)
        if not any(header.startswith(magic[:4]) for magic in ZIP_MAGIC_BYTES):
            raise CorruptedZipError("Invalid ZIP file signature.")

IGNORED_EXTRACTION_PARTS = {
    "node_modules",
    ".git",
    ".github",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
}

def safe_extract_zip(zip_path: str | Path, extract_to: Optional[str | Path] = None) -> Path:
    """
    Safely extracts a ZIP archive into a destination or isolated temporary directory.
    Enforces security validations:
      - Magic bytes check
      - Path traversal protection (e.g., ../ or absolute paths)
      - Total file count limit
      - Cumulative uncompressed size limit
      - Compression ratio threshold (Zip bomb protection)
      - Fast extraction (bypasses node_modules and VCS directories)
    """
    zip_path = Path(zip_path)
    validate_zip_header(zip_path)

    # Verify upload file size
    compressed_size = zip_path.stat().st_size
    if compressed_size > MAX_UPLOAD_SIZE_BYTES:
        raise SecurityError(
            f"Archive size ({compressed_size / (1024*1024):.1f} MB) exceeds maximum allowed limit ({MAX_UPLOAD_SIZE_BYTES / (1024*1024):.1f} MB)."
        )

    if extract_to is None:
        target_dir = Path(tempfile.mkdtemp(prefix="impactx_analysis_"))
    else:
        target_dir = Path(extract_to)
        target_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            infolist = zf.infolist()

            # Filter infolist to skip third-party directories like node_modules and .git
            valid_infolist = []
            for member in infolist:
                parts = set(Path(member.filename).parts)
                if parts.intersection(IGNORED_EXTRACTION_PARTS):
                    continue
                valid_infolist.append(member)

            members_to_extract = valid_infolist if valid_infolist else infolist

            # Check file count on active source members
            if len(members_to_extract) > MAX_FILE_COUNT:
                raise SecurityError(
                    f"Archive contains {len(members_to_extract)} source files, exceeding the limit of {MAX_FILE_COUNT} files."
                )

            total_uncompressed = 0
            for member in members_to_extract:
                # 1. Path traversal check
                member_path = target_dir / member.filename
                if not is_safe_path(target_dir, member_path):
                    raise PathTraversalError(f"Attempted path traversal in ZIP member: {member.filename}")
                
                # Check for absolute path indicators
                if member.filename.startswith(("/", "\\")) or ":" in member.filename:
                    raise PathTraversalError(f"Illegal absolute or drive path in member: {member.filename}")

                # 2. Size check
                total_uncompressed += member.file_size
                if total_uncompressed > MAX_EXTRACTED_SIZE_BYTES:
                    raise ZipBombError(
                        f"Extracted size ({total_uncompressed / (1024*1024):.1f} MB) exceeds maximum allowed limit ({MAX_EXTRACTED_SIZE_BYTES / (1024*1024):.1f} MB)."
                    )

                # 3. Ratio check for non-zero files
                if member.compress_size > 0:
                    ratio = member.file_size / member.compress_size
                    if ratio > MAX_ZIP_RATIO and member.file_size > 10 * 1024 * 1024:
                        raise ZipBombError(
                            f"Suspicious compression ratio ({ratio:.1f}) detected for member {member.filename}."
                        )

            # Perform fast extraction on source members
            for member in members_to_extract:
                destination = target_dir / member.filename
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as source, open(destination, "wb") as target:
                        while chunk := source.read(64 * 1024):
                            target.write(chunk)

            logger.info(f"Safely extracted {len(members_to_extract)} source members to {target_dir}")
            return target_dir

    except zipfile.BadZipFile as e:
        raise CorruptedZipError(f"Corrupted or invalid zip file: {e}")
