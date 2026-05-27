# Formal Gate Check Expected Artifacts

## Role

This document records the expected outputs from the two new human-run-only gate checkers.

It does not mean the checks have been run.

## Contamination Hash Checker

Script:

- [run_manual_r_bot_formal_contamination_hash_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_contamination_hash_check.py)

Expected outputs after a future human run:

1. `formal_contamination_attestation_checked_v1.csv`
2. `formal_contamination_attestation_checked_summary.md`
3. `formal_contamination_hashes_v1.json`

Expected content:

- all 40 denominator cases covered
- deterministic normalized source hashes
- exact-match findings against visible corpus text items if available
- exact-match findings against visible generated-output families if available
- blocked rows preserved where coverage is incomplete

## Retrieval Config Extractor

Script:

- [run_manual_r_bot_formal_retrieval_config_extract.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_retrieval_config_extract.py)

Expected outputs after a future human run:

1. `formal_retrieval_config_extracted_v1.json`
2. `formal_retrieval_config_extraction_report.md`

Expected content:

- extracted or blocked values for:
  - `top_k`
  - reranking mode
  - similarity threshold or explicit none
  - embedding model identity
  - index identifier
  - rule-vector width
  - total dimension

## Gate Rule

Even if these outputs are created later, formal `R-Bot @120` generation remains blocked until:

1. all 40 contamination rows pass
2. retrieval config is fully frozen
3. corpus/index provenance blockers are closed
4. the future retained run package satisfies the artifact contract

## Current Status

- scripts created: `yes`
- scripts executed in this task: `no`
- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`

