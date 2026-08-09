import json
import sqlite3
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.profile import MedicalProfileUpdate, MedicalProfileResponse
from app.api.deps import get_current_user, RoleChecker

router = APIRouter(prefix="/profile", tags=["User Medical Profile Service"])

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate Body Mass Index (BMI)."""
    if height_cm and weight_kg and height_cm > 0:
        height_m = height_cm / 100.0
        return round(weight_kg / (height_m * height_m), 2)
    return None

@router.get("/me", response_model=MedicalProfileResponse)
def get_my_profile(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Fetch current authenticated user's medical profile."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_medical_profiles WHERE user_id = ?;", (current_user["id"],))
    row = cursor.fetchone()

    if not row:
        # Create blank profile record if not present
        now_str = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO user_medical_profiles (user_id, updated_at)
            VALUES (?, ?);
        """, (current_user["id"], now_str))
        db.commit()
        cursor.execute("SELECT * FROM user_medical_profiles WHERE user_id = ?;", (current_user["id"],))
        row = cursor.fetchone()

    return MedicalProfileResponse.from_db_row(dict(row))

@router.put("/me", response_model=MedicalProfileResponse)
def update_my_profile(profile_in: MedicalProfileUpdate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Create or update current user's medical profile."""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM user_medical_profiles WHERE user_id = ?;", (current_user["id"],))
    existing = cursor.fetchone()

    bmi_val = calculate_bmi(profile_in.height_cm, profile_in.weight_kg)
    allergies_json = json.dumps(profile_in.allergies or [])
    chronic_json = json.dumps(profile_in.chronic_diseases or [])
    meds_json = json.dumps(profile_in.current_medications or [])
    now_str = datetime.now(timezone.utc).isoformat()
    preg_int = 1 if profile_in.pregnancy_status else 0

    if existing:
        cursor.execute("""
            UPDATE user_medical_profiles
            SET age = ?, gender = ?, height_cm = ?, weight_kg = ?, bmi = ?,
                blood_group = ?, pregnancy_status = ?, allergies = ?,
                chronic_diseases = ?, current_medications = ?,
                past_medical_history = ?, family_history = ?,
                smoking_status = ?, alcohol_consumption = ?, updated_at = ?
            WHERE user_id = ?;
        """, (
            profile_in.age, profile_in.gender, profile_in.height_cm, profile_in.weight_kg,
            bmi_val, profile_in.blood_group, preg_int, allergies_json,
            chronic_json, meds_json, profile_in.past_medical_history,
            profile_in.family_history, profile_in.smoking_status,
            profile_in.alcohol_consumption, now_str, current_user["id"]
        ))
    else:
        cursor.execute("""
            INSERT INTO user_medical_profiles (
                user_id, age, gender, height_cm, weight_kg, bmi, blood_group,
                pregnancy_status, allergies, chronic_diseases, current_medications,
                past_medical_history, family_history, smoking_status, alcohol_consumption, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            current_user["id"], profile_in.age, profile_in.gender, profile_in.height_cm,
            profile_in.weight_kg, bmi_val, profile_in.blood_group, preg_int,
            allergies_json, chronic_json, meds_json, profile_in.past_medical_history,
            profile_in.family_history, profile_in.smoking_status,
            profile_in.alcohol_consumption, now_str
        ))

    db.commit()
    cursor.execute("SELECT * FROM user_medical_profiles WHERE user_id = ?;", (current_user["id"],))
    row = cursor.fetchone()
    return MedicalProfileResponse.from_db_row(dict(row))

@router.delete("/me")
def reset_my_profile(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """Reset/clear medical profile for current user."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM user_medical_profiles WHERE user_id = ?;", (current_user["id"],))
    db.commit()
    return {"message": "Medical profile successfully reset"}

@router.get("/user/{target_user_id}", response_model=MedicalProfileResponse, dependencies=[Depends(RoleChecker(["doctor", "admin"]))])
def get_patient_profile(target_user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Doctor/Admin endpoint to view patient chart profile by User ID."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_medical_profiles WHERE user_id = ?;", (target_user_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient medical profile not found")
    return MedicalProfileResponse.from_db_row(dict(row))
