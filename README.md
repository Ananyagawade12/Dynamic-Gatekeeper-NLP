# Batch Relative Filtering of Confidence Scores

## Overview

This project implements a **batch-relative filtering algorithm** that determines which documents to **keep or discard** based on the _relative distribution_ of confidence scores within a batch, rather than relying on a fixed global threshold.

Given a list of raw confidence scores (logits or probabilities), the algorithm returns a **boolean mask** indicating whether each document should be retained.

The method is robust across:

- Flat score distributions
- Strong confidence clusters
- Weak confidence clusters
- Mixed and noisy score distributions

---

## Problem Statement

> Write a Python script that takes a list of raw confidence scores (logits or probabilities) and returns a boolean mask (Keep / Discard) for each document.

This repository satisfies the above requirement using a clean, reusable implementation.

---

## Repository Structure

├── batch_relative_filter.py # Core filtering algorithm
├── test_batch_relative_filter.py # Test and demonstration script
├── README.md

---

## Core Function

**File:** `batch_relative_filter.py`

````python
batch_relative_filter(scores: List[float]) -> List[bool]

## Input

- `scores`: List of raw confidence scores (logits or probabilities)

## Output

- Boolean list of the same length as `scores`:
  - `True`  → Keep document
  - `False` → Discard document

---

## Algorithm Description

The algorithm adapts dynamically to the score distribution within each batch instead of relying on a fixed threshold.

### Step 1: Distribution Analysis

- Computes the score range to detect flat distributions.

### Step 2: Z-score Normalization

- Standardizes scores using batch mean and standard deviation.

### Step 3: Case-Based Filtering

| Case | Condition | Strategy |
|-----|----------|----------|
| Flat distribution | Low score variance | Keep top few documents |
| Strong cluster | All scores high | Keep scores above batch mean |
| Weak cluster | All scores low | Keep minimal top documents |
| Mixed distribution | Clear confidence gap | Split using maximum Z-score gap |

### Step 4: Safety Guarantee

- Ensures at least one document is retained per batch.

---

## Testing

**File:** `test_batch_relative_filter.py`

The test script evaluates the algorithm on:

- Easy batches
- Hard batches
- Mixed distributions
- Flat low-confidence batches
- Adversarial distributions

Each test prints:
- Input scores
- Keep/discard mask
- Per-document decision

### Run Tests

```bash
python test_batch_relative_filter.py
````
