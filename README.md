# Smart Grid – Forecasting & Machine Learning Platform (Module 3.2)

## Overview

This repository contains the **Forecasting & Machine Learning Platform (Module 3.2)** of the Smart Grid system.

The purpose of this module is to **train, serve, monitor, and continuously improve probabilistic energy forecasts** used by downstream simulation and decision-support systems.

### Forecast Targets

This platform produces **short-term and mid-term forecasts** for:

* Electricity demand
* Solar generation
* Wind generation
* Grid imbalance indicators

All forecasts support:

* Multi-horizon outputs (24–48 steps)
* Point predictions
* Quantile-based uncertainty (0.05, 0.50, 0.95)

---

## Scope (Strict)

This repository implements **only**:

* Model training
* Model serving (real-time and batch)
* Feature handling via Vertex Feature Store
* Monitoring, drift detection, and retraining
* Inference APIs

### Explicitly Out of Scope

The following are **not** implemented here:

* Data ingestion pipelines
* Simulation or optimization logic
* Dashboards or frontend code
* Infrastructure provisioning outside ML execution

Upstream data and downstream consumers are assumed to already exist.

---

## Technology Stack (Non-Negotiable)

This project uses **only** the following technologies:

### ML Platform

* Vertex AI
* Vertex AI Pipelines (KFP / TFX)
* Vertex Training Jobs
* Vertex Endpoints (real-time + batch)
* Vertex Model Registry
* Vertex Model Monitoring

### Data & Features

* BigQuery (offline features, training data, logs)
* Vertex Feature Store (online + offline parity)

### Storage & Logging

* Google Cloud Storage (model artifacts)
* BigQuery (prediction logs, backtests, audits)

### Security

* GCP IAM
* OAuth2 service accounts
* No custom authentication mechanisms

---

## Repository Structure

```
smart-grid-ml/
│
├── pipelines/              # Vertex AI Pipelines
│   ├── training_pipeline.py
│   ├── retraining_pipeline.py
│   └── components/
│
├── training/               # Model training code
│   ├── baselines/
│   ├── lstm/
│   └── tft/
│
├── serving/                # Model serving containers
│
├── monitoring/             # Drift & performance logic
│
├── schemas/                # Feature & API contracts
│
├── configs/                # Project & training config
│
├── utils/                  # Hashing, logging, helpers
│
└── README.md
```

Each directory maps directly to a responsibility defined in the Smart Grid technical design.

---

## Build Order (Very Important)

⚠️ **Follow this order exactly. Do not skip steps.**
⚠️ **Do not start with TFT.**

### Correct Build Order

1. **Feature schema**
2. **Baseline model**
3. **Inference API + logging**
4. **LSTM training**
5. **Vertex pipeline**
6. **TFT training**
7. **Monitoring + retraining**

Starting with complex models before contracts, logging, and baselines will result in fragile, non-auditable systems.

---

## Step-by-Step Build Guide

### 1. Feature Schema (Foundation)

**Location:** `schemas/feature_schema.yaml`

Define **all features**, including:

* Names
* Data types
* Versions

This schema is the **single source of truth** for:

* Training
* Inference
* Drift detection
* Feature hashing

Nothing else should be written before this file exists and is agreed upon.

---

### 2. Baseline Models

**Location:** `training/baselines/`

Implement:

* Persistence
* Moving average
* Seasonal naïve

Purpose:

* Establish minimum performance benchmarks
* Validate inference APIs
* Provide fallback models

Baseline models must be trainable and deployable before any deep learning model.

---

### 3. Inference API + Logging

**Location:** `serving/`

Implement:

* Real-time prediction handler
* Feature retrieval from Vertex Feature Store
* Input feature hash generation
* Mandatory BigQuery logging for every prediction

At this stage, the system must already:

* Accept requests
* Return forecasts
* Log auditable prediction records

---

### 4. LSTM / Seq2Seq Training

**Location:** `training/lstm/`

Implement:

* Seq2Seq LSTM with encoder–decoder
* Input window ≈ 168 hours
* Horizon 24–48 hours

Purpose:

* Validate deep learning training on Vertex AI
* Test sliding window generation
* Benchmark against baselines

This step proves the ML infrastructure works **before** introducing TFT complexity.

---

### 5. Vertex AI Training Pipeline

**Location:** `pipelines/training_pipeline.py`

Implement:

* Data extraction from BigQuery
* Feature joins via Feature Store
* Dataset windowing
* Training job execution
* Evaluation
* Model registration

This pipeline must be:

* Deterministic
* Reproducible
* Fully automated

---

### 6. Temporal Fusion Transformer (Primary Model)

**Location:** `training/tft/`

Implement:

* TFT with static, observed, and known future features
* Multi-horizon probabilistic forecasts
* Quantile regression heads
* Pinball loss

Only introduce TFT **after**:

* Baselines are working
* LSTM training is stable
* Pipelines are reproducible

---

### 7. Monitoring & Retraining

**Location:** `monitoring/`

Implement:

* RMSE / MAE by horizon
* Pinball loss
* Calibration coverage
* Feature drift (PSI, KS-test)
* Missing data checks

Configure:

* Vertex Model Monitoring
* Alert thresholds
* Automatic retraining pipelines
* Canary deployment and rollback logic

---

## How to Run This Project Successfully

### Prerequisites

* GCP project with Vertex AI enabled
* BigQuery datasets populated
* Vertex Feature Store created
* Service account with:

  * `roles/aiplatform.admin`
  * `roles/bigquery.dataEditor`
  * `roles/storage.admin`

No additional infrastructure setup is required in this repository.

---

### Typical Workflow

1. Define feature schema
2. Train and deploy baseline model
3. Deploy inference endpoint
4. Validate prediction logging in BigQuery
5. Train LSTM model
6. Run Vertex training pipeline
7. Train and deploy TFT
8. Enable monitoring and alerts
9. Activate scheduled and triggered retraining

---

## Success Criteria

This module is considered **successfully implemented** when:

* Forecasts return point + quantile outputs
* Training and inference use identical features
* Every prediction is auditable in BigQuery
* Drift and performance degradation are detected automatically
* Models retrain and roll out safely without manual intervention
* Downstream simulation can trace forecasts deterministically

---

## Key Principle

> **Accuracy is useless without reproducibility, auditability, and controlled deployment.**

This repository prioritizes **production reliability over experimentation**.