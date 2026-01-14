# Data Contract

This document defines the input data contract for the fraud detection service.

The contract is intentionally strict to ensure predictable model behavior and to avoid silent data issues at runtime.

---

## Request Schema

All requests to the `/predict` endpoint must conform to the following schema.

| Field               | Type    | Required | Description                 |
| ------------------- | ------- | -------- | --------------------------- |
| amount_cents        | integer | Yes      | Transaction amount in cents |
| transaction_country | string  | Yes      | ISO country code            |
| channel             | string  | Yes      | Transaction channel         |
| entry_mode          | string  | Yes      | Payment entry method        |

---

## Field Constraints

### amount_cents

* Must be a positive integer
* Represents the smallest currency unit
* No implicit currency conversion is performed

---

### transaction_country

* Expected to be an uppercase ISO country code
* Values outside the training distribution may degrade accuracy

---

### channel

* Represents the transaction channel
* Example values include ONLINE and POS
* Must match known categories from training

---

### entry_mode

* Represents the payment entry method
* Example values include APP and CHIP
* Must match known categories from training

---

## Validation Rules

* All fields are mandatory
* No additional fields are allowed
* Requests with missing or invalid fields are rejected
* Validation is enforced before preprocessing

Invalid requests return a 422 response.

---

## Backward Compatibility

Any change to this contract requires:

* Updating the preprocessing pipeline
* Retraining the model
* Redeploying the service

Schema changes are treated as breaking changes.

---

## Rationale

A strict data contract prevents silent failures and ensures consistency between training and inference environments.
