# CALCITE_HEP_PERF_0063_FUNCTION_SIGNATURE_PREFLIGHT_v1

## 0. Purpose And Boundary

This is a read-only function-signature preflight for `PERF_0063` only.

- no Calcite rerun
- no DB/checker/speedup
- no code changes
- no registry writeback

## 1. Existing Evidence Recap

Calcite HEP now has bounded PG-only checker+speedup evidence on `9/10` target cases. The only remaining denominator blocker is `PERF_0063`.

This blocker is separate from the earlier wrapper/readiness issue that affected `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0052`. That earlier issue was a report-path/readiness contract bug and has already been resolved.

For `PERF_0063`, the real-route batch failed during validation with:

```text
No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)
```

The failure occurred before `sql_to_rel` and before the HEP planner, so the remaining blocker is a Calcite function typing / input normalization issue rather than a speedup or checker issue.

## 2. PERF_0063 Source Inspection

- source SQL path: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0063/source.sql)
- PG DDL path: [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0063/schema/ddl_pg.sql)
- witness path: [pg_witness_data.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0063/validation/pg_witness_data.sql)

Relevant source expression:

```sql
substr(ca_zip, 1, 5)
```

Observed `substr` / `substring` occurrences in the source:

- `substr(ca_zip, 1, 5)`
- no separate `substring(...)` occurrences were found

Surrounding predicate context:

```sql
and (
  substr(ca_zip, 1, 5) in ('85669', '86197', '88274', '83405', '86475', '85392', '85460', '80348', '81792')
  or ca_state in ('CA', 'WA', 'GA')
  or cs_sales_price > 500
)
```

Type context from PG DDL:

```sql
ca_zip text,
```

Static reading indicates the trigger is the `substr` call over a text column with bare numeric literals in positions two and three.

## 3. Calcite Failure Surface

- generation report path: [calcite_hep_real_route_missing_batch_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_real_route_missing_batch_v1.json)
- generated / parse-only candidate path: `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
- emitted SQL mode: `calcite_parse_only`
- validation_succeeded: `false`
- sql_to_rel_succeeded: `false`
- hep_planner_succeeded: `false`

Exact exception surface from the generation report:

```text
ValidationException: org.apache.calcite.runtime.CalciteContextException:
From line 14, column 8 to line 14, column 27:
No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)
```

The parse-only emitted SQL still contains the same functional surface:

```sql
"substr"("ca_zip", 1, 5)
```

This points to validator-stage function typing rather than output-surface corruption. The failure is happening before relational conversion, so the most likely root cause is Calcite-side acceptance of `substr` with numeric literals typed too broadly as `NUMERIC` instead of the integer-compatible type expected by the validator.

## 4. Static Patch Candidates

| candidate_name | example transformation | scope | expected benefit | risk | why safe/unsafe | specificity |
|---|---|---|---|---|---|---|
| `cast_numeric_literals_to_integer_inside_substr` | `substr(ca_zip, CAST(1 AS INTEGER), CAST(5 AS INTEGER))` | narrow source normalization | directly addresses the reported `<NUMERIC>` vs integer-typed argument mismatch | low | preserves `substr` surface and only narrows literal typing | case-specific or narrow adapter rule |
| `rewrite_to_sql_standard_substring_from_for` | `substring(ca_zip FROM 1 FOR 5)` | source normalization | may align better with a more standard surface if Calcite prefers it | medium | changes function surface and may interact differently with parser/validator expectations | better kept case-specific if attempted |
| `adapter_level_substr_integer_literal_normalization` | rewrite literal-only `substr(x, n1, n2)` second/third args to integer casts before handing SQL to Calcite | adapter normalization | generalizes the narrow fix without touching case files | medium | safe only if constrained to literal-only numeric args; broader matching risks changing other expressions | general but tightly scoped |
| `global_substr_surface_rewrite` | blanket rewrite of `substr` calls across inputs | adapter normalization | broadest coverage | high | too much semantic and surface risk for a single known blocker | not recommended |

Assessment:

- The safest candidate is integer-casting the literal numeric arguments while preserving the existing `substr` function surface.
- Rewriting to `substring(... FROM ... FOR ...)` is less attractive because it changes both syntax and parser surface without current evidence that it is required.
- A narrowly scoped adapter rule can be justified later if the same issue appears in additional cases, but current evidence supports starting with a single-case or literal-only normalization.

## 5. Recommended Patch Plan

Recommended patch plan:

- `implement narrow PERF_0063 substr integer-literal normalization and rerun generation/checker only`

Rationale:

- the triggering surface is isolated to `substr(ca_zip, 1, 5)`
- only one relevant `substr` occurrence was found in the source
- the exception explicitly points to argument typing, not output readiness or planner behavior
- preserving the existing `substr` surface while forcing integer-typed literals is the least risky intervention

Classification:

- `adapter_input_normalization_needed`

Risk:

- `medium`

It is medium rather than low because any adapter-stage SQL normalization still needs disciplined scoping, but the actual transformation can remain very narrow.

## 6. Next Execution Boundary

If a follow-up execution task is approved, the boundary should be:

- only `PERF_0063`
- generation + checker only
- no speedup until checker consistent
- no rerun of the existing 9 measured cases
- no registry writeback

That keeps the next step limited to validating whether the normalization resolves the validator-stage signature mismatch.

## 7. Non-Modification Note

Confirmed for this preflight:

- no Calcite rerun
- no DB/checker/speedup
- no model/API
- no code/case/registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
