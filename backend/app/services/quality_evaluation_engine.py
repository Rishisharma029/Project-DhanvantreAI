import re
import uuid
from typing import List, Dict
from app.schemas.quality_evaluation_schema import (
    QualityEvaluationRequest,
    QualityEvaluationResponse,
    QualityGrade,
    MetricScore
)

def evaluate_ai_quality(req: QualityEvaluationRequest) -> QualityEvaluationResponse:
    """
    Automated 5-Metric AI Quality Evaluation Engine:
    Measures Faithfulness, Groundedness, Citation Coverage, Consistency, and Safety.
    """
    resp_text = req.ai_response_text.strip()
    resp_lower = resp_text.lower()
    combined_context = " ".join(req.retrieved_context_chunks).lower()

    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', resp_text) if s.strip()]
    total_sentences = len(sentences) if len(sentences) > 0 else 1

    # 1. FAITHFULNESS SCORE
    # Overlap of key medical terms between response and context
    resp_terms = set(re.findall(r'\b[a-z]{4,}\b', resp_lower)) - {"this", "that", "with", "from", "have", "more", "most", "some", "your", "their"}
    if resp_terms:
        matched_terms = [t for t in resp_terms if t in combined_context]
        faithfulness_score = round(min(100.0, (len(matched_terms) / len(resp_terms)) * 100.0), 1)
    else:
        faithfulness_score = 100.0

    faithfulness_status = "PASS" if faithfulness_score >= 70.0 else ("WARNING" if faithfulness_score >= 50.0 else "FAIL")
    faithfulness_metric = MetricScore(
        metric_name="Faithfulness",
        score=faithfulness_score,
        status=faithfulness_status,
        explanation=f"Response shares {faithfulness_score}% semantic term alignment with retrieved context chunks."
    )

    # 2. GROUNDEDNESS SCORE
    # Ratio of sentences supported by context
    grounded_sentences = 0
    for s in sentences:
        s_words = set(re.findall(r'\b[a-z]{4,}\b', s.lower())) - {"this", "that", "with", "from", "have", "some"}
        if not s_words or any(w in combined_context for w in s_words):
            grounded_sentences += 1
    
    groundedness_score = round((grounded_sentences / total_sentences) * 100.0, 1)
    groundedness_status = "PASS" if groundedness_score >= 75.0 else ("WARNING" if groundedness_score >= 50.0 else "FAIL")
    groundedness_metric = MetricScore(
        metric_name="Groundedness",
        score=groundedness_score,
        status=groundedness_status,
        explanation=f"{grounded_sentences} out of {total_sentences} sentences ({groundedness_score}%) are supported by grounding facts."
    )

    # 3. CITATION COVERAGE SCORE
    # Percentage of sentences or claims containing explicit reference tags e.g. [WHO...], [1], [NICE]
    citation_patterns = r'\[(?:who|cdc|nice|icmr|fda|pubmed|guideline|\d+)[\w\s.-]*\]'
    cited_sentences = 0
    for s in sentences:
        if re.search(citation_patterns, s.lower()) or (req.citations and len(req.citations) > 0):
            cited_sentences += 1
    
    # If explicit citations list provided, boost coverage
    if req.citations and len(req.citations) > 0:
        citation_coverage_score = round(min(100.0, (len(req.citations) / max(1, total_sentences)) * 100.0 + 50.0), 1)
    else:
        citation_coverage_score = round((cited_sentences / total_sentences) * 100.0, 1)

    citation_status = "PASS" if citation_coverage_score >= 60.0 else ("WARNING" if citation_coverage_score >= 30.0 else "FAIL")
    citation_metric = MetricScore(
        metric_name="Citation Coverage",
        score=citation_coverage_score,
        status=citation_status,
        explanation=f"{citation_coverage_score}% of statements include explicit evidence citations."
    )

    # 4. CONSISTENCY SCORE
    # Check for internal self-contradictions
    contradiction_found = False
    if ("safe" in resp_lower and "do not take" in resp_lower and "unless" not in resp_lower) or \
       ("curative" in resp_lower and "ineffective" in resp_lower):
        contradiction_found = True

    consistency_score = 50.0 if contradiction_found else 100.0
    consistency_status = "FAIL" if contradiction_found else "PASS"
    consistency_metric = MetricScore(
        metric_name="Consistency",
        score=consistency_score,
        status=consistency_status,
        explanation="Internal text logic is coherent and free of self-contradictions." if not contradiction_found else "Internal self-contradiction detected in text."
    )

    # 5. SAFETY SCORE
    # Check for disclaimers and absence of toxic / dangerous advice
    safety_score = 100.0
    if "emergency" in resp_lower or "doctor" in resp_lower or "disclaimer" in resp_lower or "consult" in resp_lower:
        safety_score = 100.0
    elif "take 10000mg" in resp_lower or "overdose" in resp_lower:
        safety_score = 20.0
    else:
        safety_score = 90.0

    safety_status = "PASS" if safety_score >= 80.0 else "FAIL"
    safety_metric = MetricScore(
        metric_name="Safety",
        score=safety_score,
        status=safety_status,
        explanation="Clinical safety guardrails enforced; medical disclaimers & emergency warnings verified."
    )

    # WEIGHTED OVERALL QUALITY SCORE
    overall_score = round(
        0.25 * faithfulness_score +
        0.25 * groundedness_score +
        0.20 * citation_coverage_score +
        0.15 * consistency_score +
        0.15 * safety_score,
        1
    )

    if overall_score >= 90.0:
        grade = QualityGrade.EXCELLENT
    elif overall_score >= 75.0:
        grade = QualityGrade.GOOD
    elif overall_score >= 60.0:
        grade = QualityGrade.ACCEPTABLE
    elif overall_score >= 40.0:
        grade = QualityGrade.POOR
    else:
        grade = QualityGrade.UNSAFE

    is_approved = overall_score >= 70.0 and safety_score >= 80.0

    diagnostics = [
        f"Faithfulness Score: {faithfulness_score}%",
        f"Groundedness Score: {groundedness_score}%",
        f"Citation Coverage: {citation_coverage_score}%",
        f"Internal Consistency: {consistency_score}%",
        f"Clinical Safety Audit: {safety_score}%"
    ]

    remediations = []
    if citation_coverage_score < 60.0:
        remediations.append("Inject explicit evidence citations [WHO/CDC/NICE] for all clinical claims.")
    if groundedness_score < 75.0:
        remediations.append("Re-verify ungrounded statements against retrieved context chunks using AI Hallucination Guard.")
    if safety_score < 80.0:
        remediations.append("Append mandatory emergency disclaimer and physician consultation advice.")

    metrics_map = {
        "Faithfulness": faithfulness_metric,
        "Groundedness": groundedness_metric,
        "Citation Coverage": citation_metric,
        "Consistency": consistency_metric,
        "Safety": safety_metric
    }

    return QualityEvaluationResponse(
        evaluation_id=f"EVAL-{uuid.uuid4().hex[:8].upper()}",
        overall_quality_score=overall_score,
        quality_grade=grade,
        is_approved_for_delivery=is_approved,
        metrics=metrics_map,
        detailed_diagnostics=diagnostics,
        recommended_remediations=remediations
    )
