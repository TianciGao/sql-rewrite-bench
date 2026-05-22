# Common-core v0 Programmatic Metric Audit README v1

## Files inspected
The audit inspected governance files (`AGENTS.md`, `docs/DOC_MAP.md`, `benchmark_spec/decision_log.md`, `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`), metric/rules files where present, `scripts/cli.py`, `scripts/common_core_v0_validation.py`, relevant `scripts/**`, `tests/**`, `env/**`, case-package paths by reference, and retained Common-core artifacts under `reports/evaluation/common_core_v0/**`.

## Outputs created
This directory contains six files: execution script inventory, metric formula audit, metric-to-artifact trace, table recompute readiness plan, human findings, and this README.

## Audit method
For each route or metric, the audit located retained code or artifact paths, identified input and output artifacts, recorded denominator/numerator/filter logic, and classified whether logic is retained in code, retained only in generated artifacts, or missing/not retained.

## What was not executed
No DB engine, LLM/model call, verifier, PORT9 experiment, EXPLAIN/plan collection, timing collection, case generation, or verifier experiment was executed.

## Status interpretation
`retained_exact` means the relevant script or formula is directly retained. `retained_partial` means the route/formula is partly retained but has artifact-only or missing pieces. `inferred_from_artifact` means no generator was found but the retained artifact preserves the value. `missing_or_not_retained` means required implementation evidence is absent. `conflict_needs_human_review` is reserved for detected disagreement between code and artifacts.

## How to use this audit before submission
Use this packet as the Round 15A map. Before submission, run Round 15B static recomputation checks for rows marked `ready_for_independent_recompute`, without running DB/LLM/verifier experiments. Keep bounded prior methods, PORT readiness, verifier support, and selected plan observability within their claim boundaries.

## Source-of-truth writeback
No source-of-truth writeback is needed from this audit. Registries, taxonomy YAMLs, case facts, protocol files, and paper prose were intentionally not modified.
