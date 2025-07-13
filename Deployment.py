# -*- coding: utf-8 -*-
"""
Final Diabetes Prediction Web App----female
@author: Astroshi
"""

import pickle
import numpy as np
import streamlit as st
from fpdf import FPDF

from streamlit_lottie import st_lottie
import json
from datetime import datetime
import plotly.graph_objs as go

# Load Lottie Animation
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Lottie animation path
lottie_animation = load_lottiefile("Lottie\wdy.json")

# Load model and scaler
try:
    loaded_model = pickle.load(open("trained_model.sav", 'rb'))
    scaler = pickle.load(open("scaler.sav", 'rb'))
except FileNotFoundError:
    st.error("Model or scaler not found.")
    st.stop()

# Diabetes prediction function
def diabetes_prediction(input_data):
    try:
        input_array = np.asarray([float(i) for i in input_data]).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        prediction = loaded_model.predict(input_scaled)
        return prediction[0], input_array[0]
    except:
        return "invalid", input_data

# PDF report generator
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Diabetes Prediction Report", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def export_to_pdf(name, input_data, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Patient Name: {name}", ln=True)
    pdf.cell(0, 10, f"Date: {timestamp}", ln=True)
    pdf.ln(5)

    labels = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
              "Insulin", "BMI", "DPF", "Age"]
    for label, value in zip(labels, input_data):
        pdf.cell(0, 10, f"{label}: {value}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Result: {'Diabetic' if result == 1 else 'Not Diabetic'}", ln=True)

    filename = "diabetes_report.pdf"
    pdf.output(filename)
    return filename

# Main UI
def main():
    st.set_page_config("Diabetes Prediction", "🧬", layout="centered")

    # Theme-aware custom styling
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            font-size: 17px !important;
            color: var(--text-color) !important;
        }
        .stButton>button {
            background-color: #2e7d32 !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.6em 1.2em !important;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #43a047 !important;
        }
        .block-container {
            background-color: var(--background-color) !important;
            padding: 2em 3em !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Title: Italic and Centered
    st.markdown("""
    <h1 style='
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 800;
        font-size: 52px;
        letter-spacing: 1px;
        color: #2e7d32;
        margin-bottom: 0.4em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.15);
    '>CheckHerSugar</h1>
""", unsafe_allow_html=True)


    st_lottie(lottie_animation, speed=1.2, height=200)
    st.markdown("Fill out patient details below:")

    # Input section
    patient_name = st.text_input("Patient Name")
    inputs = [
        st.text_input("Number of Pregnancies"),
        st.text_input("Glucose Level"),
        st.text_input("Blood Pressure"),
        st.text_input("Skin Thickness"),
        st.text_input("Insulin Level"),
        st.text_input("BMI"),
        st.text_input("Diabetes Pedigree Function"),
        st.text_input("Age")
    ]

    # Prediction trigger
    if st.button("Get Prediction"):
        prediction, input_array = diabetes_prediction(inputs)

        if prediction == "invalid":
            st.warning("Please enter only numeric values.")
            return

        status = "✅ Not Diabetic" if prediction == 0 else "⚠️ Diabetic"
        st.metric("Result", status)
        st.toast("Prediction complete!", icon="✅" if prediction == 0 else "⚠️")

        # Bar Chart: Health Metrics
        st.subheader("📊 Health Metrics Overview")
        labels = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
                  "Insulin", "BMI", "DPF", "Age"]
        values = [float(v) for v in input_array]

        bar_fig = go.Figure([go.Bar(x=labels, y=values, marker_color="#66bb6a" if prediction == 0 else "#ef5350")])
        bar_fig.update_layout(title="Patient Health Metrics", xaxis_title="Metric", yaxis_title="Value")
        st.plotly_chart(bar_fig)

        # Pie Chart: Weight Distribution (Dummy values)
        weights = [0.1, 0.25, 0.15, 0.05, 0.05, 0.2, 0.1, 0.1]
        pie_fig = go.Figure(data=[go.Pie(labels=labels, values=weights)])
        pie_fig.update_layout(title="Estimated Contribution to Diabetes Risk")
        st.plotly_chart(pie_fig)

        # PDF Export
        report_path = export_to_pdf(patient_name, values, prediction)
        with open(report_path, "rb") as f:
            st.download_button("📄 Download Report as PDF", f, file_name="diabetes_report.pdf")

if __name__ == '__main__':
    main()
