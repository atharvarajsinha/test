from pathlib import Path
import joblib
import numpy as np

FEATURES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

MODEL_PATH = Path(__file__).resolve().parent.parent / 'ml_model' / 'best_model.pkl'
_model_bundle = None


class ValidationError(Exception):
    """Raised for invalid user input."""


def load_model_bundle():
    global _model_bundle
    if _model_bundle is None:
        _model_bundle = joblib.load(MODEL_PATH)
    return _model_bundle


def validate_and_build_features(payload: dict) -> np.ndarray:
    values = []
    for feature in FEATURES:
        if feature not in payload:
            raise ValidationError(f"Missing field: {feature}")
        try:
            val = float(payload[feature])
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid numeric value for {feature}")
        if feature != 'DiabetesPedigreeFunction' and val < 0:
            raise ValidationError(f"{feature} cannot be negative")
        values.append(val)
    return np.array(values, dtype=float).reshape(1, -1)


def predict_diabetes(feature_array: np.ndarray, threshold: float = 0.5) -> dict:
    bundle = load_model_bundle()
    scaler = bundle['scaler']
    model = bundle['model']

    scaled = scaler.transform(feature_array)
    probability = float(model.predict_proba(scaled)[0][1])
    pred_label = 'Diabetic' if probability >= threshold else 'Not Diabetic'

    return {
        'prediction': pred_label,
        'probability': round(probability*100, 2),
        'threshold': threshold*100,
    }
