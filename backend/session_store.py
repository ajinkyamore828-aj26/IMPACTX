import uuid, time, threading, json, os, tempfile
from pathlib import Path
from typing import Dict, Any, Optional

SESSION_TTL = 7200  # 2 hours
SESSIONS_DIR = Path(tempfile.gettempdir()) / "impactx_sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

class SessionStore:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
    
    def create(self, data: Dict[str, Any]) -> str:
        sid = str(uuid.uuid4())
        return self.set(sid, data)
    
    def set(self, sid: str, data: Dict[str, Any]) -> str:
        now = time.time()
        with self._lock:
            self._store[sid] = {"data": data, "created_at": now}
        try:
            cache_file = SESSIONS_DIR / f"{sid}.json"
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"data": data, "created_at": now}, f, default=lambda o: float(o) if hasattr(o, '__float__') else str(o))
        except Exception as e:
            pass
        return sid
    
    def get(self, sid: str) -> Optional[Dict[str, Any]]:
        now = time.time()
        with self._lock:
            entry = self._store.get(sid)
            if entry:
                if now - entry["created_at"] > SESSION_TTL:
                    del self._store[sid]
                    return None
                return entry["data"]
        
        # Check disk cache
        try:
            cache_file = SESSIONS_DIR / f"{sid}.json"
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    entry = json.load(f)
                if now - entry.get("created_at", 0) <= SESSION_TTL:
                    with self._lock:
                        self._store[sid] = entry
                    return entry.get("data")
        except Exception:
            pass
        return None
    
    def delete(self, sid: str):
        with self._lock:
            self._store.pop(sid, None)
        try:
            (SESSIONS_DIR / f"{sid}.json").unlink(missing_ok=True)
        except Exception:
            pass
    
    def cleanup_expired(self):
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._store.items() if now - v["created_at"] > SESSION_TTL]
            for k in expired:
                del self._store[k]
        try:
            for p in SESSIONS_DIR.glob("*.json"):
                if now - p.stat().st_mtime > SESSION_TTL:
                    p.unlink(missing_ok=True)
        except Exception:
            pass

store = SessionStore()

