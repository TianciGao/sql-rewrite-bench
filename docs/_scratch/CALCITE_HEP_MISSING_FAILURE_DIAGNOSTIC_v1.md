# CALCITE_HEP_MISSING_FAILURE_DIAGNOSTIC_v1

## 0. Purpose And Boundary

This is a read-only diagnostic for the Calcite HEP missing-case expansion failures.

- no Calcite rerun
- no DB/checker/speedup
- no registry writeback

## 1. Prior Batch Recap

The existing bounded Calcite HEP subset remains:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

The missing-case checker batch targeted:

- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0052`
- `PERF_0063`

Observed outcome:

- five cases reached `generation_status = generated` and `output_sql_extracted = true`, but checker recorded `candidate_sql_not_ready`
- `PERF_0063` failed earlier with `generation_status = generation_failed`
- `PERF_0063` failure message shows a Calcite validation-time function-signature mismatch for `substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)`
- `speedup_status = not_run`

## 2. Artifact Inventory

| case_id | source SQL path exists | candidate SQL path exists | generation report exists | checker JSON exists | candidate result path exists/missing |
| --- | --- | --- | --- | --- | --- |
| `PERF_0013` | yes | yes | yes | yes | missing |
| `PERF_0017` | yes | yes | yes | yes | missing |
| `PERF_0019` | yes | yes | yes | yes | missing |
| `PERF_0024` | yes | yes | yes | yes | missing |
| `PERF_0052` | yes | yes | yes | yes | missing |
| `PERF_0063` | yes | yes | yes | no | missing |

Interpretation:

- the five `candidate_sql_not_ready` cases are not missing candidate SQL files
- they are missing downstream materialization because checker never considered the candidates ready to execute
- `PERF_0063` never reached checker output creation

## 3. Candidate SQL Static Inspection

### PERF_0013

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none
- excerpt:

```sql
SELECT "nation"."n_name", CASE WHEN COUNT("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")) = 0 THEN NULL ELSE COALESCE(SUM("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")), 0) END AS "revenue"
FROM "customer",
"orders",
"lineitem",
"supplier",
"nation",
"region"
...
ORDER BY 2 DESC
```

- wrapper readiness reason:
  - checker JSON shows `real_route_record_exists = false`
  - checker JSON shows `emitted_sql_mode = missing`
  - generation report for the same case shows `emitted_sql_mode = calcite_rel_to_sql` and `emitted_sql_is_calcite_generated = true`

### PERF_0017

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none
- excerpt:

```sql
SELECT "customer"."c_custkey", "customer"."c_name", CASE WHEN COUNT("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")) = 0 THEN NULL ELSE COALESCE(SUM("lineitem"."l_extendedprice" * (1 - "lineitem"."l_discount")), 0) END AS "revenue", ...
...
FETCH NEXT 20 ROWS ONLY
```

- wrapper readiness reason:
  - same mismatch as `PERF_0013`
  - generated SQL is present and syntactically SQL-like
  - checker marked it not ready because the expected real-route record was not found

### PERF_0019

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none
- excerpt:

```sql
SELECT "t1"."c_count", COUNT(*) AS "custdist"
FROM (SELECT COUNT("orders"."o_orderkey") AS "c_count"
FROM "customer"
LEFT JOIN "orders" ON "customer"."c_custkey" = "orders"."o_custkey" AND "orders"."o_comment" NOT LIKE '%express%deposits%'
...
```

- wrapper readiness reason:
  - same shared failure mode
  - SQL file exists and is usable-looking by static inspection
  - checker failed before any PostgreSQL materialization because route metadata was treated as missing

### PERF_0024

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none
- excerpt:

```sql
SELECT "supplier"."s_name", "supplier"."s_address"
FROM "supplier",
"nation"
WHERE "supplier"."s_suppkey" IN (SELECT "ps_suppkey"
...
ORDER BY "supplier"."s_name"
```

- wrapper readiness reason:
  - same shared failure mode
  - no static evidence of placeholder, empty output, or fragment-only output

### PERF_0052

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none
- excerpt:

```sql
SELECT "customer"."c_customer_id"
FROM (SELECT "store_returns"."sr_customer_sk" AS "ctr_customer_sk", ...
...
FETCH NEXT 100 ROWS ONLY
```

- wrapper readiness reason:
  - same shared failure mode
  - candidate SQL appears structurally complete

### PERF_0063

- candidate exists: yes
- non-empty: yes
- starts with `SELECT` or `WITH`: yes
- statement count: `1`
- obvious SQL surface issue: none in the emitted parse-only text
- excerpt:

```sql
SELECT "ca_zip", SUM("cs_sales_price")
FROM "catalog_sales",
"customer",
"customer_address",
"date_dim"
WHERE "cs_bill_customer_sk" = "c_customer_sk" AND "c_current_addr_sk" = "ca_address_sk" AND ("substr"("ca_zip", 1, 5) IN ...
```

- wrapper readiness reason:
  - different from the other five
  - generation report shows `emitted_sql_mode = calcite_parse_only`
  - `validation_succeeded = false`
  - `sql_to_rel_succeeded = false`
  - `hep_planner_succeeded = false`

## 4. PERF_0063 Function Signature Diagnosis

The exact mismatch is:

- `substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)`

The triggering source SQL construct is the predicate:

```sql
substr(ca_zip, 1, 5)
```

Likely root cause:

- this is primarily a Calcite function typing / validation issue
- the numeric literals `1` and `5` are being treated under a generic numeric signature rather than the integer-like signature Calcite expects for `substr`
- this is closer to input normalization or adapter function typing than to output cleanup

Why this is not the same failure as the other five:

- `PERF_0063` fails before `sql_to_rel` and before `hep_planner`
- the other five cases reach `calcite_rel_to_sql`
- therefore `PERF_0063` is a route-level validation problem, while the other five are downstream output-contract problems

## 5. Failure Classification

| case_id | classification | evidence | likely_fix | risk |
| --- | --- | --- | --- | --- |
| `PERF_0013` | `wrapper_readiness_gate_too_strict` | candidate SQL exists, one statement, starts with `SELECT`; checker says `real_route_record_exists=false`, `emitted_sql_mode=missing` | implement output SQL cleanup/readiness fix and rerun checker only | medium |
| `PERF_0017` | `wrapper_readiness_gate_too_strict` | same shared pattern as `PERF_0013` | implement output SQL cleanup/readiness fix and rerun checker only | medium |
| `PERF_0019` | `wrapper_readiness_gate_too_strict` | same shared pattern as `PERF_0013` | implement output SQL cleanup/readiness fix and rerun checker only | medium |
| `PERF_0024` | `wrapper_readiness_gate_too_strict` | same shared pattern as `PERF_0013` | implement output SQL cleanup/readiness fix and rerun checker only | medium |
| `PERF_0052` | `wrapper_readiness_gate_too_strict` | same shared pattern as `PERF_0013` | implement output SQL cleanup/readiness fix and rerun checker only | medium |
| `PERF_0063` | `calcite_function_signature_mismatch` | generation report shows `ValidationException` on `substr(ca_zip, 1, 5)` | patch Calcite input function normalization and rerun generation/checker only | high |

Batch-level classification:

- `mixed_output_contract_and_function_signature_failures`

## 6. Recommended Next Step

- `implement output SQL cleanup/readiness fix and rerun checker only`

Reason:

- the five `candidate_sql_not_ready` cases do not look like genuine SQL-generation failures
- the checker runner is reading `reports/formal_expansion/calcite_hep_real_route_canary_v0.json`, while the missing-case batch generated `reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json`
- that mismatch explains `real_route_record_exists=false` and `emitted_sql_mode=missing`
- `PERF_0063` still needs separate function-signature normalization work, but it is not the dominant shared blocker for the other five cases

## 7. Non-Modification Note

No Calcite rerun, no DB/checker/speedup, no model/API, and no registry/review/rules/`EXECUTION_STATUS`/case changes occurred for this diagnostic. The taxonomy note files remained untouched.
