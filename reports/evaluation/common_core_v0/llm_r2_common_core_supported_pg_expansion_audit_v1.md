# LLM-R2 Common-core Supported PostgreSQL Expansion Candidate Audit v1

This is planning/audit only.

No generation, execution, checker, timing, or speedup was run.

## Bounded Prior Evidence

Current bounded PG3 evidence for `llm_r2` is:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

These rows have:

- PG3 generation dry-run passed
- static SQL inspection passed
- PostgreSQL execution/checker `_02` exact match

This remains PG3-only bounded evidence.
It is not PG40 evidence.
It is not MySQL/Spark evidence.
It is not full `common_core_v0_40_same_engine_120` evidence.

## Recovered LLM-R2 Supported Set

Recovered current support basis from `scripts/cli.py` and retained bounded
LLM-R2 scratch evidence:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

Current repo-local declaration basis:

- `LLMR2_SUPPORTED_CASE_IDS` in [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:240)

Historical bounded-smoke support notes:

- Batch A: `PERF_0008`, `PERF_0013`, `PERF_0017`
- Batch B: `PERF_0019`, `PERF_0024`, `PERF_0033`
- Batch C: `PERF_0052`, `PERF_0054`, `PERF_0063`

## Common-core 40 Intersection

The recovered support set intersects the frozen common-core 40 denominator on
these PostgreSQL candidate cases:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Recovered support outside common-core 40:

- `PERF_0063`

## Do-Not-Include Rows

Do not include these in the next bounded PG expansion slice:

- `PERF_0006`
  - already part of completed bounded PG3 exact-match evidence
- `PERF_0013`
  - already part of completed bounded PG3 exact-match evidence
- `PERF_0024`
  - already part of completed bounded PG3 exact-match evidence
- `PERF_0063`
  - runner-supported historically, but outside the frozen common-core 40
    denominator and also carries a historical logical-plan probe blocker
- `PERF_0007`
  - in common-core 40 but not runner-supported now; remains in PG5 wrapper
    extension hold
- `CONS_0005`
  - in common-core 40 but not runner-supported now; wrapper extension required
- `CONS_0007`
  - in common-core 40 but not runner-supported now; wrapper extension required
- `LONGTAIL_0011`
  - in common-core 40 but not runner-supported now; wrapper extension required
- `LONGTAIL_0013`
  - in common-core 40 but not runner-supported now; wrapper extension required

## Next Recommended PG Expansion Slice

Recommended bounded next-run PostgreSQL slice:

- `PERF_0008`
- `PERF_0017`
- `PERF_0019`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Rationale:

- all 6 are in the frozen common-core 40 denominator
- all 6 are runner-supported now by recovered declarations and retained bounded
  smoke evidence
- all 6 have case-local `source.sql`
- all 6 have case-local `schema/ddl_pg.sql`
- all 6 have case-local `validation/pg_witness_data.sql`
- none are already consumed by the completed PG3 exact-match packet

## Future Human-Run Planning Feasibility

Future human-run planning is possible for the bounded next slice on an
audit/preflight basis only.

This audit does not authorize:

- PostgreSQL generation
- PostgreSQL execution
- checker
- timing
- speedup
- MySQL/Spark
- PG40 expansion
- full `120`

## Explicit Non-Claims

- This is planning/audit only.
- No LLM-R2 run occurred.
- No PostgreSQL/checker/timing/speedup work occurred.
- This does not create a result card, proposed row, or leaderboard.
- This does not claim PG40 evidence.
- This does not claim full `120` evidence.
