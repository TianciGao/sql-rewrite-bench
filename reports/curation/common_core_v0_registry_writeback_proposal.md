# Common-core v0 Registry Writeback Proposal

## Executive Summary

This file is a proposal only.

It does not change live facts in `inventory/case_registry.csv`.
It does not make final admission decisions.
It does not claim `admitted_common_core`.

The proposal reflects the current Common-core v0.3 candidate slate plus the accepted human-gate conclusions:

- `PERF_0077` and `PERF_0082` may remain as bounded `JOB/IMDB` real-schema bridge candidates
- `PORT_0012`, `PORT_0013`, `PORT_0022`, and `PORT_0025` may remain as human-reviewed portability stress candidates
- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` may remain as review-ready SQLStorm candidates, but still require registry alignment before final freeze
- `CONS_0024` is the accepted candidate replacement for `CONS_0001`

## Proposed Writeback Table

The machine-readable proposal is stored in:

- [common_core_v0_registry_writeback_proposal.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_registry_writeback_proposal.csv)

The proposal covers all `40` candidate cases and suggests only conservative values such as:

- `common_core_v0_candidate_review_packet`
- `common_core_v0_candidate`
- `under_common_core_v0_review`
- `human_gate_approved_candidate`
- `not_yet_admitted`

Interpretation:

- no case is proposed as `admitted_common_core`
- no case is proposed as finally frozen
- the writeback would only move the candidate slate into an explicit review packet state if a human approves it later

## Key Proposal Patterns

### Stable staged candidates

Most staged tri-engine cases currently at:

- `benchmark_line = staged`
- `dataset_line = not_yet_admitted`
- `promotion_status = not_under_review` or `not_yet_admitted`
- `admission_status = staged_not_yet_admitted`

are conservatively proposed to move to:

- `proposed_benchmark_line = common_core_v0_candidate_review_packet`
- `proposed_dataset_line = common_core_v0_candidate`
- `proposed_promotion_status = under_common_core_v0_review`
- `proposed_admission_status = not_yet_admitted`

### Human-gate approved special cases

The following cases are proposed with:

- `proposed_promotion_status = human_gate_approved_candidate`

Cases:

- `PERF_0077`
- `PERF_0082`
- `CONS_0024`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

### SQLStorm longtail alignment cases

The following cases are special because their current live registry still says `not_assessed`:

- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

For these, the proposal uses:

- `proposed_benchmark_line = common_core_v0_candidate_review_packet`
- `proposed_dataset_line = common_core_v0_candidate`
- `proposed_promotion_status = human_gate_approved_candidate`
- `proposed_admission_status = not_yet_admitted`
- `proposed_next_gap = SQLStorm review-ready candidate; registry not_assessed; registry alignment required before final freeze`

This keeps the benchmark line field-consistent while preserving the unresolved registry-alignment caveat in `proposed_next_gap`.

## No-live-facts-changed Statement

No live facts have changed.

This proposal does not edit:

- `inventory/case_registry.csv`
- `inventory/source_registry.csv`
- `README.md`
- `docs/EXECUTION_STATUS.md`

Any actual writeback must happen later as a separate approved registry-first update.

## Cases Requiring Human Approval Before Actual Registry Writeback

### PERF

- `PERF_0077`
- `PERF_0082`

Reason:

- `JOB/IMDB` real-schema bridge candidates
- human approved for review slate only
- taxonomy/status cleanup still required

### PORT

- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`

Reason:

- portability stress candidates
- normalization caveat
- human approved for review slate only
- must not be used to overclaim `SpeedupTransferRate`

### LONGTAIL

- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

Reason:

- SQLStorm review-ready candidates
- live registry still says `not_assessed`
- registry alignment required before final freeze

### CONS

- `CONS_0024`

Reason:

- accepted replacement for `CONS_0001`
- still a human-reviewed consistency candidate, not final admission

## Legacy Anchor Handling

The proposal does not recommend project removal or quality downgrade for:

- `PERF_0002`
- `CONS_0001`
- `PORT_0002`
- `LONGTAIL_0001`

These remain legacy anchor / admitted reference / historical sanity cases outside the proposed Common-core v0.3 candidate slate writeback.

## Later Human Inspection Commands

Do not run these as part of this draft.

```bash
git diff -- reports/curation/common_core_v0_registry_writeback_proposal.csv
git diff -- benchmark_spec/reviews/COMMON_CORE_V0_HUMAN_GATE_DECISIONS_DRAFT.md
python - <<'PY'
import csv
from collections import Counter
with open('reports/curation/common_core_v0_registry_writeback_proposal.csv', newline='') as f:
    rows = list(csv.DictReader(f))
print('rows', len(rows))
print('proposed benchmark_line', Counter(r['proposed_benchmark_line'] for r in rows))
print('proposed promotion_status', Counter(r['proposed_promotion_status'] for r in rows))
print('proposed admission_status', Counter(r['proposed_admission_status'] for r in rows))
PY
```

## Bottom Line

This proposal is suitable as a human review packet for a later registry-first writeback decision.

It is not the writeback itself.
