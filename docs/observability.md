# Observability

This document describes how the service exposes runtime behavior through logs.

The service relies on structured logging rather than metrics or tracing.

---

## Logging Strategy

* Logs are written to standard output
* Logs are consumed by the container runtime
* No external logging backend is required

---

## Startup Logs

At startup, the service logs key configuration values:

* Environment name
* Shadow mode status
* Fraud threshold

These logs help validate correct configuration.

---

## Request Logs

* Gunicorn and Uvicorn log HTTP request metadata
* Response status codes are logged automatically

---

## Shadow Mode Logs

When shadow mode is enabled, additional logs are emitted.

Example:

SHADOW_LOG amount=500000 prob=0.9999 primary_decision=True

These logs are used for offline analysis.

---

## Intended Usage

* Debugging
* Offline recall analysis
* Configuration validation

---

## Out of Scope

* Distributed tracing
* Real-time metrics
* Alerting
