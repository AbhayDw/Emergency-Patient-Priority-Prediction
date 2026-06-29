# 🚑 AI Emergency Patient Priority Prediction System

<p align="center">
  <img src="assets/01_home_page.png" alt="Project Banner" width="900">
</p>

<p align="center">
An AI-powered Machine Learning application that predicts whether a patient requires <b>High Priority</b> or <b>Low Priority</b> emergency care based on vital signs and symptoms.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📑 Table of Contents

- Project Overview
- Features
- Tech Stack
- Dataset
- Machine Learning Workflow
- Project Structure
- Application Screenshots
- Exploratory Data Analysis
- Model Performance
- Installation
- Usage
- Future Improvements
- Author

---

# 📌 Project Overview

Emergency rooms receive multiple patients simultaneously, making quick and accurate triage essential.

This project uses **Logistic Regression** to classify patients into:

- 🔴 High Priority
- 🟢 Low Priority

based on medical information such as:

- Heart Rate
- Blood Pressure
- Oxygen Saturation
- Respiratory Rate
- Chest Pain
- Difficulty Breathing
- Pain Severity
- Previous Medical History
- Arrival Mode
- Age
- Body Temperature

---

# ✨ Features

- Machine Learning Prediction
- Interactive Streamlit Web App
- Clean User Interface
- Instant Prediction
- Logistic Regression Model
- Feature Scaling
- Label Encoding
- High Accuracy
- Easy Deployment

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| ML | Scikit-Learn |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Deployment | Streamlit |
| Model Saving | Joblib |

---

# 📊 Dataset

The dataset contains patient medical records including:

- Age
- Heart Rate
- Blood Pressure
- Oxygen Saturation
- Body Temperature
- Respiratory Rate
- Chest Pain
- Difficulty Breathing
- Consciousness Level
- Pain Severity
- Previous Medical History
- Arrival Mode

Target Variable

```
Emergency Priority
```

- 0 → Low Priority
- 1 → High Priority

---

# 🤖 Machine Learning Workflow

```
Dataset
     │
     ▼
Data Cleaning
     │
     ▼
EDA
     │
     ▼
Feature Engineering
     │
     ▼
Label Encoding
     │
     ▼
Feature Scaling
     │
     ▼
Train Test Split
     │
     ▼
Logistic Regression
     │
     ▼
Model Evaluation
     │
     ▼
Streamlit Deployment
```

---

# 📂 Project Structure

```
Emergency-Patient-Priority-Prediction/

│
├── assets/
│   ├── 01_home_page.png
│   ├── 02_input_form.png
│   ├── 03_prediction_high.png
│   ├── 04_prediction_low.png
│   ├── 05_dataset.png
│   ├── 06_heatmap.png
│   ├── 07_class_distribution.png
│   ├── 08_model_metrics.png
│   └── 09_confusion_matrix.png
│
├── app.py
├── improved_emergency_triage_dataset.csv
├── logistic_regression_model.pkl
├── scaler.pkl
├── feature_columns.pkl
├── label_encoder.pkl
├── requirements.txt
└── README.md
```

---

# 🖥️ Application Screenshots

## 🏠 Home Page

![](assets/01_home_page.png)

---

## 📝 Patient Information Form

![](assets/02_input_form.png)

---

## 🔴 High Priority Prediction

![](assets/03_prediction_high.png)

---

## 🟢 Low Priority Prediction

![](assets/04_prediction_low.png)

---

# 📊 Exploratory Data Analysis

## Dataset Overview

![](assets/05_dataset.png)

---

## Correlation Heatmap

![](assets/06_heatmap.png)

---

## Class Distribution

![](assets/07_class_distribution.png)

---

# 📈 Model Performance

## Evaluation Metrics

| Metric | Score |
|---------|-------|
| Accuracy | XX% |
| Precision | XX |
| Recall | XX |
| F1 Score | XX |

---

## Confusion Matrix

![](assets/09_confusion_matrix.png)

---

# 🚀 Installation

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

# 💻 Usage

1. Enter the patient's medical information.
2. Click **Predict**.
3. View the predicted emergency priority.

---

# 🔮 Future Improvements

- Deep Learning Models
- Explainable AI (SHAP/LIME)
- Hospital Database Integration
- Real-Time Patient Monitoring
- Multi-Class Priority Prediction
- Cloud Deployment

---

# 👨‍💻 Author

## Abhay Dwivedi

**B.Tech CSE (Cyber Security)**

### Connect with me

- GitHub: https://github.com/AbhayDw
- LinkedIn:  https://www.linkedin.com/in/abhay-dwivedi-6a8aa4279/

---

# ⭐ Support

If you found this project useful,

⭐ **Please give this repository a Star.**

It motivates me to build more Machine Learning projects.

