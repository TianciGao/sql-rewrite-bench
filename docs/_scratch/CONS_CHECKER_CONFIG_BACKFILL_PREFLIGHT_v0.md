# CONS_CHECKER_CONFIG_BACKFILL_PREFLIGHT_v0

## 1. Status

This is a no-modification preflight and proposal for `CONS_0007` and `CONS_0012`.

It does not backfill checker config.

It does not run a checker.

It does not close full 9-case generated-method consistency.

## 2. Why This Preflight Exists

PERF-only generated-method checker-backed consistency is now complete for:

- `SQLGLOT_OPT_SAME_DIALECT`: `7 / 7`, `rate=1.0`
- `LLM_DIRECT_REWRITE_STRONG`: `7 / 7`, `rate=1.0`

Full 9-case generated-method consistency remains open because:

- `CONS_0007` was blocked by missing `validation/checker.yaml`
- `CONS_0012` was blocked by missing `validation/checker.yaml`

The current question is not whether these cases have no evidence.

The current question is whether they need case-local checker backfill, or whether report-local generated-method checking can safely proceed without writing into `cases/`.

## 3. CONS Artifact Inventory

### `CONS_0007`

Present:

- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- `schema/ddl_pg.sql`
- `schema/ddl_mysql.sql`
- `schema/ddl_spark.sql`
- `validation/pg_witness_data.sql`
- `validation/mysql_witness_data.sql`
- `validation/spark_witness_data.sql`
- `validation/check_results.py`
- `validation/check_plan_artifacts.py`
- `validation/run_pg_validation.sh`
- `validation/run_mysql_validation.sh`
- `validation/run_spark_validation.sh`
- `runs/result_check.json`
- `runs/pg/result_check.json`
- `runs/mysql/result_check.json`
- `runs/spark/result_check.json`
- `runs/plan_check.json`
- `runs/pg/plans/plan_check.json`
- `runs/mysql/plans/plan_check.json`
- `runs/spark/plans/plan_check.json`
- `runs/pg/source.tsv`
- `runs/pg/rewrite_pos_01.tsv`
- `runs/pg/rewrite_neg_01.tsv`

Missing:

- `validation/checker.yaml`

Observed result-check semantics:

- root `runs/result_check.json` is `validated`
- `validation_model=engine_local_witness`
- checks include:
  - `pg_positive_equals_source=true`
  - `pg_negative_differs_from_source=true`
  - `mysql_positive_equals_source=true`
  - `mysql_negative_differs_from_source=true`
  - `spark_positive_equals_source=true`
  - `spark_negative_differs_from_source=true`

### `CONS_0012`

Present:

- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- `schema/ddl_pg.sql`
- `schema/ddl_mysql.sql`
- `schema/ddl_spark.sql`
- `validation/pg_witness_data.sql`
- `validation/mysql_witness_data.sql`
- `validation/spark_witness_data.sql`
- `validation/check_results.py`
- `validation/check_plan_artifacts.py`
- `validation/run_pg_validation.sh`
- `validation/run_mysql_validation.sh`
- `validation/run_spark_validation.sh`
- `runs/result_check.json`
- `runs/pg/result_check.json`
- `runs/mysql/result_check.json`
- `runs/spark/result_check.json`
- `runs/plan_check.json`
- `runs/pg/plans/plan_check.json`
- `runs/mysql/plans/plan_check.json`
- `runs/spark/plans/plan_check.json`
- `runs/pg/source.tsv`
- `runs/pg/rewrite_pos_01.tsv`
- `runs/pg/rewrite_neg_01.tsv`

Missing:

- `validation/checker.yaml`

Observed result-check semantics:

- root `runs/result_check.json` is `validated`
- `validation_model=engine_local_witness`
- checks include:
  - `pg_positive_equals_source=true`
  - `pg_negative_differs_from_source=true`
  - `mysql_positive_equals_source=true`
  - `mysql_negative_differs_from_source=true`
  - `spark_positive_equals_source=true`
  - `spark_negative_differs_from_source=true`

## 4. PERF `checker.yaml` Comparison

Compared reference files:

- `cases/PERF/PERF_0006/validation/checker.yaml`
- `cases/PERF/PERF_0008/validation/checker.yaml`
- `cases/PERF/PERF_0013/validation/checker.yaml`

Common behavior expressed there:

- checker type is value/result equivalence oriented
- `source.sql` and `rewrite_pos_01.sql` are expected equal
- `source.sql` and `rewrite_neg_01.sql` are expected not equal
- expected result files use PostgreSQL witness TSV naming:
  - `runs/pg/source.tsv`
  - `runs/pg/rewrite_pos_01.tsv`
  - `runs/pg/rewrite_neg_01.tsv`
- evidence points to `runs/pg/result_check.json`

Normalization / comparison hints in PERF:

- sort rows
- trim whitespace
- normalize numeric format
- normalize null
- sometimes normalize tabs

Implication:

- PERF checker config is a case-local declaration of witness-result comparison semantics
- it is richer than raw byte equality
- but it still points to the same basic positive-equals-source / negative-differs-from-source witness model already visible in the CONS `result_check.json` artifacts

## 5. Feasibility Assessment

### Can `CONS_0007` and `CONS_0012` use the same `exact_tsv_report_local` policy without case-local `checker.yaml`?

Yes, for a bounded generated-method consistency closure path.

Reason:

- both CONS cases already have PostgreSQL witness result artifacts proving the local source/positive/negative witness model exists
- both CONS cases already expose source / positive / negative SQL, schema, witness data, and validation scripts
- the generated-method PERF run already used a conservative report-local checker mode:
  - `exact_tsv_report_local`
- that mode does not require case-local `checker.yaml` if the policy is explicitly declared in the formal report-local checker command

### Does that mean case-local `checker.yaml` is unnecessary forever?

No.

If the project wants stronger case-local governance symmetry across PERF and CONS, a minimal `validation/checker.yaml` backfill could still be useful later.

But it is not required to prove that a bounded report-local generated-method checker run can be executed safely for `CONS_0007` and `CONS_0012`.

## 6. Recommended Path

Recommended choice: `A. report-local checker policy for CONS generated-method consistency, no case-local backfill`

Why this is the safest path now:

- it matches the current generated-method closure architecture, which is already report-local
- it avoids editing `cases/` just to unblock a bounded formal packet
- both blocked CONS cases already have enough existing witness evidence to justify a conservative report-local checker mode
- it keeps the distinction explicit:
  - case-local witness artifacts remain historical / package evidence
  - generated-method checker outputs remain formal report-local artifacts

Secondary option, but not recommended as first move:

- `B. minimal case-local checker.yaml backfill proposal`

This would improve case-local symmetry, but it increases governance surface area before it is necessary.

Not recommended:

- `C. keep CONS excluded from generated-method checker-backed consistency`

That would leave the full 9-case closure open even though the missing piece appears to be policy/config friction rather than missing witness evidence.

## 7. Required Artifacts For Full 9-case Closure

To close full 9-case generated-method consistency, the remaining CONS work would require:

- source TSV materialization under:
  - `reports/formal_common_core/result_materialization/source/<case_id_lower>.tsv`
- SQLGlot TSV materialization under:
  - `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/<case_id_lower>.tsv`
- Direct LLM TSV materialization under:
  - `reports/formal_common_core/result_materialization/llm_direct_rewrite/<case_id_lower>.tsv`
- SQLGlot checker outputs under:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/<case_id_lower>.json`
- Direct LLM checker outputs under:
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/<case_id_lower>.json`

Additional policy requirement:

- the command should explicitly state whether CONS generated-method checking is allowed under:
  - `exact_tsv_report_local`
  - or a stronger normalized TSV mode if later added

Current evidence suggests no special CONS-only semantics are required beyond the existing witness-result comparison model, but that must be stated as a bounded policy decision before execution.

## 8. Risks / Caveats

- existing CONS witness artifacts are draft / staged evidence, not admission evidence
- `exact_tsv_report_local` is conservative, but it is still stricter and narrower than a richer value-normalized checker
- row order / formatting sensitivity could differ from a future normalized checker mode
- generated-method checker closure on CONS would still be PostgreSQL-only for this bounded step
- closing full 9-case generated-method consistency would not automatically authorize generated-method leaderboard speedup promotion

## 9. Claim Boundaries

- this is not a backfill
- this is not a checker run
- this does not close full 9-case consistency
- no case-local files were modified
- no registry was updated
- no formal review files were updated

## 10. Recommended Next Action

- implement a bounded CONS generated-method report-local checker run preflight using `exact_tsv_report_local`, without adding case-local `checker.yaml` first

## 11. Verification / Non-modification Note

- only this preflight note was created
- no SQL was executed
- no database workloads were run
- no checker was run
- no model / LLM call was made
- no SQLGlot generation was run
- no case-local files were modified
- no registry or `docs/EXECUTION_STATUS.md` changes were made
- no formal review files were changed
- taxonomy calibration notes were untouched
