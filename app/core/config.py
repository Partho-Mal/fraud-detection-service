# app/core/config.py
import os
from functools import lru_cache

class Settings:
    ENV: str = os.getenv("ENV", "local")
    SHADOW_MODE: bool = os.getenv("MODE", "").upper() == "SHADOW"
    FRAUD_THRESHOLD: float = float(os.getenv("FRAUD_THRESHOLD", "0.5"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
