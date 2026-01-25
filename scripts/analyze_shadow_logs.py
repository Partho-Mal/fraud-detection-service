# scripts/analyze_shadow_logs.py
# RUN:
#   docker compose logs fraud-engine > shadow_mode.log
#   python3 scripts/analyze_shadow_logs.py
import re
import sys
import pandas as pd
from typing import List, Dict

# Configuration
LOG_FILE = "shadow_mode.log"

def parse_logs(log_path: str) -> List[Dict]:
    data = []
    # Regex to handle both Fraud (with latency) and Safe (sampled) logs
    # Matches: amount=123 prob=0.99 decision=True latency=10.5ms
    # Also matches legacy format if any
    pattern = re.compile(r"amount=(\d+) prob=([0-9\.]+) (?:primary_)?decision=(\w+)(?: latency=([0-9\.]+)ms)?")
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "SHADOW_LOG" in line:
                    match = pattern.search(line)
                    if match:
                        record = {
                            "amount": int(match.group(1)),
                            "prob": float(match.group(2)),
                            "is_fraud": match.group(3) == "True",
                            "latency": float(match.group(4)) if match.group(4) else None
                        }
                        data.append(record)
    except FileNotFoundError:
        print(f"Error: Could not find file {log_path}")
        sys.exit(1)
    return data

def analyze_performance(data: List[Dict]):
    if not data:
        print("No logs found.")
        return

    df = pd.DataFrame(data)
    total_tx = len(df)
    fraud_tx = df[df['is_fraud'] == True]
    safe_tx = df[df['is_fraud'] == False]
    
    print("=== FINAL SHADOW MODE REPORT ===")
    print(f"Total Transactions Logged: {total_tx}")
    print(f"Fraud Detected:            {len(fraud_tx)} ({(len(fraud_tx)/total_tx)*100:.1f}%)")
    print(f"Safe Transactions:         {len(safe_tx)}")
    
    if not fraud_tx.empty and 'latency' in df.columns:
        print("-" * 30)
        print("⚡ LATENCY STATS (Sampled)")
        print(f"p50: {df['latency'].median():.2f} ms")
        print(f"p95: {df['latency'].quantile(0.95):.2f} ms")
        print(f"p99: {df['latency'].quantile(0.99):.2f} ms")

    print("-" * 30)
    print(f"💰 VALUE PROTECTION")
    blocked_amount = fraud_tx['amount'].sum() / 100
    print(f"Total Fraud Value Blocked: ${blocked_amount:,.2f}")

if __name__ == "__main__":
    print(f"Reading logs from {LOG_FILE}...")
    data = parse_logs(LOG_FILE)
    analyze_performance(data)