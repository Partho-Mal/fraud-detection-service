# Troubleshooting

This document lists common issues and recommended checks.

---

## Service Does Not Start

* Verify Docker is running
* Check Dockerfile syntax
* Inspect container logs

---

## Shadow Logs Not Visible

* Ensure MODE=SHADOW is set
* Restart the container
* Confirm logs are not filtered

---

## High Latency

* Verify ONNX model is used
* Check preprocessing cost
* Increase WEB_CONCURRENCY

---

## Connection Resets

* Avoid single-worker setups
* Increase worker count
* Reduce load test intensity

---

## Invalid Request Errors

* Validate request schema
* Ensure required fields are present
* Confirm data types

---

## Unexpected Predictions

* Check threshold configuration
* Review preprocessing pipeline
* Validate model artifact version
