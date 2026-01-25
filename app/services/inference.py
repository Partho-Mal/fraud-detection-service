# app/services/inference.py
import os
import time
import joblib
import random
import logging
import numpy as np
import pandas as pd
import onnxruntime as ort
from typing import TYPE_CHECKING, Any, Tuple

# 1. CIRCULAR IMPORT FIX
if TYPE_CHECKING:
    from app.schemas.transaction import Transaction

# Setup Logger
logger = logging.getLogger("fraud_engine")

# 2. Load Configurations
LOG_SAMPLING_RATE = float(os.getenv("LOG_SAMPLING_RATE", "0.01")) 
FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "0.9"))

# 3. Load Resources Globally
preprocessor = None
ort_session = None

try:
    if os.path.exists("models/preprocessor.pkl"):
        loaded_obj = joblib.load("models/preprocessor.pkl")
        # SAFETY CHECK: Only use if it actually has a transform method
        if hasattr(loaded_obj, "transform"):
            preprocessor = loaded_obj
        else:
            logger.warning(f"⚠️ 'preprocessor.pkl' is a {type(loaded_obj)}, not a Transformer. Ignoring it.")
    else:
        logger.warning("⚠️ No preprocessor found. Using raw values.")

    ort_session = ort.InferenceSession("models/fraud_model.onnx")
    logger.info("✅ ONNX Model loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load models: {e}")

def run_inference(transaction: Any, *args, **kwargs) -> Tuple[bool, float, float]: 
    start = time.time()
    
    try:
        # 4. Data Preparation
        if hasattr(transaction, "model_dump"):
            transaction_dict = transaction.model_dump()
        else:
            transaction_dict = dict(transaction)
            
        df = pd.DataFrame([transaction_dict])
        
        # 5. Preprocessing (With Fallback)
        if preprocessor:
            try:
                processed_data = preprocessor.transform(df)
            except Exception as e:
                logger.error(f"Preprocessing failed: {e}")
                processed_data = df.values # Fallback to raw data
        else:
            processed_data = df.values

        # 6. ONNX Inference
        fraud_prob = 0.0
        if ort_session:
            input_name = ort_session.get_inputs()[0].name
            # ONNX requires float32
            inputs = {input_name: processed_data.astype(np.float32)}
            outputs = ort_session.run(None, inputs)
            
            try:
                # Try accessing probability (usually index 1)
                fraud_prob = float(outputs[1][0][1])
            except:
                # Fallback for single-output models
                fraud_prob = float(outputs[0][0])
        
        is_fraud = fraud_prob > FRAUD_THRESHOLD
        
        latency_ms = (time.time() - start) * 1000

        # 7. LOG SAMPLING
        if is_fraud or (random.random() < LOG_SAMPLING_RATE):
            # FAANG Standard: Log a DICTIONARY, not a string.
            # Log aggregation tools (Splunk/Datadog) parse this automatically.
            logger.info({
                "event": "inference",
                "amount": transaction_dict.get('amount_cents'),
                "prob": round(fraud_prob, 4),
                "decision": is_fraud,
                "latency_ms": round(latency_ms, 2),
                "version": "v1.2.0"
            })
        # if is_fraud or (random.random() < LOG_SAMPLING_RATE):
        #     logger.info(
        #         f"SHADOW_LOG amount={transaction_dict.get('amount_cents')} "
        #         f"prob={fraud_prob:.4f} "
        #         f"decision={is_fraud} "
        #         f"latency={latency_ms:.2f}ms"
        #     )
        
        # 8. RETURN TUPLE (Success Path)
        return is_fraud, fraud_prob, latency_ms
        
    except Exception as e:
        logger.error(f"Inference Error: {e}")
        # 9. RETURN TUPLE (Error Path) - CRITICAL FIX
        # This prevents the "ValueError: not enough values to unpack"
        return False, 0.0, 0.0
    
# import time
# import numpy as np
# import pandas as pd

# from app.core.config import get_settings

# def run_inference(transaction, preprocessor, session):
#     settings = get_settings()
#     start = time.time()

#     # df = pd.DataFrame([transaction.dict()])

#     df = pd.DataFrame([transaction.model_dump()])
#     processed = preprocessor.transform(df)

#     input_name = session.get_inputs()[0].name
#     outputs = session.run(None, {input_name: processed.astype(np.float32)})

#     fraud_prob = float(outputs[1][0][1])
#     is_fraud = fraud_prob > settings.FRAUD_THRESHOLD

#     latency_ms = (time.time() - start) * 1000

#     return is_fraud, fraud_prob, latency_ms
