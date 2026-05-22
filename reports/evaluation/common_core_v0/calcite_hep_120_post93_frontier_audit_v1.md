# Calcite HEP Post-93 Frontier Audit v1

## Scope

- Method: `calcite_hep`
- Route: `calcite_hep_same_engine_rewrite`
- Denominator: `common_core_v0_40_same_engine_120`
- Current fail-closed exact ledger: `93/120`
- PG contribution: `31/40`
- Non-PG contribution: `62/80`
- Timing denominator: `NA_not_computed`
- Leaderboard comparable: `no`

This audit re-checks every remaining non-exact row after the retained `PERF_0035` recovery canary, using only retained artifacts. It does not relax exact-match semantics, does not change the denominator, and does not reinterpret cross-engine rows as same-engine evidence.

## Bottom Line

`95/120` is **not safely reachable** from the current retained evidence under the unchanged route, denominator, and checker policy.

Allowed low-risk recovery candidates: `0`

Allowed medium-risk recovery candidates: `0`

Because there are fewer than two allowed candidates, no post-93 recovery canary package is justified in this task.

## Remaining Frontier Summary

Remaining non-exact rows after the retained `93/120` ledger: `27`

Bucket counts:

- `allowed_low_risk_recovery`: `0`
- `allowed_medium_risk_recovery`: `0`
- `disallowed_semantic_mismatch`: `2`
- `disallowed_output_shape_or_wrong_columns`: `0`
- `disallowed_methodology_boundary`: `17`
- `disallowed_parser_or_deep_feature_support`: `8`
- `disallowed_insufficient_evidence`: `0`

## Key Findings

### 1. `PERF_0006:mysql` and `PERF_0006:spark`

These remain explicit semantic mismatches, not formatting mismatches.

Retained execution evidence shows the final numeric value differs:

- source includes `0.075000`
- generated includes `0`

That is not recoverable under the allowed repair families. Any attempt to count these as recoverable would require semantic rewrite logic changes, not package-local rendering or setup repair.

### 2. Remaining `PORT` rows split into two disallowed groups

Some retained `PORT` rows are same-engine-aligned at the source level, but still require parser front-end or deeper Calcite/HEP support expansion beyond the allowed repair families. Those rows are classified as:

- `PORT_0003:pg`
- `PORT_0005:pg`
- `PORT_0008:pg`
- `PORT_0012:pg`
- `PORT_0004:mysql`
- `PORT_0013:mysql`
- `PORT_0022:mysql`
- `PORT_0025:mysql`

These stay in `disallowed_parser_or_deep_feature_support`.

The remaining `PORT` rows are explicit methodology-boundary rows for this route. Retained source SQL uses cross-dialect constructs such as backticks, `DATE_FORMAT`, `TO_CHAR`, or `::` casts under an engine label where those constructs are not same-engine evidence. Those rows stay in `disallowed_methodology_boundary`.

### 3. No remaining output-shape-only frontier

The previously recoverable helper-column and scale-preservation frontier for `PERF_0035:*` has already been consumed by the retained bounded canary that moved the ledger from `90/120` to `93/120`.

No additional rows remain where the retained evidence supports:

- proven internal helper-column removal only, or
- numeric scale preservation only,

without crossing into semantic rewrite or deeper method-support changes.

## Why No Post-93 Canary

The task required a new canary only if at least two rows remained in:

- `allowed_low_risk_recovery`, or
- `allowed_medium_risk_recovery`

This audit finds none.

The safe ceiling therefore remains `93/120` under:

- unchanged exact-match semantics
- unchanged denominator scope
- unchanged checker policy
- no SQLGlot fallback
- no cross-engine fallback
- no reinterpretation of methodology-boundary rows

## Candidate Rows

There are no exact candidate rows for a safe post-93 recovery canary.

## Paper-Safe Frontier Statement

After the retained post-90 recovery work, the remaining `27` non-exact Calcite HEP rows do not expose at least two additional low-risk or medium-risk package-local recovery candidates under the unchanged same-engine route definition. The current safe fail-closed exact ledger therefore remains `93/120` unless new retained evidence demonstrates implementation-level repair without checker relaxation, denominator change, or methodology drift.
