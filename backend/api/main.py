# from fastapi import FastAPI
# from pydantic import BaseModel
# import numpy as np
# import joblib
# from pathlib import Path

# # 1) Pydantic model (same as your schemas.py, you can also import it from there)
# class DiabetesFeatures(BaseModel):
#     pregnancies: int
#     glucose: int
#     bloodpressure: int
#     skinthickness: int
#     insulin: int
#     bmi: float
#     dpf: float
#     age: int

# # 2) Build correct path to the model file
# # backend/app.py → parent is project root
# BASE_DIR = Path(__file__).resolve().parent.parent
# MODEL_PATH = BASE_DIR / "frontend" / "pipeline" / "model" / "diabetes_model.pkl"

# # 3) Load the trained model with joblib
# classifier = joblib.load(MODEL_PATH)

# # 4) Create FastAPI app
# app = FastAPI()

# # 5) Define the /predict route
# @app.post("/predict")
# def predict_diabetes(features: DiabetesFeatures):
#     # Convert Pydantic object to numpy array in the correct order
#     data = np.array([[
#         features.pregnancies,
#         features.glucose,
#         features.bloodpressure,
#         features.skinthickness,
#         features.insulin,
#         features.bmi,
#         features.dpf,
#         features.age,
#     ]])

#     # Model prediction
#     prediction = classifier.predict(data)

#     # Convert numpy/int64 to normal int for JSON
#     result = int(prediction[0])

#     # Return JSON response
#     return {"prediction": result}

# @app.get("/")
# def root():
#     return {
#         "message": "Diabetes prediction backend is running.",
#         "info": "Use POST /predict with the required features or visit /docs for interactive API docs."
#     }
from fastapi import FastAPI

app = FastAPI()
from pydantic import BaseModel
import numpy as np
import joblib
from pathlib import Path

# 1) Pydantic model (same as your schemas.py, you can also import it from there)
class DiabetesFeatures(BaseModel):
    pregnancies: int
    glucose: int
    bloodpressure: int
    skinthickness: int
    insulin: int
    bmi: float
    dpf: float
    age: int

# 2) Build correct path to the model file
# backend/api/main.py → parent is backend/api
MODEL_PATH = Path(__file__).resolve().parent / "diabetes_model.pkl"

# 3) Load the trained model with joblib
classifier = joblib.load(MODEL_PATH)

# 4) Create FastAPI app
app = FastAPI()

# 5) Define the /predict route
@app.post("/predict")
def predict_diabetes(features: DiabetesFeatures):
    # Convert Pydantic object to numpy array in the correct order
    data = np.array([[
        features.pregnancies,
        features.glucose,
        features.bloodpressure,
        features.skinthickness,
        features.insulin,
        features.bmi,
        features.dpf,
        features.age,
    ]])

    # Model prediction
    prediction = classifier.predict(data)

    # Convert numpy/int64 to normal int for JSON
    result = int(prediction[0])

    # Return JSON response
    return {"prediction": result}

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Vercel"}