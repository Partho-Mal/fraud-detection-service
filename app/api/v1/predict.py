#  app/api/v1/predict.py
from fastapi import APIRouter
from app.schemas.transaction import TransactionInput, FraudPrediction
from app.services.inference import run_inference

router = APIRouter()

@router.post("/predict", response_model=FraudPrediction)
def predict(transaction: TransactionInput):
    # --- FIX START ---
    # OLD BROKEN WAY: 
    # preprocessor = request.app.state.preprocessor (This is gone!)
    
    # NEW FAANG WAY:
    # Just call the function. It uses the global optimized model internally.
    # We also removed the router-level "Shadow Mode" check because 
    # run_inference now handles the "Shadow Logging" automatically.
    is_fraud, prob, latency = run_inference(transaction)
    # --- FIX END ---

    return {
        "is_fraud": is_fraud,
        "confidence_score": round(prob, 4),
        "processing_time_ms": round(latency, 2),
    }


# from fastapi import APIRouter, Request
# from app.schemas.transaction import TransactionInput, FraudPrediction
# from app.services.inference import run_inference
# from app.models.shadow import is_shadow_mode, shadow_response

# router = APIRouter()

# @router.post("/predict", response_model=FraudPrediction)
# def predict(transaction: TransactionInput, request: Request):
#     preprocessor = request.app.state.preprocessor
#     session = request.app.state.session

#     is_fraud, prob, latency = run_inference(
#         transaction,
#         preprocessor,
#         session,
#     )

#     if is_shadow_mode():
#         return shadow_response(transaction, prob, latency)

#     return {
#         "is_fraud": is_fraud,
#         "confidence_score": round(prob, 4),
#         "processing_time_ms": round(latency, 2),
#     }
