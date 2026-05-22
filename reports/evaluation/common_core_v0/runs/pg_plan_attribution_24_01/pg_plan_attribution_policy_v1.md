# PG Plan Attribution Policy V1

Reviewed denominator: exactly 24 PostgreSQL candidate IDs from the preflight recommendation.
Plan command: `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` inside `BEGIN READ ONLY` with `statement_timeout=60s`.
Attribution is conservative: only `medium`, `low`, or `none` confidence is used; no denominator-wide node alignment is claimed.
中文说明：这里的 node delta 仅用于 selected-case 可观察性，不是全量因果归因基准。
