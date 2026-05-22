# Static Recompute Audit V1

## 1. Purpose
Round 15B independently recomputes Common-core v0 paper-facing metrics from retained static artifacts and compares them against retained Section 8 / Round 1-5 artifacts. No database engine, LLM/model call, verifier experiment, PORT9 experiment, EXPLAIN collection, or timing collection was run.

## 2. Scope and non-goals
The audit covers Tables 8, 9, 10, 13, 14, 15, 16, 17, 18, and 20. It does not change benchmark protocol, denominators, taxonomy definitions, case facts, registries, code, or paper prose.

## 3. Recomputed exact matches
Exact matches: 255. These include denominator composition, taxonomy coverage, pool taxonomy coverage, hard-negative guardrail counts, candidate failure-accounting identities, selected observability frontier counts, bounded PORT execution/consistency counts, verifier retained counts/scope, and artifact-map coverage/status counts.

## 4. Rounded matches
Rounded matches: 4. The rounded rows are floating-point speedup metrics where recomputation from per-case timing rows matched retained values within tolerance. GM speedup used `exp(mean(log(speedup_ratio)))` over exact + timing-success rows. Regression@20 used `count(speedup_ratio < 0.8) / timing_denominator`.

## 5. Artifact-only accepted rows
Artifact-only accepted rows: 3. R-Bot timing, SQLGlot combined same-engine 240 timing, and Direct LLM repair mixed-source 96-row timing remain retained summary artifacts because a clean lower-level denominator for independent recomputation of those paper-facing rows is not retained.

## 6. Expected NA / unsupported rows
Expected NA rows: 4. SpeedupTransferRate is expected NA because `missing_paired_target_engine_timing` is retained as the blocker. NodeAlignmentCoverage is expected NA/future work because the retained plan evidence is a selected PG frontier, not full-denominator node alignment. SQLSolver verdict split is NA because detailed proof/refute verdict rows are not retained.

## 7. Conflicts or missing inputs
Conflicts: 0. Missing inputs: 0. The mismatch CSV contains only conflict or missing-input rows and is header-only when both counts are zero.

## 8. Key semantic checks
Executed vs ready: Direct LLM repair keeps `generated_or_ready` / ready_after_preflight separate from executed semantics. The retained identity `executed = exact + mismatch = 97` reproduces, while ready_after_preflight is not treated as executed.

Hard-negative: package hard-negative guardrail rows reproduce planned 120, tested 111, not-applicable 9, executable semantic mismatch 111, and false accept 0. This is distinct from candidate failure accounting.

SQLGlot no-op: source-like/no-op count reproduces as 24, with non-exact frontier `120 - 72 = 48`.

PORT/verifier boundaries: bounded PORT6 closure is retained separately from full PORT9 experiments, and verifier support is not a same-engine rewrite baseline nor a common-core 120 denominator.

Artifact map nuance: retained `paper_artifact_index_v1.csv` covers 8/9 locations from Section 8.2 through 8.10 because Section 8.4 is not represented as a paper_location row. This is recorded as retained artifact-map coverage, not a metric conflict.

## 9. Recommendation for paper
Use exact and rounded recomputation rows as static support for the final Section 8 render and reproducibility package. Keep artifact-only rows labeled as artifact-only and keep expected NA rows out of computed-metric claims.

## 10. Source-of-truth writeback judgment
No source-of-truth writeback is needed from Round 15B. The recomputation audit did not identify conflicts requiring registry, taxonomy, case fact, protocol, code, or paper-source changes.
