# Table 1 Common-core Composition v1

This is a paper-facing contract, not a benchmark protocol change.

This file does not modify the denominator; it records the accepted paper-facing
Table 1 split.

This file does not create a final ranked leaderboard.

All future generated tables should cite this contract and keep Track A / B / C
separated.

## Table

| pool | case_count | primary_rq | selection_criteria | required_artifacts | leaderboard_role | denominator_note | status |
|---|---:|---|---|---|---|---|---|
| `PERF` | `16` | `RQ1/RQ2` | `performance-sensitive analytical rewrites` | `source; positive; negative; schema; witness; result_check; plan_check` | `speedup + correctness` | `part of Common-core v0 40-case denominator` | `accepted_current_paper_split` |
| `CONS` | `9` | `RQ1` | `semantic edge cases and hard negatives` | `source; positive; negative; witness checker` | `correctness / negative guard` | `part of Common-core v0 40-case denominator` | `accepted_current_paper_split` |
| `PORT` | `9` | `RQ3` | `cross-dialect / cross-engine portability cases` | `dialect-specific schema; validation` | `portability table` | `part of Common-core v0 40-case denominator; Table 8 should be PORT9 unless a selected PORT8 subset is explicitly frozen` | `accepted_current_paper_split` |
| `LONGTAIL` | `6` | `RQ1/RQ2` | `realistic or structurally uncommon SQL` | `package; checker artifacts` | `robustness / generalization` | `part of Common-core v0 40-case denominator` | `accepted_current_paper_split` |
| `TOTAL` | `40` | `all` | `unified Common-core v0` | `complete preflight` | `main denominator` | `same-engine Track A expands to 40 cases x 3 engines = 120 rows` | `accepted_current_paper_split` |

## Notes

- Accepted paper-facing split:
  - `PERF = 16`
  - `CONS = 9`
  - `PORT = 9`
  - `LONGTAIL = 6`
  - `TOTAL = 40`
- This contract records the current accepted Table 1 composition only.
- It does not freeze any final leaderboard ordering or method winner.
