import requests
import streamlit as st
import base64
from pathlib import Path

# 1) Page config
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered"
)

# Background image with overlay (using local image from root folder)
image_path = Path(__file__).parent.parent / "download2.jpeg"
if image_path.exists():
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{img_base64}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.75);
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 2) Title and description
st.title("🩺 Diabetes Risk Prediction")
st.write("Fill in the details below to check the **predicted diabetes risk** using a trained ML model.")

# 3) Sidebar info
st.sidebar.header("About")
st.sidebar.info(
    "This app uses a machine learning model (Random Forest) "
    "served via a FastAPI backend to predict diabetes risk."
)

# 4) Input form
with st.form("diabetes_form"):
    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
        glucose = st.number_input("Glucose", min_value=0, max_value=300, value=120, step=1)
        bloodpressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70, step=1)
        skinthickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20, step=1)

    with col2:
        insulin = st.number_input("Insulin", min_value=0, max_value=900, value=80, step=1)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, step=0.1, format="%.1f")
        dpf = st.number_input("Diabetes Pedigree Function (DPF)", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
        age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)

    submitted = st.form_submit_button("Predict")

# 5) When button is clicked, call FastAPI
if submitted:
    # Build JSON payload exactly matching your Pydantic model
    payload = {
        "pregnancies": int(pregnancies),
        "glucose": int(glucose),
        "bloodpressure": int(bloodpressure),
        "skinthickness": int(skinthickness),
        "insulin": int(insulin),
        "bmi": float(bmi),
        "dpf": float(dpf),
        "age": int(age),
    }

    try:
        # Call FastAPI backend
        # API_URL = "https://diabetes-prediction-dun.vercel.app/predict"
        response = requests.post("https://diabetes-prediction-dun.vercel.app/predict", json=payload)
        response.raise_for_status()  # raise error if status != 200

        data = response.json()
        prediction = data.get("prediction")

        # if prediction == 1:
        #     st.error("⚠️ The model predicts **high risk of diabetes**.")
        # elif prediction == 0:
        #     st.success("✅ The model predicts **low risk of diabetes**.")
        
        
        if prediction == 1:
            st.error(
        f"⚠️ The model predicts **high risk of diabetes** for:\n"
        f"- Pregnancies: {pregnancies}\n"
        f"- Glucose: {glucose}\n"
        f"- Blood Pressure: {bloodpressure}\n"
        f"- BMI: {bmi}\n"
        f"- Age: {age}"
    )
        elif prediction == 0:
            st.success(
        f"✅ The model predicts **low risk of diabetes** for:\n"
        f"- Pregnancies: {pregnancies}\n"
        f"- Glucose: {glucose}\n"
        f"- Blood Pressure: {bloodpressure}\n"
        f"- BMI: {bmi}\n"
        f"- Age: {age}"
    )
        else:
            st.warning("Received an unexpected prediction value from the server.")
    
    
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Is it running on port 8000?")
    except Exception as e:
        st.error(f"An error occurred: {e}")