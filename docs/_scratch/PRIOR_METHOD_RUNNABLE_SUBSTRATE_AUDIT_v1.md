# PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1

## 0. Purpose And Boundary

This is a read-only runnable-substrate audit for boss-requested prior methods that remain uncovered or readiness-only.

It is not implementation.
It is not execution.
It is not a closeout.
It is not a paper-writing note.
It is not a registry writeback.

The goal is to determine whether each baseline has a real repo-local runnable substrate and to identify the smallest safe next step without inventing missing infrastructure.

## 1. Summary Table

| baseline | intended role | current known status | repo-local code present | runnable entrypoint found | checkpoint/model artifact found | adapter to RewriteBench case package found | expected input format known | expected output format known | can run without external download | next classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `LearnedRewrite` | rewrite | `preflight_only`; readiness scaffold only | `partial` | `no` | `no` | `no` | `partial` | `partial` | `no` | `blocked_no_substrate` |
| `GenRewrite` | rewrite | `preflight_only`; input/cost scaffold only | `partial` | `no` | `no` | `no` | `partial` | `partial` | `no` | `blocked_no_substrate` |
| `R-Bot` | retrieval rewrite | `preflight_only`; retrieval-readiness scaffold only | `partial` | `no` | `no` | `no` | `partial` | `partial` | `no` | `blocked_no_substrate` |
| `LLM-R2` | retrieval rewrite | `preflight_only`; retrieval-readiness scaffold only | `partial` | `no` | `no` | `no` | `partial` | `partial` | `no` | `blocked_no_substrate` |
| `SlabCity` | service baseline | `blocked`; frontier-exception concept only | `no` | `no` | `not applicable` | `no` | `yes` | `partial` | `unknown` | `blocked_external_service` |
| `SQLSolver` | verifier-support | `not_integrated`; support-readiness scaffold only | `partial` | `no` | `not applicable` | `no` | `yes` | `yes` | `no` | `support_only` |

Interpretation:

- no target baseline qualifies as `runnable_now`
- no target baseline qualifies as `runnable_after_small_adapter`
- the strongest repo-local signal is readiness scaffolding, not runnable substrate
- staged `VeriEQL` code exists locally, but that does not make `SQLSolver` runnable and does not convert the SQLSolver line into a rewrite baseline

## 2. Per-baseline Findings

### LearnedRewrite

Files found:

- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `reports/baseline_smoke/learnedrewrite_input_readiness_v0.json`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `reports/baseline_smoke/learnedrewrite_input_readiness_v0.json`
  - `learnedrewrite_adapter_available=false`
  - `learnedrewrite_checkpoint_available=false`
  - `learnedrewrite_inference_entrypoint_available=false`
  - `dependency_file_available=false`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
  - current status is `preflight_only`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
  - exact blocker category: `artifact_stack_missing`

Missing pieces:

- baseline-specific runner
- model/checkpoint artifact
- inference entrypoint
- adapter from case package to baseline input representation
- declared dependency/runtime path

Blocker category:

- `blocked_no_substrate`

Minimum next action:

- draft a manual acquisition checklist for a repo-local LearnedRewrite substrate:
  - source repo or artifact location
  - required checkpoint/model files
  - dependency/runtime contract
  - input representation expected by the original method
  - output artifact shape needed to map back to a RewriteBench case package

Whether Codex should implement anything next:

- no

### GenRewrite

Files found:

- `docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json`
  - `genrewrite_runner_available=false`
  - `correction_loop_available=false`
  - `executor_feedback_loop_available=false`
  - `prompt_rule_library_available=false`
  - `pricing_snapshot_frozen=false`
- `docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md`
  - no correction loop, verifier loop, rerank path, or executor-feedback loop is present

Missing pieces:

- baseline-specific runner
- correction loop
- verifier/checker feedback loop
- rerank or n-best path
- retry policy
- correction-round budget
- prompt/rule library
- fair cost-control contract

Blocker category:

- `blocked_no_substrate`

Minimum next action:

- draft a manual acquisition checklist for the original GenRewrite control stack and the minimum reproducibility contract needed before any adapter work

Whether Codex should implement anything next:

- no

### R-Bot

Files found:

- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
  - no retrieval module
  - no demo selector
  - no rule pool
  - no rerank path
  - no retrieval reproducibility contract
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
  - `rbot_runner_available=false`
  - `retrieval_corpus_available=false`
  - `retrieval_module_available=false`
  - `rule_pool_available=false`
  - `demo_selector_available=false`

Missing pieces:

- retrieval corpus
- retrieval index
- demo selector
- rule pool
- rerank path
- contamination policy
- fair-comparison contract
- baseline-specific runner

Blocker category:

- `blocked_no_substrate`

Minimum next action:

- draft a manual acquisition checklist for the original R-Bot retrieval environment and artifact boundaries before any repo-local adapter discussion

Whether Codex should implement anything next:

- no

### LLM-R2

Files found:

- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
  - no demonstration pool
  - no rule applier
  - no demo policy
  - no contrastive or embedding path
  - no adapter
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
  - `llmr2_runner_available=false`
  - `demo_selector_available=false`
  - `embedding_vector_path_available=false`
  - `rule_pool_available=false`

Missing pieces:

- demonstration pool
- rule applier
- embedding or contrastive retrieval path
- demo policy
- fair-comparison contract
- baseline-specific runner

Blocker category:

- `blocked_no_substrate`

Minimum next action:

- draft a manual acquisition checklist for the original LLM-R2 demonstration-selection substrate and artifact contract

Whether Codex should implement anything next:

- no

### SlabCity

Files found:

- `docs/_scratch/SLABCITY_READINESS_AUDIT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `docs/_scratch/SLABCITY_READINESS_AUDIT_v0.md`
  - no SlabCity runner, adapter, CLI command, API wrapper, or service integration
  - only concrete repo signal is the inventory row
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
  - current status is `blocked`

Missing pieces:

- local runner
- adapter
- CLI or API wrapper
- synthesis engine
- verifier/solver integration
- reproducible service/runtime contract

Blocker category:

- `blocked_external_service`

Minimum next action:

- draft a manual acquisition checklist focused on whether SlabCity can be made reproducible locally at all, or whether it depends on an external service/runtime that cannot be audited within current repo boundaries

Whether Codex should implement anything next:

- no

### SQLSolver

Files found:

- `docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json`
- `docs/_scratch/baseline_inventory_boss_requirements.csv`

Evidence snippets / paths:

- `docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md`
  - no SQLSolver runner, wrapper, or solver dependency path
  - intended role is support-only, not main leaderboard
- `reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json`
  - `sqlsolver_runner_available=false`
  - `solver_dependency_available=false`
  - `schema_constraint_extraction_available=false`
  - `subset_policy_available=false`
  - `timeout_policy_available=false`

Missing pieces:

- repo-local SQLSolver checkout or packaged artifact
- wrapper
- solver dependency stack
- schema/constraint extraction path
- subset policy
- timeout policy

Blocker category:

- `support_only`

Minimum next action:

- draft a manual acquisition checklist for a repo-local SQLSolver support path, explicitly limited to bounded verifier-support use rather than rewrite-baseline use

Whether Codex should implement anything next:

- no

## 3. Candidate bounded smoke plan

No baseline currently qualifies as `runnable_now` or `runnable_after_small_adapter`.

Accordingly:

- proposed denominator: none yet
- preferred cases from the existing PG evidence packet: not applicable for immediate execution
- exact preflight needed before running: not applicable until a real repo-local runner/substrate exists
- expected artifacts: not applicable until a real runner contract exists
- claim boundary: no runnable bounded smoke should be claimed from the current repo state

Closest non-runnable future subsets if manual acquisition ever succeeds:

- rewrite-style first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
  - `PERF_0054`
- support-only first subset:
  - `CONS_0007` for `SQLSolver`

These are future candidate denominators only. They are not execution recommendations under the current substrate state.

## 4. Do-not-run list

Do not run these yet:

- `LearnedRewrite`
  - no adapter, no checkpoint, no inference entrypoint, no dependency/runtime path
- `GenRewrite`
  - no correction loop, no verifier/executor-feedback loop, no prompt/rule library, no cost-control freeze
- `R-Bot`
  - no retrieval corpus, no index, no demo selector, no rule pool, no rerank path
- `LLM-R2`
  - no demonstration pool, no rule applier, no embedding/contrastive path, no reproducibility contract
- `SlabCity`
  - no local runner and no reproducible service/runtime contract
- `SQLSolver`
  - no runner, no wrapper, no solver dependency path; intended role is support-only even if acquired later

## 5. Recommended next Codex task

Draft a manual acquisition checklist for the highest-priority baseline: `LearnedRewrite`.

Reason:

- among the remaining uncovered lines, `LearnedRewrite` is the clearest main prior-method baseline candidate rather than a retrieval-dependent appendix line, a frontier service exception, or a support-only verifier line
- the repo already has a readiness scaffold and candidate bounded subset, but it lacks the external substrate entirely
- the next bottleneck is manual acquisition and substrate verification, not code implementation

## 6. Non-modification note

- no baseline was executed
- no DB execution was performed
- no model calls were performed
- no SQLGlot execution was performed
- no packages were installed
- no external repositories were cloned
- no checkpoints or external artifacts were downloaded
- no files were modified outside this audit note
- no registry files were modified
- no review files were modified
- no rules, taxonomy, admission, or common-core files were modified
- `docs/EXECUTION_STATUS.md` was not modified
