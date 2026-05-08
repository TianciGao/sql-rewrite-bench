# Formal Generated-Output Exclusion Plan

## Role

This plan defines the human-run-only generated-output exclusion checker for formal `R-Bot` same-engine gating on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

The checker must not:

- call any LLM or API
- run `R-Bot`
- execute SQL
- modify case files

## Inputs

Required local inputs:

1. `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_manifest_draft.csv`
2. visible generated-output trees if present:
   - `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated`

Optional supporting inputs:

- visible text-readable included corpus entries referenced by the manifest
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_index_audit.csv`

## Normalization Policy

The checker must reuse the existing deterministic normalization policy:

- strip line comments beginning with `--`
- strip block comments of the form `/* ... */`
- lowercase all text
- collapse repeated whitespace
- remove trailing semicolons

This remains text normalization only.

## Required Check

For each visible generated SQL file from the known exclusion families, the checker should:

1. read the generated SQL
2. normalize it deterministically
3. compute `normalized_hash`
4. compare that hash against visible text-readable included corpus manifest entries
5. preserve blocker states when corpus text is incomplete

This checker is about generated-output presence inside the candidate retrieval/demo corpus.
It is not the denominator exact-match checker.

## Blocked-State Rule

The checker must not mark generated-output rows passed unless full included corpus text required for the check is actually available.

If any included manifest text source is missing, unreadable, non-text, or empty after normalization, rows must be preserved as:

- `blocked_corpus_text_unavailable`

If a generated-output family root is missing, that family must preserve explicit blocked rows such as:

- `blocked_missing_generated_output_source`

## Required Outputs

The human-run checker script must write:

1. `formal_generated_output_exclusion_v1.csv`
2. `formal_generated_output_exclusion_summary.md`
3. `formal_generated_output_hashes_v1.json`

Expected row-level states:

- `passed`
- `failed_generated_output_present_in_corpus`
- `blocked_corpus_text_unavailable`
- `blocked_missing_generated_output_source`
- `blocked_generated_output_unreadable`

## Human Run Boundary

This task creates the script and plan only.
It does not execute the checker.

## Gate Impact

Even after the script exists, formal `R-Bot @120` generation remains blocked until:

- the checker is actually run
- corpus text is complete enough to support row-level pass/fail
- remaining contamination and substrate blockers are closed
