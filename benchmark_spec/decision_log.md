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