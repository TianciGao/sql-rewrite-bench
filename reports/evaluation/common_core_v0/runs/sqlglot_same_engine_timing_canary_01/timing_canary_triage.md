**Timing Canary Triage**
Total rows: `18`. Executed rows: `18`. Success rows: `18`. Failed rows: `0`. Rows with timing: `18`.
Warmup / repeat settings were confirmed from `run_results.json`: `warmup_count=1`, `repeat_count=3`.

All `pg`, `mysql`, and `spark` timing runners succeeded for this canary. This package is a timing canary only, not a final `GM_Speedup` or `RegressionRate@20%` result.

Counts by engine:
- `pg`: `6`
- `mysql`: `6`
- `spark`: `6`
Counts by route:
- `sqlglot_optimize_same_dialect`: `9`
- `sqlglot_transpile_same_dialect_noop`: `9`
Counts by pool:
- `performance`: `6`
- `consistency`: `6`
- `longtail`: `6`

Observed stderr patterns:
- `mysql_cli_password_warning`: `6`
- `postgres_schema_cleanup_notice`: `6`
- `spark_native_hadoop_warning`: `6`

Extreme speedup-ratio rows:
- `CONS_0010 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=294.315`, `median_generated_ms=507.360`, `speedup_ratio=0.5801`
- `PERF_0006 / pg / sqlglot_optimize_same_dialect`: `median_source_ms=295.206`, `median_generated_ms=412.255`, `speedup_ratio=0.7161`
- `CONS_0010 / pg / sqlglot_transpile_same_dialect_noop`: `median_source_ms=508.317`, `median_generated_ms=299.047`, `speedup_ratio=1.6998`

Per-row timing summary:

| case_id | pool | engine | route_id | median_source_ms | median_generated_ms | speedup_ratio |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `CONS_0010` | `consistency` | `mysql` | `sqlglot_optimize_same_dialect` | `138.390` | `134.981` | `1.0253` |
| `CONS_0010` | `consistency` | `mysql` | `sqlglot_transpile_same_dialect_noop` | `136.381` | `137.101` | `0.9948` |
| `CONS_0010` | `consistency` | `pg` | `sqlglot_optimize_same_dialect` | `294.315` | `507.360` | `0.5801` |
| `CONS_0010` | `consistency` | `pg` | `sqlglot_transpile_same_dialect_noop` | `508.317` | `299.047` | `1.6998` |
| `CONS_0010` | `consistency` | `spark` | `sqlglot_optimize_same_dialect` | `261.182` | `277.800` | `0.9402` |
| `CONS_0010` | `consistency` | `spark` | `sqlglot_transpile_same_dialect_noop` | `274.478` | `268.975` | `1.0205` |
| `LONGTAIL_0011` | `longtail` | `mysql` | `sqlglot_optimize_same_dialect` | `134.886` | `137.371` | `0.9819` |
| `LONGTAIL_0011` | `longtail` | `mysql` | `sqlglot_transpile_same_dialect_noop` | `135.934` | `138.890` | `0.9787` |
| `LONGTAIL_0011` | `longtail` | `pg` | `sqlglot_optimize_same_dialect` | `459.669` | `468.496` | `0.9812` |
| `LONGTAIL_0011` | `longtail` | `pg` | `sqlglot_transpile_same_dialect_noop` | `400.593` | `297.170` | `1.3480` |
| `LONGTAIL_0011` | `longtail` | `spark` | `sqlglot_optimize_same_dialect` | `395.294` | `399.416` | `0.9897` |
| `LONGTAIL_0011` | `longtail` | `spark` | `sqlglot_transpile_same_dialect_noop` | `415.554` | `374.724` | `1.1090` |
| `PERF_0006` | `performance` | `mysql` | `sqlglot_optimize_same_dialect` | `118.228` | `121.202` | `0.9755` |
| `PERF_0006` | `performance` | `mysql` | `sqlglot_transpile_same_dialect_noop` | `118.257` | `120.819` | `0.9788` |
| `PERF_0006` | `performance` | `pg` | `sqlglot_optimize_same_dialect` | `295.206` | `412.255` | `0.7161` |
| `PERF_0006` | `performance` | `pg` | `sqlglot_transpile_same_dialect_noop` | `402.891` | `424.125` | `0.9499` |
| `PERF_0006` | `performance` | `spark` | `sqlglot_optimize_same_dialect` | `231.324` | `225.562` | `1.0255` |
| `PERF_0006` | `performance` | `spark` | `sqlglot_transpile_same_dialect_noop` | `245.817` | `237.930` | `1.0331` |

Recommendation:
- Proceed to the broader SQLGlot same-engine timing run. The runner stack is now clean across `pg`, `mysql`, and `spark`, and the canary produced complete timing payloads for all scoped rows.
- Keep this canary framed as pre-leaderboard evidence. Full timing materialization can proceed, but `GM_Speedup`, `RegressionRate@20%`, and any final leaderboard still require the full denominator-aware timing package.
