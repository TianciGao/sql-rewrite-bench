# Table 10 Observability Two-panel Guidance V1

This note explains how to present `Table 10` after the reviewed PG attribution packet.

## Panel split

- `Table 10A`:
  - selected PostgreSQL exact-timed plan attribution
  - cites [table10_plan_attribution_case_study_v5.csv](reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v5.csv)
  - packet facts: `24/24` parse success, `21/24` buffer/runtime-only, `22/24` low confidence, `2/24` medium confidence
- `Table 10B`:
  - failure-side observability diagnostic
  - cites [table10_failure_exemplar_selection_v1.csv](reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_failure_exemplar_selection_v1.csv)
  - retained exemplar: `CONS_0024 / pg / Direct LLM / mismatch`

## Why two panels

- `Table 10A` and `Table 10B` answer different questions.
- `10A` asks how selected exact-timed PostgreSQL rows can be inspected with node/runtime/buffer evidence.
- `10B` asks whether failure-side observability is concrete and case-identified.

## What to say

- Table 10A is selected PG plan attribution only.
- Table 10B is separate failure-side diagnostic evidence.
- Scalar timing alone is insufficient; node/runtime/buffer evidence helps inspect why a rewrite changed performance.

## What not to say

- Do not call Table 10A denominator-wide causal attribution.
- Do not merge the failure exemplar into the 24-row exact-timed denominator.
- Do not claim full PlanParseRate, full NodeAlignmentCoverage, or global causal attribution.

中文说明：Table 10 最好用两个 panel 呈现。`10A` 讲 selected exact-timed PG attribution，`10B` 讲 failure-side diagnostic。这样读者不会把 failure exemplar 错当成 24-row attribution denominator 的一部分。
