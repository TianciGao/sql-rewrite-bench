# LLM-R2 120 Runner Recovery Scaffold v1

This is a dry-run scaffold only for LLM-R2 runner recovery on the
`common_core_v0_40_same_engine_120` rerun campaign.

- no generation is authorized
- no execution is authorized
- no timing is authorized
- this does not create `120`-row LLM-R2 evidence

## Recovery objective

The recovery objective is to:

- recover runner interface expectations
- recover logical-plan substrate checks
- recover output SQL extraction contract expectations
- define reproducibility contract expectations
- define generated SQL retention path expectations
- prepare a bounded PG overlap dry-run gate

MySQL and Spark support remain unrecovered unless later artifacts prove
otherwise.

## Recovery layers

### 1. Runner interface inventory

- required inputs:
  - `llm_r2_120_preflight_v1.md`
  - `llm_r2_120_dependency_matrix_v1.csv`
  - `llm_r2_120_run_plan_v1.json`
- expected files:
  - runner recovery inventory JSON
  - dry-run validator
- Codex-can-prepare:
  - document runner entrypoint assumptions
  - document required metadata and output paths
  - validate static file shape
- human-must-provide:
  - confirm whether the external runner substrate still exists
  - confirm acceptable runner interface boundary
- forbidden-until-approved:
  - no LLM-R2 execution
  - no SQL generation
- pass/fail criteria:
  - pass if runner-facing required inputs and inventory keys are explicit
  - fail if runner assumptions remain implicit or missing
- stop condition:
  - stop if no stable runner interface can be described from retained artifacts

### 2. Logical-plan substrate inventory

- required inputs:
  - `llm_r2_120_dependency_matrix_v1.csv`
  - retained logical-plan audit references named in the preflight
- expected files:
  - scaffold CSV row
  - inventory JSON logical-plan layer entry
- Codex-can-prepare:
  - isolate logical-plan substrate expectations
  - separate route-wrapper blockers from substrate blockers
- human-must-provide:
  - confirm whether substrate recovery is in scope
- forbidden-until-approved:
  - no logical-plan reruns
  - no generation
- pass/fail criteria:
  - pass if logical-plan blockers are explicit and reviewable
  - fail if they remain one-case opaque
- stop condition:
  - stop if retained artifacts do not support a reusable substrate boundary

### 3. Output SQL extraction contract

- required inputs:
  - `llm_r2_120_dependency_matrix_v1.csv`
  - `llm_r2_120_candidate_matrix_v1.csv`
  - retained extraction audit references named in the preflight
- expected files:
  - scaffold CSV row
  - inventory JSON extraction layer entry
- Codex-can-prepare:
  - define expected extraction states
  - define expected generated artifact names for later dry-runs
- human-must-provide:
  - confirm whether one-case cleanup evidence is enough to justify later bounded
    dry-run work
- forbidden-until-approved:
  - no extraction tests on new outputs
  - no inference
- pass/fail criteria:
  - pass if a reusable extraction contract can be stated
  - fail if extraction remains one-case-only
- stop condition:
  - stop if reusable extraction criteria cannot be written without guessing

### 4. Reproducibility contract

- required inputs:
  - `llm_r2_120_run_plan_v1.json`
  - `llm_r2_120_dependency_matrix_v1.csv`
- expected files:
  - scaffold CSV row
  - inventory JSON reproducibility layer entry
- Codex-can-prepare:
  - list reproducibility-sensitive inputs
  - define required retained metadata expectations
- human-must-provide:
  - confirm acceptable reproducibility boundary for later dry-runs
- forbidden-until-approved:
  - no retrieval or corpus rebuilding
- pass/fail criteria:
  - pass if reproducibility-sensitive inputs are explicit
  - fail if they remain unfrozen
- stop condition:
  - stop if runtime identity or retrieval inputs cannot be made explicit

### 5. Generated SQL retention path contract

- required inputs:
  - `llm_r2_120_run_plan_v1.json`
  - `common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`
- expected files:
  - scaffold CSV row
  - inventory JSON retention-path entry
- Codex-can-prepare:
  - define expected future generated-SQL path conventions
  - define required sidecar artifacts for later dry-runs
- human-must-provide:
  - approve retention-path convention before any generation package is built
- forbidden-until-approved:
  - no package that implies generation authorization
- pass/fail criteria:
  - pass if future generated-SQL retention shape is explicit
  - fail if later outputs would still be ambiguous
- stop condition:
  - stop if no stable retention layout can be specified

### 6. Bounded PG overlap dry-run validator

- required inputs:
  - rerun manifest CSV
  - LLM-R2 candidate matrix CSV
  - LLM-R2 run plan JSON
  - recovery inventory JSON
- expected files:
  - `llm_r2_120_runner_dry_run_validator_v1.py`
- Codex-can-prepare:
  - implement static validation only
  - validate file shape and required keys
- human-must-provide:
  - decide whether static validation is sufficient to review the next gate
- forbidden-until-approved:
  - no runner invocation
  - no PG overlap generation
- pass/fail criteria:
  - pass if static inputs are complete and coherent
  - fail if counts or required keys are inconsistent
- stop condition:
  - stop if static validator fails

### 7. Human approval gate before generation

- required inputs:
  - this scaffold
  - recovery plan
  - recovery checklist
  - static validator result
- expected files:
  - updated freeze-ledger state only after human review
- Codex-can-prepare:
  - summarize static readiness state
  - prepare human review packet
- human-must-provide:
  - explicit approval before any runner recovery scaffolding is treated as
    generation-ready
- forbidden-until-approved:
  - no generation
  - no execution
  - no timing
- pass/fail criteria:
  - pass only with explicit human approval
  - fail if approval is absent
- stop condition:
  - stop immediately if approval is not explicit
