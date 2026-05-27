# FORMAL_PORT_RESULTS_CLOSEOUT_v0

## 1. Status

This is the formal PORT results closeout packet for the current RQ3 evidence.

This packet consolidates the current bounded PORT PostgreSQL route, consistency, diagnostic, and `PORT_0012` stress-case evidence into one paper-facing closeout.

## 2. Executive Summary

Current bounded PostgreSQL PORT results are:

- SQLGlot PG route matrix: `2 / 3`
- Direct LLM PG route matrix: `3 / 3`
- `PORT_0012` stress contrast:
  - SQLGlot fails on PostgreSQL
  - Direct LLM succeeds on PostgreSQL
  - Direct LLM also matches a report-local PostgreSQL-normalized reference on `PORT_0012`

This is useful bounded RQ3 evidence.

It is not full PORT closure.

## 3. Scope

Cases:

- `PORT_0004`
- `PORT_0012`
- `PORT_0022`

Routes:

- `SQLGLOT_TRANSPILE`
- `LLM_DIRECT_TRANSLATE`

Engine:

- PostgreSQL only

## 4. Table A: PORT PG Route Matrix

| case_id | SQLGlot PG status | SQLGlot failure category | LLM call / extraction / PG status | LLM token usage | interpretation |
| --- | --- | --- | --- | --- | --- |
| `PORT_0004` | success | none | success / success / success | `440` | both routes executed on PostgreSQL |
| `PORT_0012` | failed | `InvalidDatetimeFormat` | success / success / success | `455` in bounded matrix, `480` in targeted canary | direct contrast case: SQLGlot fails while Direct LLM executes |
| `PORT_0022` | success | none | success / success / success | `422` | both routes executed on PostgreSQL |

Matrix summary:

- SQLGlot PG success / failure: `2 / 1`
- Direct LLM PG success / failure: `3 / 0`
- Direct LLM total token usage in the bounded PG matrix: `1317`

## 5. Table B: PG-Side Reference Consistency

| case_id | SQLGlot consistency status | LLM consistency status | checker mode / normalization note | interpretation |
| --- | --- | --- | --- | --- |
| `PORT_0004` | inconsistent | consistent | exact TSV only | SQLGlot differs from reference; Direct LLM matches exactly |
| `PORT_0012` | blocked because SQLGlot PG execution failed | consistent against PG-normalized reference | original reference SQL was not PostgreSQL-compatible; report-local normalized reference used | SQLGlot route failure and reference-layer incompatibility are distinct issues |
| `PORT_0022` | inconsistent | exact mismatch but normalized consistent | exact TSV plus diagnostic normalization note | SQLGlot appears value-divergent; Direct LLM mismatch is numeric-formatting-only |

Current PG-side consistency interpretation:

- SQLGlot executable cases checked: `2`
  - exact consistent: `0`
  - exact inconsistent: `2`
- Direct LLM:
  - exact consistent: `1`
  - exact inconsistent: `1`
  - `PORT_0012` now closes under the bounded report-local normalized-reference check

## 6. PORT_0012 Case Study

`PORT_0012` is the clearest stress-case contrast in the current PORT packet.

SQLGlot failure mechanism:

- PostgreSQL execution failed with `InvalidDatetimeFormat`
- failure packet shows quoted identifiers such as `"birthday"` were converted into string literals such as `'birthday'`
- this led PostgreSQL to reject timestamp casting over a string literal rather than an identifier value

Direct LLM route:

- targeted canary succeeded on PostgreSQL
- bounded PG route matrix also succeeded on PostgreSQL
- PG-normalized reference follow-up also succeeded and matched exactly

Why original reference SQL needed report-local normalization:

- original positive reference SQL used PostgreSQL-incompatible constructs:
  - `AS DOUBLE`
  - `YEAR(...)`
- bounded report-local PostgreSQL normalization used:
  - `CAST(... AS DOUBLE)` -> `CAST(... AS DOUBLE PRECISION)`
  - `YEAR(x)` -> `EXTRACT(YEAR FROM x)`

Result:

- normalized reference execution: `success`
- Direct LLM candidate execution: `success`
- byte equal: `true`
- normalized equal: `true`
- matched value: `66.66666666666667`

Important boundary:

- the original case file was not modified

## 7. Failure / Diagnostic Buckets

- SQLGlot value mismatch on `PORT_0004`
  - reference `50.0` vs candidate `NULL`
- SQLGlot value mismatch on `PORT_0022`
  - reference `0.25` vs candidate `0.0`
- SQLGlot `PORT_0012` execution failure
  - `InvalidDatetimeFormat`
  - quoted identifier vs string literal confusion
  - datetime timestamp formatting
  - dialect normalization failure
  - portability translation failure
- Direct LLM `PORT_0022`
  - exact mismatch but normalized-consistent numeric-formatting-only case
- `PORT_0012` reference SQL PostgreSQL compatibility issue
  - `AS DOUBLE`
  - `YEAR(...)`

## 8. Boundaries / Non-Claims

- not full translation correctness
- not MySQL / Spark cross-engine closure
- not final PORT leaderboard
- not automatic clean denominator expansion
- report-local normalized reference only for `PORT_0012`
- original case files unchanged
- no registry writeback
- no formal review update

## 9. What Can Be Drafted In The Paper

- bounded PostgreSQL PORT route matrix table
- `PORT_0012` stress-case comparison between SQLGlot and Direct LLM
- diagnostic table for SQLGlot vs Direct LLM failure / mismatch modes
- report-local reference-normalization caveat for `PORT_0012`

## 10. Remaining Work

- MySQL / Spark execution matrix if needed
- normalized checker policy for PORT as a whole
- denominator expansion decision for `PORT_0012`
- full translation correctness protocol
- final PORT leaderboard packaging

## 11. Recommended Next Action

- decide whether `PORT_0012` should remain a failure-analysis case or be promoted into the clean PORT denominator after PG-normalized-reference consistency

## 12. Verification / Non-Modification Note

- only this closeout doc was created
- no SQL / database / model / SQLGlot / checker execution
- no reports were force-added
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched

