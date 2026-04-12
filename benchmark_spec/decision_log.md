# Decision Log

## DL-001
### Decision
Primary benchmark engines / dialects for v1 are fixed to:
- Spark SQL
- PostgreSQL
- MySQL

### Rationale
This constrains complexity and matches the current project freeze.

## DL-002
### Decision
The minimum benchmark unit is a case package, not a single SQL query.

### Rationale
Consistency, plan observability, provenance, and portability all require richer packaging.

## DL-003
### Decision
v1 does not include:
- compositional OOD split
- engine / dialect hold-out split

### Rationale
These settings were considered in early design discussions but are deferred to future versions.

## DL-004
### Decision
PostgreSQL remains on the Windows host and is accessed from WSL over NAT.

### Rationale
This is already validated on the current machine and should not be destabilized during bootstrap.

## DL-005
### Decision
MySQL may run inside WSL during Week 1 / early bootstrap.

### Rationale
This is the fastest path to complete tri-engine smoke closure on the current machine.

## DL-006
### Decision
Codex is allowed to work only on engineering scaffolding in the current phase.

### Allowed examples
- CLI scaffolding
- environment checks
- artifact-preflight
- JSON report generation
- helper scripts

### Disallowed examples
- workload curation
- benchmark expansion
- protocol modifications
- taxonomy redesign
- case generation

## DL-007
### Decision
All important runs must produce machine-readable artifacts.

### Rationale
This is required for reproducibility, preflight checks, and later EA&B writing.

## DL-008
### Decision
Current repository state after Week 1 is treated as a valid closeout checkpoint.

### Evidence
- PostgreSQL smoke passed
- MySQL smoke passed
- Spark smoke passed
- PERF_0001 tri-engine consistency closure passed
- first plans collected
- first commit completed

## DL-009
### Decision
Week 1 bootstrap closeout and minimal CLI scaffolding are considered complete.

### Rationale
The repository now has:
- tri-engine smoke closure
- first case-package closure
- first plan artifacts
- minimal CLI commands
- artifact-preflight reports

### Next step
Proceed to source inventory design and pool mapping preparation, while still not entering workload curation.

## DL-010
### Decision
For v0 source inventory, the consistency-oriented equivalence benchmark source is initialized with SQLEquiQuest rather than VeriEQL.

### Rationale
A single equivalence benchmark source is sufficient for early pilot inventory design.
Additional equivalence sources may be added later if needed.

### 2026-04-12 external promotion review applied

Applied the first external-case promotion review to case-local metadata.

Decisions reflected in manifests and taxonomy trial files:

- `PERF_0002` is now treated as a `common-core_candidate`
  because it has tri-engine source validation and tri-engine positive/negative rewrite validation.
- `PORT_0002` is now treated as a `common-core_candidate`
  because it has PostgreSQL source validation plus MySQL positive/negative portability validation.
- `LONGTAIL_0002` remains `not_yet_admitted`.
- `CONS_0002` remains `not_yet_admitted`.

Rationale:
the project has now reached the point where promotion review outcomes should
be reflected in case-local metadata rather than only in cross-case documents.

## DL-011
### Decision
`PERF_0002` is admitted as the first external common-core case in the repository.

### Rationale
`PERF_0002` now satisfies the current common-core admission check:
- provenance is complete
- source, positive, and negative rewrites are all present
- PostgreSQL, MySQL, and Spark all validate source behavior
- PostgreSQL, MySQL, and Spark all validate source/positive equivalence
- PostgreSQL, MySQL, and Spark all validate source/negative divergence
- plan artifacts are collected across the validated engines

### Next step
Keep `PORT_0002` under `common-core_candidate` review, while `LONGTAIL_0002` and `CONS_0002` remain staged draft cases.
