# Local Testing Guide

This document describes how to run and validate the fraud detection service locally.

---

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+ (optional, for load tests)

---

## Start the Service

Build and start the service using Docker Compose:

docker compose up --build

The API will be available at:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs

---

## Basic API Test

Send a sample transaction request:

curl -X POST \
  http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "amount_cents": 1200,
    "transaction_country": "IN",
    "channel": "POS",
    "entry_mode": "CHIP"
  }'

Expected response format:

{
  "is_fraud": false,
  "confidence_score": <float>,
  "processing_time_ms": <float>
}

---

## High-Risk Transaction Test

curl -X POST \
  http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "amount_cents": 500000,
    "transaction_country": "NG",
    "channel": "ONLINE",
    "entry_mode": "APP"
  }'

This request should typically return a fraud classification in production mode.

---

## Shadow Mode Test

Run the service in shadow mode:

docker run -p 8000:8000 -e MODE=SHADOW fraud-engine

Send a high-risk request:

curl -X POST \
  http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "amount_cents": 900000,
    "transaction_country": "NG",
    "channel": "ONLINE",
    "entry_mode": "APP"
  }'

Expected behavior:
- API response returns is_fraud=false
- Logs contain SHADOW_LOG entries indicating the model decision

---

## Verification Checklist

- Service starts without errors
- /predict endpoint responds successfully
- Shadow logs appear when MODE=SHADOW
- Latency remains within expected range
