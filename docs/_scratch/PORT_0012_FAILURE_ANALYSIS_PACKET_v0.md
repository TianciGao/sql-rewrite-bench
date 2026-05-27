# PORT_0012_FAILURE_ANALYSIS_PACKET_v0

## 1. Status

This is a tracked scratch failure-analysis packet for `PORT_0012`.

This packet records the current `PORT_0012` failure / holdout status after:

- the completed baseline route readiness sweep
- the denominator freeze proposal that keeps `PORT_0012` outside the clean PORT denominator

This packet is analysis only.

This packet is not:

- a registry writeback
- a denominator admission decision
- a formal review update
- a correctness claim
- a translation correctness claim
- a leaderboard result
- a rerun request

## 2. Case Identity And Route Role

### 2.1 Case identity

- `case_id`: `PORT_0012`
- `primary_pool`: `portability`
- `source_family`: `PARROT`
- `source_dialect`: `postgres_like_candidate`
- `target_engines`:
  - `pg`
  - `mysql`
  - `spark`
- portability focus:
  - `date_time_semantics`
  - `boolean_semantics`

### 2.2 Source SQL shape

Current `source.sql`:

```sql
SELECT CAST( SUM( CASE WHEN "sex" = 'F' THEN 1 ELSE 0 END ) AS REAL ) * 100 / NULLIF( COUNT( "id" ) , 0 ) FROM "patient" WHERE "diagnosis" = 'RA' AND TO_CHAR( CAST( "birthday" AS TIMESTAMP ) , 'YYYY' ) = '1980'
```

Observed shape:

- quoted identifiers are used
- date/time formatting is central to the filter
- the case is same-dialect-looking for PostgreSQL, but still treated as part of the portability route

### 2.3 Current route role

Current role in the PORT route:

- included in SQLGlot transpile first smoke
- included in LLM translate prompt dry-run
- not included in the clean LLM translate canary subset

Current denominator posture:

- not part of the clean PORT denominator
- holdout failure-analysis case

## 3. Existing Evidence Inspected

Tracked planning / status references:

- `docs/_scratch/BASELINE_ROUTE_READINESS_CLOSEOUT_v0.md`
- `docs/_scratch/PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0.md`
- `docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`

Baseline smoke reports inspected:

- `reports/baseline_smoke/sqlglot_transpile_preflight_v0.json`
- `reports/baseline_smoke/sqlglot_transpile_pg_canary_v0.json`
- `reports/baseline_smoke/sqlglot_transpile_pg_summary_v0.json`
- `reports/baseline_smoke/llm_direct_translate_prompt_packages_v0.json`

Case package and registry evidence inspected:

- `cases/PORT/PORT_0012/source.sql`
- `cases/PORT/PORT_0012/manifest.yaml`
- `cases/PORT/PORT_0012/rewrite_pos_01.sql`
- `cases/PORT/PORT_0012/rewrite_neg_01.sql`
- `inventory/case_registry.csv`

Missing report status:

- none of the listed baseline-smoke reports were missing at audit time

## 4. SQLGlot Transpile Failure Analysis

### 4.1 Preflight status

From `reports/baseline_smoke/sqlglot_transpile_preflight_v0.json`:

- preflight parse status: `success`
- preflight transpile status: `success`
- source dialect used: `postgres`
- target dialect: `postgres`

The preflight record shows that SQLGlot could parse and transpile the case, so this was not a parser-availability or missing-tool failure.

### 4.2 Generated SQL issue signal

The preflight `transpiled_sql_preview` for `PORT_0012` is:

```sql
SELECT CAST(CAST(SUM(CASE WHEN 'sex' = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 AS DOUBLE PRECISION) / NULLIF(NULLIF(COUNT('id'), 0), 0) FROM "patient" WHERE 'diagnosis' = 'RA' AND TO_CHAR(CAST('birthday' AS TIMESTAMPTZ), 'YYYY') = '1980'
```

Observed issue:

- quoted identifiers such as `"sex"`, `"id"`, `"diagnosis"`, and `"birthday"` were converted into string literals such as `'sex'`, `'id'`, `'diagnosis'`, and `'birthday'`

This is the central failure signal.

### 4.3 PG execution status

From `reports/baseline_smoke/sqlglot_transpile_pg_canary_v0.json`:

- execution status: `failed`
- failure category: `InvalidDatetimeFormat`
- source dialect used: `postgres`
- target dialect: `postgres`

Recorded error summary:

- PostgreSQL rejected `CAST('birthday' AS TIMESTAMPTZ)`
- the error message indicates invalid timestamp-with-time-zone input syntax for `"birthday"`

### 4.4 Summary-layer interpretation

From `reports/baseline_smoke/sqlglot_transpile_pg_summary_v0.json`:

- preflight parse status: `success`
- preflight transpile status: `success`
- execution status: `failed`
- generated SQL issue note:
  - transpiled SQL appears to cast quoted identifier literal `'birthday'` as timestamp; needs followup

### 4.5 Why this looks like translation/generated-SQL failure rather than infrastructure failure

Reasons:

- preflight parse succeeded
- preflight transpile succeeded
- the same execution harness successfully ran `PORT_0004` and `PORT_0022`
- the failure is case-local and SQL-local
- the generated SQL preview already exposes the identifier-to-string-literal corruption

Current interpretation:

- this appears to be a generated-SQL translation failure
- it does not look like a PostgreSQL environment failure
- it does not look like a missing-schema or missing-tooling failure

## 5. LLM Translate Holdout Analysis

### 5.1 Prompt dry-run status

From `reports/baseline_smoke/llm_direct_translate_prompt_packages_v0.json`:

- prompt package status for `PORT_0012`: `ready`
- source dialect: `postgres`
- target dialect: `postgres`

The dry-run record also carries the SQLGlot failure context in its notes:

- `sqlglot_transpile_preflight_status=success`
- `sqlglot_transpile_pg_execution_status=failed`
- `sqlglot_transpile_execution_layer_failure_note=quoted identifier literal 'birthday' was treated as timestamp input`
- `sqlglot_transpile_failure_category=InvalidDatetimeFormat`

### 5.2 Was model call run for `PORT_0012`?

No model-call result was inspected for `PORT_0012` in the clean canary route.

Current tracked interpretation:

- `PORT_0012` was held out
- it was not part of the clean LLM translate canary subset

### 5.3 Why it was held out

The current route documents already state the reason:

- SQLGlot transpile had already exposed an execution-layer failure on `PORT_0012`
- the case should not be mixed into the clean LLM translate subset before failure-analysis is frozen

### 5.4 Clean PORT canary subset status

The clean PORT canary subset remains:

- `PORT_0004`
- `PORT_0022`

These two cases form the current clean Step 4b LLM translate subset.

## 6. Denominator Implication

Current denominator implication:

- the clean PORT denominator remains:
  - `PORT_0004`
  - `PORT_0022`
- `PORT_0012` should remain outside the clean denominator for now
- `PORT_0012` should remain a tracked holdout until failure analysis and any optional targeted canary decision are complete

Important interpretation rule:

- do not describe the clean 2-case subset as full PORT closure

## 7. Failure Taxonomy / Bucket Assignment

Current careful bucket assignment:

- datetime / timestamp formatting
- quoted identifier vs string literal confusion
- dialect normalization / identifier-preservation failure
- generated SQL semantic/syntactic ambiguity
- portability translation failure

Most direct current bucket:

- quoted identifier vs string literal confusion leading to datetime/timestamp formatting failure in generated SQL

What should not be claimed yet:

- final translation incorrectness scoring
- final semantic non-equivalence judgment
- benchmark-level portability judgment for the whole PORT route

## 8. Recommended Next Action

- Keep `PORT_0012` as a tracked failure-analysis / stress case and only run a targeted LLM translate canary later if the formal PORT denominator policy needs a 3-case expansion decision.

## 9. Non-Goals / Claim Boundaries

- no registry writeback
- no denominator admission decision
- no formal review update
- no correctness claim
- no translation correctness claim
- no leaderboard result
- no rerun request
- no semantic equivalence claim

## 10. Verification / Non-Modification Note

- only this failure-analysis packet was created
- no database workloads were run
- no SQL was executed
- no LLM calls were made
- no SQLGlot generation was run
- no Calcite was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
