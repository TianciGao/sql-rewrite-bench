# LLM-R2 Bounded PG Overlap Dry-run Plan v1

This is a plan only.

- no generation is authorized by this file
- no execution is authorized by this file
- no timing is authorized by this file

## Why bounded PG overlap is the next gate

The next gate is a bounded PostgreSQL-only overlap slice because:

- current LLM-R2 evidence is PG-only bounded historical evidence
- MySQL and Spark support are not recovered
- runner, logical-plan substrate, output SQL extraction, generated SQL
  retention, and reproducibility must be tested before any broader
  `120`-row generation discussion

This plan does not create `120`-row LLM-R2 evidence. It only defines a future
reviewable dry-run shape that a human may later approve.

## Candidate slice selection logic

The slice is intentionally small and PostgreSQL-only.

Selection goals:

- keep the slice comfortably below full `PG40`
- exercise multiple case styles under the same-engine denominator
- include performance-style rows useful for runner and extraction checks
- include consistency-style rows useful for checker handoff readiness
- include long-tail-style rows so the slice is not limited to the simplest
  patterns
- avoid any claim that selected rows are already generated or executed

## Future dry-run objectives

1. runner invocation boundary
2. logical-plan substrate check
3. output SQL extraction check
4. generated SQL retention path check
5. failure bucket recording
6. checker handoff readiness

## Stop conditions

Stop the future dry-run immediately if:

- runner cannot load
- logical-plan substrate fails before SQL extraction
- `output_sql` cannot be extracted
- generated SQL path cannot be retained
- failure bucket cannot be assigned

## Pass criteria for a future human-approved dry-run

A future dry-run would count as passing this gate only if:

- the runner boundary is entered safely without invoking unauthorized DB work
- a logical-plan substrate status can be recorded per attempted row
- output-SQL extraction status can be recorded per attempted row
- generated SQL retention path is explicit and artifact-complete when SQL exists
- failure buckets can be assigned under the Stage-0 fail-closed policy
- checker handoff readiness can be recorded without claiming execution evidence

## Required artifacts if a future dry-run is approved

If a future dry-run is later approved, it must produce at minimum:

- run-level `run_results.json`
- run-level `run_event_long.csv`
- per-row attempt metadata
- generated SQL files only when actually produced
- explicit failure-bucket assignment for non-generated rows
- retained generated-SQL retention-path evidence
- retained checker-handoff readiness notes

## Planning phases

| Phase | Purpose |
|---|---|
| `phase_1` | freeze bounded PG overlap slice |
| `phase_2` | confirm runner invocation boundary expectations |
| `phase_3` | confirm logical-plan and extraction observation contract |
| `phase_4` | confirm retention-path and failure-bucket contract |
| `phase_5` | confirm checker-handoff readiness notes |
| `phase_6` | require explicit human approval before any dry-run |

## Explicit non-claims

- this is not a dry-run result
- this does not authorize generation
- this does not authorize execution
- this does not authorize timing
- this does not recover MySQL or Spark support
- this does not create a result card or proposed row
- this does not update `method_comparison_summary_v2`
