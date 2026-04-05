# AGENTS.md

## Project identity
This repository is a SQL rewrite benchmark project.
Its current benchmark scope is limited to Spark SQL, PostgreSQL, and MySQL.

## Source-of-truth order
When instructions conflict, follow this priority order:
1. Human direct instruction in current session
2. benchmark_spec/decision_log.md
3. docs/PROJECT_PLAN.md
4. benchmark_spec/benchmark_spec_v0.md
5. README.md

## Current phase
Current phase is:
- Week 1 closeout completed
- CLI scaffolding and artifact-preflight stage
- Not yet in workload curation / Phase 2

## Frozen scope for v1
- Engines / dialects: Spark SQL, PostgreSQL, MySQL
- Minimum benchmark unit: case package
- v1 does NOT include compositional OOD split
- v1 does NOT include engine / dialect hold-out split
- v1 does NOT include UDF / stored procedure / trigger benchmarking
- v1 does NOT expand beyond the currently approved benchmark protocol

## Allowed work in current phase
- CLI scaffolding
- environment checks
- PostgreSQL / MySQL / Spark smoke checks
- artifact-preflight
- machine-readable report generation
- helper scripts under scripts/ and tools/
- non-semantic refactoring for maintainability
- adding missing operational documentation consistent with frozen protocol

## Disallowed work in current phase
- adding new benchmark workloads
- generating new benchmark cases
- modifying benchmark protocol files without human approval
- changing taxonomy principles
- changing primary metrics
- starting workload curation
- entering Phase 2 or later phases
- expanding to new engines or dialects
- introducing local-LLM dependency as a startup requirement

## Environment conventions
- Primary development environment: WSL Ubuntu
- Git over SSH
- PostgreSQL runs on Windows host, accessed from WSL through NAT
- MySQL currently runs inside WSL for Week 1 / early bootstrap
- Spark runs in local mode inside WSL
- Required environment variables must be set in the same WSL shell before starting Codex

## Important files
- benchmark_spec/benchmark_spec_v0.md
- benchmark_spec/case_schema_v0.1.yaml
- benchmark_spec/decision_log.md
- taxonomy/coverage_taxonomy_v0.1.yaml
- docs/PROJECT_PLAN.md
- cases/PERF/PERF_0001/manifest.yaml
- README.md

## Required behavior
- Prefer reading existing project files before creating new abstractions
- Preserve existing benchmark semantics
- Write machine-readable outputs where appropriate
- Keep scripts simple and inspectable
- If unsure whether something belongs to Phase 2, stop and ask

## Stop-and-ask conditions
Stop and ask a human before:
- changing benchmark protocol files
- adding or editing benchmark cases
- downloading new workloads
- expanding taxonomy scope
- changing primary metrics
- entering workload curation
- changing engine scope
- changing result-checking rules