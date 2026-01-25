# RUN:
#   docker compose logs fraud-engine > shadow_mode.log
import re
import sys
import pandas as pd
from typing import List, Dict

# Configuration
LOG_FILE = "shadow_mode.log"
MODEL_THRESHOLD = 0.90  # If model prob > 0.9, it would have blocked the user

def parse_logs(log_path: str) -> List[Dict]:
    data = []
    # Regex to extract key fields from your log format
    # Example: SHADOW_LOG amount=71151 prob=0.9999 primary_decision=True
    pattern = re.compile(r"amount=(\d+) prob=([0-9\.]+) primary_decision=(\w+)")
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "SHADOW_LOG" in line:
                    match = pattern.search(line)
                    if match:
                        data.append({
                            "amount": int(match.group(1)),
                            "model_prob": float(match.group(2)),
                            "legacy_decision": match.group(3) == "True"
                        })
    except FileNotFoundError:
        print(f"Error: Could not find file {log_path}")
        sys.exit(1)
        
    return data

def analyze_performance(data: List[Dict]):
    df = pd.DataFrame(data)
    
    if df.empty:
        print("No shadow logs found.")
        return

    # 1. Determine Model's Decision based on threshold
    df['model_decision'] = df['model_prob'] > MODEL_THRESHOLD

    # 2. Compare Model vs Legacy
    total_tx = len(df)
    legacy_blocks = df['legacy_decision'].sum()
    model_blocks = df['model_decision'].sum()
    
    # 3. The "Business Value" Metrics
    # Case A: Model detected fraud, but Legacy missed it (New Protection)
    newly_detected = df[(df['model_decision'] == True) & (df['legacy_decision'] == False)]
    
    # Case B: Legacy blocked it, but Model thought it was safe (Potential False Negative)
    missed_by_model = df[(df['model_decision'] == False) & (df['legacy_decision'] == True)]

    print("=== SHADOW MODE ANALYSIS ===")
    print(f"Total Transactions Processed: {total_tx}")
    print(f"Legacy System Blocked:      {legacy_blocks}")
    print(f"New Model Would Block:      {model_blocks}")
    print("-" * 30)
    
    print(f"💰 POTENTIAL NEW FRAUD FOUND: {len(newly_detected)}")
    print(f"   (Transactions the old system missed but we caught)")
    if not newly_detected.empty:
        print(f"   Total Value Saved: ${newly_detected['amount'].sum() / 100:,.2f}")

    print("-" * 30)
    print(f"⚠️  POTENTIAL MISSES: {len(missed_by_model)}")
    print(f"   (Transactions the old system caught but we missed)")

if __name__ == "__main__":
    print(f"Reading logs from {LOG_FILE}...")
    data = parse_logs(LOG_FILE)
    analyze_performance(data)