# app/main.py
# app/main.py
import os
import logging
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.v1.predict import router

# Import the model session variable to check its health
from app.services.inference import ort_session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("fraud_engine")

app = FastAPI(title="Fraud Detection Engine")

# --- 1. TIMEOUT MIDDLEWARE (The "Circuit Breaker") ---
# This kills any request that takes longer than 150ms.
# It protects your queue from piling up during traffic spikes.
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        # Standard Production SLA: 300ms
        return await asyncio.wait_for(call_next(request), timeout=0.30)
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=503,
            content={"error": "Service too busy (Timeout)"}
        )

# --- 2. HEALTH CHECKS ---
@app.get("/health/live")
def liveness():
    """Kubernetes checks this to see if the POD is running."""
    return {"status": "ok"}

@app.get("/health/ready")
def readiness():
    """Load Balancers check this to see if the MODEL is loaded."""
    if ort_session is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    return {"status": "ready"}

@app.on_event("startup")
def startup():
    logger.info(
        "Service started | MODE=%s | LOG_SAMPLING_RATE=%s",
        os.getenv("MODE"),
        os.getenv("LOG_SAMPLING_RATE"),
    )

app.include_router(router)


# import os
# import logging
# from fastapi import FastAPI
# from app.api.v1.predict import router
# from app.models.onnx_model import load_onnx_artifacts

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s %(levelname)s %(name)s %(message)s",
# )

# logger = logging.getLogger("fraud_engine")

# app = FastAPI(title="Fraud Detection Engine")

# @app.on_event("startup")
# def startup():
#     artifacts = load_onnx_artifacts()
#     app.state.preprocessor = artifacts["preprocessor"]
#     app.state.session = artifacts["session"]

#     logger.info(
#         "Service started | MODE=%s | SHADOW_MODE=%s | FRAUD_THRESHOLD=%s",
#         os.getenv("MODE"),
#         os.getenv("MODE", "").upper() == "SHADOW",
#         os.getenv("FRAUD_THRESHOLD"),
#     )

# app.include_router(router)

