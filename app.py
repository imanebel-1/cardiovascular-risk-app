import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Cardiovascular Risk System",
    page_icon="🫀",
    layout="centered"
)

# =========================
# UI HEADER
# =========================
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #E6F2FF, #B3D9FF);
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #A3CFFF;
            text-align: center;
        }
        .title {
            color: #003366;
            font-size: 26px;
            font-weight: 700;
        }
        .subtitle {
            color: #1a4d80;
            font-size: 15px;
        }
        .risk-breakdown {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 12px 18px;
            margin-top: 10px;
            font-size: 14px;
            color: #333;
            border-left: 4px solid #A3CFFF;
        }
        .risk-item {
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
            border-bottom: 1px solid #eee;
        }
    </style>

    <div class="main-header">
        <div class="title">🫀 Cardiovascular Risk Prediction System</div>
        <div class="subtitle">Clinical AI Decision Support Tool</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# INPUT SECTION
# =========================
st.markdown("## 🧍 Patient Details")

age = st.slider("Age", 20, 100, 40)
sex = st.selectbox("Sex", ["Female", "Male"])

st.markdown("## 💔 Symptoms")

chest_pain_level = st.slider("Chest pain level (0 = none, 10 = severe)", 0, 10, 0)
exang = st.selectbox("Do you experience chest pain or tightness during physical activity?", ["No", "Yes"])

st.markdown("## 🧪 Clinical Measurements")

trestbps = st.slider("Resting Blood Pressure (mmHg)", 80, 200, 120)
chol = st.slider("Total Cholesterol (mg/dL)", 100, 600, 180)
diabetes = st.selectbox("Do you have diabetes or high blood sugar?", ["No", "Yes"])

restecg = st.selectbox(
    "ECG (Electrocardiogram) result",
    ["Normal", "Mild abnormality (minor ST-T wave changes)", "Significant abnormality (left ventricular hypertrophy)"]
)

thalach = st.slider("Maximum heart rate achieved during exercise (bpm)", 60, 220, 155)

slope = st.selectbox(
    "How does your heart rate respond at peak exercise?",
    [
        "Normal response (heart rate rises well)",
        "Slight abnormal response (mild ST slope flattening)",
        "Poor response (ST segment drops or flat — exercise intolerance)"
    ]
)

# Replaced "Major vessels affected" with a clinically relevant symptom
persistent_cough = st.selectbox(
    "Have you had a persistent cough lasting more than one week?",
    ["No", "Yes"]
)

# Replaced "Oldpeak (ST depression)" with understandable wording
fatigue_after_activity = st.slider(
    "How fatigued or breathless do you feel after light physical activity? (0 = none, 10 = extreme)",
    0, 10, 0
)

# =========================
# PREDICTION
# =========================
st.markdown("## 📊 Result")

if st.button("Run Assessment"):

    risk = 0.0
    breakdown = []

    # --- BASE RISK BY AGE (evidence-based thresholds) ---
    # Framingham Heart Study-informed age bands
    if age < 35:
        age_risk = 0.0
        breakdown.append(("Age < 35", "+0%"))
    elif age < 45:
        age_risk = 0.05
        breakdown.append(("Age 35–44", "+5%"))
    elif age < 55:
        age_risk = 0.10
        breakdown.append(("Age 45–54 (elevated risk group)", "+10%"))
    elif age < 65:
        age_risk = 0.15
        breakdown.append(("Age 55–64", "+15%"))
    elif age < 75:
        age_risk = 0.20
        breakdown.append(("Age 65–74", "+20%"))
    elif age < 80:
        age_risk = 0.23
        breakdown.append(("Age 75–79", "+23%"))
    else:
        age_risk = 0.28
        breakdown.append(("Age ≥ 80 (high-risk age group)", "+28%"))

    risk += age_risk

    # --- SEX (men have higher baseline CVD risk before age 55) ---
    if sex == "Male" and age < 55:
        risk += 0.05
        breakdown.append(("Male under 55 (higher baseline CVD risk)", "+5%"))
    elif sex == "Female" and age >= 55:
        risk += 0.04
        breakdown.append(("Female ≥ 55 (post-menopausal risk increase)", "+4%"))
    else:
        breakdown.append(("Sex-age interaction", "+0%"))

    # --- DIABETES ---
    # AHA: diabetes roughly doubles CVD risk
    if diabetes == "Yes":
        risk += 0.12
        breakdown.append(("Diabetes (doubles CVD risk)", "+12%"))
    else:
        breakdown.append(("No diabetes", "+0%"))

    # --- BLOOD PRESSURE ---
    # JNC 8 / ACC/AHA 2017 guidelines thresholds
    if trestbps >= 160:
        risk += 0.10
        breakdown.append(("Stage 2 hypertension (BP ≥ 160)", "+10%"))
    elif trestbps >= 140:
        risk += 0.07
        breakdown.append(("Stage 1–2 hypertension (BP 140–159)", "+7%"))
    elif trestbps >= 128:
        risk += 0.03
        breakdown.append(("Elevated blood pressure (BP 128–139)", "+3%"))
    else:
        breakdown.append(("Blood pressure normal (< 128)", "+0%"))

    # --- CHEST PAIN LEVEL ---
    # Chest pain is a major cardiac symptom
    if chest_pain_level == 0:
        breakdown.append(("No chest pain", "+0%"))
    elif chest_pain_level <= 3:
        risk += 0.05
        breakdown.append(("Mild chest pain", "+5%"))
    elif chest_pain_level <= 6:
        risk += 0.10
        breakdown.append(("Moderate chest pain", "+10%"))
    else:
        risk += 0.16
        breakdown.append(("Severe chest pain", "+16%"))

    # --- CHEST PAIN ON EXERTION (exercise-induced angina) ---
    if exang == "Yes":
        risk += 0.08
        breakdown.append(("Chest pain/tightness during activity (exercise angina)", "+8%"))
    else:
        breakdown.append(("No exercise-induced chest pain", "+0%"))

    # --- CHOLESTEROL ---
    # ACC/AHA: >200 borderline high, >240 high
    if chol >= 280:
        risk += 0.12
        breakdown.append(("Very high cholesterol (≥ 280 mg/dL)", "+12%"))
    elif chol >= 240:
        risk += 0.08
        breakdown.append(("High cholesterol (240–279 mg/dL)", "+8%"))
    elif chol >= 200:
        risk += 0.04
        breakdown.append(("Borderline high cholesterol (200–239 mg/dL)", "+4%"))
    else:
        breakdown.append(("Cholesterol in healthy range (< 200)", "+0%"))

    # --- ECG RESULT ---
    if "Significant" in restecg:
        risk += 0.10
        breakdown.append(("Significant ECG abnormality (LVH pattern)", "+10%"))
    elif "Mild" in restecg:
        risk += 0.04
        breakdown.append(("Mild ECG abnormality", "+4%"))
    else:
        breakdown.append(("Normal ECG", "+0%"))

    # --- MAX HEART RATE ---
    # Low chronotropic response = poor heart fitness
    expected_hr = 220 - age
    hr_ratio = thalach / expected_hr

    if thalach > 160:
        # Very high HR → could indicate poor fitness or arrhythmia
        risk += 0.03
        breakdown.append(("Very high max heart rate (> 160 bpm)", "+3%"))
    elif hr_ratio < 0.62:
        risk += 0.10
        breakdown.append(("Very low max heart rate for age (chronotropic incompetence)", "+10%"))
    elif hr_ratio < 0.75:
        risk += 0.06
        breakdown.append(("Below-expected max heart rate for age", "+6%"))
    else:
        # Good chronotropic response = protective
        risk -= 0.02
        breakdown.append(("Good max heart rate for age (protective)", "−2%"))

    # --- EXERCISE HEART RESPONSE (ST slope) ---
    if "Poor response" in slope:
        risk += 0.09
        breakdown.append(("Poor exercise heart response (ST depression)", "+9%"))
    elif "Slight abnormal" in slope:
        risk += 0.045
        breakdown.append(("Slight abnormal exercise response", "+4.5%"))
    else:
        risk -= 0.02
        breakdown.append(("Normal exercise heart response (protective)", "−2%"))

    # --- PERSISTENT COUGH (can indicate heart failure / fluid backup) ---
    if persistent_cough == "Yes":
        risk += 0.05
        breakdown.append(("Persistent cough > 1 week (possible cardiac symptom)", "+5%"))
    else:
        breakdown.append(("No persistent cough", "+0%"))

    # --- FATIGUE / BREATHLESSNESS AFTER LIGHT ACTIVITY ---
    if fatigue_after_activity >= 8:
        risk += 0.10
        breakdown.append(("Severe fatigue/breathlessness on light activity", "+10%"))
    elif fatigue_after_activity >= 5:
        risk += 0.06
        breakdown.append(("Moderate fatigue/breathlessness on light activity", "+6%"))
    elif fatigue_after_activity >= 2:
        risk += 0.03
        breakdown.append(("Mild fatigue/breathlessness on light activity", "+3%"))
    else:
        breakdown.append(("No notable fatigue on light activity", "+0%"))

    # --- CLAMP FINAL RISK ---
    final_prob = max(0.0, min(risk, 1.0))

    # =========================
    # OUTPUT
    # =========================
    st.markdown("### Assessment Result")

    if final_prob < 0.15:
        st.success(f"🟢 Low Risk — {final_prob*100:.1f}%")
        st.write("Your cardiovascular risk appears low based on the information provided.")
    elif final_prob < 0.40:
        st.warning(f"🟡 Moderate Risk — {final_prob*100:.1f}%")
        st.write("Some risk factors are present. Consider a clinical review.")
    elif final_prob < 0.65:
        st.warning(f"🟠 High Risk — {final_prob*100:.1f}%")
        st.write("Multiple significant risk factors detected. Medical evaluation recommended.")
    else:
        st.error(f"🔴 Very High Risk — {final_prob*100:.1f}%")
        st.write("Serious risk factors present. Please consult a cardiologist promptly.")

    # --- BREAKDOWN TABLE ---
    st.markdown("### 📋 Risk Factor Breakdown")
    breakdown_df = pd.DataFrame(breakdown, columns=["Risk Factor", "Contribution"])
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("⚠️ Educational Cardiovascular Risk Tool — Not a substitute for professional medical advice.")