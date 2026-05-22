# Formal Contamination Check Expected Artifacts v2

## Role

This document records the expected outputs from the human-run-only contamination checkers currently defined in this package.

It does not mean the checks have been run.

## Exact-Match Hash Checker

Script:

- [run_manual_r_bot_formal_contamination_hash_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_contamination_hash_check.py)

Expected outputs after a future human run:

1. `formal_contamination_attestation_checked_v1.csv`
2. `formal_contamination_attestation_checked_summary.md`
3. `formal_contamination_hashes_v1.json`

Expected content:

- all `40` denominator cases covered
- deterministic normalized source hashes
- exact-match findings against visible corpus text items if available
- exact-match findings against visible generated-output families if available
- blocked rows preserved where coverage is incomplete

## Near-Duplicate Checker

Script:

- [run_manual_r_bot_formal_near_duplicate_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_near_duplicate_check.py)

Expected outputs after a future human run:

1. `formal_near_duplicate_check_v1.csv`
2. `formal_near_duplicate_check_summary.md`

Expected content:

- all `40` denominator cases covered
- deterministic normalization reuse from the exact-match checker
- token-set, token-`3`-gram, and simple structural similarity evidence
- pass/fail/blocker row states
- `blocked_corpus_text_unavailable` preserved whenever full included corpus text is not actually available

## Generated-Output Exclusion Checker

Script:

- [run_manual_r_bot_formal_generated_output_exclusion_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_generated_output_exclusion_check.py)

Expected outputs after a future human run:

1. `formal_generated_output_exclusion_v1.csv`
2. `formal_generated_output_exclusion_summary.md`
3. `formal_generated_output_hashes_v1.json`

Expected content:

- normalized hashes for visible generated outputs from:
  - SQLGlot
  - Direct LLM
  - Calcite
  - `R-Bot` PG1 recovery canary
- exact-match checks against visible included corpus text items if available
- pass/fail/blocker row states
- explicit blocked rows when corpus text or generated-output family coverage is incomplete

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

1. all contamination rows actually pass
2. retrieval config is fully frozen
3. corpus/index provenance blockers are closed
4. the future retained run package satisfies the artifact contract

## Current Status

- scripts created: `yes`
- scripts executed in this task: `no`
- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`
