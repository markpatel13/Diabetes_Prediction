import requests
import streamlit as st
import base64
from pathlib import Path
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered"
)

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

st.title("🩺 Diabetes Risk Prediction")
st.write("Fill in the details below to check the **predicted diabetes risk** using a trained ML model.")

st.sidebar.header("About")
st.sidebar.info(
    "This app uses a machine learning model (Random Forest) "
    "served via a FastAPI backend to predict diabetes risk."
)

with st.form("diabetes_form"):
    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
        glucose = st.number_input("Glucose", min_value=0, max_value=300, value=120, step=1)
        bloodpressure = st.number_input("Blood Pressure (Systolic)", min_value=0, max_value=200, value=120, step=1)
        skinthickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20, step=1)

    with col2:
        insulin = st.number_input("Insulin", min_value=0, max_value=900, value=80, step=1)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, step=0.1, format="%.1f")
        dpf = st.number_input("Diabetes Pedigree Function (DPF)", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
        age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)

    submitted = st.form_submit_button("Predict")


def plot_glucose_chart(glucose_value):
    fig, ax = plt.subplots(figsize=(7, 3.5))

    ax.axvspan(0, 99, color="#b7e4c7", alpha=0.8, label="Normal")
    ax.axvspan(100, 125, color="#ffe08a", alpha=0.8, label="Prediabetes")
    ax.axvspan(126, 300, color="#ffadad", alpha=0.8, label="Diabetes Range")

    ax.axvline(glucose_value, color="#1d3557", linewidth=3, label=f"Your Glucose: {glucose_value}")
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Glucose (mg/dL)")
    ax.set_title("Glucose Level vs Standard Ranges")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    return fig


def plot_bmi_chart(bmi_value):
    fig, ax = plt.subplots(figsize=(7, 3.5))

    ax.axvspan(0, 18.4, color="#cfe8ff", alpha=0.8, label="Underweight")
    ax.axvspan(18.5, 24.9, color="#b7e4c7", alpha=0.8, label="Healthy")
    ax.axvspan(25, 29.9, color="#ffe08a", alpha=0.8, label="Overweight")
    ax.axvspan(30, 70, color="#ffadad", alpha=0.8, label="Obesity")

    ax.axvline(bmi_value, color="#6a040f", linewidth=3, label=f"Your BMI: {bmi_value}")
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("BMI")
    ax.set_title("BMI vs Standard Ranges")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    return fig

def plot_bp_chart(bp_value):
    fig, ax = plt.subplots(figsize=(7, 3.5))

    ax.axvspan(0, 119, color="#b7e4c7", alpha=0.8, label="Normal")
    ax.axvspan(120, 129, color="#ffe08a", alpha=0.8, label="Elevated")
    ax.axvspan(130, 139, color="#ffd6a5", alpha=0.8, label="Stage 1")
    ax.axvspan(140, 200, color="#ffadad", alpha=0.8, label="Stage 2")

    ax.axvline(bp_value, color="#5a189a", linewidth=3, label=f"Your BP: {bp_value}")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Blood Pressure (mm Hg)")
    ax.set_title("Blood Pressure vs Standard Ranges")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    return fig

if submitted:
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
        response = requests.post("https://diabetes-prediction-dun.vercel.app/predict", json=payload)
        response.raise_for_status()

        data = response.json()
        prediction = data.get("prediction")

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

        st.subheader("Health Visuals")
        st.pyplot(plot_glucose_chart(glucose))
        st.pyplot(plot_bmi_chart(bmi))
        st.pyplot(plot_bp_chart(bloodpressure))

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Is it running on port 8000?")
    except Exception as e:
        st.error(f"An error occurred: {e}")