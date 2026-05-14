# 🫀 Cardiovascular Risk Prediction System

A clinical decision support tool that estimates cardiovascular risk based on patient-reported symptoms and clinical measurements.

## 🔗 Live Demo
[Click here to open the app](https://cardio-risk-tool.streamlit.app)

## ⚙️ How It Works
The app uses a transparent rule-based scoring system starting from 0%.
Each risk factor adds a clinically-informed percentage to the total score, based on:
- Framingham Heart Study (age-based risk)
- ACC/AHA 2017 guidelines (blood pressure)
- AHA recommendations (diabetes, cholesterol)

## Risk Factors Assessed
- Age
- Sex
- Diabetes
- Blood pressure
- Chest pain (at rest and during exercise)
- Cholesterol
- ECG result
- Max heart rate
- Exercise heart response
- Persistent cough
- Fatigue/breathlessness

## Run Locally

1. Clone the repo:
   git clone https://github.com/YOUR_USERNAME/cardiovascular-risk-app.git
   cd cardiovascular-risk-app

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run heart_risk_app.py

## ⚠️ Disclaimer
This tool is for **educational purposes only**.
It is not a substitute for professional medical advice, diagnosis, or treatment.

## 🛠️ Built With
- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
- Python 3
