# CALCITE_HEP_WRAPPER_SCAFFOLD_v0

## Status

This note records the current Calcite HEP wrapper scaffold result for:

- `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold`
- `reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json`

This is a generation-only scaffold update.

It is not a PostgreSQL workload run.

It is not a checker run.

It is not a speedup run.

It is not a runnable baseline claim.

## Scope

Wrapper-scaffold target slice:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Executed scaffold canary:

- `PERF_0006`

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold`
- `source scripts/env_postgres.sh || true`
- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold --case-id PERF_0006 --execute`
- `python -m json.tool reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json >/dev/null`

Implementation constraint used by the CLI:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home`

## Dry-Run Result

Dry-run command:

- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold`

Dry-run outcome:

- status: success
- denominator surfaced: `4`
- selected cases:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
  - `PERF_0054`
- scaffold status: `adapter_parse_scaffold_only`
- planned only; no Java compile and no wrapper execution

Dry-run interpretation:

- the CLI is wired correctly for the intended four-case PERF scaffold slice
- source SQL and PostgreSQL DDL inputs are located case-locally
- the command remains generation-only by default

## Execute Result

Execute command:

- `python -m scripts.cli formal-calcite-hep-wrapper-scaffold --case-id PERF_0006 --execute`

Final execute outcome on `PERF_0006`:

- `java wrapper compiled: yes`
- `wrapper executed: yes`
- `source.sql accepted: yes`
- `schema/ddl_pg.sql accepted: yes`
- `candidate SQL emitted: yes`
- `scaffold_status=adapter_parse_scaffold_only`

Emitted SQL characteristics:

- emitted SQL path: `/tmp/calcite-hep-wrapper/outputs/perf_0006.sql`
- emitted SQL mode: `original_passthrough`
- emitted SQL matches source under normalized comparison: `true`
- parsed SQL kind reported by Calcite: `ORDER_BY`

Important interpretation:

- this is a real Calcite-linked parse scaffold
- it is not yet a real HEP rewrite route
- the current candidate SQL is original passthrough, not actual Calcite-generated rewrite SQL

## What Happened During Execution

### 1. Wrapper compile/build closure

Observed outcomes:

- `:core:classes` completed successfully from the CLI execute path
- the Java wrapper compiled successfully
- the wrapper was invoked successfully

This means:

- the Calcite build bootstrap result from the prior probe is reusable from the scaffold command
- the CLI can now drive a real Java wrapper invocation path

### 2. First execute blocker and fix

The first `PERF_0006` execute attempt failed at parse time because Calcite rejected the trailing statement semicolon in the frozen `source.sql`.

Observed blocker:

- `SqlParseException` on trailing `;`

Fix applied:

- the wrapper now strips a trailing semicolon for parse purposes only
- it still emits the original source text unchanged as passthrough output

After that fix:

- `PERF_0006` parse succeeded
- output SQL was emitted successfully

### 3. Non-blocking runtime note

Observed runtime warning:

- SLF4J defaulted to NOP logger because no `StaticLoggerBinder` implementation was present

Interpretation:

- this did not block compile or wrapper execution
- it is not currently the scaffold blocker

## Exact Current State

- `whether Java wrapper compiled:` yes
- `whether wrapper executed:` yes
- `whether source.sql was accepted:` yes
- `whether schema/ddl_pg.sql was accepted:` yes
- `whether candidate SQL was emitted:` yes
- `whether emitted SQL is original passthrough or actual Calcite-generated SQL:` original passthrough
- `exact blocker if not emitted:` none on the final `PERF_0006` execute result

Current limitation:

- the wrapper proves parse acceptance and file-based generation plumbing only
- it does not yet build a schema model from `ddl_pg.sql`
- it does not yet convert through relational algebra and HEP rules
- it does not yet emit actual Calcite-generated SQL

## Claim Boundary

What can now be claimed:

- Calcite HEP wrapper scaffold is wired into the repo CLI
- a local Java wrapper can be compiled and invoked from the benchmark repo
- `PERF_0006` source SQL can be accepted by Calcite after minimal input normalization
- generation-only scaffold output can be emitted

What cannot yet be claimed:

- Calcite HEP baseline is implemented
- HEP rule application is running
- PostgreSQL execution closure exists
- checker-backed consistency closure exists
- speedup-scored route closure exists

## Recommended Next Action

Because emitted SQL now exists:

- run Calcite HEP PG execution/checker preflight next

But the technical development priority inside the wrapper is still:

- implement schema/rel/HEP conversion next

Practical next wrapper step:

1. ingest `schema/ddl_pg.sql` into a usable Calcite schema model
2. parse and validate against that schema rather than parse-only acceptance
3. build rel conversion
4. add a tiny bounded HEP rule program
5. emit actual Calcite-generated SQL instead of passthrough

## Final Summary

- wrapper scaffold compiled: `yes`
- wrapper scaffold executed: `yes`
- source accepted: `yes`
- DDL accepted: `yes`
- candidate SQL emitted: `yes`
- emission mode: `original_passthrough`
- current scaffold status: `adapter_parse_scaffold_only`
- next action: implement schema/rel/HEP conversion, then run Calcite HEP PG execution/checker preflight

## Verification / Non-Modification Note

- no PostgreSQL workload was run
- no checker was run
- no speedup was run
- no registry file was modified
- no `docs/EXECUTION_STATUS.md` change was made
- no formal review file was modified
- no case file was modified
- no Gradle build outputs were added to git
