# Prior Methods Rerun Policy v1

## Role

This document defines how prior methods should be rerun or explicitly marked unsupported on the frozen `common_core_v0_40` denominator.

It is a policy and planning artifact only.
It does not run any method, database, SQL execution, timing, or speedup.

## Core Policy

All current method-comparison metrics must be recomputed on either:
- the frozen `common_core_v0_40` denominator, or
- an explicitly declared bounded subset derived from `common_core_v0_40`

Therefore, old numeric results are **disallowed** as current metrics for Common-core v0.

### Disallowed as current Common-core v0 metrics

The following old values may not be reused as current `common_core_v0_40` leaderboard-style metrics:
- all `prior_method_pg10` numeric results
- all `seed9` numeric results
- all bounded 4-case / 6-case / 10-case numeric results when treated as if they were frozen-denominator rows
- old `expanded_pg_evidence_46` numeric rows when treated as current `common_core_v0_40` rows
- historical GM values such as Calcite HEP `0.9443`, R-Bot `0.8804`, LearnedRewrite `0.6296`, and LLM-R2 `0.9592`

These older values may still be cited as **historical bounded evidence**.
They may not be presented as current same-engine Common-core v0 metrics.

## Reusable vs Non-reusable

### Reusable as templates only

Old implementation templates may be reused:
- Calcite HEP Java wrapper and PG checker/speedup scaffolds under `tools/calcite_hep/` and `reports/formal_expansion/calcite_hep_*`
- R-Bot / LLM4Rewrite single-case and RAG/index dry-run scaffolds from `docs/_scratch/`
- LearnedRewrite dry-run and adapter-preflight notes from `docs/_scratch/`
- LLM-R2 bounded smoke, extraction-fix, and logical-plan scaffolds from `docs/_scratch/`
- old failure categories, extraction logic, and runner sequencing as implementation guidance

### Not reusable as current results

Old numeric outputs are not comparable as current rows because the denominator changed.
They must not be copied into `common_core_v0_40` method tables.

## Row Visibility Rule

If a method cannot support a row, that row must be reported as:
- `unsupported`, or
- `not_attempted`

It must not be silently dropped.

This applies especially to:
- all non-`PERF` rows for the current prior-method family
- all MySQL rows
- all Spark rows
- PG `PERF` rows outside the method’s declared first-wave bounded denominator

## Method Contracts

### `calcite_hep`

- target denominator: `common_core_v0_40_perf_pg9_overlap`
- supported pools: `performance_only`
- supported engines: `pg_only`
- required dependencies: `tools/calcite_hep/CalciteHepRewriteSmoke.java`; Calcite wrapper/build path; PG checker/timing harness templates
- current repo has runnable code: `partial_yes_closest_to_runnable`
- old scripts reusable: `yes_repo_local_templates`
- old numeric results disallowed: `yes`
- proposed first rerun scope: `common_core_v0_40_perf_pg9_overlap on pg`
- unsupported rows: all `CONS`, `PORT`, `LONGTAIL`, MySQL, and Spark rows
- expected output artifacts: generation SQL, execution/run-event rows, checker JSON, timing rows, bounded denominator manifest
- table placement: `bounded_baseline_table` after current-denominator rerun; not primary full-table entry yet

### `r_bot`

- target denominator: `common_core_v0_40_perf_pg9_overlap_after_retrieval_stack_recovery`
- supported pools: `performance_only`
- supported engines: `pg_only`
- required dependencies: retrieval corpus, demo-selection policy, contamination/fair-comparison contract, rule pool, runnable R-Bot harness
- current repo has runnable code: `no_runner_recovery_needed`
- old scripts reusable: `yes_template_only`
- old numeric results disallowed: `yes`
- proposed first rerun scope: `common_core_v0_40_perf_pg9_overlap on pg after retrieval stack recovery`
- unsupported rows: all non-`PERF`, MySQL, and Spark rows
- expected output artifacts: generated SQL, retrieval trace, selected rules, execution/checker artifacts, timing rows for checker-consistent non-noop candidates only
- table placement: `bounded_baseline_table_after_recovery`; appendix only if recovery never closes

### `learnedrewrite`

- target denominator: `common_core_v0_40_perf_pg9_overlap_after_adapter_checkpoint_recovery`
- supported pools: `performance_only`
- supported engines: `pg_only`
- required dependencies: adapter, checkpoint, inference entrypoint, and explicit noop/source-like accounting path
- current repo has runnable code: `no_artifact_stack_missing`
- old scripts reusable: `yes_template_only`
- old numeric results disallowed: `yes`
- proposed first rerun scope: `common_core_v0_40_perf_pg9_overlap on pg after adapter/checkpoint recovery`
- unsupported rows: all non-`PERF`, MySQL, and Spark rows
- expected output artifacts: generated SQL, execution/checker artifacts, explicit noop classification, timing rows only for valid non-noop candidates
- table placement: `bounded_baseline_table_after_recovery`; appendix only if recovery never closes

### `llm_r2`

- target denominator: `common_core_v0_40_perf_pg9_overlap_after_runner_recovery`
- supported pools: `performance_only`
- supported engines: `pg_only`
- required dependencies: runner recovery, logical-plan probe path, deterministic output extraction contract
- current repo has runnable code: `no_runner_recovery_needed`
- old scripts reusable: `yes_template_only`
- old numeric results disallowed: `yes`
- proposed first rerun scope: `common_core_v0_40_perf_pg9_overlap on pg after runner recovery`
- unsupported rows: all non-`PERF`, MySQL, and Spark rows
- expected output artifacts: generated SQL, logical-plan/extraction logs, execution/checker artifacts, timing rows for checker-consistent non-noop candidates
- table placement: `bounded_baseline_table_after_recovery`; appendix only if recovery never closes

## Recommended First Rerun

`calcite_hep` should be tried first.

Why:
- it appears closest to runnable in the current repo
- it already has the strongest repo-local checker/timing template evidence
- it has the least substrate uncertainty among the four prior methods
- it provides the cleanest path to a declared current-denominator bounded baseline row

## Output Contract

Any rerun package produced from this policy should create denominator-aware raw rows and derived summaries that:
- identify unsupported rows explicitly
- separate generation failure, execution failure, mismatch, noop, and timing exclusion
- avoid copying historical bounded numeric values into current tables
- declare bounded subset denominators clearly when full `common_core_v0_40` support is absent

## Table Placement Policy

- `calcite_hep`: may enter a **bounded baseline table** after a fresh rerun on `common_core_v0_40_perf_pg9_overlap`
- `r_bot`, `learnedrewrite`, `llm_r2`: may enter a **bounded baseline table** only after substrate recovery and a fresh rerun on a declared bounded subset
- none of the four methods should enter a full primary Common-core v0 same-engine table until they have current-denominator-compatible rerun evidence
- methods that never recover beyond historical slices belong in **appendix only**
