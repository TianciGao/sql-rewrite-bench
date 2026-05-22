# PG Plan Attribution 113 Policy V1

Retained denominator: exactly 113 PostgreSQL attribution-ready candidates from the freeze folder.
Plan command: `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` with `statement_timeout=60s` inside a read-only transaction when possible.
Candidates are never silently dropped. Failures remain in the denominator and are recorded explicitly.
Attribution is conservative and remains `none`, `low`, `medium`, or `high`, although this packet uses no stronger than retained evidence supports.
中文说明：这里的目标是 route x frontier x tag coverage，不是 full 120 plan attribution，也不是 global causal attribution。
