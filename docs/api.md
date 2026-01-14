# API Reference

This document describes the external HTTP interface exposed by the fraud detection service.

The API is intentionally minimal and exposes a single prediction endpoint.

---

## POST /predict

Evaluates a transaction and returns a fraud classification.

---

### Request Body

The request must be a JSON object with the following fields.

| Field               | Type    | Description                 |
| ------------------- | ------- | --------------------------- |
| amount_cents        | integer | Transaction amount in cents |
| transaction_country | string  | ISO country code            |
| channel             | string  | Transaction channel         |
| entry_mode          | string  | Payment entry method        |

All fields are required.

---

### Example Request

```json
{
  "amount_cents": 500000,
  "transaction_country": "NG",
  "channel": "ONLINE",
  "entry_mode": "APP"
}
```

---

### Response Body

| Field              | Type    | Description          |
| ------------------ | ------- | -------------------- |
| is_fraud           | boolean | Final fraud decision |
| confidence_score   | float   | Model probability    |
| processing_time_ms | float   | End-to-end latency   |

---

### Example Response

```json
{
  "is_fraud": true,
  "confidence_score": 0.9999,
  "processing_time_ms": 6.12
}
```

---

### Shadow Mode Behavior

When shadow mode is enabled:

* The model still runs
* Predictions are logged
* The response always returns is_fraud=false

This allows safe evaluation without impacting production decisions.

---

### Error Handling

* 422 Unprocessable Entity
  Returned when the request body does not match the expected schema.

---

### Interactive Documentation

Swagger UI is available at:

[http://localhost:8000/docs](http://localhost:8000/docs)
