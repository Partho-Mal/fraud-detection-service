import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import os

# 1. Load your training data structure
# (We need to know what columns to expect)
try:
    df = pd.read_csv('credit_card_transactions.csv')
except FileNotFoundError:
    print("❌ Error: credit_card_transactions.csv not found.")
    exit(1)

# 2. Define Features matches your Schema
cat_features = ['transaction_country', 'channel', 'entry_mode']
num_features = ['amount_cents']

print(f"Training preprocessor on {len(df)} records...")

# 3. Create the Transformer
# handle_unknown='ignore' is CRITICAL for production (stops crashes on new countries)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
    ]
)

# 4. Fit & Save
preprocessor.fit(df[num_features + cat_features])

output_path = 'models/preprocessor.pkl'
joblib.dump(preprocessor, output_path)
print(f"✅ Preprocessor saved to {output_path}")
print("Test transform shape:", preprocessor.transform(df.iloc[:1][num_features + cat_features]).shape)