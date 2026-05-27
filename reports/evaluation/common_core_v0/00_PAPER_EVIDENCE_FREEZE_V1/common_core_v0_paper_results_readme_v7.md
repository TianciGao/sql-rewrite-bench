# Common-core v0 Paper Results Readme V7

This version adds the reviewed 24-row PostgreSQL EXPLAIN ANALYZE BUFFERS attribution packet.

- Table 5 v4 keeps the route-level observability framing and adds selected PG attribution coverage for the 5 main routes.
- Table 10 v4 aggregates the 24-row PG packet into route-level plan-delta evidence.
- This packet does not replace Table 6 timing and does not justify denominator-wide node alignment or global causal attribution.

中文说明：v7 的核心增量是 24 行 PG 计划归因 packet。它增强了 selected-case observability，但仍然不是 full-denominator attribution benchmark。
