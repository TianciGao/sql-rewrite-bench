# R-Bot Formal Substrate Freeze Plan

## Scope

This package prepares the formal reproducibility substrate for future `R-Bot` same-engine generation on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- planned rows = `120`

It does not authorize execution.
It does not make `R-Bot` benchmark-ready.

## Headline Decision

The formal gate remains closed.

The substrate is now organized into four decision classes:

1. retain as external artifact with checksum
2. deterministically rebuild from pinned inputs
3. repo-manifest only
4. unsupported / must block formal run

## Per-Item Freeze Decisions

### 1. Upstream `LLM4Rewrite` clone

- remote: `https://github.com/curtis-sun/LLM4Rewrite`
- pinned commit: `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375`
- current visible path: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- formal decision: `deterministically_rebuild_from_pinned_inputs`

Reason:

- the code root is already pinned by remote plus commit
- vendoring or copying the full clone into repo is not needed here
- the formal run should reconstruct the runtime from that exact commit and record the identity in retained artifacts

### 2. Knowledge-base / rule corpus

- current root:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- anchor file:
  `rule_cluster_summaries_structured.jsonl`
- anchor sha256:
  `039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`
- current observed `rule_cluster_funcs` file count: `30`
- formal decision: `deterministically_rebuild_from_pinned_inputs`

Reason:

- the corpus comes from the pinned upstream clone
- the formal package should retain a manifest of anchor hashes and counts
- full corpus copying into repo is unnecessary and out of scope

### 3. `stackoverflow-rewrite-embed.zip`

- current path:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- sha256:
  `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- formal decision: `retain_as_external_artifact_with_checksum`

Reason:

- this is a large binary artifact
- repo copy is explicitly disallowed here
- checksum-plus-external-retention URI is the correct formal shape

### 4. `chroma_db` index

- current path:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- current observed total retrieval dimension contract:
  `3172 = 1536 + 100 + 1536`
- current scratch anchor hashes:
  - `chroma.sqlite3`:
    `50d5c588aaae41b3f0d26b7f53b1546bde30632765efaa0a428d9118236392d5`
  - `index_metadata.pickle`:
    `aa39371d0b6c369442bebb8df4b4fca759d6b5abd1a58a2f84b29dd1d61a84d4`
  - `header.bin`:
    `56ac6fd6e2797ab645da45c1904068a760d15d62e298a4307443b2cad56cbffa`
- formal decision: `deterministically_rebuild_from_pinned_inputs`

Reason:

- the visible current index is scratch-lineage and not admissible as frozen benchmark substrate
- formal evidence should not rely on the exploratory PG1 rescue path
- deterministic rebuild is preferred over retaining the current scratch index snapshot

### 5. Rule-vector dimension policy

- exploratory canary patch target:
  `rule_vector_dim = 100`
- current exploratory runtime mismatch:
  `3139 = 1536 + 67 + 1536`
- formal total-dimension target:
  `3172 = 1536 + 100 + 1536`
- formal decision: `unsupported_must_block_formal_run_until_frozen`

Reason:

- the exploratory PG1 patch is not formal evidence
- the formal run must reject ad hoc padding/truncation patches
- the rule-vector width, total index dimension, and runtime extraction path must be frozen before generation may start

### 6. Smoke / formal venv

- current visible venv:
  `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- requirements checksum:
  `7c944dc6c40904d97e580890d907eea28bddc1615371659441d740a902d9a9c0`
- formal decision: `repo_manifest_only`

Reason:

- the venv itself should not be retained
- the reproducibility surface is requirements, package snapshot, Python executable identity, and build recipe

### 7. Provider / model config

- model name:
  `gpt-4o-mini`
- provider family:
  `openai_compatible`
- current alignment default:
  `provider=api.gptsapi.net`
  `base_url=https://api.gptsapi.net/v1`
- parameters:
  `temperature=0`
  `top_p=1`
  `max_tokens=2048`
  `candidate_count=1`
  `feedback_rounds=0`
- formal decision: `repo_manifest_only`

Reason:

- these are formal parameter/metadata declarations, not large substrate artifacts
- the run must log exact provider/model/base_url metadata without secrets

### 8. Demo selection policy

- exact `top_k`: unknown
- exact reranking/threshold mode: unknown
- exclusion policy required: yes
- formal decision: `unsupported_must_block_formal_run_until_frozen`

Reason:

- exact retrieval settings are not yet benchmark-frozen
- a formal denominator-aware run cannot start until the selection policy is explicit and attested

### 9. Contamination guard

- required exclusions:
  - all frozen `common_core_v0_40` cases from retrieval/demo pool
  - benchmark-generated outputs from SQLGlot
  - benchmark-generated outputs from Direct LLM
  - benchmark-generated outputs from Calcite
  - benchmark-generated outputs from `R-Bot` recovery canaries
- normalized SQL matching requirement: yes
- formal decision: `unsupported_must_block_formal_run_until_attested`

Reason:

- policy exists conceptually, but the formal attestation is not yet produced

### 10. Artifact contract

- generated SQL
- selected rules
- retrieval trace
- prompt
- raw response
- token/cost/provider metadata
- environment snapshot
- `run_results`
- formal decision: `repo_manifest_only_for_contract_definition`

Reason:

- the contract is a formal spec document now
- a future actual formal run must satisfy it before benchmark evidence exists

## Exact Missing Items Before `R-Bot @120` Generation May Start

1. a deterministic build recipe for the formal runtime from the pinned `LLM4Rewrite` commit
2. an external retention URI or deterministic rebuild contract for `stackoverflow-rewrite-embed.zip`
3. a manifest-complete inventory for the knowledge-base corpus, not just one anchor hash
4. a deterministic `chroma_db` rebuild plan under the formal `3172` total-dimension contract
5. a frozen rule-vector policy that explicitly sets runtime rule-vector width to `100` without exploratory patching
6. exact demo-selection settings:
   - retrieval mode
   - `top_k`
   - threshold if any
   - reranking/fusion mode if any
7. a formal contamination attestation package covering denominator-case exclusion and generated-output exclusion
8. a formal run-gate artifact that flips `current_benchmark_gate_ready` from `false` to `true` only after every prerequisite above is closed

## Formal Status

- formal substrate planning status: `prepared`
- formal substrate freeze status: `incomplete`
- formal run gate: `closed`
- benchmark-ready: `false`

## Bottom Line

The substrate now has a formal decision path for every major component, but several paths are still unresolved at the level required for a benchmark-facing `120`-row generation run. The gate must remain closed.
