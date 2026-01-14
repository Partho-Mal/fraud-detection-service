# ml/evaluate.py
from sklearn.metrics import recall_score, precision_score, confusion_matrix


def evaluate(model, X_test, y_test, label: str):
    y_pred = model.predict(X_test)

    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    print(f"\n{label}")
    print("Recall:", round(recall, 4))
    print("Precision:", round(precision, 4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return recall, precision
