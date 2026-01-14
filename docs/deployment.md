# Deployment

This document describes how the fraud detection service is built and run.

The deployment setup is intentionally simple and mirrors common production patterns for stateless inference services.

---

## Runtime Stack

* Docker container
* Gunicorn process manager
* Uvicorn ASGI workers
* FastAPI application

---

## Container Build

The service is built using a single Dockerfile.

Key characteristics:

* Python 3.10 slim base image
* Dependencies installed at build time
* Application code copied into the image
* No runtime package installation

---

## Process Model

* Gunicorn manages worker processes
* Each worker runs an independent Uvicorn server
* Each worker loads its own model and preprocessing pipeline

The service is stateless across requests.

---

## Environment Configuration

All runtime behavior is controlled via environment variables.

Common variables include:

* ENV
* MODE
* FRAUD_THRESHOLD
* WEB_CONCURRENCY

Configuration is read at startup.

---

## Local Deployment

Build and start the service using Docker Compose:

docker compose up --build

The service listens on port 8000 by default.

---

## Scaling Considerations

* Increase WEB_CONCURRENCY to scale CPU-bound throughput
* Horizontal scaling is achieved by running multiple containers
* No shared state exists between instances

---

## Non-Goals

* No autoscaling configuration is included
* No service discovery is implemented
* No external dependency management is required
