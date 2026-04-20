# AGENTS.md

## What this directory contains

This directory contains **review-history documents**, not live fact tables.

Files here explain:

- what was reviewed
- what judgment was made
- why that judgment was made

They do not replace:

- `inventory/case_registry.csv`
- `docs/EXECUTION_STATUS.md`
- `benchmark_spec/decision_log.md`

---

## Directory rules

### 1. Review files are history, not live status
If a review document conflicts with current case facts, prefer:

1. `inventory/case_registry.csv` for live case facts
2. `docs/EXECUTION_STATUS.md` for current stage interpretation
3. `benchmark_spec/decision_log.md` for frozen project decisions

### 2. Do not silently overwrite old reviews
Do not silently mutate an old review record to represent a new review state.

Preferred options:

- create a new versioned review file
- or create a new batch-specific review file
- or explicitly mark an older file as superseded

### 3. Keep review files scoped
A review file should answer only:

- what batch / scope it covers
- what criteria were applied
- what judgment was made
- what metadata consequence followed

Do not turn review files into:

- long-term rule documents
- live status dashboards
- registry substitutes

### 4. Use short metadata blocks
Each review file should begin with a short metadata block indicating:

- batch
- review layer
- superseded files
- status role
- live fact sources

### 5. Stop and ask before changing review semantics
Ask a human before:

- changing what a review layer means
- redefining candidate / admitted semantics
- merging review layers in a way that changes policy meaning