# 🚑 AI Emergency Patient Priority Prediction System

An AI-powered machine learning application that predicts whether a patient requires **High Priority** or **Low Priority** emergency care based on vital signs and symptoms. This system helps support faster triage decisions in emergency departments.

---

## 📌 Project Overview

Emergency rooms often receive multiple patients simultaneously. This project uses a **Logistic Regression** model to classify patients into emergency priority levels using their medical information.

The application provides instant predictions through an interactive Streamlit web interface.

---

## ✨ Features

- Predicts patient emergency priority
- User-friendly Streamlit web application
- Machine Learning powered predictions
- Data preprocessing with Label Encoding and Standard Scaling
- Fast and accurate classification
- Easy to use interface

---

## 🛠️ Tech Stack

- Python
- Scikit-learn
- Pandas
- NumPy
- Streamlit
- Joblib

---

## 📂 Project Structure

```
Emergency-Patient-Priority-Prediction/
│
├── app.py
├── improved_emergency_triage_dataset.csv
├── logistic_regression_model.pkl
├── scaler.pkl
├── label_encoder.pkl
├── feature_columns.pkl
├── requirements.txt
└── README.md
```

---

## 📊 Machine Learning Workflow

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Label Encoding
6. Feature Scaling
7. Model Training
8. Model Evaluation
9. Model Saving
10. Streamlit Deployment

---

## 📥 Input Features

- Age
- Heart Rate
- Blood Pressure
- Oxygen Saturation (SpO₂)
- Body Temperature
- Respiratory Rate
- Chest Pain
- Difficulty Breathing
- Level of Consciousness
- Pain Severity
- Previous Medical History
- Arrival Mode

---

## 🎯 Output

The model predicts one of the following:

- 🟢 Low Priority
- 🔴 High Priority

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/AbhayDw/Emergency-Patient-Priority-Prediction.git
```

Move into the project

```bash
cd Emergency-Patient-Priority-Prediction
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📈 Model Used

- Logistic Regression

---

## 📷 Application Preview

> Add screenshots of your Streamlit application here.

---

## 🔮 Future Improvements

- Multi-class emergency severity prediction
- Integration with hospital databases
- Deep Learning models
- Explainable AI (SHAP/LIME)
- Cloud deployment
- Real-time patient monitoring

---

## 👨‍💻 Author

**Abhay Dwivedi**

- GitHub: https://github.com/AbhayDw
- LinkedIn: https://www.linkedin.com/in/abhay-dwivedi-6a8aa4279/

---

## ⭐ If you found this project useful, please consider giving it a Star!
