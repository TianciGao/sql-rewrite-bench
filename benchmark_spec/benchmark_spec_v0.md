# Benchmark Spec v0

## Scope
- Dialects / engines: Spark SQL, PostgreSQL, MySQL
- Version scope: v1
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

## Week-1 goal
- PostgreSQL / MySQL / Spark smoke all pass
- taxonomy v0.1 exists
- case schema v0.1 exists
- first case package template exists
