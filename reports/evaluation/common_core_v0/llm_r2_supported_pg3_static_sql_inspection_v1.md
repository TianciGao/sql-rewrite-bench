# LLM-R2 Supported PG3 Static SQL Inspection v1

This is static inspection only.

This packet reviews retained SQL text from the completed local human-run
LLM-R2 supported PG3 generation dry-run. It does not run PostgreSQL, checker,
timing, or speedup work. It does not create paper evidence, exact-match
evidence, or `120`-row evidence.

## Scope Recap

Generated rows under review:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Retained scope under review:

- generated SQL file presence
- text-only SQL shape inspection
- obvious wrapper / side-effect / multi-statement screening
- future execution-planning eligibility screening

Not run:

- PostgreSQL execution
- checker
- timing
- speedup
- MySQL/Spark
- full `120` generation

## Per-Row Inspection Table

| case_id | generated_sql_path | file_exists | non_empty | has_select_or_with | has_semicolon | markdown_fence_detected | natural_language_wrapper_detected | multiple_statement_risk | side_effect_statement_detected | static_parse_status | static_inspection_status | eligible_for_future_execution_planning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0006/generated_sql_schema_native_clean_v1.sql` | `true` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | `UNKNOWN_NOT_RUN` | `pass_no_obvious_text_blocker` | `yes` |
| `PERF_0013` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0013/generated_sql_schema_native_clean_v1.sql` | `true` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | `UNKNOWN_NOT_RUN` | `pass_no_obvious_text_blocker` | `yes` |
| `PERF_0024` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0024/generated_sql_schema_native_clean_v2.sql` | `true` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | `UNKNOWN_NOT_RUN` | `pass_no_obvious_text_blocker` | `yes` |

## Retained Artifact Table

| case_id | generated_sql_path | stdout_path | stderr_path | runtime_snapshot_path |
| --- | --- | --- | --- | --- |
| `PERF_0006` | `retained_tmp_artifacts/PERF_0006/generated_sql_schema_native_clean_v1.sql` | `logs/PERF_0006.stdout.log` | `logs/PERF_0006.stderr.log` | `runtime_snapshots/PERF_0006_files.txt` |
| `PERF_0013` | `retained_tmp_artifacts/PERF_0013/generated_sql_schema_native_clean_v1.sql` | `logs/PERF_0013.stdout.log` | `logs/PERF_0013.stderr.log` | `runtime_snapshots/PERF_0013_files.txt` |
| `PERF_0024` | `retained_tmp_artifacts/PERF_0024/generated_sql_schema_native_clean_v2.sql` | `logs/PERF_0024.stdout.log` | `logs/PERF_0024.stderr.log` | `runtime_snapshots/PERF_0024_files.txt` |

## Generated SQL Retention Summary

All 3 retained SQL files:

- exist
- are non-empty
- contain `SELECT`
- end with a semicolon
- do not show markdown fences
- do not show obvious natural-language wrapper text
- do not show obvious multiple unrelated statements
- do not show obvious `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, or
  `CREATE` side-effect statements

Static parse status remains `UNKNOWN_NOT_RUN` because this packet does not run a
SQL parser.

## No-DB / Checker / Timing Attestation Summary

The retained run attestation remains unchanged:

- PostgreSQL execution not run
- checker not run
- timing not run
- speedup not run
- MySQL/Spark not run
- full `120` generation not run

## Gate Decision

All 3 retained SQL files pass this text-only screening stage with no obvious
text-level blockers.

This makes all 3 rows eligible for future human-reviewed PostgreSQL
execution/checker planning only. This packet does not authorize that work.

## Next Recommended Gate

Human review static SQL inspection and decide whether to authorize a future PG
execution/checker planning packet.

## Explicit Non-Claims

- This is static inspection only.
- This does not run PostgreSQL.
- This does not run checker.
- This does not run timing or speedup.
- This does not claim correctness or exact match.
- This does not claim timing evidence.
- This does not claim MySQL/Spark support.
- This does not claim full `120`-row evidence.
- This does not create a result card, proposed row, or leaderboard.
