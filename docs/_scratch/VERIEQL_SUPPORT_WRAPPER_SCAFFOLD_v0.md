# VeriEQL Support Wrapper Scaffold v0

## Scope

- Case: `CONS_0007` only
- Role: verifier/support-table scaffold only
- Boundary: no verifier execution, no PostgreSQL, no checker, no speedup, not a baseline claim

## Result

- Wrapper jsonlines emitted: `yes`
- Output path: `reports/formal_expansion/verieql_support/cons_0007_pairs.jsonl`
- Pair count: `2`
- VeriEQL execution status: `not_run`

## Emitted Pair Roles

- `source_positive`
- `source_negative`

Both records were emitted with the top-level keys expected by the staged VeriEQL batch format:

- `index`
- `schema`
- `constraint`
- `pair`

The emitted jsonlines was validated locally as parseable JSON on both lines.

## Schema Mapping

- Schema mapping result: `single_table_mapped`
- DDL source: [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/schema/ddl_pg.sql)
- Table mapped: `TMP_EMPS`
- Column count: `5`

Mapped schema object:

```json
{
  "TMP_EMPS": {
    "EMPID": "INT",
    "DEPTNO": "INT",
    "NAME": "VARCHAR",
    "SALARY": "DECIMAL",
    "COMMISSION": "INT"
  }
}
```

The current first pass keeps constraints empty and explicitly unmodeled rather than inferring integrity semantics from PostgreSQL DDL.

## Policy

- Constraint policy: `empty_or_explicitly_unmodeled_first_pass`
- Timeout policy: `timeout_seconds=600`
- Bound size: `2`
- Pair scope: `source_positive_and_source_negative`

## Mapping Status

- Source SQL present: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/source.sql)
- Positive comparator present: [rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_pos_01.sql)
- Negative comparator present: [rewrite_neg_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_neg_01.sql)
- Source-positive mapped: `yes`
- Source-negative mapped: `yes`

## Exact Blockers To Actual Verification

- `dependency_materialization_not_attempted`
- `verieql_verification_not_run`

Interpretation:

The benchmark-to-VeriEQL bridge now exists at the wrapper-input level for `CONS_0007`. What still does not exist is any executed verifier result. This command only materializes the pair transport that a later bounded VeriEQL probe would consume.

## Next Action

The next bounded step, if this support line is advanced, should be a dependency install/probe plus a strictly bounded no-side-effect VeriEQL execution canary over the emitted `source_positive` and `source_negative` records.

## Boundary

- Wrapper scaffold only
- No verifier execution
- No PostgreSQL
- No speedup
- Not a baseline claim
