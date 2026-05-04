# PORT_0012_PG_REFERENCE_NORMALIZATION_CHECK_v0

## 1. Status

This is a tracked scratch summary of the bounded PostgreSQL-only normalized-reference check for `PORT_0012`.

This check uses a report-local PostgreSQL reference variant and does not modify the original case file.

## 2. Why Normalization Was Needed

The earlier PORT PG exact-TSV consistency run could not judge `PORT_0012` fairly for the Direct LLM route because the current human positive reference SQL was not PostgreSQL-compatible as written.

Observed incompatibility signals in the original reference SQL:

- `AS DOUBLE`
- `YEAR(...)`

That made the earlier `PORT_0012` reference-check failure a reference-layer problem rather than candidate-route evidence.

## 3. Normalization Policy Used

The report-local PostgreSQL reference variant was created from `cases/PORT/PORT_0012/rewrite_pos_01.sql` with bounded compatibility-only changes:

- `CAST(... AS DOUBLE)` -> `CAST(... AS DOUBLE PRECISION)`
- `YEAR(x)` -> `EXTRACT(YEAR FROM x)`

No broader semantic rewrite was applied.

Original case file remained unchanged.

## 4. LLM Candidate Execution Result

Candidate SQL source:

- `reports/formal_port/llm_translate_port_0012_targeted_call_v0.json`

Observed result:

- route: `LLM_DIRECT_TRANSLATE`
- candidate execution status: `success`
- row count: `1`
- token usage total: `480`

## 5. Normalized-Reference Consistency Result

Observed result:

- normalized reference execution status: `success`
- LLM candidate execution status: `success`
- reference row count: `1`
- LLM row count: `1`
- byte equal: `true`
- normalized equal: `true`
- checker status: `consistent`

Materialized TSV result:

- reference: `66.66666666666667`
- LLM: `66.66666666666667`

Interpretation:

- for this bounded PostgreSQL-only check, the earlier `PORT_0012` blocker was resolved by using a report-local PostgreSQL-compatible reference variant
- under that normalized reference, the Direct LLM candidate matched exactly

## 6. Boundary

- PG-only
- report-local reference variant
- not full translation correctness
- not cross-engine closure
- not full PORT closure
- original case file unchanged

## 7. Recommended Next Action

- keep `PORT_0012` as a failure-analysis / stress case by default, but carry this normalized-reference success as explicit PG-side evidence if a later denominator-expansion decision is reviewed

