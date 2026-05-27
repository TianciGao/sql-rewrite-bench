# VeriEQL Support Wrapper Scaffold v0

## Scope

- Case: `CONS_0035`
- Role: verifier/support-table scaffold only
- Boundary: no verifier execution in the scaffold command itself, no PostgreSQL, no checker, no speedup, not a baseline claim

## Result

- Wrapper jsonlines emitted: `yes`
- Output path: `reports/formal_expansion/verieql_support/cons_0035_pairs.jsonl`
- Pair count: `2`
- VeriEQL execution status in scaffold command: `not_run`
- Runner input-contract patch applied: `yes`
- `--case-id` generalization for wrapper scaffold: `yes`

## Emitted Pair Roles

- `source_positive`
- `source_negative`

Both records now carry the full runner-safe metadata contract:

- `index`
- `file`
- `name`
- `benchmark`
- `case_id`
- `pair_role`
- `schema`
- `constraint`
- `pair`

The emitted jsonlines was validated locally as parseable JSON on both lines.

## Schema Mapping

- Schema mapping result: `single_table_mapped`
- DDL source: [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/schema/ddl_pg.sql)
- Table mapped: `EMP`
- Column count: `3`

Mapped schema object:

```json
{
  "EMP": {
    "EMPNO": "INT",
    "MGR": "INT",
    "DEPTNO": "INT"
  }
}
```

The first pass still keeps constraints empty and explicitly unmodeled.

## Policy

- Constraint policy: `empty_or_explicitly_unmodeled_first_pass`
- Timeout policy: `timeout_seconds=600`
- Bound size: `2`
- Pair scope: `source_positive_and_source_negative`

## Mapping Status

- Source SQL present: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/source.sql)
- Positive comparator present: [rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/rewrite_pos_01.sql)
- Negative comparator present: [rewrite_neg_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/rewrite_neg_01.sql)
- Source-positive mapped: `yes`
- Source-negative mapped: `yes`

## Exact Blockers To Actual Verification

- `verieql_verification_not_run`

Interpretation:

At the wrapper stage, the benchmark-to-VeriEQL bridge is closed for `CONS_0035`. The command now emits case-local runner-ready jsonlines instead of a `CONS_0007`-specific artifact, and the output contract matches the VeriEQL batch runner’s actual metadata expectations.

## Next Action

Next action after this scaffold is the bounded module-mode canary on the emitted `CONS_0035` jsonlines.

## Boundary

- Wrapper scaffold only
- No verifier execution inside this command
- No PostgreSQL
- No speedup
- Not a baseline claim
