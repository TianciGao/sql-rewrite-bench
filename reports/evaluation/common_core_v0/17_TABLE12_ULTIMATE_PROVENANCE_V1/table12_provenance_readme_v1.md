# Table 12 Ultimate Provenance Audit V1 README

## Inputs Inspected
The final Section 8 render directory was checked and was absent. The audit therefore used the task-provided draft Table 12 target values plus retained artifacts: Table 3 method evidence, candidate failure accounting, speedup slice summary, Table 6 timing, Table 7 failure accounting, method candidate rejection accounting, case-level failure export, route result cards, route reconciliation artifacts, Round 15 program audit, and Round 16 static recompute artifacts.

## Search Commands Used
Read-only searches included the requested `rg` patterns, repeated with `--no-ignore` so ignored report artifacts were included; the requested `find reports/evaluation/common_core_v0 ... | sort`; and the requested `git log --all --name-only` / `git log --all -S` history searches. No history was modified and no branch checkout was performed.

## Outputs Created
This directory contains exactly six files: `table12_cell_provenance_v1.csv`, `table12_artifact_dependency_graph_v1.csv`, `table12_generator_script_audit_v1.csv`, `table12_formula_source_map_v1.csv`, `table12_provenance_summary_v1.md`, and `table12_provenance_readme_v1.md`.

## Status Definitions
`fully_traceable_to_runner_and_artifact` means the cell can be followed to a retained runner and retained output artifact. `traceable_to_artifact_chain` means retained artifacts support the value but a local aggregation generator is missing. `traceable_to_static_policy` means the value is a placement or expected-NA policy/boundary cell. `artifact_only_no_generator_retained` means no generator is retained for that layer. Generator statuses distinguish dedicated generator scripts, upstream runners, missing local aggregation scripts, artifact-only gaps, static policy cells, and not-applicable cells.

## What Was Not Executed
No DB, LLM/model, verifier, PORT9, EXPLAIN, timing, table regeneration, benchmark case generation, or experiment command was run. Runner paths are recorded as provenance only.

## How To Use This Audit
Use `table12_cell_provenance_v1.csv` for cell-level review, `table12_artifact_dependency_graph_v1.csv` to see recursive lineage edges, `table12_generator_script_audit_v1.csv` to target hardening work, and `table12_formula_source_map_v1.csv` to verify formulas and denominator rules before final rendering.

## Source-of-Truth Writeback
No source-of-truth writeback is needed. The audit recommends adding static regeneration scripts for aggregation layers, without changing retained values.
