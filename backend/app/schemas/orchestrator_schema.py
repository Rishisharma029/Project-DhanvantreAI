from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any

class ToolExecutionTrace(BaseModel):
    tool_name: str
    input_params: Dict[str, Any]
    output_summary: str
    status: str = "success"

class PromptPreviewResponse(BaseModel):
    system_prompt: str
    user_prompt: str
    injected_context_summary: Dict[str, Any]

class CitationItem(BaseModel):
    title: str
    snippet: str
    evidence_grade: Optional[str] = "Grade A (Level 1a Evidence)"
    source_db: Optional[str] = "WHO & CDC Clinical Database"

class PatientVitals(BaseModel):
    temperature_f: Optional[float] = None
    spo2_pct: Optional[float] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None

class OrchestratorRequest(BaseModel):
    query: Optional[str] = Field(default=None, description="User natural language health input")
    user_message: Optional[str] = Field(default=None, description="Alias for query")
    session_uuid: Optional[str] = None

    # Demographics
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    pregnancy_status: Optional[bool] = None

    # Clinical history
    allergies: Optional[List[str]] = []
    chronic_diseases: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    smoking_status: Optional[str] = None        # "never" | "current" | "former"
    alcohol_status: Optional[str] = None        # "none" | "social" | "heavy"
    occupation: Optional[str] = None
    travel_history: Optional[str] = None

    # Vitals (if provided)
    vitals: Optional[PatientVitals] = None

    # Conversation tracking
    turns_answered: Optional[int] = 0
    previously_asked_question_ids: Optional[List[str]] = []
    accumulated_symptoms: Optional[List[str]] = []

    @model_validator(mode="before")
    @classmethod
    def resolve_query_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("query") and data.get("user_message"):
                data["query"] = data["user_message"]
            if data.get("query") and isinstance(data["query"], str):
                from app.utils.sanitizer import sanitize_text
                data["query"] = sanitize_text(data["query"])
                data["user_message"] = data["query"]
        return data

class ClinicalLLMResponse(BaseModel):
    # Reasoning
    thought_process: str
    reasoning_timeline: List[str] = []         # Ordered reasoning steps for UI display
    assessment_stage: str = "Adaptive Questioning (Turn 1)"

    # Extracted data
    extracted_symptoms: List[str] = []
    extracted_entities: Dict[str, Any] = {}    # Full structured entity map

    # Syndrome & Emergency
    syndrome_detected: Optional[str] = None
    is_emergency: bool = False
    emergency_alert: Optional[str] = None
    triage_status: str = "GREEN_STABLE"

    # Differential
    differential_diagnosis: List[Dict[str, Any]] = []
    confidence_score: float = 0.38

    # Questioning
    followup_questions: List[str] = []
    termination_reason: Optional[str] = None   # Why questioning stopped

    # Explainability
    clinical_rationale: str = ""
    matched_symptoms: List[str] = []
    missing_symptoms: List[str] = []
    conditions_less_likely: List[str] = []

    # Evidence
    citations: List[CitationItem] = []

    # Recommendations
    recommended_medicines: List[Dict[str, Any]] = []
    medicine_recommendation_suppressed: bool = False
    medicine_suppression_reason: Optional[str] = None
    
    # Investigations & Scoring
    recommended_investigations: Dict[str, Any] = {}
    clinical_scores: List[Dict[str, Any]] = []

    # Safety
    safety_score: Optional[float] = 100.0
    safety_grade: Optional[str] = "SAFE"
    warnings: List[str] = []

    # Knowledge gap
    knowledge_gap_logged: bool = False

    # Audit
    tool_traces: List[ToolExecutionTrace] = []
    disclaimer: str = (
        "This output is for clinical decision support only and does not constitute "
        "personalized medical advice. Always consult a licensed physician."
    )
