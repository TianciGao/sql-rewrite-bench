# CALCITE_HEP_IMPLEMENTATION_FEASIBILITY_v0

## Status

This is a feasibility audit for moving Calcite HEP from `preflight_only` toward a runnable small-subset baseline.

It is an implementation audit only.

It is not a Calcite execution run.

It is not a database workload run.

It is not a registry writeback.

It is not a case update.

## Short Answer

- `runnable_now: no`
- current recommendation: keep Calcite HEP as `readiness-only` for now
- follow-on recommendation: proceed only to a Calcite HEP scaffold, not to baseline execution

## Scope Reviewed

Candidate subset under review:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

Repository surfaces reviewed:

- existing Calcite HEP readiness command/report in `scripts/cli.py` and `reports/baseline_smoke/calcite_hep_parse_readiness_v0.json`
- repository dependency/build footprint under `datasets/raw/calcite/calcite/`
- existing common-core case package inputs for SQL, DDL, witness data, checker, and PostgreSQL result/speedup reuse

## Current Evidence

### 1. Existing readiness scaffold exists, but it is explicitly non-runnable

The current CLI command:

- `baseline-smoke-calcite-readiness`

Current implementation status in `scripts/cli.py`:

- refuses `--execute`
- emits a static readiness report only
- hardcodes:
  - `calcite_adapter_available = false`
  - `calcite_build_path_available = false`
  - `calcite_dependency_available = false`

Current report:

- `reports/baseline_smoke/calcite_hep_parse_readiness_v0.json`

Current report conclusions:

- `first_subset_candidate_count = 6`
- `maybe_later_count = 3`
- all records remain:
  - `calcite_parse_attempted = false`
  - `calcite_rewrite_attempted = false`
  - `parse_status = not_attempted_adapter_missing`

Important nuance:

- the readiness command correctly reflects that no Calcite adapter exists today
- however, its `build_path_available = false` value is now stale relative to the repository contents, because a local Calcite source/build tree is present

### 2. A local Calcite source/build tree does exist

Under `datasets/raw/calcite/calcite/` the repository already contains:

- `build.gradle.kts`
- `settings.gradle.kts`
- `gradlew`
- `gradle/wrapper/gradle-wrapper.jar`
- `core/src/main/java/org/apache/calcite/plan/hep/HepPlanner.java`
- `core/src/main/java/org/apache/calcite/plan/hep/HepProgramBuilder.java`
- `core/src/main/java/org/apache/calcite/sql/parser/SqlParser.java`
- `core/src/main/java/org/apache/calcite/tools/Frameworks.java`
- `core/src/main/java/org/apache/calcite/rel/rel2sql/RelToSqlConverter.java`

Environment evidence on this machine:

- `/usr/bin/java` exists
- `/usr/bin/javac` exists

This means:

- Calcite HEP is not blocked by missing source checkout
- Calcite HEP is not blocked by missing Java runtime/compiler
- a local build bootstrap path is conceptually available

### 3. A runnable local adapter does not exist

Repository inspection found:

- no repo-local Calcite HEP wrapper under `scripts/` or `tools/`
- no repo-local Java main or Python bridge that accepts case SQL and emits rewritten SQL
- no built Calcite jars under the repo checkout
- no repo-local `build/libs` materialization for a reusable wrapper

No local Gradle dependency cache evidence was found under `~/.gradle` for Calcite dependencies during this audit.

This means:

- there is no current adapter entrypoint that can be invoked from the benchmark CLI
- there is no evidence that the local Calcite checkout has already been dependency-resolved and built on this machine

### 4. Build bootstrap is present in structure, but not materially closed

The Calcite build files reference external repositories:

- `datasets/raw/calcite/calcite/build.gradle.kts` uses `mavenCentral()`

Therefore:

- the local source tree is build-capable in principle
- but a first actual wrapper build would still depend on successful Gradle dependency resolution
- that dependency/materialization step has not yet been proven by any repo artifact

### 5. The candidate subset is case-input ready

All six candidate cases already expose the inputs a method baseline would need:

- `source.sql`
- `schema/ddl_pg.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- checker/result artifacts such as `runs/result_check.json`
- PostgreSQL validation/checker material such as `validation/checker.yaml` and `validation/pg_witness_data.sql`

The subset also aligns with existing Calcite HEP subset constants already present in `scripts/cli.py`:

- `CALCITE_HEP_FIRST_SUBSET_CASES`

This means:

- source SQL can already be exported directly from case packages for the six-case subset
- case-local PostgreSQL DDL exists and is sufficient to drive later PG-side execution/checking
- case packaging is not the blocker

## Candidate Subset Quality

Subset packaging/readiness assessment:

- `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` are strong first-subset inputs
- `CONS_0007` is rewrite-interesting and already schema-complete
- `CONS_0012` is useful, but has `LIMIT/OFFSET` semantics that make it a slightly riskier early adapter target

Net assessment:

- the six-case subset is reasonable for a scaffold
- the four PERF cases are the cleanest first runnable slice
- the two CONS cases are good follow-on checks once basic rewrite/export works

## Reuse Available From Existing PG Paths

If Calcite HEP can emit candidate PostgreSQL SQL, the repository already has reusable downstream pieces:

- PostgreSQL execution patterns via existing `psycopg.connect(...)`-based formal runners
- row-count/result checking patterns via existing common-core checker paths
- method-speedup scoring structure via existing common-core / expanded PERF speedup runners

What does **not** need to be invented from scratch:

- case selection
- source SQL lookup
- validation schema conventions
- checker/result artifact conventions
- PostgreSQL-side speedup measurement logic

What **does** still need to be implemented:

- method-specific candidate generation for Calcite HEP
- a materialization location for generated Calcite SQL
- route-specific integration glue so the existing checker/speedup machinery can consume Calcite-generated SQL

## Exact Blocker Category

Primary blocker category:

- `adapter_missing`

Secondary blocker categories:

- `build_bootstrap_unproven`
- `dependency_materialization_missing`
- `route_integration_missing`

Not blockers:

- `case_input_missing`
- `source_sql_missing`
- `pg_checker_path_missing`
- `pg_speedup_path_missing`

## Missing Components

Missing components required before Calcite HEP becomes runnable:

1. A local adapter wrapper
- likely a small Java main class or tiny dedicated Gradle subproject
- input: case `source.sql` plus case-local `schema/ddl_pg.sql`
- output: candidate rewritten PostgreSQL SQL plus route-local metadata

2. A proven build/materialization step
- compile the wrapper against the local Calcite checkout
- confirm dependency resolution completes successfully
- produce a stable invocation path from the benchmark repo

3. Rule/program definition for the first subset
- choose a bounded HEP program rather than “all default rules”
- start with a conservative rule set aimed at simple projection/filter/join/aggregate normalization

4. CLI integration glue
- preflight command for Calcite candidate generation readiness
- generation command that emits per-case candidate SQL
- route-local artifact naming that can plug into existing checker/speedup stages

5. SQL export/normalization boundary
- convert Calcite relational output back to PostgreSQL-acceptable SQL
- define what to do when Calcite produces dialect-generic SQL that still needs PostgreSQL normalization

## Recommended Minimal Adapter Path

If this work proceeds, the minimal path should be:

1. Build a tiny repo-local Java wrapper around the existing Calcite checkout
- use the local source tree under `datasets/raw/calcite/calcite/`
- avoid introducing a new external service
- avoid introducing model calls or new runtime infrastructure

2. Start with the four cleaner PERF cases first
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

3. Use case-local PostgreSQL DDL as the schema source
- derive the Calcite schema from `schema/ddl_pg.sql`
- use `source.sql` as the input query

4. Emit candidate SQL into route-local report artifacts first
- do not write back into case packages
- do not mutate registry or formal review state

5. Reuse existing PostgreSQL checker/speedup patterns after candidate generation works
- first checker-backed execution on the four PERF cases
- then extend to `CONS_0007`
- then evaluate whether `CONS_0012` is worth including in the first runnable slice

## Estimated Implementation Effort

Best-case effort if Gradle dependency resolution works cleanly:

- `1 to 2 focused engineering days`

More realistic effort if build/bootstrap friction appears:

- `2 to 4 engineering days`

Effort drivers:

- wrapper implementation is moderate
- schema ingestion from case-local DDL is the most important design task
- downstream PG checker/speedup reuse is comparatively cheaper than generation
- the biggest uncertainty is not SQL export from case packages; it is Calcite wrapper/bootstrap closure

## Recommendation

Recommendation for current project state:

- do **not** move Calcite HEP directly from `preflight_only` to a runnable baseline today
- keep it as `readiness-only` at this moment
- if human priority exists, proceed only to a bounded Calcite HEP scaffold

Recommended next action:

- implement a minimal local wrapper/scaffold first
- target the four PERF cases before the two CONS cases
- require successful local build closure before reclassifying Calcite HEP as runnable

## Final Decision

- `runnable_now: no`
- `missing components:` adapter wrapper, proven build/dependency closure, route integration, bounded HEP rule program
- `exact blocker category:` `adapter_missing` with `build_bootstrap_unproven` and `dependency_materialization_missing`
- `recommended minimal adapter path:` local Java wrapper over the existing Calcite checkout using case-local `source.sql` and `schema/ddl_pg.sql`, then reuse existing PG checker/speedup paths
- `estimated implementation effort:` `1 to 2 focused engineering days` best case, `2 to 4 engineering days` with bootstrap friction
- `proceed or not:` proceed to Calcite HEP scaffold only if this baseline is a near-term priority; otherwise keep as `readiness-only`

## Verification / Non-Modification Note

- no database workload was run
- no model call was made
- no registry file was modified
- no case file was modified
- no report was force-added
