# Formal Corpus/Index Audit

## Scope

This audit covers the retrieval corpus and `chroma_db` substrate currently known for formal `R-Bot` same-engine generation on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It is a substrate audit only.
It is not generation evidence, not execution evidence, and not benchmark readiness.

## Headline Answers

- known corpus files: `LLM4Rewrite` knowledge-base root, `rule_cluster_summaries_structured.jsonl`, `rule_cluster_funcs` directory, `rag/prompts.py`, `my_rewriter/prompts.py`, `my_rewriter/config.py`, and `stackoverflow-rewrite-embed.zip`
- known index artifacts: `chroma_db` directory, `chroma.sqlite3`, `index_metadata.pickle`, `header.bin`, and a build log/exit-code trace
- `/tmp`-only today: all known corpus and index substrate items are still identified from `/tmp` paths rather than retained benchmark package paths
- SHA-256 or anchor hashes exist for: `rule_cluster_summaries_structured.jsonl`, `stackoverflow-rewrite-embed.zip`, `rag/prompts.py`, `my_rewriter/prompts.py`, `my_rewriter/config.py`, `chroma.sqlite3`, `index_metadata.pickle`, and `header.bin`
- retained external URI/provenance is still missing for: `stackoverflow-rewrite-embed.zip`
- deterministic rebuild of the Chroma index is protocol-defined but not yet closed, because corpus manifest completeness and retained external archive provenance are still missing
- total dimension `3172 = 1536 + 100 + 1536` can be formalized and is already frozen as policy
- rule-vector width `100` is now formal deterministic policy, not exploratory evidence
- current formal `@120` generation gate cannot open

## 1. Known Corpus Files

Known included corpus-side artifacts:

- upstream clone root:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- knowledge-base root:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- anchor summary file:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_summaries_structured.jsonl`
- rule function directory:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`
- retrieval archive:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- prompt/config source files:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py`
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py`
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py`

Known excluded corpus-side families:

- `cases/**/source.sql` for the `common_core_v0_40` denominator
- generated SQL families from:
  - `sqlglot_same_engine_generation_01`
  - `direct_llm_same_engine_generation_01`
  - `calcite_same_engine_generation_01`
  - `r_bot_pg1_recovery_canary_01`

## 2. Known Index Artifacts

Known index-side artifacts:

- index root:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- index anchors:
  - `chroma.sqlite3`
  - `cbe4ef38-1d2b-4a34-87de-2028505d6c1c/index_metadata.pickle`
  - `cbe4ef38-1d2b-4a34-87de-2028505d6c1c/header.bin`
- build-side provenance:
  - `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log`
  - exit code `0` noted in substrate inventory

## 3. Hash Coverage

Artifacts with retained SHA-256 or anchor hashes:

- `rule_cluster_summaries_structured.jsonl`
  - `039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`
- `stackoverflow-rewrite-embed.zip`
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- `rag/prompts.py`
  - `5d512e0ce872f9818731ef36afa997f50d762af2b40cf54e3f2897f0ee83a8fd`
- `my_rewriter/prompts.py`
  - `8343c81948836589d4b21c76e82bdc7d2e448afb57ca416805a87b054a0e3999`
- `my_rewriter/config.py`
  - `0440f9dfe5b7ee00f276f9edb3b8b776da5ada21829db2eafc5b7d1aa0bf98d8`
- `chroma.sqlite3`
  - `50d5c588aaae41b3f0d26b7f53b1546bde30632765efaa0a428d9118236392d5`
- `index_metadata.pickle`
  - `aa39371d0b6c369442bebb8df4b4fca759d6b5abd1a58a2f84b29dd1d61a84d4`
- `header.bin`
  - `56ac6fd6e2797ab645da45c1904068a760d15d62e298a4307443b2cad56cbffa`

Artifacts still lacking file-level hash retention:

- upstream clone root itself
- knowledge-base root as a complete file inventory
- `rule_cluster_funcs` directory contents beyond file count `30`
- build log and exit-code files as checksum-retained audit items

## 4. /tmp-Only And Provenance Gaps

Still `/tmp`-only:

- upstream clone
- knowledge-base root
- summary file
- rule function directory
- retrieval archive
- prompt/config source files
- `chroma_db` root
- index anchor files
- build log

Still lacking retained external URI/provenance:

- `stackoverflow-rewrite-embed.zip`

Interpretation:

- checksum identity is partial but real
- retained benchmark provenance is still incomplete
- the first corpus blocker is not “nothing is known”; it is “known items are not yet fully retained and enumerated”

## 5. Deterministic Rebuild Answer

Can the Chroma index be deterministically rebuilt?

Answer: `not yet closed, but yes in principle under the current formal contract`

Reasoning:

- pinned upstream commit exists
- anchor corpus checksum exists
- retrieval archive checksum exists
- formal rebuild recipe exists
- formal dimension contract can be frozen

But the rebuild is still blocked because:

- the corpus manifest is not inventory-complete
- the external retained provenance handle for the retrieval archive is missing
- the formal rebuilt index package does not yet exist
- exact retrieval `top_k`, reranking mode, and threshold are still unset

## 6. Dimension Contract Answer

Can `3172 = 1536 + 100 + 1536` be formalized?

Answer: `yes`

Current status:

- total dimension `3172` is already frozen in the formal retrieval config
- rule-vector width `100` is already frozen as deterministic policy
- exploratory PG1 vector patch is explicitly rejected as formal evidence

This means:

- the policy is formalized
- the implementation artifact is not yet closed because no formal rebuilt index is retained

## 7. Gate Outcome

- formal gate open: `no`
- formal `@120` generation may start: `no`
- current benchmark metric evidence: `false`

## 8. Exact Remaining Blockers

1. complete the corpus manifest for all included knowledge-base assets
2. assign retained external provenance for `stackoverflow-rewrite-embed.zip`
3. retain a formal rebuilt `chroma_db` package or equivalent rebuild output identity under the frozen `3172` contract
4. retain index anchor hashes from that formal rebuilt index
5. freeze exact retrieval `top_k`
6. freeze exact reranking mode
7. freeze exact similarity threshold, or attest that no threshold is used
8. retain provider/model identity for the future formal run without exposing secrets
9. complete contamination attestation rows
10. validate that the future run path can satisfy the full artifact contract

## Bottom Line

The first corpus/index blocker is partly narrowed but not closed.

The corpus and index substrate are now auditable enough to define the formal contract, but they are still `/tmp`-rooted and provenance-incomplete, so `R-Bot @120` generation may not start.

