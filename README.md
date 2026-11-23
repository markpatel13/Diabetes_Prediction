# Diabetes Prediction

An end-to-end diabetes risk prediction project with a FastAPI backend, a Streamlit frontend, and a scikit-learn model trained on the Pima Indians diabetes dataset.

## Overview

The project is split into two parts:

- `backend/` serves the trained model through a FastAPI API.
- `frontend/` contains the Streamlit app and the training pipeline used to build the model.

The frontend sends patient feature data to the API, which returns a binary prediction for diabetes risk.

## Features

- Simple Streamlit interface for entering health metrics.
- FastAPI endpoint for model inference.
- Random Forest model trained with scikit-learn.
- Basic visual summaries for glucose, BMI, and blood pressure.
- Lightweight project structure that is easy to run locally.

## Project Structure

```text
Diabetes_Prediction/
├─ backend/
│  ├─ api/
│  │  └─ main.py
│  ├─ requirements.txt
│  └─ schemas.py
├─ frontend/
│  ├─ app.py
│  ├─ dataset/
│  │  └─ kaggle_diabetes.csv
│  └─ pipeline/
│     ├─ config.py
│     ├─ data_preprocessing.py
│     ├─ evaluate.py
│     └─ train.py
├─ requirements.txt
├─ start.sh
└─ README.md
```

## Requirements

- Python 3.10 or newer
- `pip`
- A virtual environment is recommended

## Installation

Create and activate a virtual environment, then install dependencies from both requirements files:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

## Training the Model

The training pipeline reads the dataset from `frontend/dataset/kaggle_diabetes.csv` and saves the trained model to `backend/api/diabetes_model.pkl`.

From the project root:

```bash
cd frontend/pipeline
python train.py
```

To inspect model quality after training:

```bash
python evaluate.py
```

## Running the Backend

Start the FastAPI server from the project root:

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:

- `GET /` returns a basic status message.
- `POST /predict` accepts the feature payload and returns a prediction.

## Running the Frontend

In a second terminal, start the Streamlit app:

```bash
streamlit run frontend/app.py
```

The frontend currently posts prediction requests to:

```text
https://diabetes-prediction-dun.vercel.app/predict
```

If you are running the backend locally, update that URL in `frontend/app.py` to point to your local server, for example:

```text
http://127.0.0.1:8000/predict
```

## One-Command Startup

The provided `start.sh` launches both services for Unix-like environments. It now targets the correct FastAPI module path:

```bash
bash start.sh
```

On Windows, it is usually easier to run the backend and frontend in separate terminals.

## API Request Schema

`POST /predict` expects JSON with the following fields:

```json
{
  "pregnancies": 1,
  "glucose": 120,
  "bloodpressure": 72,
  "skinthickness": 20,
  "insulin": 80,
  "bmi": 25.0,
  "dpf": 0.5,
  "age": 30
}
```

The response is:

```json
{
  "prediction": 0
}
```

Where `0` means low risk and `1` means high risk.

## Notes

- The model file is not committed automatically, so train the model before running the backend locally.
- The preprocessing step replaces zero values in selected medical columns with more suitable statistics.
- If the frontend cannot reach the backend, check the API URL in `frontend/app.py` and confirm the server is running.

## Troubleshooting

- If you see import errors in the pipeline scripts, run them from inside `frontend/pipeline/` or use the package-aware invocation from the project root.
- If FastAPI cannot load the model, confirm that `backend/api/diabetes_model.pkl` exists.
- If Streamlit cannot connect to the API, make sure the backend is reachable on the expected host and port.


<!-- cd C:\Users\Dell\OneDrive\Desktop\Diabetes_Prediction
python -m streamlit run frontend\app.py -->

<!-- cd C:\Users\Dell\OneDrive\Desktop\Diabetes_Prediction
python -m uvicorn backend.api.main:app --reload --port 8000 -->

<!-- API_URL = "http://127.0.0.1:8000/predict" -->