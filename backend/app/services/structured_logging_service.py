import json
import logging
import re
import sys
import time
from typing import Dict, Any, Optional

# =========================================================
# PHI & Sensitive Data Redaction Patterns (HIPAA Compliant)
# =========================================================
PHI_PATTERNS = [
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[REDACTED_EMAIL]'),
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '[REDACTED_SSN]'),
    (re.compile(r'\b(?:\d[ -]*?){13,16}\b'), '[REDACTED_CARD]'),
    (re.compile(r'"password"\s*:\s*"[^"]+"', re.IGNORECASE), '"password": "[REDACTED]"'),
    (re.compile(r'"token"\s*:\s*"[^"]+"', re.IGNORECASE), '"token": "[REDACTED]"'),
    (re.compile(r'"patient_name"\s*:\s*"[^"]+"', re.IGNORECASE), '"patient_name": "[REDACTED_PHI]"'),
    (re.compile(r'"raw_symptoms"\s*:\s*\[[^\]]+\]', re.IGNORECASE), '"raw_symptoms": ["[REDACTED_PHI_SYMPTOMS]"]'),
]

def sanitize_phi(text: str) -> str:
    """Sanitize protected health information and sensitive credentials from log payloads."""
    sanitized = text
    for pattern, replacement in PHI_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "structured_data"):
            log_obj.update(record.structured_data)
        
        json_str = json.dumps(log_obj)
        return sanitize_phi(json_str)

# Configure Root Logger for JSON Output
logger = logging.getLogger("auramed_structured")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

class StructuredLogger:
    @staticmethod
    def _log(level: int, event_type: str, message: str, metadata: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None):
        structured_data = {
            "event_type": event_type,
            "correlation_id": correlation_id or "N/A",
            "metadata": metadata or {}
        }
        record = logger.makeRecord(
            logger.name, level, "(unknown)", 0, message, None, None
        )
        record.structured_data = structured_data
        logger.handle(record)

    @classmethod
    def log_api_request(cls, method: str, endpoint: str, status_code: int, duration_ms: float, correlation_id: str, client_ip: str = "127.0.0.1"):
        """Log API HTTP Request without exposing PHI parameters."""
        level = logging.ERROR if status_code >= 500 else (logging.WARNING if status_code >= 400 else logging.INFO)
        metadata = {
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": client_ip
        }
        cls._log(level, "API_REQUEST", f"HTTP {method} {endpoint} -> {status_code}", metadata, correlation_id)

    @classmethod
    def log_recommendation_event(cls, disease_id: int, top_medicines_count: int, confidence_score: float, correlation_id: str):
        """Log Recommendation Pipeline Event with anonymized entity IDs."""
        metadata = {
            "disease_id": disease_id,
            "medicines_matched": top_medicines_count,
            "confidence": round(confidence_score, 4)
        }
        cls._log(logging.INFO, "RECOMMENDATION_PIPELINE", f"Generated {top_medicines_count} recommendations for Disease ID {disease_id}", metadata, correlation_id)

    @classmethod
    def log_ai_reasoning_event(cls, pipeline_name: str, rule_in_count: int, rule_out_count: int, execution_time_ms: float, correlation_id: str):
        """Log AI Differential Reasoning Execution."""
        metadata = {
            "pipeline": pipeline_name,
            "rule_in_count": rule_in_count,
            "rule_out_count": rule_out_count,
            "execution_time_ms": round(execution_time_ms, 2)
        }
        cls._log(logging.INFO, "AI_REASONING", f"AI Reasoning '{pipeline_name}' evaluated {rule_in_count} matches / {rule_out_count} rejections", metadata, correlation_id)

    @classmethod
    def log_error(cls, event_type: str, error_msg: str, stack_trace: Optional[str] = None, correlation_id: str = "N/A"):
        """Log System Errors with sanitized stack trace."""
        metadata = {
            "error_message": error_msg,
            "stack_trace": stack_trace or "None"
        }
        cls._log(logging.ERROR, event_type, f"System Error: {error_msg}", metadata, correlation_id)
