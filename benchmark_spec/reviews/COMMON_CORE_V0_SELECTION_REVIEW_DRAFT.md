# COMMON_CORE_V0_SELECTION_REVIEW_DRAFT

## Status

This file is a draft selection review for a Common-core v0.3 40-case candidate slate.

It is not final admission.
It does not update registry facts.
It does not modify `inventory/case_registry.csv`, `inventory/source_registry.csv`, `README.md`, or `docs/EXECUTION_STATUS.md`.

## Review Basis

This draft is derived from the following existing curation outputs and current live registry rows:

- `reports/curation/common_core_v0_40_artifact_preflight.md`
- `reports/curation/common_core_v0_replacement_preflight.md`
- `reports/curation/longtail_sqlstorm_common_core_review_prep.md`
- `inventory/case_registry.csv`
- `docs/DOC_MAP.md`
- `docs/PROJECT_PLAN.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/CASE_ADMISSION_RULES_v0.md`

## Candidate Slate

### PERF 16

- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0034`
- `PERF_0035`
- `PERF_0052`
- `PERF_0054`
- `PERF_0056`
- `PERF_0062`
- `PERF_0077`
- `PERF_0082`

### CONS 9

- `CONS_0005`
- `CONS_0007`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0024`
- `CONS_0036`
- `CONS_0037`

### PORT 9

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

### LONGTAIL 6

- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

## Draft Findings

### 1. Overall slate shape

The slate preserves the intended `16 / 9 / 9 / 6` pool mix and remains within the current benchmark scope defined for Spark SQL, PostgreSQL, and MySQL.

### 2. Strongest current area

The strongest part of the slate remains the template-backed performance backbone:

- `TPC-H` cases `PERF_0006`, `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`
- `TPC-DS` cases `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`

These cases already appeared in the artifact preflight as `complete_for_selection_review`.

### 3. Replacement logic carried into v0.3

This draft incorporates the replacement preflight recommendations:

- `PERF_0062` in place of `PERF_0002`
- `CONS_0024` in place of `CONS_0001`
- `PORT_0008` in place of `PORT_0002`

It also incorporates the focused SQLStorm longtail review-prep recommendations:

- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

### 4. Source-balance interpretation

The resulting slate is source-balanced enough for a candidate-slate phase:

- template performance remains split across `TPC-H` and `TPC-DS`
- `JOB/IMDB` remains narrow and explicitly supplemental
- consistency remains Calcite-led with a smaller VeriEQL supplement
- portability remains fully inside the current PARROT route family
- longtail now mixes Stack-substrate anchors with direct SQLStorm query-text diversity

## Explicit Non-finality

This draft is not final admission.

It does not assert that any of these cases should now be marked:

- `common-core_candidate`
- `admitted_common_core`
- `admitted_extended`

It is only a draft selection review input for a later human decision.

## Explicit Registry Boundary

This draft does not update registry facts.

In particular, it does not change:

- `benchmark_line`
- `dataset_line`
- `admission_status`
- `promotion_status`
- `next_gap`

All live case facts remain in `inventory/case_registry.csv`.

## Required Human Review Gates

### LONGTAIL SQLStorm gate

`LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` remain `registry not_assessed`.

They therefore require:

- human review
- possible registry alignment before final freeze

This is the most explicit unresolved governance caveat in the slate.

### PORT stress-case gate

The following PORT stress cases carry normalization or comparability caveats and require explicit human approval:

- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`

More broadly, the entire PORT line remains in review-prep territory rather than finalized common-core admission territory.

### JOB or IMDB PERF gate

`PERF_0077` and `PERF_0082` require human approval as real-schema bridges.

They are useful as realism supplements, but they are not as governance-stable as the TPC-backed performance core.

### CONS gate

The consistency line is structurally strong enough for review-prep, but it still remains in manual-review territory:

- package quality and review basis remain open
- plan semantics remain not finally reviewed
- `CONS_0024` is a replacement candidate, not a final admission result

## Draft Recommendation

Use this 40-case slate as the Common-core v0.3 candidate slate for human selection review only.

Before any final freeze, require explicit human decisions on:

1. whether the `JOB/IMDB` bridge cases stay in the candidate slate
2. whether the normalization-caveat PORT cases are approved
3. whether the three SQLStorm LONGTAIL cases can be carried forward despite `registry not_assessed`, or whether a narrow registry/status alignment should happen first

## Bottom Line

This draft supports a plausible Common-core v0.3 candidate slate.

It does not support final admission claims yet.

The strongest unresolved governance issues are:

- LONGTAIL SQLStorm registry alignment
- PORT stress-case approval
- JOB or IMDB bridge approval
