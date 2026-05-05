# SLABCITY_MANUAL_ACQUISITION_CHECKLIST_v1

## 0. Status

This document is documentation-only. It is not implementation, not execution, not a runnable-substrate claim, not registry writeback, and not a closeout artifact.

Current repo-local state remains blocked. No local SlabCity runner exists, and no reproducible service/runtime contract exists.

## 1. External-Service Boundary

SlabCity cannot count as prior-method coverage unless one of the following is acquired:

1. a repo-local runnable implementation
2. a reproducible, auditable service/runtime contract

A paper description alone is not enough. A private or inaccessible hosted service is not enough. An ad hoc manual rewrite inspired by SlabCity is not SlabCity coverage.

If SlabCity requires a remote service, the service interface, version, inputs, outputs, quotas, determinism, logging, and reproducibility policy must all be documented before any bounded smoke is considered valid.

## 2. External Artifacts Needed

Manual acquisition must recover:

- exact SlabCity source repo or artifact package, if any
- exact commit hash, release, or archived version
- local runner or executable entrypoint, if available
- service endpoint contract, if service-based
- API or client version, if service-based
- authentication or access model, without storing secrets
- dependency/runtime contract
- model or backend version, if applicable
- prompt, rule, or config bundle, if applicable
- supported SQL dialect/subset
- expected input schema
- expected output format
- license and redistribution constraints
- runtime, quota, determinism, and availability assumptions
- logging and auditability requirements

Current repo-local evidence does not provide any of these as a runnable local or service-backed contract.

## 3. Input Contract To Recover

Manual acquisition must recover the exact input contract, including:

- whether SlabCity accepts raw SQL text
- whether it requires schema DDL
- whether it requires query plans
- whether it requires execution feedback, cost feedback, examples, or workload context
- whether it is PostgreSQL-specific or dialect-agnostic
- whether it requires external catalog or statistics state
- whether it requires private prompts, private rules, or service-side hidden context
- whether it can process RewriteBench case packages without manual rewrite

Current repo-local evidence only suggests a high-level contract of `SQL + schema/constraints + synthesizer config`, which is not enough to claim a runnable substrate.

## 4. Output Contract To Recover

Manual acquisition must recover the exact output contract, including:

- whether it outputs rewritten SQL directly
- whether it outputs ranked candidates
- whether it outputs a rule sequence, plan, or internal representation
- whether it outputs logs, traces, confidence, or cost metadata
- whether it emits machine-readable results
- whether failures can be classified
- whether output SQL can be passed into the existing PostgreSQL checker and speedup pipeline

Required future output categories:

- `generated_sql`
- `candidate_rank`
- `method_trace`
- `runtime_metadata`
- `failure_category`
- `service_version_or_runner_version`
- `reproducibility_metadata`

## 5. Reproducible Service Contract Requirements

If SlabCity is service-based, require all of the following before any bounded smoke:

- stable endpoint or local service container
- versioned API contract
- fixed model/backend version
- deterministic or logged sampling parameters
- request/response logging policy
- quota and rate-limit documentation
- authentication handled outside the repo
- no secrets committed
- replayability or cached response policy
- permission to report results
- permission to store sanitized request/response artifacts
- failure behavior documented
- timeout policy documented

If these cannot be satisfied, classify SlabCity as `blocked_external_service`.

## 6. RewriteBench Adapter Boundary

No wrapper or adapter should be created now.

Any future adapter must define:

- case package to SlabCity input
- SlabCity output to candidate SQL
- candidate SQL to existing PostgreSQL checker/speedup pipeline
- service/client logs to reproducibility artifacts
- failure outputs to failure taxonomy
- strict separation between SlabCity method behavior and RewriteBench checker behavior

Artifact paths needed later:

- `source_snapshot_ref` or `service_contract_ref`
- `runtime_contract_note`
- `input_contract_note`
- `generated_sql`
- `method_trace`
- `service_request_response_log`
- `runtime_metadata`
- `failure_log`
- `support_summary_json` or `baseline_summary_json`

## 7. Minimum Bounded Smoke After Acquisition

Only after acquisition succeeds:

- denominator: `1-3` cases only
- PostgreSQL-only first
- suggested first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- no registry writeback
- no admission/common-core claim
- no final leaderboard claim
- no full prior-method coverage claim

Required first-smoke metrics:

- `generation_success_count`
- `execution_success_count`
- `checker_consistency_count`
- `failure_count_by_category`
- if speedup is run later: `GM_Speedup` / `W/T/L` only on checker-consistent outputs

Claim boundary for any future smoke:

`bounded_SlabCity_substrate_smoke_only_not_full_prior_method_coverage`

## 8. Stop Conditions

Stop and classify acquisition as blocked if any of the following remains unresolved:

- no source repo or artifact package
- no local runner
- no service contract
- no stable endpoint or local container
- no input contract
- no output SQL
- no machine-readable output
- no reproducibility/logging policy
- no license or permission clarity
- requires inaccessible private service
- requires private prompts, rules, or backend state that cannot be audited
- cannot separate SlabCity behavior from manual human rewrite
- cannot pass output into the RewriteBench checker

## 9. Final Decision Tree

- `acquired_and_runnable_local`
  A pinned local runner exists with a reproducible dependency/runtime contract and auditable input/output behavior.

- `acquired_service_contract_reproducible`
  No local runner exists, but a stable, auditable, replayable service/runtime contract exists and is strong enough for bounded reproducible evidence.

- `acquired_but_adapter_needed`
  Upstream runtime or service artifacts are available, but RewriteBench still lacks the minimal adapter needed to produce bounded checker-backed outputs.

- `acquired_but_not_reproducible`
  Some runtime path exists, but logging, determinism, permissions, or artifact capture remain too weak for reproducible evidence.

- `blocked_external_service`
  The baseline depends on a remote or hidden service/runtime contract that cannot currently be audited or reproduced.

- `unavailable_blocked`
  The source, service, runtime, or output contract is too incomplete to proceed safely at all.

## 10. Current Provisional Decision

Based only on current repo-local evidence, SlabCity should currently be classified as:

- `blocked_external_service`
- `unavailable_blocked` for runnable prior-method evidence until a local runner or reproducible service/runtime contract is acquired

## 11. Recommended Next Step

The next step should be to produce a final prior-method acquisition status rollup across `LearnedRewrite`, `GenRewrite`, `R-Bot`, `LLM-R2`, `SQLSolver`, and `SlabCity`.

The repo-local evidence is already sufficient to show that all remaining boss-requested lines are either blocked, support-only, or readiness-only. A rollup is therefore a better next consolidation step than attempting further acquisition planning depth for another still-missing substrate.

## 12. Non-Modification Note

No execution occurred. No download occurred. No model call occurred. No DB run occurred. No SQLGlot run occurred. No service call occurred. No wrapper was created. No adapter was created. No script was modified. No registry, review, rules, or `docs/EXECUTION_STATUS.md` file was modified.
