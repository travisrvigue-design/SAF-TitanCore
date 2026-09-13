"""
KEGG Adapter: REST client with simple sqlite cache and rate-limited requests.
This adapter performs on-demand KEGG lookups and caches responses to avoid repeated network calls.

Note: This module uses the KEGG REST API pattern but does NOT include bulk downloads or redistribution.
You must ensure you have KEGG permissions for any bulk ingest. This adapter is intended for on-demand queries
and mocked testing in CI.
"""
import time
import requests
import sqlite3
import json
import threading
from pathlib import Path
from typing import Optional

CACHE_DB = Path(".cache/kegg_cache.db")
CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
_LOCK = threading.Lock()


class KEGGAdapter:
    def __init__(self, base_url: str = "https://rest.kegg.jp", rate_limit_per_minute: int = 60):
        self.base_url = base_url.rstrip('/')
        self.rate_limit_per_minute = rate_limit_per_minute
        self._last_request_ts = 0.0
        self._min_interval = 60.0 / max(1, rate_limit_per_minute)
        self._init_db()

    def _init_db(self):
        with _LOCK:
            conn = sqlite3.connect(str(CACHE_DB))
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
            conn = sqlite3.connect(str(CACHE_DB))
            c = conn.cursor()
            c.execute("SELECT response, timestamp FROM cache WHERE key = ?", (key,))
            row = c.fetchone()
            conn.close()
            if row:
                return {"response": json.loads(row[0]), "timestamp": row[1]}
            return None

    def _set_cached(self, key: str, data: dict):
        with _LOCK:
            conn = sqlite3.connect(str(CACHE_DB))
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

    def get_pathway_by_ko(self, ko_id: str, use_cache: bool = True) -> dict:
        key = f"ko:{ko_id}"
        if use_cache:
            cached = self._get_cached(key)
            if cached:
                return cached["response"]
        self._throttle()
        url = f"{self.base_url}/link/pathway/ko:{ko_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"KEGG request failed: {resp.status_code} {resp.text}")
        # KEGG returns plain text; store as text wrapper
        data = {"text": resp.text}
        self._set_cached(key, data)
        return data

    def get_gene_info(self, gene_id: str, use_cache: bool = True) -> dict:
        key = f"gene:{gene_id}"
        if use_cache:
            cached = self._get_cached(key)
            if cached:
                return cached["response"]
        self._throttle()
        url = f"{self.base_url}/get/{gene_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"KEGG request failed: {resp.status_code} {resp.text}")
        data = {"text": resp.text}
        self._set_cached(key, data)
        return data


if __name__ == '__main__':
    # quick smoke test (will perform live HTTP call if internet is available)
    a = KEGGAdapter(rate_limit_per_minute=5)
    try:
        print(a.get_pathway_by_ko('K00001'))
    except Exception as e:
        print('KEGG adapter smoke failed (expected in offline CI):', e)
