# ml/verify_model.py
import joblib
import pandas as pd

# 1. Load the file
MODEL_PATH = "models/fraud_model.pkl"

try:
    print(f"Loading {MODEL_PATH}...")
    artifact = joblib.load(MODEL_PATH)
    
    # Check if we have the expected dictionary keys
    if "model" in artifact and "preprocessor" in artifact:
        print("Structure check passed: Found 'model' and 'preprocessor'.")
    else:
        print("Structure check failed: Missing keys.")
        exit()

    # 2. Extract components
    model = artifact["model"]
    preprocessor = artifact["preprocessor"]

    # 3. Create dummy data (must match your training columns)
    # Using 'amount_cents', 'transaction_country', 'channel', 'entry_mode'
    dummy_data = pd.DataFrame([{
        "amount_cents": 5000, 
        "transaction_country": "US",
        "channel": "ONLINE",
        "entry_mode": "CHIP"
    }])

    # 4. Run a test prediction
    print("Attempting prediction...")
    processed_data = preprocessor.transform(dummy_data)
    prediction = model.predict(processed_data)

    print(f"Prediction successful! Result: {prediction[0]} (0=Legit, 1=Fraud)")

except Exception as e:
    print(f"Error: {e}")