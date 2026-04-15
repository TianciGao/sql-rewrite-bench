# Decision Log

## DL-001
### Decision
Primary benchmark engines / dialects for v1 are fixed to:
- Spark SQL
- PostgreSQL
- MySQL

### Rationale
This constrains scope and matches the current project freeze.

---

## DL-002
### Decision
The minimum benchmark unit is a case package, not a single SQL query.

### Rationale
Consistency, provenance, plan observability, and portability all require richer packaging.

---

## DL-003
### Decision
v1 does not include:
- compositional OOD split
- engine / dialect hold-out split

### Rationale
These settings were considered in early design discussions but are deferred to future versions.

---

## DL-004
### Decision
Four formal pools only:
- performance
- longtail
- consistency
- portability

`Manual Seed Cases` is treated as `manual_seed` source family / curation channel, not as a fifth pool.

### Rationale
Pools are for final case-package归档; manual seeds belong to source-layer / construction-layer.

---

## DL-005
### Decision
Source and case must be tracked separately.

### Rationale
- source = 原料
- case package = benchmark 单位
- source_family = 来源分类
- pool = case 归档

This separation is now treated as a required repository convention.

---

## DL-006
### Decision
PostgreSQL remains on the Windows host and is accessed from WSL over NAT in the validated local development path.

### Rationale
This path is already validated and should not be destabilized during bootstrap / early pilot.

---

## DL-007
### Decision
MySQL may run inside WSL during Week-1 / early bootstrap for local tri-engine smoke closure.

### Rationale
This is an operational unblocking decision, not a semantic benchmark decision.

---

## DL-008
### Decision
`PERF_0002` is admitted as the first external common-core case.

### Rationale
The case satisfies the current common-core admission basis with tri-engine closure.

---

## DL-009
### Decision
`PORT_0002` is admitted as the second external common-core case.

### Rationale
`PORT_0002` now has sufficiently strong portability closure and should no longer be described as merely a candidate.

---

## DL-010
### Decision
VeriEQL is accepted as the current Batch-2 consistency supplement source.

### Rationale
The line has already materialized into `CONS_0003` and `CONS_0004`, proving it usable for controlled consistency-pool seed extraction.

### Consequence
In current-state documents, “SQLEquiQuest / VeriEQL 待二选一” must no longer be treated as still pending.

---

## DL-011
### Decision
`CONS_0004` should remain a staged, not_yet_admitted tri-engine validated draft for now.

### Rationale
The case is useful and valid, and it now has controlled PostgreSQL + MySQL + Spark witness validation.
However, immediate broader deepening is still not required in the current phase.

### Consequence
The real next issue for `CONS_0004` is no longer Spark closure, but whether to keep it staged or deliberately deepen the consistency line in a later pass.

---

## DL-012
### Decision
Current active phase is document / source-state / case-state alignment and M1-closeout preparation.

### Rationale
Before broader workload curation or benchmark expansion, the repository must synchronize:
- phase docs
- source registry
- external draft status
- coverage-map / gap-report expectations

### Consequence
Do not broaden source acquisition or large-scale workload curation until the current sync layer is finished.

---

## DL-013
### Decision
All important checks and runs must produce machine-readable artifacts.

### Rationale
This is required for reproducibility, preflight checks, and later EA&B writing.

---

## DL-014
### Decision
M1 source-layer closeout artifacts are now complete.

### Basis
The repository now has:
- synchronized external draft status
- synchronized current phase closeout checklist
- synchronized DOC_MAP
- aligned target-source snapshot
- first formal M1 coverage map
- formal M1 gap report

### Consequence
Broad workload curation must still not begin immediately.
The next action is an explicit human decision on unresolved target-source branches:
- JOB: deepen or freeze as partial realized supplement
- DSB: start acquisition or remain target-only

---

## DL-015
### Decision
The current Stack line does not provide a direct SQL query corpus.
It is therefore frozen as a realism substrate / dumps-based source, not as an active direct-query source.

### Rationale
Current repository inspection shows that `datasets/raw/stack_queries/` contains:
- archive files
- XML dumps
- notes / interpretation files

It does not currently provide a ready direct SQL query corpus comparable to active case-seed sources.

### Consequence
- Do not describe Stack as an already available direct SQL query source
- Treat Stack as realism substrate only in the current phase
- The next unresolved source decisions are now JOB and DSB

---

## DL-016
### Decision
The current JOB line is frozen as a partial realized performance supplement for now.

### Rationale
The JOB line has already materialized into `PERF_0003` and `PERF_0004`, proving it usable as a controlled supplement source.
However, the current phase is still source-layer closeout / pre-curation preparation, not broader workload expansion.

### Consequence
- Do not describe JOB as a fully closed source line
- Do not deepen the JOB line further in the current phase
- The next remaining unresolved source decision is now DSB

---

## DL-017
### Decision
`CONS_0003` and `CONS_0004` now both have tri-engine closure on PostgreSQL, MySQL, and Spark.

### Rationale
The previously identified Spark-side consistency gap for the VeriEQL-derived staged drafts has now been closed by direct execution and plan collection.

### Consequence
- Both cases remain staged / not_yet_admitted
- Immediate next work should shift from engine-closure repair to small pilot evaluation and selective next-step planning
- DSB remains unresolved and should not be silently frozen without an explicit human decision
