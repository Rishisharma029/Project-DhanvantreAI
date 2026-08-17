"""
AuraMed AI — Clinical Syndrome Engine v2.0
==========================================
Detects high-risk symptom cluster syndromes BEFORE individual disease matching.
This ensures dangerous presentations are never misclassified as benign illness.

Each syndrome specifies:
  - required_keywords: symptom triggers
  - min_match_count: minimum required to fire
  - triage: RED_URGENT / YELLOW_MODERATE / GREEN_STABLE
  - is_emergency: triggers hard-stop if True
  - differentials: disease candidates this syndrome unlocks
  - targeted_questions: high info-gain questions for this syndrome
"""
from typing import List, Dict, Any, Optional


class ClinicalSyndrome:
    def __init__(
        self,
        syndrome_id: str,
        name: str,
        specialty: str,
        required_keywords: List[str],
        supporting_findings: List[str],
        excluded_findings: List[str],
        red_flags: List[str],
        min_match_count: int,
        triage: str,
        is_emergency: bool,
        priority: int,
        differentials: List[Dict[str, Any]],
        recommended_investigations: List[str],
        targeted_questions: List[str],
        question_category: str = "General"
    ):
        self.syndrome_id = syndrome_id
        self.name = name
        self.specialty = specialty
        self.required_keywords = [k.lower() for k in required_keywords]
        self.supporting_findings = [k.lower() for k in supporting_findings]
        self.excluded_findings = [k.lower() for k in excluded_findings]
        self.red_flags = [k.lower() for k in red_flags]
        self.min_match_count = min_match_count
        self.triage = triage
        self.is_emergency = is_emergency
        self.priority = priority
        self.differentials = differentials
        self.recommended_investigations = recommended_investigations
        self.targeted_questions = targeted_questions
        self.question_category = question_category

    def evaluate(self, query_text: str, symptoms: List[str]) -> Optional[Dict[str, Any]]:
        # Check if any excluded finding is present (and not negated)
        for ex in self.excluded_findings:
            ex_sym = any(ex in s.lower() for s in symptoms)
            ex_text = ex in query_text.lower() and not any(neg + ex in query_text.lower() for neg in ["no ", "not ", "without ", "free of ", "denies ", "never "])
            if ex_sym or ex_text:
                return None
            
        matched = []
        for k in self.required_keywords:
            # Check if keyword matches a normalized symptom name
            matched_sym = any(k in s.lower() for s in symptoms)
            # Or if it is in the query text and not negated
            matched_text = k in query_text.lower() and not any(neg + k in query_text.lower() for neg in ["no ", "not ", "without ", "free of ", "denies ", "never "])
            if matched_sym or matched_text:
                matched.append(k)
                
        if len(matched) >= self.min_match_count:
            # Check supporting and red flags for analytics (optional usage by caller)
            matched_supporting = []
            for k in self.supporting_findings:
                if any(k in s.lower() for s in symptoms) or (k in query_text.lower() and not any(neg + k in query_text.lower() for neg in ["no ", "not ", "without ", "free of ", "denies ", "never "])):
                    matched_supporting.append(k)
                    
            matched_red = []
            for k in self.red_flags:
                if any(k in s.lower() for s in symptoms) or (k in query_text.lower() and not any(neg + k in query_text.lower() for neg in ["no ", "not ", "without ", "free of ", "denies ", "never "])):
                    matched_red.append(k)
            
            return {
                "syndrome_id": self.syndrome_id,
                "syndrome_name": self.name,
                "specialty": self.specialty,
                "matched_findings": matched,
                "matched_supporting": matched_supporting,
                "matched_red_flags": matched_red,
                "triage": self.triage,
                "is_emergency": self.is_emergency,
                "priority": self.priority,
                "differentials": self.differentials,
                "recommended_investigations": self.recommended_investigations,
                "targeted_questions": self.targeted_questions,
                "question_category": self.question_category
            }
        return None


try:
    from app.data.syndrome_kb import SYNDROME_KB
except ImportError:
    SYNDROME_KB = []

CLINICAL_SYNDROME_LIBRARY: List[ClinicalSyndrome] = []

for s_dict in SYNDROME_KB:
    CLINICAL_SYNDROME_LIBRARY.append(
        ClinicalSyndrome(
            syndrome_id=s_dict["syndrome_id"],
            name=s_dict["name"],
            specialty=s_dict.get("specialty", "General"),
            required_keywords=s_dict["required_keywords"],
            supporting_findings=s_dict.get("supporting_findings", []),
            excluded_findings=s_dict.get("excluded_findings", []),
            red_flags=s_dict.get("red_flags", []),
            min_match_count=s_dict["min_match_count"],
            triage=s_dict["triage"],
            is_emergency=s_dict["is_emergency"],
            priority=s_dict["priority"],
            differentials=s_dict["differentials"],
            recommended_investigations=s_dict.get("recommended_investigations", []),
            targeted_questions=s_dict.get("targeted_questions", []),
            question_category=s_dict.get("question_category", "General")
        )
    )



def evaluate_clinical_syndromes(
    query_text: str, symptoms: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Evaluates input symptoms against the Clinical Syndrome Library.
    Returns the HIGHEST priority matched syndrome, or None if none match.
    Syndromes are evaluated in priority order (highest first).
    """
    matches = []
    for syndrome in CLINICAL_SYNDROME_LIBRARY:
        result = syndrome.evaluate(query_text, symptoms)
        if result:
            matches.append(result)

    if matches:
        for m in matches:
            # Score: 2 points for every required keyword matched, 1 point for every supporting finding
            m["match_score"] = (len(m["matched_findings"]) * 2) + len(m["matched_supporting"])
            
        # Sort primarily by match score (highest first), then by priority as a tiebreaker
        matches.sort(key=lambda x: (x["match_score"], x["priority"]), reverse=True)
        return matches[0]
    return None
