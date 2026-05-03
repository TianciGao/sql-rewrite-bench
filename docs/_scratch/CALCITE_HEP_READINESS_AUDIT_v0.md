# CALCITE_HEP_READINESS_AUDIT_v0

## 1. Executive Summary

This document records a read-only readiness audit for a possible `CALCITE_HEP_RULES` baseline route.

Current conclusion:

- Calcite exists in this repository as a source family and case-provenance line.
- Calcite does not currently exist in this repository as a runnable baseline adapter.
- There is no repository-owned Calcite runner, no Java adapter, no Maven/Gradle build path, and no CLI baseline command for `CALCITE_HEP_RULES`.
- The baseline inventory explicitly treats Calcite as subset-bounded and adapter-dependent.

Current recommendation:

- Treat Calcite HEP as **subset-only**.
- Treat it as **not execution-ready** in the current repository state.

Recommended next action:

- implement a **no-execution Calcite parse-readiness scaffold**

This audit is not:

- a benchmark protocol change
- an execution result
- a correctness claim
- a speedup claim
- a registry writeback
- a formal review update

## 2. Repository / Build Readiness

### 2.1 Repository support signals

Observed signals:

- The repository contains many Calcite-derived consistency cases and review-prep materials.
- The repository does not contain an executable Calcite baseline path.

Read-only findings:

- No existing Calcite runner, adapter, script, or Java entrypoint was found.
- No `CALCITE_HEP_RULES` CLI command was found in `scripts/cli.py`.
- No local Java source tree was found.
- No `pom.xml`, `build.gradle`, `settings.gradle`, or `gradlew` was found.

Interpretation:

- Calcite is present as **source provenance / case-family material**.
- Calcite is not present as a **runnable optimizer baseline implementation**.

### 2.2 Environment / toolchain signals

Environment checks:

- `java -version`: available
- `mvn -version`: not installed
- `gradle -version`: not installed

Interpretation:

- Java itself is available in the environment.
- The repository still lacks both:
  - a build path
  - an adapter implementation

Java presence alone is not enough to treat Calcite as execution-ready.

## 3. Baseline Inventory Finding

Inventory row inspected:

- `CALCITE_HEP_RULES`

### 3.1 Inventory table

| baseline_id | boss_group | leaderboard_role | current interpretation | blockers |
|---|---|---|---|---|
| `CALCITE_HEP_RULES` | `P0_control_or_tool` | `speedup_leaderboard` | important baseline concept, but only for a Calcite-supported SQL subset and only if adapter/regeneration path exists | no adapter, no SQL-to-Rel path, no Rel-to-SQL path, no build path, no Spark-native route |

### 3.2 Key inventory facts

- baseline method: Apache Calcite fixed-rule / HepPlanner baseline
- category: rule / optimizer framework
- environment:
  - Java
  - Maven/Gradle
  - Apache Calcite
  - possible SQL-to-Rel and Rel-to-SQL adapter
- `common_core_fit`: yes, for SQL subset accepted by Calcite
- `subset_only`: yes
- `token_cost_class`: none
- recommended use: must-run rule framework baseline
- notes: use HEP/fixed rule order first; Volcano can be second setting

### 3.3 Inventory interpretation

The inventory does not justify treating Calcite as runnable now.

It supports a narrower interpretation:

- Calcite is strategically important.
- Calcite requires a dedicated adapter layer.
- Calcite should be treated as subset-bounded.

## 4. Current 9-Case Compatibility Assessment

Current PG-native 9-case PERF/CONS smoke set:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

This section is a static compatibility assessment only.
No Calcite parse or rewrite was run.

| case_id | pool | likely Calcite parse risk | likely HEP rewrite usefulness | reason | recommended inclusion status |
|---|---|---|---|---|---|
| `PERF_0006` | performance | low | medium | compact TPC-H aggregate/filter/order pattern | candidate |
| `PERF_0008` | performance | low | medium | classic join/aggregate/order/limit pattern | candidate |
| `PERF_0013` | performance | medium | medium | interval year syntax may require dialect normalization | maybe |
| `PERF_0017` | performance | medium | medium | interval month syntax plus grouped reporting | maybe |
| `PERF_0024` | performance | medium | high | correlated subqueries and nested aggregates are rewrite-relevant but subset-sensitive | maybe |
| `PERF_0033` | performance | low | medium | straightforward TPC-DS join/aggregate/order/limit shape | candidate |
| `PERF_0054` | performance | low | medium | straightforward TPC-DS join/aggregate/order/limit shape | candidate |
| `CONS_0007` | consistency | low | high | Calcite-derived correlated `EXISTS` case aligns naturally with Calcite semantics | candidate |
| `CONS_0012` | consistency | low | high | Calcite-derived `LIMIT/OFFSET` decorrelation-style case is directly relevant to HEP rule behavior | candidate |

### 4.1 9-case interpretation

Best first-canary subset candidates:

- `CONS_0007`
- `CONS_0012`
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Higher-risk members of the 9-case set:

- `PERF_0013`
- `PERF_0017`
- `PERF_0024`

Main risk themes:

- interval syntax normalization
- correlated subquery handling
- nested aggregate subqueries

## 5. 35-Case High-Level Compatibility

This section is high-level only.
It does not inspect all 35 case packages deeply.

Current planning signals considered:

- original preliminary common-core packet: `29`
- health-gated keep-for-review: `27`
- human-screened possible additions: `8`
- next possible human-review slate: `35`
- pending / not clean: `PERF_0038`
- extended-oriented: `PERF_0076`

### 5.1 Pool-level assessment

#### PERF

- likely moderate subset candidate
- strongest fit is in cleaner TPC-H and TPC-DS grouped-reporting shapes
- risk rises with:
  - interval syntax
  - deeper correlation
  - engine-normalized SQL artifacts

#### CONS

- strongest subset candidate
- this is where repository provenance already overlaps most directly with Calcite
- likely best target for a first no-execution Calcite readiness scaffold

#### PORT

- weakest fit for first Calcite HEP baseline work
- current PORT line is source-dialect and datetime/type sensitive
- not a good first denominator for a Calcite HEP route

#### LONGTAIL

- high risk
- likely too structurally heterogeneous for a first bounded Calcite subset

### 5.2 35-case interpretation

Current answer:

- Calcite HEP should **not** be treated as a likely full-coverage 35-case route.
- If pursued, it should be framed as a **subset-only candidate**.
- Most plausible first subset:
  - selected PERF
  - selected CONS
- least plausible first subset:
  - PORT-heavy
  - LONGTAIL-heavy

## 6. Blockers

Primary blockers:

- no Calcite runner in repository
- no Java adapter in repository
- no Maven/Gradle project in repository
- no Calcite dependency wiring in repository
- no SQL-to-Rel path defined in repo
- no Rel-to-SQL regeneration path defined in repo
- no frozen HEP rule pack defined in repo
- no execution harness defined for Calcite-produced output

Technical risk list:

- parser dialect mismatch
- SQL comments / dialect normalization issues
- output dialect uncertainty after rewrite
- Java adapter absence
- dependency installation risk
- HEP rule selection ambiguity
- result execution path not defined
- subset-only denominator risk
- Spark path ambiguity

Case-shape risks:

- interval literal handling
- correlated subqueries
- nested `EXISTS`
- nested aggregate subqueries
- `LIMIT` / `OFFSET`
- PostgreSQL-specific normalization artifacts

## 7. Recommendation

Recommendation:

> **Treat Calcite as subset-only, and not execution-ready.**

Reasoning:

- The inventory itself already narrows Calcite to a supported SQL subset.
- The repository lacks an adapter/build path.
- The current 9-case and 35-case signals do not support a full-route denominator claim.

Calcite should therefore be treated as:

- not a full common-core baseline candidate today
- not execution-ready today
- potentially valuable as a selective prior-method / support baseline after adapter scaffolding exists

## 8. Next Action

Exactly one recommended next action:

> **Implement a no-execution Calcite parse-readiness scaffold.**

Reason:

- It answers the first missing engineering question without overclaiming:
  - which cases can be parsed
  - which cases fit the intended Calcite subset
  - where dialect / regeneration blockers appear

It does not require:

- benchmark policy change
- execution claims
- correctness claims
- speedup claims

## 9. Verification / Non-Modification Note

This audit was read-only.

Confirmed:

- files modified: none
- files created: none during the audit itself
- database workloads run: no
- PostgreSQL / MySQL / Spark queries run: no
- Calcite transformations run: no
- Java builds run: no
- dependency installation: no
- LLM calls: no
- SQLGlot generation: no
- registry changed: no
- `docs/EXECUTION_STATUS.md` changed: no
- formal review files changed: no
- case-local files changed: no
- taxonomy files changed: no
- untracked taxonomy calibration notes touched: no

The three untracked taxonomy calibration notes remained out of scope:

- `TAXONOMY_CALIBRATION_NOTE_CONS_0001_0040.md`
- `TAXONOMY_CALIBRATION_NOTE_LONGTAIL_0001_0024.md`
- `TAXONOMY_CALIBRATION_NOTE_PORT_0001_0028.md`
