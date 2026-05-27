# R-Bot Substrate Freeze Gate v1

## Role

This gate defines what must be closed before `R-Bot` may produce current Common-core v0 same-engine benchmark evidence on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It does not authorize execution by itself.

## Current State

Current status remains:

- `benchmark_ready = false`
- `current_benchmark_gate_ready = false`
- `retrieval_stack_status = partial_tmp_only`
- `retrieval_corpus_status = partial_tmp_only`
- `prompt_demo_policy_status = not_frozen`
- `contamination_guard_status = not_available`

## Required Freeze / Attestation Conditions

All of the following must be true before current benchmark evidence is allowed.

### 1. Upstream LLM4Rewrite commit pinned

Required close condition:

- the upstream `LLM4Rewrite` code identity is pinned and recorded in retained artifacts

Current pinned identity already observed:

- remote: `https://github.com/curtis-sun/LLM4Rewrite`
- commit: `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375`

Remaining gate:

- the formal denominator-aware run must retain and attest that pinned identity in package artifacts

### 2. Retrieval corpus retained or deterministically rebuilt

Required close condition:

- retrieval archive and knowledge-base assets are either:
  - retained via approved artifact URIs and checksums, or
  - reproducibly rebuilt under a deterministic documented contract

Current observed anchors:

- `stackoverflow-rewrite-embed.zip`
  sha256=`e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `rule_cluster_summaries_structured.jsonl`
  sha256=`039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`

Current blocker:

- identities are known, but the corpus is still treated as temporary external substrate rather than frozen benchmark substrate

### 3. Chroma index retained or deterministically rebuilt

Required close condition:

- the `chroma_db` retrieval index is either:
  - retained via approved artifact URI/provenance, or
  - reproducibly rebuilt from the frozen corpus and dependency snapshot under a deterministic contract

Current observed anchor hashes:

- `chroma.sqlite3`
  `50d5c588aaae41b3f0d26b7f53b1546bde30632765efaa0a428d9118236392d5`
- `index_metadata.pickle`
  `aa39371d0b6c369442bebb8df4b4fca759d6b5abd1a58a2f84b29dd1d61a84d4`
- `header.bin`
  `56ac6fd6e2797ab645da45c1904068a760d15d62e298a4307443b2cad56cbffa`

Current blocker:

- the index remains temporary scratch substrate, not current-evidence substrate

### 4. Embedding / rule-vector dimensions frozen

Required close condition:

- embedding dimension, rule-vector dimension, and index dimension are frozen and mutually aligned
- deterministic alignment policy replaces exploratory patch behavior

Current observed state:

- expected dimension surfaced in recovery artifacts: `100`
- exploratory patch requested: `true`
- exploratory patch applied: `true`
- actual observed retained dimension: not fully surfaced

Current blocker:

- benchmark-facing deterministic vector-alignment policy is not yet closed

### 5. Demo selection policy frozen

Required close condition:

- one fixed retrieval corpus snapshot
- one fixed index snapshot
- one fixed runner/config snapshot
- exact retrieval settings surfaced and retained:
  - retrieval mode
  - `top_k`
  - threshold if any
  - reranking/fusion mode if any

Current blocker:

- the policy shape exists, but exact retrieval hyperparameters are not yet benchmark-frozen

### 6. Contamination guard attested

Required close condition:

- run artifacts must attest:
  - frozen denominator ID
  - target-case exclusion policy
  - denominator near-duplicate exclusion policy
  - prior benchmark-generated output exclusion
  - no post-hoc manual tuning

Current blocker:

- the guard is defined but not yet operationally attested in run artifacts

### 7. Generated SQL / selected rules / retrieval trace / prompt / raw response / token-cost / provider metadata artifact contract satisfied

Required close condition:

- every formal row that reaches generation retains:
  - generated SQL
  - selected rules trace
  - retrieval trace
  - prompt text or structured prompt payload
  - raw model response
  - token/cost/provider metadata
  - environment snapshot without secrets
  - denominator-aware package `run_results.json`

Current blocker:

- the contract is defined, but no denominator-aware formal run has yet satisfied it

## Final Gate Rule

Before current Common-core same-engine benchmark evidence is allowed:

1. all seven freeze/attestation conditions above must be closed
2. `current_benchmark_gate_ready` must become `true`
3. the formal run must preserve explicit blocked/failed/unsupported rows on the `120`-row denominator

## Bottom Line

The substrate is identifiable enough to plan a formal `120`-row route, but it is not yet frozen enough to support current benchmark evidence. The present package is protocol-ready, not benchmark-ready.
