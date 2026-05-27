# LLM-R2 Recovered-Extraction PG3 Failed Rerun Review v1

This is governance review only.

No LLM-R2 inference, PostgreSQL, checker, timing, speedup, MySQL, or Spark
command was run for this packet.

## Scope

- `route_id = llm_r2_recovered_extraction_route_v1`
- rows:
  - `PERF_0006`
  - `PERF_0013`
  - `PERF_0024`
- PostgreSQL only
- recovered-extraction route only

## Generation Result

- `generated_rows = 3`
- `output_sql_extracted_rows = 3`
- `recovered_sql_retained_rows = 3`

All three recovered-route generation runs succeeded and retained separate-route
artifacts.

## Execution / Checker Result

- `pg_source_executed_rows = 3`
- `pg_generated_executed_rows = 0`
- `exact_match_rows = 0`
- `generated_execution_failed_rows = 3`

## Per-Case Table

| case_id | engine | generated_status | source_execution_status | generated_execution_status | exact_match | failure_bucket | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | generated SQL contains duplicated trailing `SELECT` after a complete query body |
| `PERF_0013` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | generated SQL contains duplicated trailing `SELECT` after a complete query body |
| `PERF_0024` | `pg` | `generated` | `executed` | `failed` | `false` | `execution_failed` | generated SQL contains duplicated trailing `SELECT` after a complete query body |

## Failure Class

- `failure_bucket = execution_failed`
- PostgreSQL syntax error
- generated SQL contains duplicated or malformed trailing `SELECT` after an
  already complete query body

## Rollup

- `recovered_pg3_appendix_extension = failed`
- `recovered_pg9_appendix_evidence = not_achieved`
- `timing_rows = 0`
- `mysql_rows = 0`
- `spark_rows = 0`
- `full120_evidence = no`
- `leaderboard_comparable = no`

## Relationship To Existing Evidence

- original-route PG9 remains unchanged:
  - `9 generated / 3 exact / 6 execution_failed`
- recovered-route PG6 remains unchanged:
  - `6 generated / 6 PG exact`
- recovered-route PG3 rerun failed:
  - `3 generated / 0 exact`
- therefore recovered-route PG9 cannot be claimed

## Paper-Safe Interpretation

- `LLM-R2` can be reported only as bounded or diagnostic appendix evidence
- it is not suitable for the main `120` denominator table
- it is not suitable for leaderboard comparison
- further wrapper repair would require a new route and must not be mixed with
  current original-route or recovered-route evidence packets

## Non-Claims

- This does not create recovered PG9 appendix evidence.
- This does not replace the frozen original-route PG9 packet.
- This does not create PG40 evidence.
- This does not create full `120` evidence.
- This does not claim MySQL/Spark support.
- This does not claim timing or speedup.
- This does not create a leaderboard row.
- This does not create or update a result card.
- This does not update `method_comparison_summary_v2`.

## Next Recommended Gate

Stop the recovered-route PG9 appendix pursuit for now and preserve:

- original-route PG9 as frozen bounded original-route evidence
- recovered-route PG6 as separate bounded recovered-route appendix evidence

Any further work should be a separate recovered-route extraction-failure audit
or a new recovery route, not an extension of the current packet family.
