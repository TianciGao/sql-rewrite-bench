# CALCITE_HEP_WRAPPER_SCAFFOLD_v0

## Status

This note records the current 4-case Calcite HEP wrapper scaffold smoke result for:

- `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold`
- `reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json`

This remains a generation-only scaffold result.

Explicit non-claim boundary:

- not a real HEP rewrite
- not PostgreSQL execution
- not checker-backed
- not speedup-scored
- not a runnable Calcite HEP baseline claim

## Scope

Expanded clean PERF scaffold slice:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold --case-id PERF_0006 --case-id PERF_0008 --case-id PERF_0033 --case-id PERF_0054 --execute`
- `python -m json.tool reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json >/dev/null`

Implementation constraint used by the CLI:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home`

## Dry-Run Result

Dry-run outcome:

- status: success
- denominator surfaced: `4`
- selected cases:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
  - `PERF_0054`
- scaffold status: `adapter_parse_scaffold_only`
- dry-run only; no Java compile and no wrapper invocation

Interpretation:

- the CLI is wired for the intended 4-case PERF subset
- source SQL and PostgreSQL DDL inputs resolve case-locally
- the default route remains generation-only

## 4-Case Execute Result

Execute outcome on the clean 4-case PERF subset:

- `java wrapper compiled:` yes
- `wrapper executed:` `4/4`
- `parse success count:` `4/4`
- `output SQL emitted count:` `4/4`
- `final semicolon normalized for parse:` `4/4`
- `scaffold_status:` `adapter_parse_scaffold_only`
- `emission mode:` `original_passthrough` for all emitted outputs

Per-case result:

| case_id | wrapper_execute | source.sql accepted | schema/ddl_pg.sql accepted | Calcite parse | final semicolon normalized | output SQL emitted | emitted SQL mode | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | yes | yes | yes | yes | `original_passthrough` | none |
| `PERF_0008` | yes | yes | yes | yes | yes | yes | `original_passthrough` | none |
| `PERF_0033` | yes | yes | yes | yes | yes | yes | `original_passthrough` | none |
| `PERF_0054` | yes | yes | yes | yes | yes | yes | `original_passthrough` | none |

Observed parsed SQL kind for all four cases:

- `ORDER_BY`

## What This Proves

- the local Calcite checkout can still be built from the scaffold CLI route
- the tiny Java wrapper compiled successfully
- the wrapper can be invoked repeatedly across the intended clean 4-case PERF subset
- all four `source.sql` inputs were accepted after the existing final-semicolon normalization
- all four `schema/ddl_pg.sql` inputs were accepted as scaffold inputs
- candidate SQL files were emitted for all four cases

## What This Does Not Prove

- no relational conversion has been built yet
- no `FrameworkConfig`-based validation path has been built yet
- no `RelBuilder` route exists yet
- no `HepPlanner` rule program is running yet
- no `RelToSql` emission route exists yet
- no PostgreSQL execution was run
- no checker was run
- no speedup run was performed

The current candidate SQL is still original passthrough output, not actual Calcite-generated rewrite SQL.

## Minor Reliability Tightening

While expanding from 1 canary to 4 cases, the CLI scaffold path was tightened so each execute case clears any stale `/tmp` output SQL before wrapper invocation.

Interpretation:

- a failed rerun no longer risks inheriting a prior emitted file
- emitted-count reporting is now aligned with the current execute attempt

## Exact Current State

- `wrapper compile status:` success
- `per-case wrapper execution status:` `4/4` success
- `source.sql accepted:` `4/4`
- `schema/ddl_pg.sql accepted:` `4/4`
- `Calcite parse status:` `4/4`
- `final semicolon normalization status:` `4/4`
- `output SQL emitted:` `4/4`
- `emitted SQL mode:` `original_passthrough`
- `exact blockers:` none in the final 4-case execute result

## Next Required Step

Implement the real Calcite route next:

1. build `FrameworkConfig` and schema-backed validation from `ddl_pg.sql`
2. convert SQL to rel form with Calcite
3. run a bounded `HepPlanner` rule set
4. emit rewritten SQL through a real `RelToSql` path

In short:

- implement real Calcite `RelBuilder / FrameworkConfig / HepPlanner / RelToSql` route next

## Verification / Non-Modification Note

- no PostgreSQL workload was run
- no checker was run
- no speedup run was performed
- no registry file was modified
- no `docs/EXECUTION_STATUS.md` change was made
- no formal review file was modified
- no case file was modified
- no Gradle build outputs were added to git
