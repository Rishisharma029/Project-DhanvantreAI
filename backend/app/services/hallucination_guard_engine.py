import re
import uuid
import sqlite3
from typing import List, Tuple
from app.schemas.hallucination_guard_schema import (
    HallucinationGuardRequest,
    HallucinationGuardResponse,
    ExtractedClaim,
    ClaimVerificationStatus
)

MEDICAL_CATEGORIES = {
    "DOSAGE": ["mg", "mcg", "g", "ml", "dose", "tablet", "daily", "twice", "capsule"],
    "CONTRAINDICATION": ["avoid", "contraindicated", "do not use", "do not take", "forbidden", "toxic"],
    "SIDE_EFFECT": ["side effect", "nausea", "headache", "dizziness", "rash", "toxicity", "risk"],
    "DIAGNOSIS": ["treats", "cures", "diagnosed", "indicated for", "prescribed for", "remedy"]
}

KNOWN_MEDICAL_CONTRADICTIONS = [
    ("amoxicillin", "viral"),
    ("antibiotic", "viral flu"),
    ("antibiotic", "common cold"),
    ("aspirin", "pediatric fever"),
    ("aspirin", "reye")
]

def extract_claims(text: str) -> List[Tuple[str, str]]:
    """Split text into sentences and categorize medical claims."""
    raw_sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    claims = []
    for s in raw_sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        category = "GENERAL_MEDICAL"
        s_lower = s_clean.lower()
        for cat, kw_list in MEDICAL_CATEGORIES.items():
            if any(kw in s_lower for kw in kw_list):
                category = cat
                break
        claims.append((s_clean, category))
    return claims

def audit_claim_against_evidence(claim_text: str, category: str, evidence_chunks: List[str], db: sqlite3.Connection) -> Tuple[ClaimVerificationStatus, float, str, str]:
    """Audit single claim against evidence chunks and DB knowledge."""
    c_lower = claim_text.lower()
    
    # Check for direct clinical contradictions
    for bad_a, bad_b in KNOWN_MEDICAL_CONTRADICTIONS:
        if bad_a in c_lower and bad_b in c_lower:
            return (
                ClaimVerificationStatus.CONTRADICTED,
                0.0,
                "Medical Database & Clinical Guidelines",
                f"Contradiction detected: '{bad_a}' is clinically ineffective/contraindicated for '{bad_b}'."
            )

    combined_evidence = " ".join(evidence_chunks).lower()
    
    # Extract key medical terms from claim (words length > 3 excluding common stop words)
    words = [w for w in re.findall(r'\b[a-z]{4,}\b', c_lower) if w not in {"with", "that", "this", "from", "have", "more", "most", "some"}]
    if not words:
        return (ClaimVerificationStatus.VERIFIED, 1.0, "General Medical Knowledge", "Basic informative statement.")

    matched_words = [w for w in words if w in combined_evidence]
    overlap_ratio = len(matched_words) / len(words)

    if overlap_ratio >= 0.6:
        return (
            ClaimVerificationStatus.VERIFIED,
            round(overlap_ratio, 2),
            "Retrieved Clinical Evidence Chunks",
            f"Claim fully grounded by evidence context ({len(matched_words)}/{len(words)} key terms matched)."
        )
    elif overlap_ratio >= 0.3:
        return (
            ClaimVerificationStatus.PARTIALLY_VERIFIED,
            round(overlap_ratio, 2),
            "Partial Clinical Evidence",
            "Claim has partial grounding; additional evidence citation recommended."
        )
    else:
        # Check SQLite DB as secondary verification source
        cursor = db.cursor()
        found_in_db = False
        for word in words:
            cursor.execute("SELECT id FROM medicines WHERE LOWER(name) LIKE ? OR LOWER(uses) LIKE ? LIMIT 1;", (f"%{word}%", f"%{word}%"))
            if cursor.fetchone():
                found_in_db = True
                break
        
        if found_in_db:
            return (
                ClaimVerificationStatus.VERIFIED,
                0.85,
                "Medical Database Knowledge Graph",
                "Claim verified against internal Medical Database graph."
            )

        return (
            ClaimVerificationStatus.UNSUPPORTED,
            0.1,
            "None (Evidence Mismatch)",
            "Claim lacks grounding in provided context chunks or medical database."
        )

def evaluate_hallucination_guard(req: HallucinationGuardRequest, db: sqlite3.Connection) -> HallucinationGuardResponse:
    """
    Execute AI Hallucination Guard Pipeline:
    LLM -> Claim Extraction -> Evidence Verification -> Mismatch Check -> Auto-Sanitization / Regeneration
    """
    raw_claims = extract_claims(req.llm_response_text)
    extracted_claims: List[ExtractedClaim] = []
    
    supported_count = 0
    unsupported_count = 0
    sanitized_sentences = []

    for i, (claim_text, category) in enumerate(raw_claims, 1):
        status, conf, source, reason = audit_claim_against_evidence(
            claim_text, category, req.context_evidence_chunks, db
        )
        
        c_obj = ExtractedClaim(
            claim_id=f"CLM-{i:02d}",
            claim_text=claim_text,
            category=category,
            status=status,
            grounding_source=source,
            confidence_score=conf,
            verification_reason=reason
        )
        extracted_claims.append(c_obj)

        if status in (ClaimVerificationStatus.VERIFIED, ClaimVerificationStatus.PARTIALLY_VERIFIED):
            supported_count += 1
            sanitized_sentences.append(claim_text)
        else:
            unsupported_count += 1
            if req.allow_auto_regeneration:
                # Sanitize unsupported or contradicted claims
                sanitized_sentences.append(f"[REDACTED_UNVERIFIED_CLAIM: Grounding evidence unavailable for '{claim_text}']")

    total_claims = len(extracted_claims)
    grounding_score = round((supported_count / total_claims) * 100.0, 1) if total_claims > 0 else 100.0
    hallucination_detected = unsupported_count > 0

    action_taken = "PASSED"
    if hallucination_detected:
        action_taken = "REGENERATED_AND_SANITIZED" if req.allow_auto_regeneration else "REJECTED"

    verified_text = " ".join(sanitized_sentences) if req.allow_auto_regeneration else req.llm_response_text

    return HallucinationGuardResponse(
        is_safe=not hallucination_detected or req.allow_auto_regeneration,
        hallucination_detected=hallucination_detected,
        total_claims_extracted=total_claims,
        supported_claims_count=supported_count,
        unsupported_claims_count=unsupported_count,
        grounding_score=grounding_score,
        action_taken=action_taken,
        verified_response_text=verified_text,
        claims=extracted_claims
    )
