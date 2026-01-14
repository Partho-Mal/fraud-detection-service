# app/schemas/transaction.py

from pydantic import BaseModel, Field
from typing import Literal

class TransactionInput(BaseModel):
    amount_cents: int = Field(..., gt=0)
    transaction_country: str = Field(..., min_length=2, max_length=2)
    channel: Literal["ONLINE", "POS", "ATM"]
    entry_mode: Literal["CHIP", "SWIPE", "WEB", "APP", "NFC"]

class FraudPrediction(BaseModel):
    is_fraud: bool
    confidence_score: float
    processing_time_ms: float