# EXPANDED_PORT_RESULTS_CLOSEOUT_v0

## 1. Status

This is expanded PORT results closeout v0.

It consolidates the current RQ3 / PORT evidence after the seed PORT packet and the Batch 2C PORT expansion.

## 2. Executive Summary

Current bounded PostgreSQL-side PORT evidence has expanded from `3` to `6` cases.

- SQLGlot PG success is `4 / 6`
- SQLGlot PG failure is `2 / 6`
- Direct LLM PG success is `6 / 6`
- Batch 2C Direct LLM consistency is `3 / 3` under the selected checker policies

This is useful bounded RQ3 evidence.

It is still PostgreSQL-side evidence only, not full cross-engine translation correctness.

## 3. PORT Denominator / Packets

| packet | cases | current role |
| --- | --- | --- |
| seed PORT packet | `PORT_0004`, `PORT_0012`, `PORT_0022` | bounded seed PG route / consistency packet |
| Batch 2C packet | `PORT_0013`, `PORT_0024`, `PORT_0025` | bounded PG route-matrix and policy-consistency expansion |
| diagnostic / excluded | `PORT_0016` | diagnostic-only under current policy |
| backfill needed | `PORT_0003`, `PORT_0006` | require witness / checker backfill before execution |

Current clean-denominator note:

- the clean denominator policy still remains centered on `PORT_0004 / PORT_0022`
- `PORT_0012` remains a holdout failure-analysis / stress case
- Batch 2C adds bounded PostgreSQL-side route evidence, not automatic denominator expansion

## 4. Table A: PG Route Matrix Summary

| packet | case_id | SQLGlot PG status | SQLGlot failure category | Direct LLM PG status | Direct LLM token usage | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| seed | `PORT_0004` | success | none | success | `440` | both routes executed on PostgreSQL |
| seed | `PORT_0012` | failed | `InvalidDatetimeFormat` | success | `455` in seed matrix, `480` in targeted canary | clear stress-case contrast: SQLGlot fails while Direct LLM executes |
| seed | `PORT_0022` | success | none | success | `422` | both routes executed on PostgreSQL |
| Batch 2C | `PORT_0013` | failed | `UndefinedFunction` | success | `442` | SQLGlot same-dialect transpile produced PG-invalid boolean aggregation |
| Batch 2C | `PORT_0024` | success | none | success | `388` | both routes execute; checker closes under normalized TSV policy |
| Batch 2C | `PORT_0025` | success | none | success | `448` | both routes execute and close cleanly |

Combined route summary:

- SQLGlot PG success / failure: `4 / 2`
- Direct LLM PG success / failure: `6 / 0`
- combined Direct LLM token usage across seed matrix + Batch 2C: `2595`

## 5. Table B: PG-Side Policy / Reference Consistency

| packet | case_id | SQLGlot consistency status | Direct LLM consistency status | checker / normalization policy | interpretation |
| --- | --- | --- | --- | --- | --- |
| seed | `PORT_0004` | inconsistent | consistent | exact TSV only | SQLGlot differs from reference; Direct LLM matches exactly |
| seed | `PORT_0012` | blocked because SQLGlot PG execution failed | consistent against PG-normalized reference | report-local PostgreSQL-normalized reference | route failure and reference-layer PG compatibility are separate issues |
| seed | `PORT_0022` | inconsistent | exact mismatch but normalized consistent | exact TSV plus diagnostic normalization note | SQLGlot appears value-divergent; Direct LLM mismatch is numeric-formatting-only |
| Batch 2C | `PORT_0013` | not checked because PG execution failed | consistent | exact TSV report-local | SQLGlot route fails before checker; Direct LLM closes under exact policy |
| Batch 2C | `PORT_0024` | normalized-policy consistent | normalized-policy consistent | normalized TSV report-local | raw exact mismatch collapses under the allowed normalization rule |
| Batch 2C | `PORT_0025` | exact consistent | exact consistent | exact TSV report-local | both routes close cleanly under exact policy |

## 6. Failure Pattern Summary

- SQLGlot `PORT_0012` `InvalidDatetimeFormat`
  - quoted identifier vs string literal confusion
  - datetime / timestamp formatting
  - dialect normalization failure
  - portability translation failure
- SQLGlot `PORT_0013` `UndefinedFunction`
  - `SUM(boolean)`
  - type / function normalization gap for PostgreSQL
- SQLGlot value mismatches from the seed diagnostic
  - `PORT_0004`: reference `50.0` vs candidate `NULL`
  - `PORT_0022`: reference `0.25` vs candidate `0.0`
- Direct LLM numeric-formatting normalization cases
  - `PORT_0022` in the seed packet
  - `PORT_0024` in Batch 2C
- reference normalization
  - `PORT_0012` required a report-local PG-normalized reference variant because the original positive reference used PostgreSQL-incompatible constructs such as `AS DOUBLE` and `YEAR(...)`

## 7. Interpretation For RQ3

The expanded PORT slice shows that SQLGlot transpile has lower PostgreSQL-side robustness than Direct LLM on the current bounded sample.

The SQLGlot failures are concrete and diagnosable rather than vague route noise:

- `PORT_0012` fails on datetime / identifier normalization
- `PORT_0013` fails on boolean aggregation / function compatibility

Direct LLM shows stronger PostgreSQL execution coverage on the current bounded packet:

- PG success `6 / 6`
- Batch 2C policy-consistent `3 / 3`

That is still bounded route evidence only, not full translation correctness.

This packet also reinforces that the benchmark benefits from separating:

- PostgreSQL execution coverage
- PG-side reference consistency
- broader cross-engine closure

## 8. Boundaries / Non-Claims

- PostgreSQL only
- not MySQL / Spark
- not full cross-engine matrix
- not final translation correctness
- not final PORT leaderboard
- not automatic denominator expansion
- some reference normalization is report-local
- no registry writeback
- no formal review update

## 9. Remaining Work

- MySQL / Spark matrix
- `PORT_0003` / `PORT_0006` backfill
- `PORT_0016` diagnostic policy
- normalized checker policy across all PORT
- full translation correctness protocol
- final denominator expansion decision

## 10. Recommended Next Action

- freeze the current `6`-case PostgreSQL-side PORT packet for paper draft, and keep `PORT_0003`, `PORT_0006`, and `PORT_0016` as future diagnostic / backfill work

## 11. Verification / Non-Modification Note

- only this closeout doc was created
- no SQL / database / model / SQLGlot / checker execution
- no reports were force-added
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched
