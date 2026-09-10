"""
Thread-safe in-memory cache for graph operations and features.
"""

from typing import Any, Optional, Dict
import threading

class AnalysisCache:
    """Thread-safe in-memory cache for parsed entities, graph metrics, and features."""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._cache[key] = value

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def has(self, key: str) -> bool:
        with self._lock:
            return key in self._cache

# Global cache instance
global_cache = AnalysisCache()
