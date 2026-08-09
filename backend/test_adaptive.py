import sys
sys.path.insert(0, '.')
from app.services.clinical_question_bank import rank_questions_by_information_gain

# Test with 3 candidate diseases
candidates = ["Asthma", "Community-Acquired Pneumonia", "Pulmonary Embolism"]
symptoms = ["shortness of breath", "cough"]
already_asked = []

questions = rank_questions_by_information_gain(
    symptoms=symptoms,
    candidate_diseases=candidates,
    already_asked_ids=already_asked,
    limit=3
)

for idx, q in enumerate(questions):
    print(f"Q{idx+1}: {q['question']}")
    print(f"   Differentiates: {q['helps_differentiate']}")
    print(f"   ID: {q['question_id']}")
    print()
