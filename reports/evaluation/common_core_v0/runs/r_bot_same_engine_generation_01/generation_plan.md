# R-Bot Formal `@120` Generation Plan

## Role

This package freezes the human-run generation plan for the formal
`R-Bot` Common-core v0 same-engine denominator:

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `denominator_id = common_core_v0_40_same_engine_120`
- `planned_rows = 120`

It does not execute the run by itself.
It does not create benchmark metrics by itself.

## Package Root vs Output Root

This package is stored under:

- `reports/evaluation/common_core_v0/runs/r_bot_same_engine_generation_01/`

The actual retained formal run outputs must still be written under the frozen
artifact-contract run root:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/`

That split is intentional:

- this directory holds the human-run generation package
- the retained formal outputs must remain at the contract path already frozen by the artifact-contract package

## Inputs Frozen Into This Package

- [formal_gate_status_v13.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v13.md)
- [r_bot_common_core_v0_40_same_engine_candidate_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv)
- [r_bot_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [formal_artifact_expected_paths.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_artifact_contract_01/formal_artifact_expected_paths.json)
- [formal_artifact_contract_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_artifact_contract_01/formal_artifact_contract_matrix.csv)
- [runtime_environment_snapshot_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)

## Formal Runtime and Retrieval Inputs

The human-run script is pinned to:

- formal Python: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python`
- formal Chroma index: `/tmp/rewritebench_rbot_formal_chroma_index_01`
- retained index identifier:
  `reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json`

Formal parameter freeze used by the package:

- model: `gpt-4o-mini`
- temperature: `0`
- top_p: `1`
- max_tokens: `2048`
- candidate_count: `1`
- feedback_rounds: `0`
- retrieval_top_k: `10`
- reranking_mode: `rrf`
- `rrf_k = 60`
- similarity_threshold: `explicit_none_observed`

## Current Recovered Runner Boundary

The committed recovered runner surface visible in `scripts/cli.py` is still the
PG-oriented single-case `LLM4Rewrite` smoke path:

- implemented entrypoint:
  `formal-rbot-llm4rewrite-single-case-smoke-run`
- currently recovered supported PG case IDs:
  `PERF_0006`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`,
  `PERF_0024`, `PERF_0033`, `PERF_0052`, `PERF_0054`, `PERF_0063`

Therefore this package does not drop any denominator rows.
Instead it keeps explicit planned statuses:

- `human_run_generation_ready` for the recovered PG-supported subset
- `blocked_or_unsupported` for all other rows

This preserves denominator awareness without pretending the recovered committed
runner already covers all `120` rows.

## What The Script Does When Human-Run

The package script is human-run only and is designed to:

1. require `OPENAI_API_KEY` visibility without writing its value
2. require the frozen formal Python and formal Chroma index paths
3. initialize the retained formal run root
4. preserve all `120` rows in `run_event_long.csv`
5. mark blocked/unsupported rows explicitly
6. attempt generation only for rows marked `human_run_generation_ready`
7. continue after row failures
8. write row-level artifacts and package-level summaries without computing execution, timing, speedup, or leaderboard metrics

## Output Contract Inside The Generation Phase

The script is designed to write, per represented row:

- generated SQL when available
- prompt text artifact
- raw response artifact
- selected-rules trace
- retrieval trace
- token/cost/provider metadata
- environment snapshot
- row-level run metadata

When the recovered runner does not expose a given artifact directly, the script
is designed to preserve an explicit placeholder artifact rather than silently
omit that path.

## Decision Boundary

This package means:

- the formal `@120` generation package now exists
- a human may run the generation script

This package does not mean:

- generation has already occurred
- denominator-aware formal run evidence already exists
- execution, validity, timing, speedup, or leaderboard evidence exists
