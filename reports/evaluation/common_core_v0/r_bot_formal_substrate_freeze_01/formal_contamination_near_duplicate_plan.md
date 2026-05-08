# Formal Contamination Near-Duplicate Plan

## Role

This plan defines the human-run-only near-duplicate contamination checker for formal `R-Bot` same-engine gating on:

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
3. `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_manifest_draft.csv`
4. any visible text-readable included corpus entries referenced by that manifest

Optional supporting inputs:

- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_hashes_v1.json`
- `reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_index_audit.csv`

## Normalization Policy

The checker must reuse the existing deterministic normalization policy:

- strip line comments beginning with `--`
- strip block comments of the form `/* ... */`
- lowercase all text
- collapse repeated whitespace
- remove trailing semicolons

This remains text normalization only.
It is not AST normalization.

## Heuristic Features

For each denominator source SQL and each visible corpus text item, the checker should compute:

1. normalized SQL text
2. normalized token sequence
3. token set
4. token `3`-gram set
5. simple structural features such as:
   - token count
   - distinct token count
   - keyword counts for `select`, `from`, `where`, `join`, `group`, `order`, `having`, `union`, `exists`, `in`
   - parenthesis counts

These features are heuristic-only.
They are intended to produce machine-readable pass/fail/blocker states, not benchmark semantic claims.

## Comparison Rule

For each denominator case, the checker should compare the source SQL features against all visible text-readable included manifest items.

Minimum recorded outputs per row:

- best visible manifest match ID if any
- token-set Jaccard score
- token-`3`-gram Jaccard score
- structural similarity score
- combined heuristic similarity score

Near-duplicate detection rule should be explicit and deterministic in the script.

Recommended default trigger:

- token-set Jaccard at or above a high threshold
- token-`3`-gram Jaccard at or above a high threshold
- structural similarity at or above a high threshold

## Blocked-State Rule

The checker must not mark a denominator row passed unless full included corpus text required for the check is actually available.

If any included manifest text source is missing, unreadable, non-text, or empty after normalization, rows must be preserved as:

- `blocked_corpus_text_unavailable`

Required examples of exact blocker reasons include:

- `manifest_path_missing:...`
- `manifest_text_unavailable:...`
- `manifest_text_empty_after_normalization:...`

## Required Outputs

The human-run checker script must write:

1. `formal_near_duplicate_check_v1.csv`
2. `formal_near_duplicate_check_summary.md`

Expected row-level states:

- `passed`
- `failed_near_duplicate_detected`
- `blocked_missing_source_sql`
- `blocked_corpus_text_unavailable`

## Human Run Boundary

This task creates the script and plan only.
It does not execute the checker.

## Gate Impact

Even after the script exists, formal `R-Bot @120` generation remains blocked until:

- the checker is actually run
- corpus text is complete enough to support row-level pass/fail
- remaining contamination and substrate blockers are closed
