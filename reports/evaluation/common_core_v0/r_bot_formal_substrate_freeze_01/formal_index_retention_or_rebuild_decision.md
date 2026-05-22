# Formal Index Retention Or Rebuild Decision

## Decision

`deterministically_rebuild_formal_chroma_index_do_not_retain_current_tmp_snapshot_as_current_evidence`

## Scope

This decision applies to the formal `R-Bot` retrieval index for:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Why The Current Index Is Not Retained As Formal Evidence

Current observed index:

- path:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- origin:
  scratch-lineage recovery build
- retained state:
  partially hashed, but still `/tmp`-only

Reasons not to retain it as current benchmark substrate:

1. it is `/tmp`-rooted rather than retained under a formal benchmark package path
2. it was built along the PG1 exploratory recovery line, not the formal `@120` denominator line
3. the corpus manifest was not inventory-complete when the current snapshot was identified
4. the retrieval archive still lacks retained external URI/provenance
5. exact retrieval `top_k`, reranking mode, and threshold are still unset

## Why Rebuild Is The Formal Path

Rebuild is the correct formal path because:

- upstream repo and commit are pinned
- corpus-side anchor hashes exist
- retrieval archive checksum exists
- formal total dimension policy is frozen at `3172 = 1536 + 100 + 1536`
- rule-vector width `100` is now formal deterministic policy
- the existing formal rebuild recipe already rejects exploratory patch evidence

## Formal Decision Boundary

Accepted:

- deterministic rebuild from pinned inputs
- retention of rebuilt index identifier and rebuilt anchor hashes
- retention of build metadata under the future formal run package

Rejected:

- promoting the current scratch `chroma_db` snapshot into current benchmark evidence
- treating the exploratory PG1 compatibility patch as formal dimension evidence
- silently dropping the retained provenance requirement for `stackoverflow-rewrite-embed.zip`

## What Must Exist Before Rebuild Is Closed

1. complete corpus manifest for all included knowledge-base assets
2. retained external provenance handle for `stackoverflow-rewrite-embed.zip`
3. exact frozen retrieval `top_k`
4. exact frozen reranking mode
5. exact frozen similarity threshold, or an explicit attestation that none is used
6. retained rebuilt index identifier
7. retained rebuilt index anchor hashes

## Gate Outcome

- retain current `/tmp` index as formal evidence: `no`
- deterministically rebuild formal index: `yes`
- formal `@120` generation may start now: `no`

## Bottom Line

The current scratch `chroma_db` is useful as a historical audit anchor, but not as retained formal substrate.

The formal route is deterministic rebuild under the pinned corpus, frozen `3172` dimension contract, and completed provenance freeze.

