# First Pilot Evaluation Plan

## File role
This file defines a **pre-pilot evaluation slice** based on the currently stabilized subset of the repository.

It does **not** imply that the repository has reached full pilot scale, M2 completion, or broad benchmark-expansion readiness.
Instead, it exists to:
- organize the first small experimental slice,
- define which cases are currently stable enough to report,
- clarify which metrics should be reported first,
- and provide an initial paper-table skeleton.

---

## 1. Current interpretation

The repository has completed:
- local tri-engine smoke closure,
- first anchor-case closure,
- source / case / admission document alignment,
- first formal coverage map,
- first formal gap report,
- and a minimal CLI / artifact-preflight layer.

However, the repository has **not** yet reached:
- full M2 pilot scale,
- broad workload curation,
- large-scale benchmark expansion,
- or full baseline-comparison execution.

Therefore, the next appropriate step is a **small, controlled first evaluation slice**, not a formal full-pilot claim.

---

## 2. Goal of the first evaluation slice

The first evaluation slice is designed to answer four narrow questions:

1. Can the benchmark already demonstrate a stable multi-pool structure?
2. Can the benchmark already show admitted vs staged case stratification?
3. Can the benchmark already demonstrate tri-engine consistency evidence on a small subset?
4. Can the benchmark already generate paper-usable summary tables without pretending that the full pilot is complete?

This slice is intended to support:
- early paper drafting,
- table and figure prototyping,
- and fast detection of missing experiment fields.

---

## 3. Included cases in the first slice

The following cases are included:

### 3.1 Stable anchors
- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`

### 3.2 Admitted external common-core cases
- `PERF_0002`
- `PORT_0002`

### 3.3 Tri-engine validated staged consistency drafts
- `CONS_0003`
- `CONS_0004`

These eight cases are chosen because they provide:
- all four pools,
- both anchor and external lines,
- admitted and staged status contrast,
- and strong enough engine-validation evidence to support early reporting.

---

## 4. Explicitly excluded cases in the first slice

The following cases are not included in the first slice:

- `LONGTAIL_0002`
- `CONS_0002`
- `PERF_0003`
- `PERF_0004`

### Reason for exclusion
These cases are currently excluded because they still have unresolved closure gaps, especially:
- PG-only validation,
- partial engine validation,
- or staged probe status without strong enough first-slice stability.

Their exclusion does **not** imply low value.
It only means they are not yet the best choices for the first paper-facing evaluation slice.

---

## 5. First-slice reporting targets

The first slice should prioritize **stability and interpretability** over scale.

### 5.1 Core reporting axes
The first slice should report:

- case distribution by pool,
- case distribution by maturity level,
- admitted vs staged split,
- source-family to case mapping,
- engine-validation coverage,
- and plan-artifact coverage.

### 5.2 First-slice metric focus
The first slice should prioritize:

#### Correctness
- `ExecutableRate`
- `ResultConsistencyRate`
- `NegativeRejectionRate`

#### Generalization
- `CrossEngineExecutableRate`
- `CrossEngineConsistencyRate`

#### Observability
- `PlanArtifactCoverage`

These are preferred first because they align with the benchmark’s current strongest evidence:
- multi-engine closure,
- correctness-aware benchmark structure,
- and plan-level artifact capture.

### 5.3 Metrics intentionally deferred
The following are deferred to later phases:
- full baseline ranking
- workload-level performance comparison
- large-scale speedup analysis
- broad ranking-shift study
- mature portability leaderboard
- broader source-universe expansion

---

## 6. First paper-table skeleton

The first slice should be sufficient to generate at least the following tables.

### Table A. Case maturity matrix
Columns:
- case_id
- pool
- source_family
- maturity
- validated_engines
- admitted_or_staged

### Table B. Source-to-case materialization table
Columns:
- source_family
- current role
- materialized cases
- current line status

### Table C. Included vs excluded first-slice cases
Columns:
- case_id
- included_in_first_slice
- reason

### Table D. Engine-validation summary
Columns:
- case_id
- postgres
- mysql
- spark
- notes

### Table E. Plan-artifact coverage summary
Columns:
- case_id
- result_artifacts_present
- plan_artifacts_present
- current observability status

---

## 7. First-slice non-goals

The first slice explicitly does **not** claim:

- that the repository has reached full pilot scale,
- that the benchmark is already ready for broad leaderboard reporting,
- that all source-universe branches are closed,
- that DSB has been activated,
- that broad workload curation has begun,
- or that full baseline comparison is ready.

This file must not be interpreted as an M2 completion claim.

---

## 8. Operational next step after this file

After this plan is created, the next immediate work should be:

1. generate the first case-maturity matrix,
2. generate the first source-to-case mapping table,
3. generate the first admitted-vs-staged summary,
4. and prepare one compact pilot-results appendix block for paper drafting.

Only after these small reporting artifacts exist should the team decide whether to:
- deepen staged draft lines,
- activate DSB,
- or broaden source expansion.

---

## 9. Current recommended interpretation

The repository is now in the following state:

- source-layer closeout is largely synchronized,
- a small stable case subset exists,
- the first evaluation slice is justified,
- but the project is still pre-pilot / early-pilot in scale.

Therefore, this file should be treated as:
**an evaluation-slice planning document, not a final pilot declaration.**