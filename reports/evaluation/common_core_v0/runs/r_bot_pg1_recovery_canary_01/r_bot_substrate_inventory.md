# R-Bot PG1 Substrate Inventory

This inventory records the reproducibility substrate currently visible for the `R-Bot` `PERF_0006 / pg` recovery canary.

It is a substrate audit only.
It is not method execution, not API execution, not checker evidence, and not current benchmark evidence.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- current canary package:
  [r_bot_pg1_recovery_canary_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/README.md)

## Headline Status

The substrate is partly identifiable and auditable, but it is not yet frozen as current Common-core evidence.

What is now concretely visible:

- upstream `LLM4Rewrite` clone path
- upstream git remote
- upstream commit hash
- retrieval archive path and SHA-256
- knowledge-base summary file path and SHA-256
- built `chroma_db` path with a few anchor file hashes
- smoke venv path with a package snapshot

What is still not frozen:

- retrieval/demo policy
- contamination guard
- current-evidence retention decision for `/tmp` artifacts
- a frozen output artifact contract enforced by the actual canary package

## 1. Upstream Clone Identity

Visible clone root:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`

Observed git identity:

- remote: `https://github.com/curtis-sun/LLM4Rewrite`
- commit: `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375`

Observed state:

- `.git` directory present
- `git status --short` returned no visible dirty rows in the read-only probe

Interpretation:

- the upstream code root is identifiable
- but it is still a `/tmp` substrate, not a repo-pinned retained artifact inside the benchmark tree

## 2. Retrieval Corpus And Knowledge Base

Visible knowledge-base root:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`

Key observed files:

- rule summary file:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_summaries_structured.jsonl`
- rule function directory:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`

Observed counts:

- rule function file count: `30`

Observed hash:

- `rule_cluster_summaries_structured.jsonl`
  - sha256: `039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`

Interpretation:

- the knowledge-base substrate is physically present
- only part of it is currently checksummed
- it is still temporary unless a retention decision and manifest freeze are applied

## 3. Retrieval Archive

Visible archive path:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

Observed file size:

- `71,610,403` bytes

Observed hash:

- sha256:
  `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`

Interpretation:

- the archive is identifiable enough to be named in a freeze manifest
- but it remains `/tmp`-only until retained or explicitly declared temporary non-current substrate

## 4. RAG Index

Visible index path:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`

Observed size:

- `204M`

Observed anchor files:

- `chroma.sqlite3`
- `cbe4ef38-1d2b-4a34-87de-2028505d6c1c/index_metadata.pickle`
- `cbe4ef38-1d2b-4a34-87de-2028505d6c1c/header.bin`
- plus the associated binary index payload files

Observed hashes:

- `chroma.sqlite3`
  - sha256: `50d5c588aaae41b3f0d26b7f53b1546bde30632765efaa0a428d9118236392d5`
- `index_metadata.pickle`
  - sha256: `aa39371d0b6c369442bebb8df4b4fca759d6b5abd1a58a2f84b29dd1d61a84d4`
- `header.bin`
  - sha256: `56ac6fd6e2797ab645da45c1904068a760d15d62e298a4307443b2cad56cbffa`

### Build provenance

Visible build-side evidence:

- build log:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log`
- build exit code:
  `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_exit_code.txt`

Observed build status:

- build exit code: `0`

Observed build note:

- scratch notes describe this as the `openai_like` dependency-recovery build line
- the log shows build completion and no token/cost artifact

Important limitation:

- this index is now physically present and partly hashed
- but its provenance is still scratch-lineage, not yet frozen as current Common-core benchmark substrate

## 5. Smoke Venv

Visible smoke venv path:

- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`

Observed package snapshot:

- a full `pip freeze` snapshot is available by read-only probe
- a previous machine-readable import probe is also visible:
  `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke_probe.json`

Key observed packages in the venv:

- `chromadb==1.5.9`
- `jpype1==1.7.0`
- `jsonlines==4.0.0`
- `llama-index==0.14.21`
- `llama-index-core==0.14.21`
- `llama-index-embeddings-huggingface==0.7.0`
- `llama-index-embeddings-openai==0.6.0`
- `llama-index-llms-openai==0.7.7`
- `llama-index-llms-openai-like==0.7.2`
- `llama-index-vector-stores-chroma==0.5.5`
- `openai==2.34.0`
- `psycopg2-binary==2.9.12`
- `sqlglot==30.7.0`
- `prettytable==3.17.0`
- `scipy==1.17.1`

Associated temporary requirements file:

- `/tmp/rewritebench_rbot_llm4rewrite_requirements_smoke.txt`
- sha256:
  `7c944dc6c40904d97e580890d907eea28bddc1615371659441d740a902d9a9c0`

Interpretation:

- dependency substrate is stronger than “missing imports”
- the real issue is that the runnable dependency substrate is `/tmp`-scoped and not yet frozen as a declared current-evidence environment

## 6. Prompt / Demo Policy Source

Visible source files:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py`

Observed hashes:

- `rag/prompts.py`
  - sha256: `5d512e0ce872f9818731ef36afa997f50d762af2b40cf54e3f2897f0ee83a8fd`
- `my_rewriter/prompts.py`
  - sha256: `8343c81948836589d4b21c76e82bdc7d2e448afb57ca416805a87b054a0e3999`
- `my_rewriter/config.py`
  - sha256: `0440f9dfe5b7ee00f276f9edb3b8b776da5ada21829db2eafc5b7d1aa0bf98d8`

Current status:

- source files are identifiable
- policy is still `not_frozen`

Meaning:

- file identity exists
- experiment policy does not

That distinction matters. Checksummed prompt/config files do not by themselves freeze:

- retrieval top-k
- tie-break rules
- manual override policy
- allowed corpus scope

## 7. Contamination Guard

Current status from the canary package:

- `not_available`

Current gap:

- no frozen attestation that the retrieval corpus excludes frozen-denominator answer leakage
- no frozen attestation that prior RewriteBench-generated outputs are absent from the retrieval index
- no frozen rule against post-outcome demo tuning for the canary

So the substrate may be technically runnable, but still not admissible as current evidence.

## 8. Generated SQL And Trace Artifact Contract

Current declared contract from repo-local scaffolds:

- generated SQL path in the canary package:
  `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`
- temporary runner-side trace paths documented in scratch notes:
  - selected rules JSON
  - retrieval trace JSON
  - token/cost log JSON

Historical scratch evidence also shows a previous bounded smoke line produced:

- generated SQL
- selected rules
- retrieval trace
- token/cost log

But those remain historical bounded smoke evidence only, not current Common-core canary evidence.

## 9. What Counts As Frozen vs Temporary

### Identifiable but still temporary

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- `/tmp/rewritebench_rbot_llm4rewrite_requirements_smoke.txt`

### Not yet frozen for current evidence

- retrieval/demo policy
- contamination guard
- explicit retention decision for the `/tmp` index
- explicit retention decision for the smoke venv dependency snapshot
- explicit actual-run contract logging endpoint/model details without secrets

## 10. Inventory Decision

Current status should be described as:

`substrate_identified_but_not_frozen_for_current_evidence`

Reason:

- enough material now exists to draft a real freeze manifest
- but the policy gates still fail, and the retained benchmark-side freeze boundary is not complete

## Recommendation

Do not allow `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` to produce current benchmark evidence yet.

First complete:

1. upstream identity pin
2. retrieval corpus pin
3. index snapshot pin
4. demo policy freeze
5. contamination guard freeze
6. output artifact contract freeze
