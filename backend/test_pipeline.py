import sys
sys.path.insert(0, '.')
import sqlite3
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.services.llm_orchestrator import orchestrate_llm_pipeline

conn = sqlite3.connect('../medical_database.db')
req = OrchestratorRequest(
    patient_id='TEST',
    conversation_turns=[{'role': 'user', 'text': 'I have severe chest pain crushing in nature radiating to my left arm'}]
)
res = orchestrate_llm_pipeline(req, conn)

out = res.dict() if hasattr(res, "dict") else res
print(out.get('differential_diagnosis'))
