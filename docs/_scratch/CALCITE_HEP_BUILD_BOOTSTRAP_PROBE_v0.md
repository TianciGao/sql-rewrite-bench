# CALCITE_HEP_BUILD_BOOTSTRAP_PROBE_v0

## Status

This note records a bounded local build bootstrap probe for:

- `datasets/raw/calcite/calcite/`

It is a build/bootstrap probe only.

It is not a Calcite rewrite run.

It is not a database workload run.

It is not a benchmark experiment.

It is not a registry update.

## Scope

Commands probed:

1. `./gradlew --version`
2. `./gradlew :core:classes --dry-run`
3. `./gradlew :core:classes`

Probe environment constraint:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home`

This was used to avoid writing under `/home/tianci_gao/.gradle` during the probe.

## Environment

- `java version`: `openjdk version "17.0.18" 2026-01-20`
- `javac version`: `javac 17.0.18`
- `gradle wrapper version`: `Gradle 8.7`
- `gradle wrapper build time`: `2024-03-22 15:52:46 UTC`
- `JVM reported by Gradle`: `17.0.18 (Ubuntu 17.0.18+8-Ubuntu-124.04.1)`
- `OS reported by Gradle`: `Linux 6.6.87.2-microsoft-standard-WSL2 amd64`

## Probe Results

### 1. Wrapper version probe

Initial in-sandbox result:

- failed before wrapper bootstrap because Gradle tried to write its lock/download state under `/home/tianci_gao/.gradle`

Retry with temporary Gradle home:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home ./gradlew --version`
- result: success

Observed behavior:

- Gradle wrapper downloaded `gradle-8.7-bin.zip`
- wrapper initialized successfully after download

Interpretation:

- the local checkout can bootstrap the Gradle wrapper when given a writable Gradle home and normal network access

### 2. Dry-run result

Command:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home ./gradlew :core:classes --dry-run`

Initial in-sandbox result:

- failed
- error: `Could not determine a usable wildcard IP for this machine.`

Exact stacktrace blocker:

- Gradle initialization failed in file-lock/daemon networking setup
- root cause: `java.net.SocketException: Operation not permitted (Socket creation failed)`

Interpretation:

- this was a sandbox/network-socket restriction, not a Calcite project failure

Escalated dry-run result:

- success
- build completed as dry-run task graph resolution
- final status: `BUILD SUCCESSFUL in 3m 12s`

Observed task graph evidence:

- `buildSrc` configured and built
- project configuration completed
- `:core:classes` reached dry-run `SKIPPED` state as expected

Interpretation:

- the local checkout can resolve/configure enough of the build to plan `:core:classes`

### 3. Compile/build probe result

Command:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home ./gradlew :core:classes`

Result:

- success
- final status: `BUILD SUCCESSFUL in 44s`

Observed compile/build evidence:

- `:core:fmppMain` ran
- `:core:javaCCMain` ran and generated parser sources
- `:linq4j:compileJava` ran
- `:core:compileJava` ran
- `:core:classes` completed successfully

Observed warnings:

- Kotlin DSL warnings during configuration
- JavaCC parser-generation warnings
- Java compiler notes about unchecked or unsafe operations

None of the observed warnings blocked `:core:classes`.

## Dependency Materialization

- `dependencies materialized: yes`

Evidence:

- Gradle wrapper distribution was downloaded successfully
- project configuration completed successfully
- `buildSrc` tasks executed successfully
- `:core:classes` compiled successfully against resolved dependencies

Practical meaning:

- the earlier `dependency_materialization_missing` concern from the feasibility audit is now materially reduced for local wrapper work

## Build Bootstrap Conclusion

- `wrapper bootstrap: success`
- `dry-run result: success`
- `compile/build probe result: success`
- `exact blocker if failed:` none at the project level

Important nuance:

- the only blockers observed during the probe were environment/sandbox restrictions:
  - default Gradle home not writable inside the sandbox
  - socket creation blocked inside the sandbox during Gradle daemon/file-lock setup

Those blockers were not Calcite source/build failures.

## Wrapper Scaffold Feasibility

- `wrapper scaffold now feasible: yes`

Why:

- the local Calcite checkout can now be treated as build-bootstrapped enough for a future tiny HEP wrapper
- Java/Javac are present
- Gradle wrapper resolves
- `:core:classes` compiles successfully

What this does **not** prove:

- no HEP wrapper exists yet
- no Calcite rewrite execution was run
- no SQL export path was validated yet
- no PostgreSQL checker or speedup integration was executed yet

## Recommended Next Action

Because the build probe succeeded:

- proceed to a tiny Java wrapper scaffold for Calcite HEP

Recommended bounded next step:

1. add a minimal local Java entrypoint that links against the existing Calcite checkout
2. accept case-local `source.sql` and `schema/ddl_pg.sql`
3. emit route-local candidate SQL only
4. keep initial scope to the clean PERF subset before wider route integration

If this probe had failed, the recommendation would have remained:

- keep Calcite HEP readiness-only

That is no longer the recommended state based on the build bootstrap result.

## Git / Artifact Hygiene

- no build outputs were added to git
- repository `git status --short` remained unchanged except for the pre-existing unrelated untracked taxonomy notes
- no case files were modified
- no registry files were modified
- no `docs/EXECUTION_STATUS.md` updates were made

## Final Summary

- `java version:` `17.0.18`
- `javac version:` `17.0.18`
- `gradle wrapper version:` `8.7`
- `dry-run result:` success
- `compile/build probe result:` success
- `dependencies materialized:` yes
- `wrapper scaffold now feasible:` yes
- `exact blocker if failed:` none at the Calcite project level; only sandbox environment restrictions were observed during the initial in-sandbox attempts
- `recommended next action:` proceed to tiny Java wrapper scaffold

