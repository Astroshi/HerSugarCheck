# HerSugarCheck

**HerSugarCheck** is a web application that predicts the likelihood of diabetes in pregnant females based on health input data. Built with a beautifully crafted UI using **Streamlit**, the app leverages a trained **Support Vector Machine (SVM)** model that achieves an accuracy greater than **75%** on a real-world dataset.

## Features

- Trained **SVM classifier** on a dataset of pregnant females with diabetes risk factors.
- Clean UI with real-time predictions and result summaries.
- Achieved **>75% accuracy** on test data.
- Fully deployed with **Streamlit Cloud** for instant web access.
- Includes animated visual elements (Lottie), prediction charts, and detailed feedback.

## Model Overview

- Algorithm: Support Vector Machine (SVM)
- Dataset: Medical records of pregnant females (features like pregnancies, glucose, BMI, etc.)
- Preprocessing: Normalization, missing value handling, and feature selection
- Evaluation Metric: Accuracy score (>75%)

## Screenshots

You can see screenshots of the app in the `HerSugarcheck UI` folder.  
The deployed web app link is provided in this repository.

```python
# Example usage in app
st.text_input("Enter glucose level:")
st.selectbox("Select BMI category:")


## Author

Astroshi
