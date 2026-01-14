# Shadow Mode

This document explains how shadow mode is implemented and used.

Shadow mode allows model evaluation using real request data without impacting production decisions.

---

## Definition

In shadow mode:

* The model inference path executes normally
* Predictions are logged
* API responses do not enforce fraud decisions

---

## Purpose

Shadow mode is used to:

* Evaluate new model versions
* Measure recall changes
* Validate threshold tuning
* Observe real traffic distributions

---

## Runtime Behavior

When MODE=SHADOW:

* The fraud decision returned to clients is forced to false
* The model probability and decision outcome are logged

Production behavior remains unchanged.

---

## Example Log

SHADOW_LOG amount=900000 prob=0.9999 primary_decision=True

---

## Recall Measurement

Recall is measured offline by comparing:

* Shadow model decisions
* Known fraud labels

No online decisioning is affected.

---

## Enabling Shadow Mode

Set the environment variable:

MODE=SHADOW

Any other value disables shadow mode.

---

## Safety Guarantees

* No customer-facing impact
* No decision overrides
* No state persistence
