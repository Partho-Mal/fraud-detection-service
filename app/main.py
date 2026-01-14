# app/main.py
import os
import logging
from fastapi import FastAPI
from app.api.v1.predict import router
from app.models.onnx_model import load_onnx_artifacts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("fraud_engine")

app = FastAPI(title="Fraud Detection Engine")

@app.on_event("startup")
def startup():
    artifacts = load_onnx_artifacts()
    app.state.preprocessor = artifacts["preprocessor"]
    app.state.session = artifacts["session"]

    logger.info(
        "Service started | MODE=%s | SHADOW_MODE=%s | FRAUD_THRESHOLD=%s",
        os.getenv("MODE"),
        os.getenv("MODE", "").upper() == "SHADOW",
        os.getenv("FRAUD_THRESHOLD"),
    )

app.include_router(router)

