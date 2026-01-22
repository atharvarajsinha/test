from pathlib import Path
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.preprocessing import RobustScaler

warnings.filterwarnings('ignore')

DATA_URL = 'data/diabetes.csv'
TARGET = 'Outcome'
FEATURES_WITH_INVALID_ZEROS = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
MODEL_DIR = Path('ml_model')
MODEL_PATH = MODEL_DIR / 'best_model.pkl'


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_URL)


def preprocess_data(df: pd.DataFrame):
    df = df.copy()
    df[FEATURES_WITH_INVALID_ZEROS] = df[FEATURES_WITH_INVALID_ZEROS].replace(0, np.nan)

    # outcome-aware median imputation
    for col in FEATURES_WITH_INVALID_ZEROS:
        med0 = df.loc[(df[TARGET] == 0) & (df[col].notna()), col].median()
        med1 = df.loc[(df[TARGET] == 1) & (df[col].notna()), col].median()
        df.loc[(df[TARGET] == 0) & (df[col].isna()), col] = med0
        df.loc[(df[TARGET] == 1) & (df[col].isna()), col] = med1

    # cap insulin outliers
    q1, q3 = df['Insulin'].quantile([0.25, 0.75])
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    df['Insulin'] = np.where(df['Insulin'] > upper, upper, df['Insulin'])

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X, y


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_prob),
    }


def train_and_select_best():
    df = load_data()
    X_train, X_test, y_train, y_test, scaler, X_full, y_full = preprocess_data(df)

    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    grids = {
        'Logistic Regression': (
            LogisticRegression(max_iter=2000, random_state=42),
            {'C': [0.1, 1, 10], 'solver': ['liblinear', 'lbfgs']}
        ),
        'Random Forest': (
            RandomForestClassifier(random_state=42),
            {'n_estimators': [300, 500], 'max_depth': [8, None], 'max_features': [3, 5, 7], 'min_samples_split': [2, 5]}
        ),
        'Gradient Boosting': (
            GradientBoostingClassifier(random_state=42),
            {'learning_rate': [0.01, 0.1], 'n_estimators': [100, 300], 'max_depth': [3, 5], 'subsample': [0.9, 1.0]}
        ),
    }

    results, trained = [], {}
    X_cv = scaler.transform(X_full)

    for name, (base_model, params) in grids.items():
        search = GridSearchCV(base_model, params, scoring='accuracy', cv=cv, n_jobs=-1)
        search.fit(X_train, y_train)
        best_model = search.best_estimator_
        trained[name] = best_model

        cv_acc = cross_val_score(best_model, X_cv, y_full, cv=cv, scoring='accuracy', n_jobs=-1).mean()
        metrics = evaluate_model(best_model, X_test, y_test)
        metrics.update({'model': name, 'cv_accuracy': cv_acc})
        results.append(metrics)

    comparison = pd.DataFrame(results).sort_values(by=['roc_auc', 'f1_score'], ascending=False)
    best_name = comparison.iloc[0]['model']
    best_model = trained[best_name]

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({'model': best_model, 'scaler': scaler}, MODEL_PATH)

    print('\nModel comparison:')
    print(comparison[['model', 'cv_accuracy', 'accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']].to_string(index=False))
    print(f'\nBest model: {best_name}')
    print(f'Saved model bundle to: {MODEL_PATH.resolve()}')


if __name__ == '__main__':
    train_and_select_best()
