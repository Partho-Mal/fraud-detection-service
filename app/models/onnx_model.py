# app/models/onnx_model.py
import joblib
import onnxruntime as ort

def load_onnx_artifacts():
    artifacts = joblib.load("models/fraud_model.pkl")
    session = ort.InferenceSession("models/fraud_model.onnx")

    return {
        "preprocessor": artifacts["preprocessor"],
        "session": session,
    }