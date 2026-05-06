# CALCITE_HEP_PERF_0063_SIGNATURE_FIX_FAILURE_DIAGNOSTIC_v1

## 0. Purpose And Boundary

This is a read-only diagnostic for the failed `PERF_0063` signature-fix attempt.

- no Calcite rerun
- no DB/checker/speedup
- no code changes
- no registry writeback

## 1. Previous Attempt Recap

The attempted narrow normalization was:

- original: `substr(ca_zip, 1, 5)`
- normalized: `substr(ca_zip, CAST(1 AS INTEGER), CAST(5 AS INTEGER))`
- normalized input artifact: `/tmp/calcite-hep-wrapper/real-route/perf_0063_normalized_input.sql`

That attempt still failed at validation time:

```text
No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)
```

Generation did not clear validation, so checker did not run and speedup remains `not_run`.

## 2. Artifact Inspection

- normalized input path: `/tmp/calcite-hep-wrapper/real-route/perf_0063_normalized_input.sql`
- normalized input contains CASTs: `yes`
- parse-only candidate path: `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
- parse-only candidate contains CASTs: `yes`

Normalized input excerpt:

```sql
substr(ca_zip, CAST(1 AS INTEGER), CAST(5 AS INTEGER))
```

Parse-only emitted SQL excerpt:

```sql
"substr"("ca_zip", CAST(1 AS INTEGER), CAST(5 AS INTEGER))
```

Generation report failure surface:

- report path: [calcite_hep_real_route_perf_0063_signature_fix_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_real_route_perf_0063_signature_fix_v1.json)
- failure:

```text
ValidationException: org.apache.calcite.runtime.CalciteContextException:
From line 14, column 8 to line 14, column 61:
No match found for function signature substr(<CHARACTER>, <NUMERIC>, <NUMERIC>)
```

The key observation is that the casted form is present both before Calcite input handoff and in the parse-only emitted SQL. So the normalization was applied and used, but the validator still reports the second and third arguments under a `NUMERIC` signature.

## 3. Root-cause Classification

Chosen classification:

- `calcite_cast_still_typed_numeric`

Why this classification fits best:

- the normalized input artifact clearly contains `CAST(... AS INTEGER)`
- the parse-only emitted SQL also preserves those casts
- the failure message still collapses the second and third arguments to `<NUMERIC>`

This makes `normalization_not_applied_to_actual_calcite_input` unlikely. It also makes the earlier wrapper/readiness theory irrelevant here.

`substr_function_surface_not_supported` is possible, but current evidence points more specifically to Calcite continuing to type the arguments too broadly under the `substr` surface rather than simply rejecting all substring forms.

## 4. Patch Options

### Ensure normalized input is used

Assessment:

- not the best next step

Why:

- the normalized input artifact contains the casts
- the parse-only candidate also contains the casts
- that means the corrected input path already reached the wrapper

### SQL-standard substring FROM/FOR

Example:

```sql
substring(ca_zip FROM 1 FOR 5)
```

Assessment:

- strongest next bounded experiment

Why:

- it changes the function surface rather than only the literal typing
- the current evidence suggests casted numeric arguments are still ending up under the same rejected `substr(..., NUMERIC, NUMERIC)` signature
- this is still narrow and can remain `PERF_0063`-only

Risk:

- medium

### `SUBSTRING(ca_zip, 1, 5)`

Assessment:

- weaker than SQL-standard `FROM/FOR`

Why:

- it preserves the same positional argument surface and may still hit the same validator path
- it is less clearly distinct from the currently failing `substr` family than `substring(... FROM ... FOR ...)`

Risk:

- medium

### Stop at 9/10

Assessment:

- safe fallback, but lower value than one more narrow syntax experiment

Why:

- current matrix already has strong `9/10` evidence
- however this remaining blocker is isolated enough that one more case-local syntax normalization is still justified before freezing the boundary

## 5. Recommended Next Step

- `implement SQL-standard substring normalization and rerun generation/checker only`

Reason:

- the cast-based normalization was definitely applied
- the failure surface did not change in a way that suggests the input path is still wrong
- the next safest bounded change is to switch only the `PERF_0063` Calcite input surface from `substr(...)` to `substring(... FROM ... FOR ...)`

## 6. Non-Modification Note

Confirmed for this diagnostic:

- no Calcite rerun
- no DB/checker/speedup
- no model/API
- no code/case/registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
