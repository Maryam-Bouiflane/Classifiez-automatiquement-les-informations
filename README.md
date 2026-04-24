---
title: P4 Classification App
emoji: 🌍
colorFrom: pink
colorTo: pink
sdk: gradio
sdk_version: 6.11.0
app_file: app.py
pinned: false
---

# Employee Churn Prediction App
### 1) Context
The digital services company TechNova Partners is experiencing unusually high employee turnover. The HR department wants to identify the reasons behind these resignations, as they are costly for the company (recruitment costs, training, etc.).

### 2) Goal
This app predicts whether an employee is likely to leave the company based on HR data.

---

## 🚀 Features

- Select an employee ID
- Predict churn probability
- Get risk classification (low / high)

---

## 🧠 Model

- Logistic Regression (scikit-learn)
- Feature preprocessing (StandardScaler + OneHotEncoder)
- Optimized decision threshold (F1-score)

---

## 📊 Inputs

- Age, salary, department, satisfaction scores, etc.
- HR dataset merged from internal sources

---

## 📤 Output

- Probability of leaving
- Binary prediction (churn / no churn)

---

## 🛠 Tech Stack

- Python
- scikit-learn
- pandas
- Gradio
- Hugging Face Spaces

---

## 📦 Deployment

This app is automatically deployed via GitHub Actions CI/CD pipeline.


