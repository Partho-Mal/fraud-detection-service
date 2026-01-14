# app/services/inference.py
import time
import numpy as np
import pandas as pd

from app.core.config import get_settings

def run_inference(transaction, preprocessor, session):
    settings = get_settings()
    start = time.time()

    df = pd.DataFrame([transaction.dict()])
    processed = preprocessor.transform(df)

    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: processed.astype(np.float32)})

    fraud_prob = float(outputs[1][0][1])
    is_fraud = fraud_prob > settings.FRAUD_THRESHOLD

    latency_ms = (time.time() - start) * 1000

    return is_fraud, fraud_prob, latency_ms
