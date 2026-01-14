# ml/convert_to_onnx.py
import joblib
import onnxmltools
import pandas as pd
import json
import re
from onnxmltools.convert.common.data_types import FloatTensorType
from onnxmltools.utils import save_model

MODEL_PATH = "models/fraud_model.pkl"
ONNX_PATH = "models/fraud_model.onnx"

# --- 🛠️ Runtime Patch Setup 🛠️ ---
# We intercept the JSON parsing to remove the brackets that confuse the converter
original_json_loads = json.loads

def patched_json_loads(s, **kwargs):
    # Only intervene if we see the XGBoost config with the problematic pattern
    if isinstance(s, str) and "learner_model_param" in s and "base_score" in s:
        # Regex to find "base_score":"[5E-1]" and turn it into "base_score":"5E-1"
        # This removes the brackets that cause the "could not convert string to float" error
        s = re.sub(r'"base_score":"\[(.*?)\]"', r'"base_score":"\1"', s)
    return original_json_loads(s, **kwargs)
# ----------------------------------

def convert():
    print(f"Loading {MODEL_PATH}...")
    artifact = joblib.load(MODEL_PATH)
    xgb_model = artifact["model"]
    preprocessor = artifact["preprocessor"]

    # 1. Determine input shape
    dummy_input = pd.DataFrame([{
        "amount_cents": 0, 
        "transaction_country": "US", 
        "channel": "ONLINE", 
        "entry_mode": "APP"
    }])
    processed_dummy = preprocessor.transform(dummy_input)
    n_features = processed_dummy.shape[1]
    print(f"Detected {n_features} features.")

    # 2. Define input type
    initial_types = [('float_input', FloatTensorType([None, n_features]))]
    
    # 3. Apply Patch & Convert
    print("Converting to ONNX with runtime patch...")
    
    # Install the patch globally
    json.loads = patched_json_loads
    
    try:
        onnx_model = onnxmltools.convert_xgboost(xgb_model, initial_types=initial_types)
        print("Conversion successful.")
    except Exception as e:
        print(f"Conversion failed: {e}")
        return
    finally:
        # Remove the patch immediately after (Safety)
        json.loads = original_json_loads

    # 4. Save
    save_model(onnx_model, ONNX_PATH)
    print(f"Model saved to {ONNX_PATH}")

if __name__ == "__main__":
    convert()