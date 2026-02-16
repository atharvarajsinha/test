# diabeto — Diabetes Detection System

A full-stack **Machine Learning + Django** web application that predicts whether a patient is diabetic based on medical diagnostic features.

---

## Introduction

Diabetes is a chronic disease affecting millions worldwide. Early detection helps:
- Prevent severe complications (heart disease, kidney failure, vision loss)
- Enable timely treatment and lifestyle changes

Note: This project builds a **machine learning prediction system** and used via a **Django web app + REST API**.

---

## Dataset Information

- **Dataset**: Pima Indians Diabetes Dataset  
- **Source**: National Institute of Diabetes and Digestive and Kidney Diseases  
- **Samples**: 768  
- **Features**: 8 input features + 1 target  

### Features in Dataset

| Feature | Description |
|--------|------------|
| Pregnancies | Number of times pregnant |
| Glucose | Plasma glucose concentration |
| BloodPressure | Diastolic blood pressure |
| SkinThickness | Triceps skin fold thickness |
| Insulin | Serum insulin |
| BMI | Body mass index |
| DiabetesPedigreeFunction | Genetic risk score |
| Age | Age |
| Outcome | Target (0 = No Diabetes, 1 = Diabetes) |

---

## Problem Statement

Build a machine learning model that:
- Predicts diabetes accurately
- Handles missing/invalid data
- Compares multiple models
- Selects the best-performing model

---

## ML Pipeline

### 🔹 Data Preprocessing
- Replaced invalid zero values with `NaN`
- Applied **target-based median imputation**
- Handled outliers using **IQR (Insulin feature)**

### 🔹 Feature Scaling
- Used **RobustScaler** (robust to outliers)

### 🔹 Models Used (3 Only)
- Logistic Regression (baseline)
- Random Forest (bagging)
- Gradient Boosting (boosting)

---

## Model Training

- **Stratified K-Fold Cross Validation (10 folds)**
- Hyperparameter tuning using **GridSearchCV**
- Evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC-AUC (primary metric)

---

## Results

| Model | ROC-AUC | Accuracy |
|------|--------|---------|
| Gradient Boosting | ~0.95 | ~86% |
| Random Forest | ~0.94 | ~86% |
| Logistic Regression | ~0.83 | ~75% |

Imp: **Best Model: Gradient Boosting**

---

## Project Structure

```

diabeto/
│
├── diabeto/          # Django project config
├── core/             # App (views, APIs, ML utilities)
├── ml_model/         # Saved model (best_model.pkl)
├── notebooks/        # EDA + training notebook
├── data/             # Dataset
├── train.py          # Training pipeline
├── manage.py
└── requirements.txt

````

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Train model

```bash
python train.py
```

### 3. Run Django server

```bash
python manage.py runserver
```

### 4. Open UI

```
http://127.0.0.1:8000/
```

---

## API Usage

### Endpoint

```
POST /predict-api/
```

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/predict-api/ \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 2,
    "Glucose": 140,
    "BloodPressure": 70,
    "SkinThickness": 20,
    "Insulin": 85,
    "BMI": 30.5,
    "DiabetesPedigreeFunction": 0.45,
    "Age": 45
  }'
```

### Example Response

```json
{
  "prediction": "Diabetic",
  "probability": 0.87
}
```

---

## Key Challenges Solved

* Handling invalid medical data (0 ≠ valid value)
* Avoiding data leakage
* Choosing correct metric (ROC-AUC over accuracy)
* Balancing performance and interpretability

---

## Tech Stack

* Backend: Django
* Machine Learning: Scikit-learn
* Data Processing: Pandas, NumPy
* Visualization: Matplotlib, Seaborn
* Model Persistence: Joblib

---

## Conclusion

This project demonstrates a complete ML pipeline.

Gradient Boosting achieved the best performance (~95% ROC-AUC), making it the most reliable model for diabetes prediction.

---
~ Atharva Raj Sinha