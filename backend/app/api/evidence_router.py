import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.evidence_schema import (
    EvidenceCitationRequest, EvidenceCitationResponse, CitedStatementItem
)
from app.services.evidence_citation_engine import (
    execute_evidence_citation_engine, evaluate_explanation_statements
)

router = APIRouter(prefix="/evidence", tags=["Evidence Citation Engine ⭐⭐⭐⭐⭐"])

@router.post("/cite", response_model=EvidenceCitationResponse)
def cite_evidence_endpoint(req: EvidenceCitationRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Execute 4-Tier Evidence Citation & Enforcement Engine:
    Maps medical claims against 4 Evidence Tiers: Drug Database, Clinical Guidelines, Drug Interactions, and Medical Literature.
    Strictly flags or rejects unsupported statements.
    """
    try:
        return execute_evidence_citation_engine(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evidence Citation Engine failure: {str(e)}")

@router.post("/verify-statement", response_model=CitedStatementItem)
def verify_single_statement_endpoint(
    statement: str, medical_query: str, db: sqlite3.Connection = Depends(get_db)
):
    """Verify a single medical statement against evidence sources."""
    cited_stmts, _, _, _ = evaluate_explanation_statements(
        query=medical_query, proposed_explanation=statement, db=db, strict=True
    )
    if not cited_stmts:
        raise HTTPException(status_code=400, detail="Could not parse statement")
    return cited_stmts[0]
