# Common-core v0 Deterministic Reproduction Plan V1

## Purpose
This file records the reviewer-facing deterministic rerun plan for Common-core v0.

## Mode Boundary
- Deterministic mode does not call LLM APIs.
- Deterministic mode does not run verifier tools.
- Deterministic mode does not run PORT9.
- Deterministic mode may run DB/timing commands only when `--execute` is explicit.
- LLM and full rerun modes remain separate from deterministic artifact review.

## Invocation
- Mode action: `execute`
- Requested steps: `rbot-pg15-timing`
- Output directory: `reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic`

## Selected Steps

### rbot-pg15-timing
- Description: R-Bot PG15 bounded appendix timing.
- Command: `bash reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/run_manual_r_bot_pg15_timing.sh`
- Runner exists: yes
- Requires DB: yes
- Requires Java: no
- Requires LLM: no
- Requires verifier: no
- Notes: Bounded appendix route; requires DB timing environment.
