import os
import sys

# Set Python Path to include backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.validate_cases import run_clinical_case_validator

if __name__ == "__main__":
    run_clinical_case_validator()
