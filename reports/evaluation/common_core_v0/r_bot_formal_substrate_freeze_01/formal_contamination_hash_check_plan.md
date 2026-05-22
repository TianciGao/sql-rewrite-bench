# Formal Contamination Hash Check Plan

## Role

This plan defines the human-run-only contamination checker for formal `R-Bot` same-engine gating on:

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

1. `reports/curation/common_core_v0_final_denominator.csv`
2. denominator case source SQL files under `cases/*/*/source.sql`
3. `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_v1.csv`
4. `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_manifest_draft.csv`
5. visible generated-output trees if present:
   - `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`
   - `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated`

Optional local inputs:

- visible corpus text files identified in the manifest draft, if they are accessible and text-readable

## Normalization Policy

This checker uses a deterministic text normalization policy.

Comment handling:

- line comments beginning with `--` are stripped
- block comments of the form `/* ... */` are stripped

Case handling:

- the normalized SQL string is lowercased

Whitespace handling:

- all repeated whitespace collapses to a single space
- leading and trailing whitespace are stripped

Statement terminator handling:

- trailing semicolons are removed

This is a text normalization policy only.
It is not AST normalization.

## Required Checks

For each of the 40 denominator cases, the checker must:

1. read the source SQL file
2. normalize it deterministically
3. compute `normalized_source_hash`
4. compare it against any visible retrieval corpus text items from the manifest
5. compare it against visible generated SQL files from:
   - SQLGlot
   - Direct LLM
   - Calcite
   - `R-Bot` PG1 recovery canary

Exact match meaning:

- same normalized hash under the checker normalization policy

Near-duplicate meaning:

- not computed by this checker unless an explicit future heuristic is added
- current expected output should remain blocked for near-duplicate checks

## Required Outputs

The human-run checker script must write:

1. `formal_contamination_attestation_checked_v1.csv`
2. `formal_contamination_attestation_checked_summary.md`
3. `formal_contamination_hashes_v1.json`

## Blocked-State Rules

The checker must preserve blocked status when:

- a denominator source SQL file is missing
- a manifest path is missing
- a manifest item is non-text or unreadable
- a generated-output source tree is missing
- a generated-output file is unreadable
- near-duplicate checking is not implemented

Required blocked labels:

- `blocked_missing_source_sql`
- `blocked_missing_generated_output_source`
- `blocked_unavailable_corpus_text_source`
- `blocked_pending_near_duplicate_check`
- `blocked_partial_check_only`

## Human Run Boundary

The checker is intended to be run by a human later.
This task creates the script and plan only.
It does not execute the checker.

## Gate Impact

Even after the script exists, the formal gate remains closed until:

- the checker is actually run
- all 40 rows have completed machine-readable attestation
- retrieval config extraction is completed
- remaining corpus/index blockers are closed

