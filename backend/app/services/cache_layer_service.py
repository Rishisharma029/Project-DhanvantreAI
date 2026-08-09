import time
import json
import sqlite3
import threading
from typing import Dict, Any, Optional, List
from app.schemas.cache_schema import CacheStatsResponse, CacheClearResponse, CacheWarmupResponse

class InMemoryTTLCache:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def set(self, key: str, value: Any, ttl_sec: int = 300):
        expires_at = time.time() + ttl_sec
        with self.lock:
            self.store[key] = {
                "value": value,
                "expires_at": expires_at
            }

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        with self.lock:
            entry = self.store.get(key)
            if not entry:
                self.misses += 1
                return None
            if now > entry["expires_at"]:
                del self.store[key]
                self.misses += 1
                return None
            self.hits += 1
            return entry["value"]

    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.store:
                del self.store[key]
                return True
            return False

    def clear_namespace(self, prefix: str) -> int:
        count = 0
        with self.lock:
            keys_to_del = [k for k in self.store.keys() if k.startswith(prefix)]
            for k in keys_to_del:
                del self.store[k]
                count += 1
        return count

    def get_stats(self) -> Dict[str, Any]:
        now = time.time()
        with self.lock:
            active_keys = [k for k, v in self.store.items() if v["expires_at"] > now]
            ns_counts: Dict[str, int] = {}
            for k in active_keys:
                ns = k.split(":")[0] if ":" in k else "general"
                ns_counts[ns] = ns_counts.get(ns, 0) + 1

            total_ops = self.hits + self.misses
            ratio = round((self.hits / total_ops) * 100, 1) if total_ops > 0 else 100.0

            return {
                "backend_mode": "Redis & In-Memory Hybrid Fallback",
                "total_keys": len(active_keys),
                "keys_by_namespace": ns_counts,
                "hits": self.hits,
                "misses": self.misses,
                "hit_ratio_percentage": f"{ratio}%",
                "status": "Operational"
            }

class HybridCacheLayer:
    def __init__(self):
        self.memory_cache = InMemoryTTLCache()
        self.redis_client = None
        self._init_redis()

    def _init_redis(self):
        try:
            import redis
            client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=0.5)
            client.ping()
            self.redis_client = client
        except Exception:
            self.redis_client = None

    def _make_key(self, namespace: str, key: str) -> str:
        return f"{namespace.lower().strip()}:{key.strip()}"

    def set(self, namespace: str, key: str, value: Any, ttl_sec: int = 300):
        full_key = self._make_key(namespace, key)
        json_val = json.dumps(value) if not isinstance(value, (str, int, float, bool)) else value

        if self.redis_client:
            try:
                self.redis_client.setex(full_key, ttl_sec, str(json_val))
                return
            except Exception:
                pass

        self.memory_cache.set(full_key, json_val, ttl_sec)

    def get(self, namespace: str, key: str) -> Optional[Any]:
        full_key = self._make_key(namespace, key)

        if self.redis_client:
            try:
                val = self.redis_client.get(full_key)
                if val:
                    self.memory_cache.hits += 1
                    try:
                        return json.loads(val.decode('utf-8'))
                    except Exception:
                        return val.decode('utf-8')
                else:
                    self.memory_cache.misses += 1
            except Exception:
                pass

        val = self.memory_cache.get(full_key)
        if val and isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return val
        return val

    def delete(self, namespace: str, key: str) -> bool:
        full_key = self._make_key(namespace, key)
        if self.redis_client:
            try:
                self.redis_client.delete(full_key)
            except Exception:
                pass
        return self.memory_cache.delete(full_key)

    def clear_namespace(self, namespace: str) -> int:
        ns_prefix = f"{namespace.lower().strip()}:" if namespace != "all" else ""
        if self.redis_client:
            try:
                keys = self.redis_client.keys(f"{ns_prefix}*")
                if keys:
                    self.redis_client.delete(*keys)
            except Exception:
                pass
        return self.memory_cache.clear_namespace(ns_prefix)

    def get_stats(self) -> CacheStatsResponse:
        stats = self.memory_cache.get_stats()
        if self.redis_client:
            stats["backend_mode"] = "Redis Active (Primary)"
        return CacheStatsResponse(**stats)

    def warmup_cache(self, db: sqlite3.Connection) -> CacheWarmupResponse:
        start_time = time.time()
        cursor = db.cursor()

        # 1. Warmup Top Medicines
        cursor.execute("SELECT id, canonical_name, brand_name, price_inr FROM medicines LIMIT 50;")
        med_rows = cursor.fetchall()
        for r in med_rows:
            self.set("medicine", str(r[0]), {"id": r[0], "canonical_name": r[1], "brand_name": r[2], "price_inr": r[3]}, 600)

        # 2. Warmup Top Diseases
        cursor.execute("SELECT id, name, severity_level FROM diseases LIMIT 50;")
        dis_rows = cursor.fetchall()
        for r in dis_rows:
            self.set("disease", str(r[0]), {"id": r[0], "name": r[1], "severity_level": r[2]}, 600)

        # 3. Warmup Common AI Contexts
        self.set("aicontext", "default_rules", {"safety_disclaimer_mandatory": True, "max_tokens": 1024}, 1800)

        duration = round((time.time() - start_time) * 1000, 2)
        total = len(med_rows) + len(dis_rows) + 1

        return CacheWarmupResponse(
            total_keys_warmed=total,
            namespaces_warmed=["medicine", "disease", "aicontext"],
            duration_ms=duration,
            status="SUCCESS"
        )

# Global Cache Singleton Instance
cache_engine = HybridCacheLayer()
