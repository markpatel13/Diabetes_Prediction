# pipeline/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR.parent / "dataset" / "kaggle_diabetes.csv"

# Model is now in backend/api folder
PROJECT_ROOT = BASE_DIR.parent.parent
MODEL_PATH = PROJECT_ROOT / "backend" / "api" / "diabetes_model.pkl"