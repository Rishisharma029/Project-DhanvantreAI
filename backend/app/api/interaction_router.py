import sqlite3
from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.interaction_schema import (
    PairwiseCheckRequest, RegimenCheckRequest, CurrentVsRecommendedRequest,
    InteractionCheckResponse, CurrentVsRecommendedResponse
)
from app.services.interaction_engine import (
    check_pairwise_interaction, check_regimen_interactions, check_current_vs_recommended
)

router = APIRouter(prefix="/interactions", tags=["Drug Interaction Engine"])

@router.post("/check-pair", response_model=InteractionCheckResponse)
def check_pair_endpoint(body: PairwiseCheckRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Check pairwise drug interaction between Drug A and Drug B:
    - Classifies severity: Major 🔴, Moderate 🟡, Minor 🟢, Safe
    - Evaluates brand names & underlying active ingredients
    """
    return check_pairwise_interaction(body.drug_a, body.drug_b, db)

@router.post("/check-regimen", response_model=InteractionCheckResponse)
def check_regimen_endpoint(body: RegimenCheckRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Check all pairwise combinations in a multi-drug regimen (Polypharmacy Matrix).
    """
    return check_regimen_interactions(body.medicines, db)

@router.post("/check-current-vs-recommended", response_model=CurrentVsRecommendedResponse)
def check_current_vs_recommended_endpoint(body: CurrentVsRecommendedRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Safety Cross-Checker:
    Compares patient's active current medicines against proposed/recommended medicines to prevent dangerous adverse interactions.
    """
    return check_current_vs_recommended(body.current_medicines, body.recommended_medicines, db)
