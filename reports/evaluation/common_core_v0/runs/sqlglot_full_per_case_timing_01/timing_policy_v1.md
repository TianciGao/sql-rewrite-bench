# Timing Policy v1

- warmup count: 1
- repeat count: 3
- timeout policy: 30s per query attempt
- speedup ratio: source_runtime_ms / rewrite_runtime_ms using row-local medians
- win: speedup_ratio > 1.05
- tie: 0.95 <= speedup_ratio <= 1.05
- loss: speedup_ratio < 0.95
- Regression@20: speedup_ratio < 0.8
- routes stay separated: `sqlglot_transpile_same_dialect_noop`, `sqlglot_optimize_same_dialect`
