# FORMAL_PORT_PG_TRANSLATION_CONSISTENCY_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the bounded PostgreSQL-only PORT translation consistency run.

This summary records PG-side reference consistency only.

## 2. Preflight

Preflight command:

- `python -m scripts.cli formal-port-pg-translation-consistency-preflight`

Observed preflight result:

- ready records: `5 / 6`
- blocked records: `1 / 6`
- SQLGlot blocked:
  - `PORT_0012`
  - blocker: existing PG route execution already failed with `InvalidDatetimeFormat`
- LLM ready:
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`

## 3. SQLGlot PG Reference Consistency

Route status:

- PG executable: `2 / 3`
- blocked / failed PG route case:
  - `PORT_0012`
  - failure category: `InvalidDatetimeFormat`

Reference-check result on executable cases:

- checked: `2`
- consistent: `0`
- inconsistent: `2`
- failed during checker run: `0`
- PG reference consistency rate: `0.0`

Case detail:

- `PORT_0004`
  - row count equal: `true`
  - byte equal: `false`
  - checker status: `inconsistent`
- `PORT_0022`
  - row count equal: `true`
  - byte equal: `false`
  - checker status: `inconsistent`

## 4. Direct LLM PG Reference Consistency

Route status:

- PG executable from existing route evidence: `3 / 3`

Reference-check run result:

- checked: `2`
- consistent: `1`
- inconsistent: `1`
- execution failed: `1`
- PG reference consistency rate over checked records: `0.5`

Case detail:

- `PORT_0004`
  - row count equal: `true`
  - byte equal: `true`
  - checker status: `consistent`
- `PORT_0012`
  - checker status: `execution_failed`
  - failure category: `UndefinedObject`
  - failure note: PG reference SQL uses `AS DOUBLE`, which PostgreSQL rejected
- `PORT_0022`
  - row count equal: `true`
  - byte equal: `false`
  - checker status: `inconsistent`

## 5. PORT_0012 Interpretation

`PORT_0012` now has three distinct PG-side facts:

- SQLGlot route execution failed with `InvalidDatetimeFormat`
- Direct LLM route execution succeeded in the targeted canary and the bounded PG route matrix
- PG reference consistency was not closed for the LLM route because the current positive reference SQL failed to execute on PostgreSQL during the exact-TSV check

This means the current blocker on `PORT_0012` reference consistency is different from the earlier SQLGlot route failure.

## 6. Exact TSV Notes

Checker mode:

- `exact_tsv_report_local`

Observed implication:

- row-count equality did not imply byte equality
- both SQLGlot executable cases and one LLM case produced single-row outputs with exact-value mismatch against the current PG-side reference output

## 7. Boundaries

- PG-side reference consistency only
- not translation correctness
- not MySQL / Spark
- not cross-engine closure
- not full PORT closure
- not denominator expansion
- not checker-backed benchmark admission evidence

## 8. Recommended Next Action

- review the current PostgreSQL reference SQL layer, especially `PORT_0012`, before treating PORT PG reference consistency as a stable denominator-expansion signal

