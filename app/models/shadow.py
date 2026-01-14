# app/models/shadow.py
import logging
from app.core.config import get_settings

logger = logging.getLogger("fraud_engine")

def is_shadow_mode():
    settings = get_settings()
    return settings.SHADOW_MODE


def shadow_response(transaction, fraud_prob, latency_ms):
    settings = get_settings()

    primary_decision = fraud_prob > settings.FRAUD_THRESHOLD

    logger.info(
        f"SHADOW_LOG "
        f"amount={transaction.amount_cents} "
        f"prob={fraud_prob:.4f} "
        f"primary_decision={primary_decision}"
    )

    return {
        "is_fraud": False,  # force no impact
        "confidence_score": round(fraud_prob, 4),
        "processing_time_ms": round(latency_ms, 2),
    }

