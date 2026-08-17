import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.clinical_question_bank import HIERARCHICAL_QUESTION_BANK, rank_questions_by_information_gain

def test_question_bank_categories_and_metadata():
    categories = set(item.category for item in HIERARCHICAL_QUESTION_BANK)
    expected_categories = {
        "General", "Respiratory", "Cardiology", "Neurology", "GASTROENTEROLOGY",
        "Dermatology", "Urology", "Endocrinology", "Pediatrics", "Pregnancy",
        "Psychiatry", "Musculoskeletal", "Ophthalmology", "ENT", "Emergency"
    }
    assert {c.upper() for c in expected_categories}.issubset(set(c.upper() for c in categories))

    for item in HIERARCHICAL_QUESTION_BANK:
        assert item.question_id.strip() != ""
        assert item.question.strip() != ""
        assert 0.0 <= item.information_gain <= 1.0
        assert item.priority >= 1

def test_information_gain_ranking_respiratory():
    symptoms = ["cough", "fever"]
    top_diseases = ["Viral Upper Respiratory Infection", "Pneumonia", "COVID-19"]
    
    ranked = rank_questions_by_information_gain(symptoms, top_diseases, limit=3)
    assert len(ranked) == 3
    q_texts = [q["question"] for q in ranked]
    assert any("cough" in q.lower() or "mucus" in q.lower() or "shortness of breath" in q.lower() or "symptom" in q.lower() for q in q_texts)

def test_information_gain_ranking_cardiology():
    symptoms = ["chest pain", "sweating"]
    top_diseases = ["Angina Pectoris", "Myocardial Infarction"]
    
    ranked = rank_questions_by_information_gain(symptoms, top_diseases, limit=3)
    assert len(ranked) == 3
    categories = [q["category"] for q in ranked]
    assert "Cardiology" in categories or "Emergency" in categories or "General" in categories
