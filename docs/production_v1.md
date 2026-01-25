# Release Notes: v1.2.0 (Production Hardening)

This release transitions the Fraud Detection Engine from a prototype to a production-grade microservice capable of handling **170+ RPS** on commodity hardware with **99.9% reliability**.

---

## 1. Performance Architecture

**ONNX Runtime Migration**
Replaced Scikit-Learn pickle-based inference with ONNX Runtime, reducing p95 latency by ~70% (**300ms → 90ms**).

**Concurrency Tuning**
Configured `WEB_CONCURRENCY=8` to align with available CPU cores, maximizing throughput while avoiding excessive context switching.

**Thread Safety**
Enforced single-threaded execution for Scikit-Learn (`LOKY_MAX_CPU_COUNT=1`) to eliminate thread contention inside Gunicorn workers.

---

## 2. Resilience & Reliability (SRE Principles)

**Circuit Breaker (Timeouts)**
Implemented a strict **300ms timeout middleware**. Requests exceeding the SLA are shed immediately (`503 Service Unavailable`) to prevent queue buildup and preserve system availability during traffic spikes.

**Health Probes**
Added Kubernetes-compatible health checks:

* `/health/live` — Confirms the pod is running
* `/health/ready` — Confirms the ONNX model is fully loaded and ready for inference

---

## 3. Observability

**Structured Logging**
Migrated from raw text logs to **JSON structured logs**, enabling downstream systems (Datadog, Splunk) to automatically extract fields such as `latency_ms`, `fraud_probability`, and `transaction_amount`.

**Log Sampling**
Introduced probabilistic log sampling (**1% rate**) to reduce I/O overhead while retaining statistically meaningful visibility into system behavior.

---

## 4. Testing & Verification

**K6 Load Testing Suite**
Added a comprehensive load testing framework to simulate real-world traffic patterns:

* `capacity_test.js` — Ramping VU test to determine system saturation point (observed: ~35 concurrent users)
* `stress_test_realism.js` — Simulates varied geographies, transaction channels, and attack vectors

**Shadow Mode Analysis**
Added offline analysis scripts to parse shadow traffic logs and estimate blocked fraud value (**~$199k in simulation**) without impacting live production traffic.
