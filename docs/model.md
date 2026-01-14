# Model Overview

This document describes the fraud detection model used for inference.

The focus is on how the model is served rather than how it is trained.

---

## Model Type

* Binary classification model
* Outputs probability of fraud
* Trained offline

---

## Input Features

* Numeric and categorical features
* Derived from transaction metadata
* Preprocessing applied before inference

The model expects features in a fixed order and format.

---

## Preprocessing

* Implemented as a fitted preprocessing pipeline
* Applied consistently during training and inference
* Loaded once at application startup

---

## ONNX Runtime

The trained model is exported to ONNX format for inference.

Benefits:

* Lower inference latency
* Reduced dependency footprint
* Stable runtime behavior

---

## Decision Threshold

The final fraud decision is derived by comparing the model probability to a configurable threshold.

The threshold is controlled via the FRAUD_THRESHOLD environment variable.

---

## Model Lifecycle

* Train model offline
* Evaluate on validation data
* Export to ONNX
* Deploy as immutable artifact

Model updates require redeployment.

---

## Limitations

* No online learning
* No concept drift detection
* No per-user personalization
