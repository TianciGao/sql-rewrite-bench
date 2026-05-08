# R-Bot Paper Parameter Extraction v1

## Scope

This document records the paper-derived `R-Bot` parameter facts supplied for this task and maps them onto the repository's formal benchmark packaging.

It does not run databases.
It does not execute SQL.
It does not call any LLM/API.
It does not authorize benchmark execution.

## Source Basis

Repository artifacts read:

- [r_bot_parameter_freeze_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v1.json)
- [formal_retrieval_config_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v2.json)
- [formal_retrieval_config_extracted_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extracted_v1.json)
- [formal_gate_status_v3.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v3.md)
- [formal_index_dimension_contract_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_index_dimension_contract_v1.json)
- [r_bot_common_core_v0_40_same_engine_protocol.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_protocol.md)
- [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json)
- [COMMON_CORE_V0_EVALUATION_PROTOCOL.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md)

Paper-derived facts supplied for this task:

- `R-Bot(GPT-4)` uses `gpt-4o`
- `R-Bot(GPT-3.5)` uses `gpt-3.5-turbo-0125`
- default `temperature = 0.1`
- retrieval `top_k = 10`
- `RRF` parameter default `= 60`
- embedding candidate `= text-embedding-3-small`
- paper timing uses five executions and averages after excluding highest and lowest

## Extracted Paper Parameters

### Paper-faithful generation parameters

- `paper_faithful_config.model_variants.gpt4 = gpt-4o`
- `paper_faithful_config.model_variants.gpt35 = gpt-3.5-turbo-0125`
- `paper_faithful_config.temperature = 0.1`

Not recovered from the supplied paper facts in this task:

- `top_p`
- `max_tokens`
- `candidate_count`
- `feedback_rounds`
- provider/base_url details

These remain `not stated in supplied paper facts` rather than inferred.

### Paper-faithful retrieval parameters

- `paper_faithful_config.retrieval_top_k = 10`
- `paper_faithful_config.reranking_mode = rrf`
- `paper_faithful_config.rrf_k = 60`
- `paper_faithful_config.embedding_model_candidate = text-embedding-3-small`

Consistency check against repository-visible extraction:

- [formal_retrieval_config_extracted_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_extracted_v1.json) already extracted `embedding_model_identity.value = text-embedding-3-small`
- therefore the embedding candidate is `consistent_with_repo_extraction`

Still not recovered from repository extraction:

- explicit similarity threshold or explicit none
- retained formal index identifier
- retained rebuild-time embedding provider/base_url identity

### Paper timing note

Paper timing fact recorded for separation only:

- run count: `5`
- aggregate rule: `average after excluding highest and lowest`

This document does not change benchmark timing policy.

## Benchmark-Common Mapping

The benchmark-common config is not the same thing as the paper-faithful config.

The benchmark-common config for `common_core_v0_40_same_engine_120` should preserve:

- denominator: `common_core_v0_40_same_engine_120`
- route: `r_bot_same_engine_rewrite`
- same external LLM parameter policy as Direct LLM unless a documented method exception is approved

Direct LLM benchmark-side baseline visible in repository:

- model: `gpt-4o-mini`
- temperature: `0`
- top_p: `1`
- max_tokens: `2048`
- provider: `api.gptsapi.net`
- base_url: `https://api.gptsapi.net/v1`

Therefore benchmark-common should currently be interpreted as:

- external LLM generation policy aligned to Direct LLM
- retrieval `top_k` retained at the paper value `10` absent a documented benchmark-side exception
- retrieval reranking mode retained as `rrf`
- `rrf_k = 60`

This separation avoids conflating:

- paper-faithful method reproduction
- benchmark-common leaderboard comparability policy

## Closure Impact

Closed by paper-parameter extraction at the documentation freeze layer:

- paper-faithful model identities are now explicit
- paper-faithful temperature is now explicit
- retrieval `top_k` is now explicit
- reranking mode is now explicit as `rrf`
- `rrf_k` is now explicit
- embedding model candidate now has paper support and repo-extraction consistency
- paper timing recipe is recorded separately from benchmark timing policy

Not closed by this extraction:

- similarity threshold or explicit none
- retained rebuild-time embedding provider/base_url identity
- retained formal index identifier
- contamination closure
- corpus manifest closure
- generated-output coverage closure
- near-duplicate checker implementation
- retained artifact-contract closure

## Bottom Line

This package supports a two-layer interpretation:

- `paper_faithful_config` captures the paper-stated `R-Bot` settings
- `benchmark_common_config` captures the benchmark-facing settings for Common-core v0 same-engine comparison

That separation closes parameter-identity ambiguity, but it does not open formal `@120` generation.
