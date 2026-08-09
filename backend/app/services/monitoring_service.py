import time
from typing import Dict, Any, Optional
from contextlib import contextmanager

# =========================================================
# In-Memory Metrics Registry (Prometheus Compatible Exporter)
# =========================================================
class MetricsRegistry:
    def __init__(self):
        self.http_requests_total: Dict[str, int] = {}
        self.http_errors_total: Dict[str, int] = {}
        self.http_request_durations: Dict[str, list] = {}
        self.ai_pipeline_durations: Dict[str, list] = {}
        self.rag_retrieval_durations: Dict[str, list] = {}
        self.system_health_status: Dict[str, int] = {
            "database": 1,
            "cache": 1,
            "ai_engine": 1
        }

    def record_http_request(self, method: str, endpoint: str, status_code: int, duration_sec: float):
        key = f'{method}:{endpoint}:{status_code}'
        self.http_requests_total[key] = self.http_requests_total.get(key, 0) + 1
        
        endpoint_key = f'{method}:{endpoint}'
        if endpoint_key not in self.http_request_durations:
            self.http_request_durations[endpoint_key] = []
        self.http_request_durations[endpoint_key].append(duration_sec)
        # Keep last 1000 observations per endpoint
        if len(self.http_request_durations[endpoint_key]) > 1000:
            self.http_request_durations[endpoint_key].pop(0)

        if status_code >= 400:
            error_key = f'{endpoint}:{status_code}'
            self.http_errors_total[error_key] = self.http_errors_total.get(error_key, 0) + 1

    def record_ai_pipeline_timing(self, pipeline_name: str, duration_sec: float, status: str = "success"):
        key = f'{pipeline_name}:{status}'
        if key not in self.ai_pipeline_durations:
            self.ai_pipeline_durations[key] = []
        self.ai_pipeline_durations[key].append(duration_sec)
        if len(self.ai_pipeline_durations[key]) > 1000:
            self.ai_pipeline_durations[key].pop(0)

    def record_rag_retrieval_timing(self, query_type: str, duration_sec: float, top_k: int = 10):
        key = f'{query_type}:top_{top_k}'
        if key not in self.rag_retrieval_durations:
            self.rag_retrieval_durations[key] = []
        self.rag_retrieval_durations[key].append(duration_sec)
        if len(self.rag_retrieval_durations[key]) > 1000:
            self.rag_retrieval_durations[key].pop(0)

    def generate_prometheus_metrics(self) -> str:
        lines = []

        # 1. Request Total Counter
        lines.append("# HELP http_requests_total Total number of HTTP requests processed.")
        lines.append("# TYPE http_requests_total counter")
        for key, count in self.http_requests_total.items():
            method, endpoint, status = key.split(":")
            lines.append(f'http_requests_total{{method="{method}",endpoint="{endpoint}",status="{status}"}} {count}')

        # 2. Error Counter
        lines.append("# HELP http_errors_total Total number of failed HTTP requests.")
        lines.append("# TYPE http_errors_total counter")
        for key, count in self.http_errors_total.items():
            endpoint, status = key.split(":")
            lines.append(f'http_errors_total{{endpoint="{endpoint}",status="{status}"}} {count}')

        # 3. HTTP Latency Averages
        lines.append("# HELP http_request_duration_seconds_avg Average HTTP request latency in seconds.")
        lines.append("# TYPE http_request_duration_seconds_avg gauge")
        for key, durations in self.http_request_durations.items():
            method, endpoint = key.split(":")
            avg_dur = sum(durations) / len(durations) if durations else 0.0
            lines.append(f'http_request_duration_seconds_avg{{method="{method}",endpoint="{endpoint}"}} {avg_dur:.6f}')

        # 4. AI Pipeline Timings
        lines.append("# HELP ai_pipeline_duration_seconds_avg Average AI pipeline execution time in seconds.")
        lines.append("# TYPE ai_pipeline_duration_seconds_avg gauge")
        for key, durations in self.ai_pipeline_durations.items():
            pipeline, status = key.split(":")
            avg_dur = sum(durations) / len(durations) if durations else 0.0
            lines.append(f'ai_pipeline_duration_seconds_avg{{pipeline="{pipeline}",status="{status}"}} {avg_dur:.6f}')

        # 5. RAG Retrieval Latency
        lines.append("# HELP rag_retrieval_duration_seconds_avg Average RAG retrieval duration in seconds.")
        lines.append("# TYPE rag_retrieval_duration_seconds_avg gauge")
        for key, durations in self.rag_retrieval_durations.items():
            query_type, top_k = key.split(":")
            avg_dur = sum(durations) / len(durations) if durations else 0.0
            lines.append(f'rag_retrieval_duration_seconds_avg{{query_type="{query_type}",top_k="{top_k}"}} {avg_dur:.6f}')

        # 6. Component Health Status
        lines.append("# HELP system_health_status Health status of platform components (1=Healthy, 0=Unhealthy).")
        lines.append("# TYPE system_health_status gauge")
        for comp, status in self.system_health_status.items():
            lines.append(f'system_health_status{{component="{comp}"}} {status}')

        return "\n".join(lines) + "\n"

# Singleton Metrics Instance
metrics_registry = MetricsRegistry()

@contextmanager
def track_ai_pipeline_timing(pipeline_name: str):
    start_time = time.time()
    status = "success"
    try:
        yield
    except Exception:
        status = "error"
        raise
    finally:
        elapsed = time.time() - start_time
        metrics_registry.record_ai_pipeline_timing(pipeline_name, elapsed, status)

@contextmanager
def track_rag_retrieval_timing(query_type: str = "hybrid_search", top_k: int = 10):
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        metrics_registry.record_rag_retrieval_timing(query_type, elapsed, top_k)
