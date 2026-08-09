from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AnsweredTurn(BaseModel):
    question_id: str
    question_text: str
    answer: str

class NextQuestion(BaseModel):
    question_id: str
    question_type: str
    question_text: str
    options: Optional[List[str]] = []
    rationale: str

class TopConditionItem(BaseModel):
    name: str
    probability: int
    supporting: List[str]
    missing: List[str]

class NextBestQuestion(BaseModel):
    question: str
    reason: str
    information_gain: str = "High"
    diseases_separated: Optional[List[str]] = []

class CandidateDiseaseProbability(BaseModel):
    disease_name: str
    probability: float
    matched_symptoms: List[str]
    severity_level: str

class AdaptiveEvaluationRequest(BaseModel):
    session_uuid: Optional[str] = None
    reported_symptoms: List[str] = Field(..., min_length=1, description="List of canonical symptom names e.g. ['fever', 'headache']")
    answered_turns: Optional[List[AnsweredTurn]] = []
    max_questions: Optional[int] = 5
    confidence_threshold: Optional[float] = 0.85

class AdaptiveEvaluationResponse(BaseModel):
    confidence_score: float
    is_emergency: bool = False
    emergency_warning: Optional[str] = None
    enough_information: bool = False
    should_continue: bool = True
    question_count: int = 0
    max_questions: int = 5
    next_question: Optional[NextQuestion] = None
    candidate_diseases: List[CandidateDiseaseProbability] = []
    termination_reason: Optional[str] = None

class AdaptiveEngineJSONResponse(BaseModel):
    triage: str = "GREEN"
    confidence: int = 38
    top_conditions: List[TopConditionItem] = []
    next_best_question: Optional[NextBestQuestion] = None
    questions_remaining: int = 4
    ready_for_recommendation: bool = False

