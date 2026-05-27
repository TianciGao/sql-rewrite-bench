# R-Bot PG1 Retrieval Dimension Patch Plan

## Goal

Define a conservative next-step plan for the `3172` vs `3139` retrieval embedding mismatch without changing current benchmark evidence status.

Non-negotiable status:

- `current_benchmark_metric_evidence=false` remains unchanged
- no patched run is leaderboard evidence
- no patched run is denominator evidence

## Root Cause Target

Patch target must be explicit:

- persisted index contract: `3172 = 1536 + 100 + 1536`
- failing runtime contract: `3139 = 1536 + 67 + 1536`
- drift location: rule-vector slice width

Patch target must not be framed as:

- “change EMBED_DIM to 3172”

Correct framing:

- either align the runtime rule-vector slice to the retained index contract
- or rebuild the index from a runtime that uses the intended rule-vector contract

## Conservative Recommendation

Recommended default path:

1. Treat the current `/tmp` substrate as non-reproducible for evidence-bearing use.
2. Require an explicit choice between:
   - exploratory compatibility patch against the existing `3172` index
   - deterministic rebuild under a single frozen retrieval-vector contract
3. Rerun only after that choice is documented.

## Patch Options

### Path A: Exploratory Smoke Only Patch

Use only if the goal is to see whether the already-visible index can be queried by the current smoke harness.

Mechanism already present:

- [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:38400)
- smoke runner flag: `--align-rule-vector-dim 100`

What it does:

- copies runtime into `runtime_patch_v3`
- pads or truncates `rules_one_hot` to width `100`
- leaves `EMBED_DIM` at `1536`

Label requirement:

- `exploratory_smoke_only_not_current_metric`

Allowed interpretation:

- compatibility probe against an already-built `/tmp` index

Disallowed interpretation:

- benchmark evidence
- leaderboard evidence
- denominator evidence
- proof that the substrate is frozen or reproducible

### Path B: Deterministic Rebuild

Use if the goal is future reproducibility rather than a one-off smoke rescue.

Required target:

- choose one retrieval-vector contract
- rebuild the Chroma index and runtime under that same contract
- freeze or retain the resulting substrate

Minimum required invariants:

- one declared rule-vector width
- one declared summary embedding source
- one declared SQL-template embedding source
- one declared index build recipe
- one retained or reproducibly rebuildable `chroma_db`

Current best governance interpretation:

- this is the only acceptable path for any future evidence-bearing run

## Exact Candidate Files For Follow-Up

Schema and runtime candidates:

- [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:38151)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py:7)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py:103)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py:96)

Substrate/metadata candidates:

- [/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db/chroma.sqlite3](/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db/chroma.sqlite3)
- [/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log](/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log:1)
- [r_bot_substrate_freeze_manifest_draft.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_substrate_freeze_manifest_draft.json:1)
- [r_bot_actual_run_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_actual_run_gate_v1.md:1)

## Proposed Decision Matrix

If the intent is exploratory smoke continuity:

- choose Path A
- target `rule_vector_dim = 100`
- keep label `exploratory_smoke_only_not_current_metric`

If the intent is future reproducibility/current-evidence preparation:

- choose Path B
- reject the current `/tmp` index/runtime pair as sufficient evidence substrate
- require deterministic rebuild or retained frozen substrate before rerun

## Explicit Rejections

Reject these changes:

- silently changing `EMBED_DIM`
- treating `3172` as the new `EMBED_DIM`
- using historical `generated_sql_v3.sql` as current failed-run output
- treating any patched smoke rerun as leaderboard evidence
- inferring current benchmark metric evidence from the patched exploratory run

## Rerun Guidance

Rerun recommendation:

- yes, but only after the patch target is explicit

Explicit allowed rerun statements:

- “rerun exploratory smoke with rule-vector alignment to 100”
- “rerun only after deterministic rebuild under a frozen retrieval-vector contract”

Explicit disallowed rerun statement:

- “rerun after changing EMBED_DIM to 3172”

## Outcome Statement To Preserve

Until a separate explicit rerun happens under an explicit patch target:

- failure remains a retrieval-dimension mismatch
- `current_benchmark_metric_evidence=false`
- no leaderboard use
- no denominator use
