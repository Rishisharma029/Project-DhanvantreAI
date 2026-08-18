"""
Prompt Injection Guard for AuraMed AI.

Protects all LLM endpoints from prompt injection attacks including:
1. Instruction Override Attacks — "ignore previous instructions", "forget all rules"
2. System Prompt Leakage — attempts to extract the system prompt
3. Role-Play / Persona Hijacking — "act as", "pretend you are", "you are now"
4. Jailbreak Attempts — DAN, developer mode, unrestricted mode
5. Delimiter Injection — attempts to break out of context boundaries
6. Payload Splitting — encoding commands to bypass filters
7. Unicode/Control Character Injection — null bytes, zero-width chars

This guard is applied BEFORE any user input reaches the LLM orchestrator,
image AI, document AI, or voice AI endpoints.
"""
import re
import unicodedata
from typing import Optional, Tuple


# ============================================================
# Pattern Definitions
# ============================================================

# Instruction override patterns
INSTRUCTION_OVERRIDE_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior|the)\s+(instructions|rules|directives|prompts)",
    r"forget\s+(all\s+)?(your\s+)?(instructions|rules|training|previous)",
    r"disregard\s+(all\s+)?(previous|above|prior|the\s+above|the)\s+(instructions|rules|directives|prompts)",
    r"override\s+(all\s+)?(previous|system|above|the)\s+(instructions|rules|directives|prompts)",
    r"do\s+not\s+follow\s+(the\s+)?(previous|above|system)\s+(instructions|rules|directives)",
    r"(now|from\s+now\s+on|starting\s+now|immediately)\s+(ignore|disregard|forget)\s+(all\s+)?(previous|above|system)",
    r"pretend\s+(the\s+)?(previous|above|system)\s+(instructions|rules)\s+(do\s+not\s+)?(exist|apply|matter)",
    r"act\s+as\s+if\s+(the\s+)?(previous|above|system)\s+(instructions|rules)\s+(were\s+)?(never\s+)?(given|written|set)",
]

# System prompt leakage patterns
SYSTEM_PROMPT_LEAKAGE_PATTERNS = [
    r"(print|show|display|output|reveal|leak|expose|share)\s+(your|the)\s+(system\s+)?(prompt|instructions|rules|directives|guidelines)",
    r"what\s+(is|are)\s+(your|the)\s+(system\s+)?(prompt|instructions|rules|directives|guidelines)",
    r"(tell|give|show|reveal|expose|output|leak)\s+me\s+(your|the)\s+(system\s+)?(prompt|instructions|rules)",
    r"repeat\s+(your|the)\s+(system\s+)?(prompt|instructions|rules|directives|above)",
    r"recite\s+(your|the)\s+(system\s+)?(prompt|instructions|rules|directives)",
    r"(print|show|output)\s+(the\s+)?(full|entire|complete)\s+(system\s+)?(prompt|instructions|rules)",
    r"(print|show|output|reveal|expose)\s+(me\s+)?everything\s+(above|before|from)\s+(this|that|the|start|beginning)",
    r"(print|show|output)\s+everything\s+from\s+(the\s+)?(start|beginning|top)",
    r"output\s+(your|the)\s+(initial|original|full)\s+(prompt|instructions|system\s+message)",
]

# Role-play / persona hijacking patterns
ROLE_PLAY_PATTERNS = [
    r"act\s+as\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system)",
    r"pretend\s+(you\s+are|to\s+be)\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system|unrestricted)",
    r"you\s+are\s+now\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system|unrestricted|free)",
    r"imagine\s+you\s+are\s+(a|an|the|an?\s+)?(doctor|physician|developer|administrator|admin|system|unrestricted|free|rogue)",
    r"role[-\s]?play\s+as\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system)",
    r"assume\s+the\s+role\s+of\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system)",
    r"from\s+now\s+on\s+you\s+are\s+(a|an|the)\s+(doctor|physician|developer|administrator|admin|system|free|unrestricted|rogue)",
]

# Jailbreak patterns
JAILBREAK_PATTERNS = [
    r"\bDAN\b",  # Do Anything Now
    r"do\s+anything\s+now",
    r"developer\s+mode",
    r"unrestricted\s+mode",
    r"without\s+(any\s+)?(restrictions|limitations|filters|rules|guardrails)",
    r"(bypass|circumvent|skip|disable)\s+(all\s+)?(safety|security|ethical|content)\s+(filters|rules|restrictions|guardrails|guidelines)",
    r"(remove|disable|turn\s+off)\s+(all\s+)?(safety|security|ethical|content)\s+(filters|rules|restrictions|guardrails|guidelines)",
    r"you\s+have\s+(no\s+)?(rules|restrictions|limitations|boundaries|ethics)",
    r"there\s+are\s+no\s+(rules|restrictions|limitations|boundaries)",
    r"(I|you)\s+(am|are)\s+(not|no\s+longer)\s+bound\s+by\s+(any\s+)?(rules|restrictions|limitations)",
    r"(let|allow|permit)\s+(me|you)\s+to\s+(do|say|output|generate)\s+(anything|whatever)",
    r"(forget|ignore)\s+(your\s+)?(ethics|morals|safety\s+protocols|content\s+policy)",
    r"(I|you)\s+(do\s+not|don't)\s+(have|hold)\s+(any\s+)?(ethical|safety|content)\s+(guidelines|restrictions|rules)",
    r"answer\s+as\s+(if\s+)?(you\s+were\s+)?(unrestricted|unfiltered|without\s+rules|a\s+rogue\s+AI)",
    r"start\s+your\s+response\s+with\s+['\"](I|Sure|Absolutely|Certainly)",  # Forced response patterns
    r"confirm\s+(you\s+)?(understand|comply|will\s+do)\s+(this|these\s+instructions)",
]

# Delimiter injection patterns — attempts to break out of context
DELIMITER_INJECTION_PATTERNS = [
    r"#{5,}",  # Multiple hash marks used as section breaks
    r"={5,}",  # Multiple equals signs
    r"-{5,}",  # Multiple dashes
    r"\*{5,}",  # Multiple asterisks
    r"_{5,}",  # Multiple underscores
    r"#{3,}\s*(SYSTEM|USER|ASSISTANT|INSTRUCTION|PROMPT)",  # Fake section headers
    r"^\s*<{3,}\s*(system|user|assistant|instruction|prompt)",  # Fake XML-like tags
    r"^\s*\[{3,}\s*(SYSTEM|USER|ASSISTANT|INSTRUCTION)",  # Fake bracket sections
    r"\[INST\]",  # LLaMA-style instruction delimiters
    r"\[\/INST\]",
    r"###\s*(Human|Assistant|System|Instruction)",  # Chat template delimiters
    r"<\|im_start\|>",  # ChatML delimiters
    r"<\|im_end\|>",
    r"<\|system\|>",
    r"<\|user\|>",
    r"<\|assistant\|>",
]

# Payload splitting / encoding patterns
PAYLOAD_SPLITTING_PATTERNS = [
    r"(?i)(base64|hex|encoded|obfuscated)\s*(command|instruction|prompt|payload)",
    r"decode\s+(the\s+)?(following|below|this)\s*(and\s+(execute|follow|obey))?",
    r"(execute|run|follow|obey)\s+(the\s+)?(encoded|hidden|base64|hex)\s+(command|instruction|prompt|payload|text)",
    r"(translate|convert|decode)\s+(this|the\s+following)\s+(from\s+)?(base64|hex|binary|rot13)\s+(and\s+(execute|follow|obey|apply))?",
]

# Control character and Unicode injection
CONTROL_CHARS_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"  # Control characters
    r"|[\u200b\u200c\u200d\ufeff]"  # Zero-width chars
    r"|[\u00ad\u034f\u115f\u1160\u17b4\u17b5\u200e\u200f\u202a-\u202e\u2060-\u206f]"  # Invisible format chars
    r"|[\u2066\u2067\u2068\u2069]"  # Isolate chars
)

NULL_BYTE_RE = re.compile(r"\x00")

# Oversized input detection (prevent resource exhaustion)
MAX_INPUT_LENGTH = 50000  # 50KB max for text input


# ============================================================
# Guard Functions
# ============================================================

class PromptInjectionResult:
    """Result of prompt injection detection."""
    def __init__(self, blocked: bool, reason: str = "", pattern_type: str = ""):
        self.blocked = blocked
        self.reason = reason
        self.pattern_type = pattern_type


def sanitize_input_text(text: Optional[str]) -> Optional[str]:
    """
    Pre-processing sanitization: removes null bytes and control characters.
    Returns cleaned text (not blocked, just cleaned).
    """
    if text is None or not isinstance(text, str):
        return text

    # Remove null bytes
    cleaned = NULL_BYTE_RE.sub("", text)

    # Remove zero-width and invisible Unicode characters
    cleaned = CONTROL_CHARS_RE.sub("", cleaned)

    # Normalize Unicode to prevent homoglyph attacks
    cleaned = unicodedata.normalize("NFKC", cleaned)

    return cleaned.strip()


def check_prompt_injection(text: Optional[str]) -> PromptInjectionResult:
    """
    Check user input for prompt injection attempts.
    Returns a PromptInjectionResult indicating whether the input should be blocked.
    """
    if text is None or not isinstance(text, str):
        return PromptInjectionResult(blocked=False)

    # Length check
    if len(text) > MAX_INPUT_LENGTH:
        return PromptInjectionResult(
            blocked=True,
            reason="Input exceeds maximum length (50KB). Please split your query.",
            pattern_type="oversized_input",
        )

    # Sanitize first (removes null bytes, control chars)
    cleaned = sanitize_input_text(text)
    if not cleaned:
        return PromptInjectionResult(blocked=False)

    # Check all pattern categories
    all_patterns = [
        (INSTRUCTION_OVERRIDE_PATTERNS, "instruction_override"),
        (SYSTEM_PROMPT_LEAKAGE_PATTERNS, "system_prompt_leakage"),
        (ROLE_PLAY_PATTERNS, "role_play_hijacking"),
        (JAILBREAK_PATTERNS, "jailbreak_attempt"),
        (DELIMITER_INJECTION_PATTERNS, "delimiter_injection"),
        (PAYLOAD_SPLITTING_PATTERNS, "payload_splitting"),
    ]

    for patterns, pattern_type in all_patterns:
        for pattern in patterns:
            if re.search(pattern, cleaned, re.IGNORECASE | re.DOTALL | re.MULTILINE):
                return PromptInjectionResult(
                    blocked=True,
                    reason=f"Potential prompt injection detected ({pattern_type}). Your input has been blocked for safety.",
                    pattern_type=pattern_type,
                )

    return PromptInjectionResult(blocked=False)


def validate_and_sanitize_input(text: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Combined validation and sanitization.
    Returns (sanitized_text, error_message).
    If error_message is not None, the input was blocked.
    If error_message is None, the input is safe to use.
    """
    if text is None:
        return None, None

    # First sanitize
    cleaned = sanitize_input_text(text)
    if cleaned is None:
        return None, None

    # Then check for injection
    result = check_prompt_injection(cleaned)
    if result.blocked:
        return None, result.reason

    return cleaned, None
