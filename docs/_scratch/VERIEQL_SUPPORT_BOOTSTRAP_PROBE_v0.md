# VeriEQL Support Bootstrap Probe v0

## Scope

- Case: `CONS_0007` only
- Role: verifier/support-table feasibility only
- Boundary: no PostgreSQL execution, no speedup, no equivalence verification execution, no baseline claim

## Result

- Repo-local VeriEQL code present: `yes`
- Runtime Python observed: `Python 3.12.3`
- VeriEQL README assumption: `Python 3.10+`, `Python 3.11` recommended
- Dependency materialization status: `not attempted`
- CLI entrypoint discovered: `yes`
- Runnable now: `no`

## Repo Signals

- Checkout present: [datasets/raw/verieql/staged/VeriEQL/README.md](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/README.md)
- Requirements present: [requirements.txt](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt)
- Entrypoint present: [__main__.py](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/__main__.py)
- Batch timeout CLI present: [parallel/cli_within_timeout.py](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/parallel/cli_within_timeout.py)
- Environment module present: [environment.py](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/environment.py)

## Expected VeriEQL Input

The staged code expects a verifier-oriented transport rather than direct case-package execution. The visible batch format is `jsonlines` with top-level keys:

- `index`
- `schema`
- `constraint`
- `pair`

The `pair` shape is `[sql1, sql2]`. The `schema` shape is table/column/type metadata, and constraint handling needs an explicit bridge from case-local DDL and integrity assumptions into VeriEQL’s expected structure.

## CONS_0007 Mapping Check

- Source SQL present: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/source.sql)
- Positive rewrite present: [rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_pos_01.sql)
- Negative rewrite present: [rewrite_neg_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_neg_01.sql)
- PostgreSQL DDL present: [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/schema/ddl_pg.sql)
- Requested checker path absent: `cases/CONS/CONS_0007/validation/checker.yaml` does not exist

Mapping status:

- Source/positive pair can be mapped: `yes`, in principle
- Source/negative pair can be mapped: `yes`, in principle

Reason:

- `CONS_0007` is a single-table case on `tmp_emps`
- `source.sql`, `rewrite_pos_01.sql`, `rewrite_neg_01.sql`, and `schema/ddl_pg.sql` are all present
- This is enough to scaffold a pair-to-VeriEQL adapter, but not enough to run VeriEQL directly without a wrapper

## Timeout And Subset Policy

A bounded support wrapper will need a frozen first-pass policy before any execution probe:

- timeout: `600s` is the natural starting point because the staged repo documents timeout-driven batch execution
- bound size: start with `1` or `2`
- pair scope: `source vs positive` and `source vs negative`
- integrity-constraint mode: explicit and frozen, not inferred ad hoc

## Exact Blockers

- `dependency_materialization_not_attempted`
- `case_to_verifier_pair_wrapper_missing`
- `subset_policy_missing`
- `timeout_policy_missing`
- `constraint_schema_bridge_missing`
- `missing_validation_checker_yaml`

## Interpretation

This is the strongest remaining support-table candidate because the repo-local VeriEQL checkout is already staged and the `CONS_0007` SQL pair is structurally simple. The blocker is not raw source availability. The blocker is that the benchmark repo still lacks the bridge layer that converts a case package into VeriEQL’s expected schema/constraint/pair batch format under a bounded timeout policy.

The missing `validation/checker.yaml` is also a concrete mismatch against the requested reuse path. That does not prevent a future VeriEQL-specific support wrapper, but it does mean there is no direct case-local checker contract here to reuse as-is.

## Recommended Next Action

Recommended next action: `wrapper scaffold`

Concretely:

1. Add a read-only support wrapper that converts `CONS_0007` into one VeriEQL jsonlines record for `source vs positive` and one for `source vs negative`.
2. Freeze a tiny support-only policy with explicit timeout and bound size.
3. Do dependency install/probe only when ready to test that wrapper.

If that wrapper is not prioritized, keep VeriEQL in the support-only backlog rather than describing it as runnable now.
