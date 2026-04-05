# SQL Rewrite Benchmark

## Scope
- Engines / dialects: Spark SQL, PostgreSQL, MySQL
- Minimum benchmark unit: case package
- v1 excludes compositional OOD split
- v1 excludes engine / dialect hold-out split

## Week 1 status
- PostgreSQL smoke: passed
- MySQL smoke: passed
- Spark smoke: passed
- benchmark_spec v0 created
- coverage_taxonomy v0.1 created
- case_schema v0.1 created
- first smoke case package created

## Environment conventions
- Primary development environment: WSL Ubuntu
- Git over SSH
- PostgreSQL runs on Windows host, accessed from WSL over NAT
- MySQL currently runs inside WSL for Week 1 unblocking
- Spark runs in local mode inside WSL
- Codex must be started inside the same WSL shell with required env vars

## Current focus
Week 1 closeout:
1. Run a tri-engine minimal case closure for PERF_0001
2. Save machine-readable outputs
3. Add minimal CLI / preflight scaffolding
