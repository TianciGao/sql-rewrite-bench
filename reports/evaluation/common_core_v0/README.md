# Common-core v0 Evaluation Artifacts

This directory no longer contains only schema templates.

It now serves as the paper-facing, denominator-aware evidence area for the
`common_core_v0` evaluation work, while still retaining schema and manifest
templates used by the evaluation pipeline.

It is not a final ranked leaderboard directory.

## Purpose

This directory is the stable evaluation home for the frozen `common_core_v0`
40-case package and its related paper-facing artifacts.

The current same-engine denominator family is anchored on:

- [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)
- [COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/reviews/COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md)

For same-engine tri-engine reporting, the intended denominator is:

- `40` cases
- `3` engines: PostgreSQL / MySQL / Spark
- total `120` rows
- denominator family: `common_core_v0_40_same_engine_120`

The paper-safe framing is:

- this directory is a denominator-aware evidence ledger
- it is not a final ranked leaderboard
- rows may differ in route structure, engine scope, execution scope, and timing
  scope

## Artifact Layers

This directory currently contains multiple artifact layers that should not be
confused.

### 1. Schema and manifest templates

These remain the low-level reporting-shape artifacts for evaluation runs:

- `evaluation_manifest.template.json`
- `run_event_long.schema.csv`
- `method_case_summary.schema.csv`
- `same_engine_leaderboard.schema.csv`
- `controls_summary.schema.csv`
- `port_translation_summary.schema.csv`
- `verifier_support_summary.schema.csv`
- `plan_observability_summary.schema.csv`
- `failure_bucket_summary.schema.csv`

### 2. Paper index and navigation files

These are the stable entry points for paper-facing reading:

- [00_PAPER_RESULTS_INDEX.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_RESULTS_INDEX.md)
- [00_PAPER_RESULTS_INDEX.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_RESULTS_INDEX.csv)

### 3. Method-comparison evidence ledger

The current canonical table-level artifact is:

- [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)

It is a paper-facing denominator-aware evidence ledger, not a single-scalar
leaderboard.

### 4. Result cards and proposed rows

This directory now includes paper-facing result cards and proposed rows for
individual methods or routes, including:

- route-level SQLGlot cards and proposed rows
- bounded and fail-closed Calcite HEP evidence
- retained R-Bot result cards

Proposed rows are preview artifacts only. They are not canonical table rows by
themselves.

### 5. Validity and speedup summaries

Method- or route-level summaries remain important evidence layers, including:

- validity summaries
- speedup summaries
- route audits
- fail-closed syntheses
- frontier audits

These summaries must still be interpreted with their denominator and timing
scope attached.

### 6. Controls, preflight, and run directories

The directory also retains:

- bounded control or boundary evidence
- preflight-oriented artifacts
- run subdirectories under `runs/`

These are evidence-support artifacts, not automatic admissions to a paper
method table.

## Canonical Raw Table

`run_event_long` remains the canonical raw result table shape.

Every executed, verified, skipped, failed, timed-out, or unsupported event
should be representable there before any summary table is derived. Derived
tables should not invent rows that cannot be traced back to `run_event_long`.

## Denominator Discipline

The current frozen common-core denominator is the `40`-case `common_core_v0`
selection, with same-engine tri-engine expansion to `120` rows when that route
definition applies.

Older or alternate denominators must remain separate and must not be silently
merged into the current common-core `120` denominator. Examples include:

- `seed_common_core_9`
- `expanded_pg_evidence_46`
- `prior_method_pg10`
- `port_bounded_6`

PG-only subset evidence is not tri-engine `120`-row evidence.

Route-specific `120` denominators are not automatically interchangeable with
method-family aggregates.

The `240`-row combined SQLGlot same-engine aggregate is not the same thing as a
single `120`-row common-core route.

No failed, unsupported, parser-blocked, generation-failed, execution-failed,
mismatched, or methodology-boundary row should disappear from denominator-aware
reporting.

## Method Evidence Caveats

### SQLGlot

SQLGlot currently has distinct retained artifacts that must stay separate:

- combined same-engine aggregate evidence
- `sqlglot_optimize_same_dialect`
- `sqlglot_transpile_same_dialect_noop`

Route-level evidence is not a method-family aggregate.

### Direct LLM

Direct LLM currently has strong same-engine evidence, but that does not by
itself authorize a winner claim or a ranked-leaderboard interpretation.

### Calcite HEP

Calcite HEP currently has:

- a PG-only canonical row in `method_comparison_summary_v2`
- a separate fail-closed `93 / 120` paper-facing correctness synthesis

Those artifacts are related but not interchangeable. The `93 / 120` row is
paper-useful denominator-aware evidence, not a canonical timing-backed
leaderboard row.

### R-Bot

R-Bot remains PG-only subset evidence in its current canonical paper-facing
form. Its MySQL/Spark artifacts are boundary evidence, not a tri-engine `120`
paper row.

## Metric Readiness Caveats

Geometric-mean speedup values in this directory are timing-denominator scoped.
They must not be compared as full-denominator leaderboard scalars unless later
policy and evidence explicitly support that move.

Important incomplete or separate metric families remain:

- `SpeedupTransferRate` is not computed for current portability evidence
- plan observability is not yet a complete common-core v0 method-ranking metric
- verifier support is not a rewrite leaderboard metric

Support/verifier evidence, portability evidence, and controls must remain
separated from rewrite-ranking interpretation.

## Paper-Safe Usage

Use this directory as a denominator-aware evidence ledger for paper writing.

Safe uses include:

- citing the paper index as the stable reading entry point
- citing method-comparison rows as denominator-aware evidence
- citing route-level proposed rows as preview-only, non-canonical artifacts
- citing bounded subset evidence with its explicit denominator caveat

Unsafe uses include:

- citing this directory as a final ranked leaderboard
- merging route-level evidence into method-family aggregates without explicit
  policy
- treating PG-only subset evidence as tri-engine `120` evidence
- comparing subset timing speedups as if they were full-denominator scalars
- treating controls, verifier support, or portability packets as rewrite-method
  leaderboard rows

## Boundary

Artifacts in this directory document retained evidence and reporting structure.

They do not by themselves:

- authorize benchmark runs
- convert proposed rows into canonical status
- create a final leaderboard
- change checker policy
- change denominator policy
- change benchmark admission status
