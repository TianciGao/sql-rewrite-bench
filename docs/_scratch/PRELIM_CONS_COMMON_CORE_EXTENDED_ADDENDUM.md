# Preliminary CONS Common-Core / Extended Addendum Proposal

- Status: scratch proposal / not admitted / not registry-backed decision / not registry writeback
- Date: 2026-05-01

## 1. Purpose

This proposal evaluates the governed CONS subset as a semantic addendum to the current benchmark discussion.

The goal is to identify consistency cases that may later complement the existing PERF+PORT seed with a small, interpretable semantic-denominator layer.

This is a proposal only. It is not admitted, not registry writeback, not a common-core promotion, and not a final benchmark-line decision.

## 2. Selection Principles

- current-generation result and plan governance
- clear semantic goal
- clear positive rewrite
- clear hard negative
- taxonomy tags present
- no known mismatch
- compact enough for fair semantic comparison
- not primarily stress / failure-analysis only

## 3. Governed Subset Summary

The current governed CONS subset contains `17` cases.

For all `17` cases:

- case-root `runs/result_check.json` is present
- case-root `runs/plan_check.json` is present
- registry status is `staged_not_yet_admitted`
- cases are not admitted
- plan semantics are not formally reviewed

The governed subset spans both current consistency source families:

- `Calcite`
- `VeriEQL`

This proposal treats that governed subset as a bounded semantic addendum only. It does not fold CONS into the existing PERF+PORT seed at this stage.

## 4. Proposed 5-Case CONS Add-On Seed Table

| case_id | source_family | proposed role | evidence/governance status | key semantic pattern | why included | blocker before final adoption | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0007` | Calcite | semantic_baseline | staged; tri-engine; case-root result and plan governance present | compact correlated `EXISTS` decorrelation baseline | clean, compact, and easy to explain in a fair semantic comparison | ordinary human review only | low |
| `CONS_0012` | Calcite | decorrelation_baseline | staged; tri-engine; case-root result and plan governance present | `LIMIT` / `OFFSET` threshold rewrite | adds a governed threshold-style decorrelation case with a very clear hard negative | explicit framing around `OFFSET` semantics | low |
| `CONS_0024` | Calcite | outer_join_baseline | staged; tri-engine; case-root result and plan governance present | outer join guarded by grouped correlated `EXISTS` | adds compact outer-join and grouped-subquery coverage without moving into the most pathological stress cases | explanation is slightly more involved than the simplest baselines | medium |
| `CONS_0031` | VeriEQL | semantic_baseline | staged; tri-engine; case-root result and plan governance present | compact `EXISTS` and `NOT EXISTS` decorrelation | strongest compact VeriEQL semantic baseline and good source-family counterweight to Calcite | ordinary human review only | low |
| `CONS_0034` | VeriEQL | aggregation_baseline | staged; tri-engine; case-root result and plan governance present | CASE expression aggregation rewrite | adds governed VeriEQL aggregation coverage with a clear positive rewrite | expression-heavy aggregation semantics should be noted during human review, but the case remains a good semantic addendum candidate | medium |

This 5-case add-on seed is recommended for human review only. It is not admitted, not registry writeback, and not merged into the main PERF+PORT seed.

Additional seed caveats:

- `CONS_0034` remains in the add-on seed because its aggregation rewrite value is strong, but its expression-heavy aggregation semantics should be noted during human review.
- `CONS_0005` is valuable, but it should be treated as null-sensitive anti-join stress unless human review decides otherwise.
- `CONS_0037` is valuable, but it should be treated as duplicate-sensitive outer-join aggregate stress unless human review decides otherwise.
- CONS remains a separate addendum and is not merged into the main PERF+PORT seed yet.

## 5. Extended CONS Set

- Null / anti-join / null-semantics stress:
  - `CONS_0005`
  - Expected use: null-sensitive anti-join stress and semantic robustness where `NOT IN` / null behavior is the main point rather than a compact denominator baseline.

- Null / boolean semantic stress:
  - `CONS_0011`, `CONS_0017`, `CONS_0032`, `CONS_0040`
  - Expected use: semantic robustness and null-semantics stress, especially where boolean projection or three-valued logic pressure is the main value.

- Expression-heavy aggregate:
  - `CONS_0006`, `CONS_0034`
  - Expected use: aggregation stress and robustness under CASE-heavy or expression-dense aggregate factoring.

- Set operation / long-tail structure:
  - `CONS_0009`, `CONS_0040`
  - Expected use: decorrelation stress and plan-observability examples for long-tail semantic structure.

- Non-equi correlated aggregate:
  - `CONS_0023`
  - Expected use: semantic robustness for non-equi correlated aggregation.

- Predicate-pushdown / HAVING gap:
  - `CONS_0036`
  - Expected use: aggregation stress and plan-observability discussion around grouped-filter scope.

- Duplicate-sensitive outer-join aggregate stress:
  - `CONS_0010`, `CONS_0037`
  - Expected use: duplicate sensitivity and semantic robustness under left-join aggregate rewrites.

- Calibration / governance-normalization only:
  - `CONS_0029`
  - Expected use: narrow calibration support only, not a strong reporting anchor.

## 6. Explicit Exclusions and Backlog

- `CONS_0001`–`CONS_0004` remain legacy / anchor / partial backlog rather than current addendum candidates.
- Broader CONS cases outside the governed `17` still need more governance normalization before broader candidate screening.
- This addendum does not include LONGTAIL.
- This addendum does not alter the existing PERF+PORT seed proposal.

## 7. Open Blockers

- human review
- plan semantics not formally reviewed
- broader CONS governance normalization
- final common-core / extended decision still pending

## 8. Recommended Next Step

Do not update registry yet.

Keep CONS as a separate addendum for human review rather than merging it into the existing PERF+PORT seed proposal now.

Reasonable next actions are:

- human review of the proposed `5`-case CONS add-on seed
- a later decision on whether `CONS_0005` and `CONS_0037` should remain extended-only stress cases

This document should remain a scratch proposal only until that review occurs.
