# PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0

## 1. Status

This is a tracked scratch denominator freeze proposal for formal experiments after the completed baseline route readiness sweep.

This document is:

- a denominator freeze proposal for formal experiments
- a scratch planning packet
- a bounded next-step proposal after readiness closure

This document is not:

- admission
- registry writeback
- final leaderboard definition
- formal review update
- benchmark protocol freeze

## 2. Current Readiness Closeout Reference

Primary current readiness closeout reference:

- `docs/_scratch/BASELINE_ROUTE_READINESS_CLOSEOUT_v0.md`

Supporting route and smoke references:

- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md`
- `docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md`
- `docs/_scratch/PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md`
- `docs/_scratch/baseline_smoke_common_core_v0.json`

Interpretation:

- the readiness sweep has established a bounded runnable smoke denominator
- it has not yet established a formal experiment denominator
- this proposal defines the next candidate denominator plan for a later formal run

## 3. Proposed Common-Core Denominator

Proposed initial common-core denominator for the first formal experiment packet:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

Rationale:

- this is the exact PG-native 9-case denominator already exercised across the completed smoke sweep
- all cases are registry-tracked, staged, formal-skeleton-complete, and tri-engine-closure `yes`
- Steps 1, 2a, and 4a have already demonstrated full PG execution-layer smoke on this set
- the set spans:
  - TPC-H performance cases
  - TPC-DS performance cases
  - compact Calcite-derived semantic consistency cases

Planning posture:

- treat this as the first formal experiment denominator candidate
- do not treat it as admitted common-core
- do not treat it as final leaderboard scope

## 4. Proposed PORT Denominator

Proposed initial PORT denominator for a bounded formal translation experiment packet:

- clean subset:
  - `PORT_0004`
  - `PORT_0022`
- held-out failure-analysis path:
  - `PORT_0012`

Rationale:

- `PORT_0004` and `PORT_0022` already passed clean Step 4b LLM translate execution-layer smoke
- Step 2b SQLGlot transpile already captured a concrete failure on `PORT_0012`
- `PORT_0012` should remain a formal holdout until failure-analysis is frozen

Planning posture:

- for a clean first formal PORT denominator, use `PORT_0004` and `PORT_0022`
- keep `PORT_0012` outside the clean denominator until the failure-analysis packet is complete
- do not represent the clean 2-case subset as full PORT closure

## 5. Proposed Extended Diagnostic Set

Proposed extended diagnostic layer for later formal or appendix-oriented analysis:

- `PERF_0038`
  - keep as pending / not clean
  - useful for denominator boundary discussion, not for first freeze
- `PERF_0076`
  - retain as extended-oriented characterization material
- semantic extension candidates from the existing CONS addendum:
  - `CONS_0024`
  - `CONS_0031`
  - `CONS_0034`
- support-analysis-only lines:
  - `CONS_0007`
  - `CONS_0012`
  - under SQLSolver / VeriEQL support framing only, not as runnable verifier execution

Purpose of this extended diagnostic layer:

- plan-observability characterization
- semantic-stress discussion
- appendix or reviewer-facing diagnostic analysis
- future denominator expansion after additional policy review

This is not the first formal run denominator.

## 6. Staged / Excluded Set

Staged but excluded from the first formal denominator freeze:

- `PORT_0012`
  - active failure-analysis holdout
- `PERF_0038`
  - pending / not clean
- `PERF_0076`
  - extended-oriented, not clean first-denominator material
- broader PERF+PORT preliminary candidates outside the current smoke denominator
  - keep staged for later review, not for first freeze
- broader CONS addendum cases outside the compact 2-case semantic layer
  - keep as addendum / extension only
- LONGTAIL
  - exclude from the first formal denominator freeze

Route-level staged or excluded baseline lines:

- Step 3 Calcite HEP
- Step 5 LearnedRewrite
- Step 6 GenRewrite
- Step 7 R-Bot / LLM-R2
- Step 8 SlabCity
- Step 9 SQLSolver / VeriEQL support

Reason:

- these routes are readiness-only, support-only, or deferred
- they should not be used as first formal denominator-defining baselines

## 7. Eligibility Criteria

A case should satisfy all of the following before entering the first formal experiment denominator proposal:

- present in `inventory/case_registry.csv`
- `benchmark_line=staged` or stronger governed status
- `formal_skeleton_status=complete`
- `release_grade_status=incomplete` is acceptable only for this proposal stage, but missing formal skeleton is not
- `tri_engine_closure=yes`
- tracked result and plan evidence exists
- no known active positive-output mismatch in the denominator role
- no active portability or semantic caveat that would make denominator interpretation unfair
- the case is compatible with the currently runnable route being used in the experiment packet

Additional route-specific eligibility:

- PG-native common-core denominator:
  - must already be covered by a completed execution-layer smoke route
- clean PORT denominator:
  - must already be covered by a completed clean subset smoke route
- extended diagnostic set:
  - may retain caveats, but must be clearly labeled diagnostic rather than denominator-clean

## 8. Required Fields Per Case Before Formal Run

Before a case enters a formal run packet, the following should be explicitly checked and frozen:

- `case_id`
- `primary_pool`
- `source_family`
- `current_maturity`
- `benchmark_line`
- `package_engineering_status`
- `validated_engines`
- `tri_engine_closure`
- `formal_skeleton_status`
- `release_grade_status`
- `admission_status`
- `promotion_status`
- `admission_blockers`
- `current_role`
- `notes_link`

Artifact / package checks per case:

- `source.sql` exists
- `manifest.yaml` exists
- positive rewrite path exists where route requires it
- negative rewrite path exists where route requires it
- result-check artifact exists
- plan-check artifact exists
- route-specific smoke evidence exists for inclusion in the formal packet

Interpretation requirement:

- every included case must have a clear denominator role
- every caveat must be explicitly documented before formal run assembly

## 9. Open Blockers

Denominator-level blockers:

- `PORT_0012` failure-analysis packet is not yet frozen
- no formal decision has been made on whether to lift smoke material into a formal protocol draft
- current readiness scaffolds remain scratch-stage and not formal experiment policy

Route-level blockers:

- Calcite adapter/build path missing
- LearnedRewrite artifact/adapter path missing
- GenRewrite correction-loop / verifier / cost-control stack missing
- R-Bot / LLM-R2 retrieval / demo / rule-pool stack missing
- SlabCity local adapter or reproducible service/runtime contract missing
- SQLSolver / VeriEQL solver wrapper / subset / timeout / schema-constraint path missing

Case-level blockers for first-freeze caution:

- `PORT_0012` remains an active holdout
- `PERF_0038` remains pending / not clean
- `PERF_0076` remains extended-oriented rather than clean-denominator material

Governance blockers:

- no admission decision
- no formal review packet for denominator promotion yet
- no benchmark protocol-level freeze yet

## 10. Recommended Next Action

- Create a tracked `PORT_0012` failure-analysis packet and use it to decide whether the formal PORT denominator remains `2` clean cases or expands to `3`.

