# LLM-R2 120 Recovery Plan v1

This is a recovery-planning document only for `LLM-R2` on the
`common_core_v0_40_same_engine_120` rerun campaign.

## Scope

This plan covers:

- runner recovery
- logical-plan substrate recovery
- output SQL extraction recovery
- reproducibility contract recovery
- bounded PG overlap dry-run planning
- the human approval gate required before any generation

## Non-scope

This plan does not:

- authorize SQL generation
- authorize PostgreSQL, MySQL, or Spark execution
- authorize timing or speedup work
- create `120`-row LLM-R2 evidence
- create a result card
- create a proposed row
- update `method_comparison_summary_v2`

MySQL and Spark support remain unrecovered unless later retained artifacts prove
otherwise.

## Current known blockers

From the retained Stage-1 preflight scaffold and dependency matrix:

- runner: missing
- logical-plan substrate: incomplete probe blocker retained
- output SQL extraction: partial one-case cleanup only
- input format contract: partially recovered only
- per-engine SQL dialect support: PG bounded only; MySQL/Spark not recovered
- generated SQL retention path: missing for a common-core `120` rerun
- checker handoff: bounded PG-only historical evidence
- reproducibility contract: missing

## Recovery phases

### 1. Runner recovery

Goal:
- recover a reusable non-executing route wrapper contract for LLM-R2

Required input artifacts:
- `llm_r2_120_preflight_v1.md`
- `llm_r2_120_dependency_matrix_v1.csv`
- `llm_r2_120_run_plan_v1.json`
- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`

Allowed Codex actions:
- inspect retained runner-related artifacts
- document expected file/layout/runtime assumptions
- draft wrapper-interface contracts
- draft output-path and metadata-path conventions

Forbidden actions:
- run LLM-R2
- invoke model inference
- generate SQL
- execute any database

Expected output artifacts:
- a runner recovery note or contract draft
- a retained-path map for expected runner inputs and outputs

Stop conditions:
- stop if no stable runner entrypoint can be identified from retained artifacts
- stop if required external repo/runtime assumptions remain unspecified

### 2. Logical-plan substrate recovery

Goal:
- determine what must be stabilized so logical-plan-stage failures can be
  reasoned about as a reusable route problem rather than a one-case probe

Required input artifacts:
- `docs/_scratch/LLMR2_LOGICAL_PLAN_FAILURE_AUDIT_PERF_0006_v1.md`
- `docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md`
- `docs/_scratch/LLMR2_EXTERNAL_REPO_SUBSTRATE_AUDIT_v1.md`

Allowed Codex actions:
- read retained logical-plan and substrate audits
- draft a logical-plan dependency contract
- isolate which substrate assumptions are PG-only and which are generic

Forbidden actions:
- rerun logical-plan probes
- run any generation step
- patch benchmark cases

Expected output artifacts:
- a logical-plan substrate contract draft
- a blocker map that separates missing substrate from route-wrapper issues

Stop conditions:
- stop if the retained artifacts do not specify a reusable substrate boundary
- stop if failure modes remain one-off and not contractible

### 3. Output SQL extraction recovery

Goal:
- convert one-case cleanup knowledge into a reusable extraction-contract plan

Required input artifacts:
- `docs/_scratch/LLMR2_OUTPUT_SQL_EXTRACTION_AUDIT_PERF_0006_v1.md`
- `docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md`
- `llm_r2_120_candidate_matrix_v1.csv`

Allowed Codex actions:
- inspect retained extraction audits
- document extraction-state categories
- draft a reusable extraction contract and artifact schema

Forbidden actions:
- generate model outputs
- test extractor behavior on new outputs
- assume MySQL/Spark extraction support

Expected output artifacts:
- an output-SQL extraction contract draft
- explicit stop/go criteria for later bounded dry-run review

Stop conditions:
- stop if extraction behavior cannot be generalized beyond one-case retained
  evidence
- stop if the required generated-output artifact schema is not recoverable

### 4. Reproducibility contract

Goal:
- freeze what must be controlled so later bounded dry-runs are repeatable and
  auditable

Required input artifacts:
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- `llm_r2_120_run_plan_v1.json`

Allowed Codex actions:
- enumerate reproducibility-sensitive inputs
- draft environment/runtime/seed/materialization contract notes
- document required artifact-retention paths

Forbidden actions:
- run retrieval
- rebuild indexes
- stage new external corpora

Expected output artifacts:
- reproducibility contract draft
- explicit list of human-provided prerequisites

Stop conditions:
- stop if demo-selection, retrieval inputs, or runtime identity cannot be made
  explicit from retained artifacts

### 5. Bounded PG overlap dry-run plan

Goal:
- define a later bounded PG-only dry-run shape without authorizing it

Required input artifacts:
- `prior_methods_pg10_bounded_appendix_v1.md`
- `llm_r2_120_preflight_v1.md`
- `llm_r2_120_candidate_matrix_v1.csv`
- `common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`

Allowed Codex actions:
- identify a planning-only PG overlap candidate set
- draft a dry-run-only package shape
- define required artifact outputs if a human later approves it

Forbidden actions:
- run PG overlap generation
- reclassify bounded PG10 evidence as `120` evidence
- claim MySQL/Spark readiness

Expected output artifacts:
- a bounded PG overlap dry-run plan draft
- a human-review gate for any future package creation

Stop conditions:
- stop if runner, logical-plan, extraction, and reproducibility contracts are
  still unresolved

### 6. Human approval gate before any generation

Goal:
- make explicit that no generation can proceed without a human decision after
  reviewing the recovery artifacts above

Required input artifacts:
- this plan
- the Stage-1 preflight scaffold
- any later recovery subplans produced under this plan

Allowed Codex actions:
- prepare review packets
- summarize unresolved blockers

Forbidden actions:
- authorize generation implicitly
- create executable run packages that suggest approval has already happened

Expected output artifacts:
- a human review checkpoint note
- an approval-or-stop decision request

Stop conditions:
- stop if human approval is not explicit

## Recovery boundary

- no generation is authorized by this plan
- no execution is authorized by this plan
- no timing is authorized by this plan
- no speedup is authorized by this plan
- no `120`-row LLM-R2 evidence is created by this plan
