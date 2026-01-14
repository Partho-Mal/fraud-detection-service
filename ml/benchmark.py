# ml/benchmark.py
import joblib
import time
import pandas as pd
import onnxruntime as ort
import numpy as np

# Load Data
_, preprocessor = joblib.load("models/fraud_model.pkl").values()
dummy_input = pd.DataFrame([{"amount_cents": 5000, "transaction_country": "US", "channel": "ONLINE", "entry_mode": "APP"}])
input_data = preprocessor.transform(dummy_input).astype(np.float32)

def benchmark_pickle(n=1000):
    model = joblib.load("models/fraud_model.pkl")["model"]
    start = time.time()
    for _ in range(n):
        model.predict_proba(input_data)
    print(f"Pickle (Sklearn): {(time.time() - start)/n*1000:.3f} ms/request")

def benchmark_onnx(n=1000):
    sess = ort.InferenceSession("models/fraud_model.onnx")
    input_name = sess.get_inputs()[0].name
    start = time.time()
    for _ in range(n):
        sess.run(None, {input_name: input_data})
    print(f"ONNX (Runtime):   {(time.time() - start)/n*1000:.3f} ms/request")

if __name__ == "__main__":
    print("Benchmarking 1,000 requests...")
    benchmark_pickle()
    benchmark_onnx()