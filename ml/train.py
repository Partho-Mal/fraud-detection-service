# ml/train.py
import joblib
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

from preprocess import load_and_preprocess
from evaluate import evaluate


DATA_PATH = "ml/datasets/credit_card_transactions.csv"
MODEL_PATH = "models/fraud_model.pkl"


def train():
    X_train, X_test, y_train, y_test, preprocessor = load_and_preprocess(
        DATA_PATH
    )

    print("Training baseline model")
    baseline = XGBClassifier(
        eval_metric="logloss",
        random_state=42,
    )
    baseline.fit(X_train, y_train)
    evaluate(baseline, X_test, y_test, "Baseline")

    print("Applying SMOTE")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    print("Training SMOTE model")
    smote_model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
    )
    smote_model.fit(X_resampled, y_resampled)
    evaluate(smote_model, X_test, y_test, "SMOTE")

    joblib.dump(
        {
            "model": smote_model,
            "preprocessor": preprocessor,
        },
        MODEL_PATH,
    )

    print("Model saved successfully")


if __name__ == "__main__":
    train()
