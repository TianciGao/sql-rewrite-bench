# R-Bot PG1 Recovery Policy Freeze Plan

This document defines the minimum policy freeze required before `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` is allowed to generate current-denominator evidence for the `PERF_0006 / pg` canary.

It is a recovery-governance artifact only.

## Current Policy State

Observed state from the canary package:

- prompt/demo policy: `not_frozen`
- contamination guard: `not_available`
- retrieval/index substrate: `partial_tmp_only`

So even if the technical runner executes, the result should not yet be treated as current Common-core evidence.

## Freeze Target

The canary should move from:

- scratch-backed recovery smoke

to:

- repo-documented, reproducible, bounded current-denominator canary evidence

That requires four freezes:

1. substrate freeze
2. retrieval/demo policy freeze
3. contamination guard freeze
4. artifact contract freeze

## 1. Substrate Freeze

Record and freeze:

- upstream repository identity
- upstream commit SHA
- local substrate root
- smoke venv path
- dependency file used
- knowledge-base snapshot
- retrieval archive snapshot
- exact Chroma index snapshot used by the canary

Minimum machine-readable manifest fields:

- `upstream_repo_url`
- `upstream_commit`
- `smoke_venv_path`
- `requirements_snapshot_path`
- `knowledge_base_files`
- `rag_archive_path`
- `rag_archive_hash`
- `index_path`
- `index_build_command`
- `index_build_log_path`
- `index_backend_mode`

Without this, the canary still depends on unnamed `/tmp` state.

## 2. Demo Selection Policy Freeze

Freeze the exact retrieval/demo contract used for the canary.

The policy must answer:

1. What corpus is eligible for retrieval?
2. What retriever/index mode is used?
3. How many candidates are retrieved?
4. How are ties broken?
5. Is there any random seed or nondeterministic ordering?
6. Are manual demo substitutions allowed?
7. Which artifacts must be captured to prove what the method actually saw?

Required fixed fields:

- `retrieval_corpus_id`
- `index_snapshot_id`
- `retrieval_mode`
- `top_k`
- `tie_break_rule`
- `seed_or_determinism_note`
- `manual_demo_override_allowed=false`
- `selected_rules_artifact_required=true`
- `retrieval_trace_artifact_required=true`

Recommended policy boundary:

- no per-case hand tuning after inspecting case outcomes
- one frozen policy for the canary, then reuse or explicitly version-bump it later

## 3. Contamination Guard Freeze

The contamination guard must explicitly prohibit leakage from the frozen denominator into retrieval evidence.

The guard should state:

1. No benchmark gold rewrites for frozen denominator rows may appear in the retrieval corpus.
2. No RewriteBench-generated SQL outputs may be re-indexed into the corpus before evaluation.
3. No demo set may be edited after observing a target-row outcome unless a new experiment version is declared.
4. Corpus provenance must be documented and auditable.

Minimum attestation fields:

- `frozen_denominator_id`
- `corpus_origin_description`
- `contains_frozen_target_rewrites=false`
- `contains_prior_rewritebench_outputs=false`
- `manual_demo_tuning_after_outcome=false`
- `attested_by`
- `attested_at`

## 4. Artifact Contract Freeze

If actual generation is later permitted, the canary must emit:

- generated SQL
- selected rules
- retrieval trace
- token/cost log
- method stdout/stderr
- structured run result status

Minimum output paths to freeze:

- `generated/PERF_0006/pg/r_bot_pg_rewrite.sql`
- `selected_rules.json`
- `retrieval_trace.json`
- `token_cost_log.json`
- `run_results.json`

## Allow/Block Rule For `RBOT_CANARY_ALLOW_ACTUAL_RUN=1`

`RBOT_CANARY_ALLOW_ACTUAL_RUN=1` may be used for current evidence only if all checks below are true.

### Must be true

1. `OPENAI_API_KEY` is visible in the launch shell.
2. The smoke venv dependency set is present and documented.
3. The upstream substrate root and commit are pinned.
4. The retrieval corpus snapshot is pinned.
5. The Chroma index snapshot is pinned.
6. The demo selection policy is frozen.
7. The contamination guard is frozen.
8. The artifact contract is frozen.
9. The run is explicitly labeled as current bounded canary evidence, not historical smoke.

### Must remain false

- manual demo override after looking at `PERF_0006`
- reliance on an untracked `/tmp` index with no provenance
- reliance on unstated prompt/policy mutations
- reuse of old `prior_method_pg10` numeric results as current metrics

## Decision For The Immediate Next Step

Immediate next step should still be:

- freeze substrate and policy first

Immediate next step should not be:

- actual PG1 model-backed generation

Current decision:

`RBOT_CANARY_ALLOW_ACTUAL_RUN=1` should remain blocked for current evidence until substrate and policy freeze are complete.
