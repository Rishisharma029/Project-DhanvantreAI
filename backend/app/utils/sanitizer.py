import re
import html
from typing import Optional, Any

def sanitize_text(text: Optional[str]) -> Optional[str]:
    """
    Sanitizes raw user input text before storing in database or processing.
    Strips script tags, event handlers, javascript: URIs, and escapes HTML entities.
    """
    if text is None or not isinstance(text, str):
        return text

    # Remove script and iframe tags completely
    clean = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<iframe[^>]*>.*?</iframe>", "", clean, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.IGNORECASE | re.DOTALL)

    # Remove inline event handlers like onload=, onerror=, onclick=
    clean = re.sub(r"on\w+\s*=\s*['\"].*?['\"]", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"javascript:\s*", "", clean, flags=re.IGNORECASE)

    # Escape HTML special characters (&, <, >, ", ')
    return html.escape(clean.strip())

def sanitize_dict_fields(data: Dict[str, Any], target_fields: List[str]) -> Dict[str, Any]:
    """
    Sanitizes specified text fields within a dictionary.
    """
    sanitized = dict(data)
    for field in target_fields:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitize_text(sanitized[field])
    return sanitized
