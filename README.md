# SQL Rewrite Benchmark

## Scope
- Engines / dialects: Spark SQL, PostgreSQL, MySQL
- Minimum benchmark unit: case package
- v1 excludes compositional OOD split
- v1 excludes engine / dialect hold-out split

## Repository interpretation
This repository is currently best understood as a **pre-pilot / early-pilot SQL rewrite benchmark build**.

It has already progressed beyond bootstrap and now contains:
- a stable four-pool benchmark structure,
- explicit source-to-case separation,
- stable anchor cases,
- admitted external common-core cases,
- staged drafts with different closure levels,
- and a first paper-facing evaluation slice.

This repository should **not** yet be interpreted as:
- a full pilot-scale benchmark release,
- a fully closed source universe,
- a broad workload-curation completion,
- or a full baseline-comparison package.

## Current stable first slice
The current first evaluation slice includes:

- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`
- `PERF_0002`
- `PORT_0002`
- `CONS_0003`
- `CONS_0004`

These cases were selected because they jointly provide:
- all four pools,
- anchor / admitted / staged maturity contrast,
- and sufficiently stable multi-engine validation evidence.

## Current repository status
The repository currently contains:

### Stable anchors
- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`

### Admitted external common-core cases
- `PERF_0002`
- `PORT_0002`

### Tri-engine validated staged drafts
- `CONS_0003`
- `CONS_0004`

### Staged but excluded from the first slice
- `LONGTAIL_0002`
- `CONS_0002`
- `PERF_0003`
- `PERF_0004`

## Source-layer interpretation
Different source families currently play different roles:

- **TPC-DS**: active external performance line
- **SQLStorm**: active long-tail source, but staged case line
- **Calcite**: active consistency seed source, but staged case line
- **VeriEQL**: active consistency supplement line
- **PARROT**: active external portability line
- **JOB**: partial realized performance supplement
- **Stack**: realism substrate only, not a direct SQL query corpus
- **DSB**: unresolved / not yet started
- **Manual Seed Cases**: internal anchor source family, not a fifth pool

## Environment conventions
- Primary development environment: WSL Ubuntu
- Git over SSH
- PostgreSQL runs on Windows host and is accessed from WSL over NAT
- MySQL runs inside WSL for local validation
- Spark runs in local mode inside WSL
- Codex / automation helpers should be started inside the same WSL shell with required environment variables

## Current engineering baseline
The repository currently has:
- PostgreSQL smoke passed
- MySQL smoke passed
- Spark smoke passed
- tri-engine smoke / preflight CLI checks
- machine-readable result and plan artifacts
- first formal coverage map
- first formal gap report
- first pilot reporting tables

## Current focus
The current focus is **first-slice evaluation and paper-facing result organization**, not broad source expansion.

This means the immediate emphasis is on:
1. generating stable pilot tables,
2. drafting the first results subsection,
3. and organizing current evidence into a paper-ready form.

The current focus is **not**:
- broad workload curation,
- large-scale source expansion,
- or full baseline-comparison execution.

## Project design principles
- source != benchmark unit
- case package = benchmark unit
- four formal pools only:
  - performance
  - longtail
  - consistency
  - portability
- `Manual Seed Cases` is a source family / curation channel, not a fifth pool

## Recommended current reading path
If you are new to the repository, start from:
1. `docs/PROJECT_PLAN.md`
2. `benchmark_spec/decision_log.md`
3. `docs/M1_GAP_REPORT.md`
4. `reports/pilot/`
5. `docs/FIRST_PILOT_RESULTS.md` / `docs/FIRST_SLICE_APPENDIX.md`