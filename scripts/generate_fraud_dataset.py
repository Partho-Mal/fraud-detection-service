# scripts/generate_fraud_dataset.py
import csv
import random
import uuid
from datetime import datetime, timedelta

TOTAL_TRANSACTIONS = 10_000
FRAUD_MIN = 100
FRAUD_MAX = 500

random.seed(42)

fraud_count = random.randint(FRAUD_MIN, FRAUD_MAX)

countries = ["IN", "US", "GB", "AE", "SG"]
channels = ["POS", "ONLINE", "ATM"]
entry_modes = ["CHIP", "NFC", "SWIPE", "WEB", "APP"]
currency = "INR"

start_time = datetime(2026, 1, 1)

rows = []

for i in range(1, TOTAL_TRANSACTIONS + 1):
    is_fraud = i <= fraud_count

    transaction_id = i
    user_id = str(uuid.uuid4())
    merchant_id = str(uuid.uuid4())

    if is_fraud:
        amount_cents = random.randint(200_000, 10_000_000)
        transaction_country = random.choice(countries[1:])
        channel = "ONLINE"
        entry_mode = random.choice(["WEB", "APP"])
    else:
        amount_cents = random.randint(1_000, 500_000)
        transaction_country = "IN"
        channel = random.choice(channels)
        entry_mode = random.choice(entry_modes)

    device_id = str(uuid.uuid4())
    created_at = start_time + timedelta(seconds=random.randint(0, 30 * 24 * 3600))

    rows.append([
        transaction_id,
        user_id,
        merchant_id,
        amount_cents,
        currency,
        transaction_country,
        channel,
        entry_mode,
        device_id,
        created_at.strftime("%Y-%m-%d %H:%M:%S"),
        is_fraud
    ])

random.shuffle(rows)

with open("credit_card_transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "transaction_id",
        "user_id",
        "merchant_id",
        "amount_cents",
        "currency",
        "transaction_country",
        "channel",
        "entry_mode",
        "device_id",
        "created_at",
        "is_fraud"
    ])
    writer.writerows(rows)

print(f"Generated {TOTAL_TRANSACTIONS} transactions with {fraud_count} fraud cases")
