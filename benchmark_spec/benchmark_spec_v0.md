# Benchmark Spec v0

## Role of this document
This file defines the current executable benchmark boundary for the repository.
For the full research plan, see `docs/PROJECT_PLAN.md`.

## Scope
- Dialects / engines: Spark SQL, PostgreSQL, MySQL
- Version scope: v1 bootstrap / early pilot
- No compositional OOD split
- No engine hold-out split

## Tracks
A. Same-engine rewrite  
B. Plan-observable rewrite  
C. Cross-dialect / cross-engine rewrite

## Minimum benchmark unit
Case package

## Primary metric groups
1. Consistency
2. Performance
3. Plan observability
4. Generalization

## Current required artifacts
- benchmark_spec/case_schema_v0.1.yaml
- taxonomy/coverage_taxonomy_v0.1.yaml
- cases/PERF/PERF_0001/manifest.yaml
- runs/smoke_case/
- runs/plans/

## Current phase
- Week 1 closeout completed
- Next step: minimal CLI scaffolding and artifact-preflight
- Not yet in workload curation / Phase 2

## Current rules
- Do not add benchmark workloads without human approval
- Do not generate new benchmark cases in the current phase
- Do not modify benchmark protocol files without human approval
- Do not enter workload curation or benchmark expansion in the current phase

## Current confirmed status
- PostgreSQL smoke passed
- MySQL smoke passed
- Spark smoke passed
- PERF_0001 tri-engine consistency closure passed
- First plan artifacts collected
- Initial repository commit completed