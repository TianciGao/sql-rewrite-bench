# Formal Gate Status v4

## Scope

This document updates the formal gate status after the paper-parameter extraction and formal-parameter freeze update package.

It incorporates:

- [r_bot_paper_parameter_extraction_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_paper_parameter_extraction_v1.md)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [formal_retrieval_config_v3.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v3.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- paper parameters extracted: `yes`
- benchmark-common parameters proposed: `yes`
- blockers closed by paper parameters: `yes, at the documentation freeze layer`
- formal `R-Bot @120` generation may start: `no`
- `current_benchmark_gate_ready`: `false`

## Closed By Paper Parameters

Closed or materially clarified by this package:

1. paper-faithful model identities are now explicit:
   - `R-Bot(GPT-4) = gpt-4o`
   - `R-Bot(GPT-3.5) = gpt-3.5-turbo-0125`
2. paper-faithful temperature is now explicit:
   - `temperature = 0.1`
3. retrieval `top_k` is now frozen at `10` for:
   - `paper_faithful_config`
   - `benchmark_common_config`
4. reranking mode is now frozen as `rrf` for:
   - `paper_faithful_config`
   - `benchmark_common_config`
5. `rrf_k` is now frozen as `60` for:
   - `paper_faithful_config`
   - `benchmark_common_config`
6. embedding model candidate is now explicit as `text-embedding-3-small` and is consistent with repository extraction
7. benchmark-common versus paper-faithful configuration separation is now explicit
8. paper timing recipe is now recorded separately from benchmark-common timing policy

## What This Package Does Not Close

This package closes parameter ambiguity.
It does not close substrate, contamination, or artifact evidence gates.

Still open at the retrieval/config layer:

- exact similarity threshold or explicit none remains unresolved
- exact retained rebuild-time embedding provider/base_url identity remains unresolved
- exact retained formal index identifier remains unresolved

Still open outside the parameter layer:

- all `40` contamination rows are still blocked
- manifest-side contamination coverage is still incomplete
- generated-output contamination coverage is still incomplete
- machine-readable near-duplicate checking is still not implemented
- corpus manifest is still not inventory-complete
- retained external provenance for `stackoverflow-rewrite-embed.zip` is still missing
- formal rebuilt `chroma_db` package is still missing
- retained runtime/environment snapshot path is still missing
- retained artifact-contract closure is still missing

## Paper-Faithful Config

Paper-faithful config now means:

- model variants:
  - `gpt-4o`
  - `gpt-3.5-turbo-0125`
- `temperature = 0.1`
- `retrieval_top_k = 10`
- `reranking_mode = rrf`
- `rrf_k = 60`
- embedding model candidate:
  - `text-embedding-3-small`
- paper timing note:
  - five executions
  - average after excluding highest and lowest

Still not claimed as closed under paper-faithful config:

- similarity threshold or explicit none
- exact provider/base_url details
- formal retained substrate evidence

## Benchmark-Common Config

Benchmark-common config now means:

- denominator: `common_core_v0_40_same_engine_120`
- route: `r_bot_same_engine_rewrite`
- external LLM generation policy aligned to Direct LLM unless a documented exception is approved
- current aligned generation policy:
  - model `gpt-4o-mini`
  - `temperature = 0`
  - `top_p = 1`
  - `max_tokens = 2048`
  - `candidate_count = 1`
  - `feedback_rounds = 0`
- retrieval policy retained from paper unless justified otherwise:
  - `top_k = 10`
  - `reranking_mode = rrf`
  - `rrf_k = 60`

Benchmark-common timing policy remains:

- controlled by [COMMON_CORE_V0_EVALUATION_PROTOCOL.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md)
- not silently changed to the paper timing recipe by this package

## Exact Remaining Blockers

1. exact similarity threshold or explicit none is still not frozen
2. exact retained rebuild-time embedding provider/base_url identity is still not fully attested
3. formal rebuilt `chroma_db` index package and retained formal index identifier do not yet exist
4. corpus manifest is still not complete enough for deterministic retained rebuild
5. retained external provenance handle for `stackoverflow-rewrite-embed.zip` is still missing
6. dependency lock is still candidate-only rather than a complete retained final lock
7. retained runtime package snapshot and environment metadata path do not yet exist
8. contamination attestation is still blocked because all `40` rows remain blocked
9. exact generated-output contamination hits remain present on `11` rows and must be resolved or formally excluded in the retained corpus/output line
10. manifest-side contamination coverage is incomplete because current included manifest entries are not all text-readable hashable items
11. generated-output contamination coverage is incomplete because the visible `calcite` generated family is missing
12. machine-readable near-duplicate exclusion checking is not implemented
13. the future retained run package has not yet been validated as satisfying the full artifact contract

## Gate Outcome

The formal gate remains closed.

Closed by this package:

- parameter ambiguity around model families, temperature, `top_k`, `rrf`, and `rrf_k`

Not closed by this package:

- contamination
- corpus provenance
- rebuilt formal index
- retained artifact contract
- remaining retrieval identity/details

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The paper-parameter package successfully separates:

- `paper_faithful_config`
- `benchmark_common_config`

That is a useful governance closure, but it is not a run gate closure.

Expected answer remains:

- formal `R-Bot @120` generation may start: `no`
