# R-Bot PG1 Substrate Retention Decision

This document turns the discovered `R-Bot` / `LLM4Rewrite` substrate inventory into a retention decision for the `PERF_0006 / pg` recovery canary.

It is a reproducibility-governance artifact only.
It does not authorize execution.
It does not create current benchmark evidence.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- `denominator_id = common_core_v0_40_pg40`
- `canary_denominator_id = common_core_v0_40_perf_pg1_r_bot_recovery_canary`

## Headline Decision

The substrate is now identifiable enough to freeze by manifest and policy, but not enough to authorize current-evidence actual generation.

Retention strategy:

- retain identities, hashes, manifests, and policy files in-repo
- do not copy large `/tmp` binaries into the repo in this step
- treat `/tmp` clone, archive, index, and venv as temporary external substrate until a later human decides whether to:
  - retain them in an external artifact store
  - rebuild them deterministically
  - or promote them into a separately managed retained substrate location

## Retention Decisions By Item

### 1. Upstream `LLM4Rewrite` clone

Observed identity:

- remote: `https://github.com/curtis-sun/LLM4Rewrite`
- commit: `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375`
- current local path:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`

Decision:

- do **not** vendor into this repo now
- do **not** add as a submodule now
- do retain remote URL, commit SHA, and path in a freeze manifest
- treat the actual clone as external substrate

Reason:

- current task forbids copying large `/tmp` artifacts
- current repository phase does not justify silently promoting an external prior-method codebase into the benchmark repo
- checksum-plus-identity retention is enough for the PG1 recovery gate at this stage

### 2. `stackoverflow-rewrite-embed.zip`

Observed identity:

- path:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- sha256:
  `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`

Decision:

- do **not** copy into the repo in this step
- retain the path and SHA-256 in the freeze manifest
- recommended long-term retention target: external artifact store or separately managed retained substrate directory

Reason:

- it is a large binary artifact
- current instruction explicitly forbids copying large `/tmp` artifacts into the repo
- checksum-only is acceptable for the current freeze package, but not sufficient alone for current-evidence generation

### 3. Knowledge-base root

Observed root:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`

Observed anchor:

- `rule_cluster_summaries_structured.jsonl`
  - sha256:
    `039823a6b5e87476dfc7a7be1cc9ac1bbeed31ec8972ceaa72364c1a56a03b5d`

Decision:

- retain root path, anchor hash, and file-count metadata in manifest
- adopt a manifest strategy rather than copying the whole knowledge-base now
- future retention should include a machine-readable inventory of:
  - anchor JSONL
  - rule-cluster function file count
  - optionally per-file hashes if current evidence is later pursued

Reason:

- enough to identify the corpus line now
- not enough yet to call the corpus fully pinned for current benchmark evidence

### 4. `chroma_db` index

Observed path:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`

Observed anchor hashes:

- `chroma.sqlite3`
  - `50d5c588aaae41b3f0d26b7f53b1546bde30632765efaa0a428d9118236392d5`
- `index_metadata.pickle`
  - `aa39371d0b6c369442bebb8df4b4fca759d6b5abd1a58a2f84b29dd1d61a84d4`
- `header.bin`
  - `56ac6fd6e2797ab645da45c1904068a760d15d62e298a4307443b2cad56cbffa`

Decision:

- do **not** retain the full binary index in-repo
- retain the anchor hashes and build provenance in manifest
- current preferred long-term strategy: either
  - retain a binary snapshot outside the repo with explicit URI/provenance, or
  - rebuild deterministically from retained corpus and documented dependency snapshot

Current policy choice:

- treat the current index as `temporary_scratch_index_not_current_evidence`
- do not authorize it as frozen current benchmark substrate yet

Reason:

- it is a large scratch artifact
- provenance is only partially frozen
- the demo policy and contamination guard are still unresolved

### 5. Smoke venv

Observed path:

- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`

Decision:

- do **not** retain the venv itself
- retain:
  - smoke requirements file checksum
  - package snapshot
  - key package versions in manifest

Reason:

- virtual environments are implementation artifacts, not benchmark artifacts
- requirements and package snapshot are the reproducibility surface that matters

### 6. Prompt/config files

Observed files:

- `rag/prompts.py`
- `my_rewriter/prompts.py`
- `my_rewriter/config.py`

Decision:

- retain checksums in manifest
- do not treat checksummed files alone as a frozen demo policy
- require separate policy files in this package to define the experiment contract

Reason:

- file identity and policy identity are different things

## Retention Mode Summary

### Retain now in repo

- remote URL / commit SHA
- archive SHA-256
- knowledge-base anchor SHA-256
- index anchor hashes
- smoke requirements checksum
- package snapshot summary
- prompt/config checksums
- policy documents

### Do not retain now in repo

- full upstream clone
- zip archive binary
- full `chroma_db` binary
- full smoke venv

### Required later for current evidence

- either external retained snapshot URIs or deterministic rebuild contract for:
  - retrieval archive
  - knowledge-base
  - `chroma_db`

## Decision Boundary

This freeze package is enough to move from:

- `unknown_tmp_substrate`

to:

- `identified_tmp_substrate_with_retention_policy`

It is not enough to move to:

- `current_evidence_generation_allowed`

## Recommended Next Step

After this package, the next useful step is not execution.

The next useful step is:

1. approve the demo policy
2. approve the contamination guard
3. approve the artifact contract
4. decide whether the current `/tmp` index is acceptable only for exploratory smoke or must be rebuilt/preserved before any actual run
