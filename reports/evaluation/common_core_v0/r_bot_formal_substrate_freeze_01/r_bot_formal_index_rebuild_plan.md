# R-Bot Formal Index Rebuild Plan

## Role

This document defines the benchmark-facing rebuild path for the formal `R-Bot` retrieval index.

It intentionally rejects using the exploratory PG1 vector patch as formal metric evidence.

## Current Observed State

Current visible scratch index:

- path:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- scratch total-dimension contract:
  `3172 = 1536 + 100 + 1536`

Current failing exploratory runtime:

- `3139 = 1536 + 67 + 1536`

Interpretation:

- the stored scratch index appears aligned to a `100`-wide rule-vector slice
- the exploratory runtime drifted to `67`
- the exploratory PG1 patch padded/truncated to `100`, which is acceptable only as exploratory smoke rescue, not formal evidence

## Formal Decision

The formal route must rebuild the index deterministically.

It must **not** use:

- ad hoc runtime padding
- ad hoc runtime truncation
- a silent dimension patch during generation
- the current scratch `chroma_db` snapshot as direct formal evidence substrate

## Formal Dimension Policy

Freeze the formal retrieval-vector contract as:

- summary embedding width: `1536`
- rule-vector width: `100`
- SQL/template embedding width: `1536`
- formal total dimension: `3172`

Formal rule:

- runtime construction and index build must agree on all three widths
- any dimension mismatch blocks the run
- no benchmark-facing row may be repaired by exploratory patching

## Rebuild Inputs

The rebuild must be derived from pinned inputs only:

1. upstream `LLM4Rewrite` remote and pinned commit
2. knowledge-base corpus from that pinned checkout
3. retained `stackoverflow-rewrite-embed.zip` identified by checksum
4. frozen dependency snapshot
5. frozen model/provider policy for any embedding-side dependency if required by the build line
6. frozen demo/retrieval policy metadata

## Required Retained Build Metadata

The future rebuild must retain:

- upstream remote and commit
- corpus root identity
- archive checksum and external retention URI
- dependency snapshot / requirements checksum
- exact vector-width contract
- index build command or recipe
- index build log
- build exit status
- retained index identity or deterministic rebuild attestation

## Recommended Build Shape

1. materialize a fresh runtime from the pinned upstream checkout
2. verify the rule-vector width is explicitly `100` before index build starts
3. rebuild the retrieval corpus/index under that same fixed contract
4. record the resulting total dimension as `3172`
5. retain either:
   - external index snapshot URI plus checksums, or
   - a deterministic rebuild attestation that makes external snapshot retention unnecessary

## Rejections

Reject the following as formal benchmark substrate:

- “use the scratch index because it already works”
- “pad to 100 at runtime and call it formal”
- “change only `EMBED_DIM`”
- “treat the PG1 exploratory patch as proof of reproducibility”

## Gate Outcome

Until the rebuild recipe and retained metadata above exist, the formal gate remains closed.
