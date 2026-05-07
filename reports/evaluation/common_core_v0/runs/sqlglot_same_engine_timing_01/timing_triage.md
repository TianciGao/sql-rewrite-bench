**Timing Triage**
Total timing rows: `137`. Executed rows: `137`. Success rows: `137`. Failed rows: `0`. Rows with timing: `137`.
Warmup / repeat were confirmed from `run_results.json`: `warmup_count=1`, `repeat_count=3`.

This is timing evidence only. It is not final `GM_Speedup`, not final `RegressionRate@20%`, and not a final same-engine leaderboard.

Counts by engine:
- `pg`: `49`
- `mysql`: `50`
- `spark`: `38`
Counts by route:
- `sqlglot_optimize_same_dialect`: `65`
- `sqlglot_transpile_same_dialect_noop`: `72`
Counts by pool:
- `performance`: `56`
- `consistency`: `36`
- `longtail`: `36`
- `portability`: `9`

Median runtime distribution summary:
- `median_source_ms`: min `114.077`, p25 `166.770`, median `298.268`, p75 `393.489`, max `1547.776`
- `median_generated_ms`: min `113.628`, p25 `167.642`, median `297.474`, p75 `378.239`, max `1538.215`
- `speedup_ratio`: min `0.5799`, p25 `0.9908`, median `1.0075`, p75 `1.0377`, max `1.7537`, mean `1.0274`

Top fastest speedup-ratio rows:
- `PERF_0077 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=530.901`, `median_generated_ms=302.726`, `speedup_ratio=1.7537`
- `PERF_0062 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=458.198`, `median_generated_ms=314.610`, `speedup_ratio=1.4564`
- `PERF_0017 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=438.922`, `median_generated_ms=308.007`, `speedup_ratio=1.4250`
- `PERF_0034 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=414.952`, `median_generated_ms=305.133`, `speedup_ratio=1.3599`
- `PERF_0077 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=404.190`, `median_generated_ms=301.000`, `speedup_ratio=1.3428`
- `CONS_0009 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=396.842`, `median_generated_ms=296.170`, `speedup_ratio=1.3399`
- `PERF_0019 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=398.452`, `median_generated_ms=297.544`, `speedup_ratio=1.3391`
- `CONS_0005 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=396.839`, `median_generated_ms=297.075`, `speedup_ratio=1.3358`
- `LONGTAIL_0022 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=406.331`, `median_generated_ms=304.852`, `speedup_ratio=1.3329`
- `PERF_0082 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=408.585`, `median_generated_ms=316.484`, `speedup_ratio=1.2910`

Top slowest speedup-ratio rows:
- `PERF_0035 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=301.839`, `median_generated_ms=520.464`, `speedup_ratio=0.5799`
- `CONS_0007 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=295.728`, `median_generated_ms=487.619`, `speedup_ratio=0.6065`
- `PORT_0003 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=299.094`, `median_generated_ms=414.403`, `speedup_ratio=0.7217`
- `CONS_0010 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=296.388`, `median_generated_ms=405.806`, `speedup_ratio=0.7304`
- `CONS_0012 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=299.679`, `median_generated_ms=404.429`, `speedup_ratio=0.7410`
- `PERF_0082 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=313.462`, `median_generated_ms=418.595`, `speedup_ratio=0.7488`
- `PERF_0034 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=302.998`, `median_generated_ms=402.949`, `speedup_ratio=0.7520`
- `PERF_0035 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=331.315`, `median_generated_ms=413.443`, `speedup_ratio=0.8014`
- `PERF_0052 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=363.258`, `median_generated_ms=409.538`, `speedup_ratio=0.8870`
- `CONS_0036 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=294.660`, `median_generated_ms=325.575`, `speedup_ratio=0.9050`

Extreme or suspicious timing values:
- `PERF_0056 / spark / sqlglot_optimize_same_dialect`: `median_source_ms=1547.776`, `median_generated_ms=1498.023`, `speedup_ratio=1.0332`
- `PERF_0056 / spark / sqlglot_transpile_same_dialect_noop`: `median_source_ms=1524.026`, `median_generated_ms=1538.215`, `speedup_ratio=0.9908`

Observed stderr warning patterns:
- `mysql_cli_password_warning`: `50`
- `postgres_schema_cleanup_notice`: `49`
- `spark_native_hadoop_warning`: `38`

Recommendation:
- Proceed to speedup-summary materialization next. The full timing run is complete, denominator-shaped within the timing-eligible slice, and all 137 rows executed successfully.
- Keep the next package explicitly framed as timing/speedup evidence, not a final leaderboard, until denominator-aware exclusions and reporting policy are materialized.
