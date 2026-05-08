# R-Bot Formal Run Gate v1

## Decision

`formal_r_bot_common_core_v0_40_same_engine_generation_not_allowed_yet`

## Scope

This is the benchmark-facing run gate for future `R-Bot` same-engine generation on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Current Gate Status

- formal gate: `closed`
- benchmark-ready: `false`
- `current_benchmark_gate_ready = false`

## Conditions That Must All Be Closed Before Generation May Start

1. pinned `LLM4Rewrite` runtime rebuild recipe exists
2. knowledge-base corpus manifest is complete enough for deterministic rebuild
3. retained external artifact URI/provenance exists for `stackoverflow-rewrite-embed.zip`
4. formal `chroma_db` rebuild recipe exists
5. formal total-dimension policy is frozen at `3172 = 1536 + 100 + 1536`
6. exploratory PG1 vector patch is rejected as formal evidence path
7. exact demo-selection settings are frozen:
   - retrieval mode
   - `top_k`
   - threshold if any
   - reranking/fusion mode if any
8. formal contamination attestation artifact exists
9. formal artifact contract path is satisfiable by the future run package

## Exact Missing Items Right Now

- no formal runtime rebuild recipe from pinned upstream commit
- no external retained artifact URI for `stackoverflow-rewrite-embed.zip`
- no complete knowledge-base manifest freeze
- no formal index rebuild recipe under the frozen dimension contract
- no fully frozen rule-vector alignment policy beyond the exploratory patch notes
- no exact frozen `top_k`
- no exact frozen threshold/reranking mode
- no formal contamination attestation artifact

## Explicit Rejection

The following do **not** open the gate:

- PG1 exploratory generation success
- PG1 exploratory exact-match execution success
- the exploratory `rule_vector_dim = 100` compatibility patch
- the existence of the current scratch `chroma_db`
- any historical `prior_method_pg10` evidence

## Gate Outcome

Until every missing item above is closed:

- formal `R-Bot @120` generation may not start
- no row may be promoted into current benchmark metric evidence
- the route remains protocol-defined but substrate-blocked

## Bottom Line

The formal gate remains closed because every substrate item now has a decision path, but not every item yet has a closed retention/rebuild/attestation path.
