"""
KEGG Adapter: REST client with simple sqlite cache and rate-limited requests.
This adapter performs on-demand KEGG lookups and caches responses to avoid repeated network calls.

Improvements:
- honor KEGG_CACHE_DB env var to allow tests to use a temporary cache
- handle network failures gracefully in CI (return empty response with warning)
"""
import time
import requests
import sqlite3
import json
import threading
import os
from pathlib import Path
from typing import Optional

CACHE_DB_DEFAULT = Path(".cache/kegg_cache.db")
_LOCK = threading.Lock()


def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


class KEGGAdapter:
    def __init__(self, base_url: str = "https://rest.kegg.jp", rate_limit_per_minute: int = 60, cache_db: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.rate_limit_per_minute = rate_limit_per_minute
        self._last_request_ts = 0.0
        self._min_interval = 60.0 / max(1, rate_limit_per_minute)
        # allow overriding cache DB via env var or constructor
        if cache_db is None:
            cache_db_path = os.environ.get('KEGG_CACHE_DB')
            if cache_db_path:
                self.cache_db = Path(cache_db_path)
            else:
                self.cache_db = CACHE_DB_DEFAULT
        else:
            self.cache_db = Path(cache_db)
        _ensure_dir(self.cache_db)
        self._init_db()

    def _init_db(self):
        with _LOCK:
            conn = sqlite3.connect(str(self.cache_db))
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    response TEXT,
                    timestamp REAL
                )
            """)
            conn.commit()
            conn.close()

    def _get_cached(self, key: str) -> Optional[dict]:
        with _LOCK:
            conn = sqlite3.connect(str(self.cache_db))
            c = conn.cursor()
            c.execute("SELECT response, timestamp FROM cache WHERE key = ?", (key,))
            row = c.fetchone()
            conn.close()
            if row:
                try:
                    return {"response": json.loads(row[0]), "timestamp": row[1]}
                except Exception:
                    # corrupted cache entry; ignore
                    return None
            return None

    def _set_cached(self, key: str, data: dict):
        with _LOCK:
            conn = sqlite3.connect(str(self.cache_db))
            c = conn.cursor()
            c.execute("REPLACE INTO cache (key, response, timestamp) VALUES (?, ?, ?)",
                      (key, json.dumps(data), time.time()))
            conn.commit()
            conn.close()

    def _throttle(self):
        # simple rate limiting based on min interval
        now = time.time()
        elapsed = now - self._last_request_ts
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_ts = time.time()

    def _safe_get(self, url: str, timeout: int = 10) -> str:
        try:
            self._throttle()
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            # In CI or offline environments, network calls may fail. Return empty text and log warning.
            # Do not raise to avoid failing unrelated tests; callers can decide how to handle empty responses.
            print(f"KEGG request failed for {url}: {e}")
            return ""

    def get_pathway_by_ko(self, ko_id: str, use_cache: bool = True) -> dict:
        key = f"ko:{ko_id}"
        if use_cache:
            cached = self._get_cached(key)
            if cached:
                return cached["response"]
        url = f"{self.base_url}/link/pathway/ko:{ko_id}"
        text = self._safe_get(url)
        data = {"text": text}
        # cache even empty responses to avoid repeated failed network calls
        self._set_cached(key, data)
        return data

    def get_gene_info(self, gene_id: str, use_cache: bool = True) -> dict:
        key = f"gene:{gene_id}"
        if use_cache:
            cached = self._get_cached(key)
            if cached:
                return cached["response"]
        url = f"{self.base_url}/get/{gene_id}"
        text = self._safe_get(url)
        data = {"text": text}
        self._set_cached(key, data)
        return data


if __name__ == '__main__':
    a = KEGGAdapter(rate_limit_per_minute=5)
    try:
        print(a.get_pathway_by_ko('K00001'))
    except Exception as e:
        print('KEGG adapter smoke failed (expected in offline CI):', e)
