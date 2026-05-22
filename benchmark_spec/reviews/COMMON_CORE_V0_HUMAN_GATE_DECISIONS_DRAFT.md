# COMMON_CORE_V0_HUMAN_GATE_DECISIONS_DRAFT

## Status

This document is a draft.

It is not final admission.
It does not change live registry facts.
It does not update `inventory/case_registry.csv`.
It does not authorize leaderboard rerun or final benchmark freeze.

## Boundary

This is a curation-layer human-gate summary for the Common-core v0.3 candidate slate only.

It does not claim:

- `admitted_common_core`
- final `common-core` freeze
- final `extended` freeze
- final policy change
- final protocol change

Registry facts have not changed.
Leaderboard rerun must wait until any proposed registry alignment is explicitly approved.

## Final Candidate Slate By Pool

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

## Accepted Human Gate Decisions

### PERF human gate

Accepted:

- `PERF_0077`
- `PERF_0082`

Interpretation:

- both may remain in the Common-core v0.3 candidate slate
- both are bounded `JOB/IMDB` real-schema bridge candidates
- both still require taxonomy and status cleanup
- both must not dominate the performance denominator

### PORT human gate

Accepted:

- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`

Interpretation:

- all four may remain in the Common-core v0.3 candidate slate
- they are human-reviewed portability stress candidates
- final reporting must explicitly separate:
  - execution
  - consistency policy
  - normalization caveat
  - speedup-transfer claims
- these cases must not be used to overclaim `SpeedupTransferRate`

### LONGTAIL human gate

Accepted:

- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

Interpretation:

- all three may remain in the Common-core v0.3 candidate slate
- all three are review-ready SQLStorm longtail candidates
- final freeze still requires registry and status alignment because the live registry still marks them `not_assessed`

### CONS replacement gate

Accepted:

- `CONS_0024` as the candidate replacement for `CONS_0001`

Interpretation:

- this is not final admission
- this remains a human-reviewed consistency candidate

### Legacy anchor treatment

The following cases should not be removed from the project and should not be described as low quality:

- `PERF_0002`
- `CONS_0001`
- `PORT_0002`
- `LONGTAIL_0001`

Interpretation:

- they remain legacy anchor / admitted reference / historical sanity cases
- they are not selected for the Common-core v0.3 slate because their currently scanned layout lacks current-generation `result_check` / `plan_check` artifacts

## Unresolved Caveats

### PERF

- `PERF_0062` is still a replacement candidate, not a final admission result
- `PERF_0077` and `PERF_0082` need taxonomy and status cleanup before any final freeze

### CONS

- the consistency line remains under human review
- `CONS_0024` is accepted as the replacement candidate, but still remains not finally admitted

### PORT

- `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025` remain review-slate cases rather than final admitted common-core facts
- `PORT_0012`, `PORT_0013`, `PORT_0022`, and `PORT_0025` carry explicit normalization-caveat handling requirements

### LONGTAIL

- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` are human-approved for the review slate but still need registry/status alignment before final freeze
- `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` remain manual or hybrid Stack-substrate cases with plan-semantics caveats

## Explicit Non-claim Boundary

This draft does not claim:

- that the candidate slate is finally frozen
- that the registry has already been aligned
- that any case has become `admitted_common_core`
- that leaderboard rerun should start now

## Registry Statement

Registry facts have not changed.

Any future writeback based on this document must be separately approved and applied to `inventory/case_registry.csv` through an explicit registry-first update.

## Rerun Gate

Leaderboard rerun must wait until:

1. registry alignment is approved
2. the candidate-slate statuses are written back, if desired
3. the SQLStorm longtail `not_assessed` states are resolved
4. the PORT stress-case normalization caveat framing is explicitly accepted
