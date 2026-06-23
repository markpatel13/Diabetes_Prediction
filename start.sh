#!/bin/bash

# Exit immediately if a command fails
set -e

# 1) Start FastAPI backend (Uvicorn) in the background
uvicorn backend.app:app --host 0.0.0.0 --port 8000 &

# 2) Start Streamlit frontend in the foreground
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0