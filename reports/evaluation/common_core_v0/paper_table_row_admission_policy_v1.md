# Draft Paper Table Row Admission Policy v1

This file is a reviewable governance draft for the `common_core_v0` paper-facing
method-comparison work.

It is not a frozen benchmark rule, does not update
`method_comparison_summary_v2`, and does not create a leaderboard.

## Scope

- denominator family in scope: `common_core_v0_40_same_engine_120`
- intended same-engine row count: `40 cases x 3 engines = 120`
- purpose: classify retained artifacts by safe paper-table role before any later
  human policy freeze

## Core Guardrails

- Proposed rows are not canonical leaderboard rows.
- Route-level evidence is not a method-family aggregate.
- PG-only subset evidence is not a tri-engine `120`-row row.
- The `240`-row combined SQLGlot aggregate is not the same as a `120`-row
  common-core route.
- Support/verifier rows do not belong in a rewrite speedup leaderboard.
- Portability route rows do not belong in the same-engine method leaderboard.
- Controls and guards are not rewrite method rows.
- Subset timing speedups must not be compared as full-denominator leaderboard
  scalars.
- `leaderboard_comparable = yes` is not allowed unless full-denominator timing
  and admission policy explicitly support that boundary.

## Policy Categories

| policy_category | allowed table placement | required denominator condition | timing / speedup rule | leaderboard_comparable rule | examples from current artifacts | explicit non-claims |
|---|---|---|---|---|---|---|
| `same_engine_method_evidence_candidate` | `main_same_engine_evidence_table` | Must be same-engine rewrite evidence with an explicit denominator, explicit engine scope, and explicit failure accounting. The denominator may be full `120`, route-specific `120`, or an explicit same-engine subset, but it must not be hidden. | Timing may be shown only if the timing denominator is explicit. Subset timing must remain subset-scoped. | Default `no`. May become `yes` only after later human policy freeze plus aligned full-denominator timing evidence. | `direct_llm_same_engine_rewrite`, `calcite_hep_pg_rewrite`, `sqlglot_combined_same_engine_240` | Not a ranked leaderboard row by default. Not a claim that denominators are directly comparable. |
| `route_level_proposed_row_only` | `route_level_appendix` | Must be a retained route packet or proposed row with explicit denominator and route boundary. | May carry retained timing fields, but only as route-scoped fields. | Always `no` in this draft. | `calcite_hep_fail_closed_120_proposed`, `sqlglot_optimize_same_dialect`, `sqlglot_transpile_same_dialect_noop` | Not canonical. Not a method-family aggregate. Not automatic admission to the main table. |
| `bounded_subset_evidence_only` | `bounded_subset_appendix` | Evidence is same-engine but denominator is a bounded subset or PG-only slice rather than the intended tri-engine `120`. | Timing may be reported only on the bounded subset denominator. | Always `no` in this draft. | `r_bot_same_engine_rewrite`, `llm_r2`, `learnedrewrite` | Not a tri-engine `120` row. Not a full-method comparable scalar. |
| `portability_route_only` | `portability_table` | Must be explicit cross-dialect or transfer-route evidence with its own portability denominator. | `SpeedupTransferRate` must remain `NA_not_computed` unless aligned target-engine benefit evidence exists. | Always `no` in this draft. | `sqlglot_cross_dialect_transpile_portability`, `llm_translate_portability` | Not same-engine leaderboard evidence. Not rewrite speedup evidence. |
| `support_or_verifier_only` | `verifier_support_table` | Must be verifier or support evidence with a verifier-specific denominator. | No rewrite speedup field should be compared. | Always `no` in this draft. | `sqlsolver`, `verieql` | Not rewrite-generation rows. Not leaderboard rows. |
| `control_reference_or_guard_only` | `controls_table` | Must be explicit control, reference, or negative-guard evidence. | Control timing may exist, but it is not prior-method timing. | Always `no` in this draft. | `native_identity_control`, `human_positive_reference`, `hard_negative_guard` | Not rewrite methods. Not prior-method leaderboard rows. |
| `plan_observability_only` | `not_ready` unless a separate plan table is defined | Must be plan-observability evidence with explicit plan denominator and non-rewrite metric contract. | Rewrite speedup fields are out of scope. | Always `no` in this draft. | No retained dedicated common-core paper row currently promoted in `reports/evaluation/common_core_v0/` | Not rewrite correctness or speedup evidence. |
| `insufficient_or_missing_evidence` | `not_ready` | Denominator, role, or retained artifact packet is incomplete for paper-table placement. | Timing must not be promoted. | Always `no` in this draft. | Use only when retained artifacts are missing or insufficiently packaged. No row in the current classification table is assigned here. | Not ready for paper-table placement. |

## Current Artifact Classification

| current_row_id | policy_category | recommended_placement | denominator_basis | timing boundary | why this placement is safe |
|---|---|---|---|---|---|
| `calcite_hep_pg_rewrite` | `same_engine_method_evidence_candidate` | `main_same_engine_evidence_table` | Explicit PG-only `common_core_v0_40_pg40` denominator retained in canonical ledger. | Timing exists only on the PG subset. | Same-engine evidence row with explicit subset scope and explicit caveats. |
| `calcite_hep_fail_closed_120_proposed` | `route_level_proposed_row_only` | `route_level_appendix` | Explicit fail-closed `common_core_v0_40_same_engine_120` denominator. | `NA_not_computed`. | Strong proposed denominator-aware row, but still not canonical and not timing-backed. |
| `sqlglot_combined_same_engine_240` | `same_engine_method_evidence_candidate` | `main_same_engine_evidence_table` | Explicit `240` aggregate denominator across two same-engine routes. | Timing exists only on the combined `137` timing-success subset. | Already canonical evidence-ledger material, but must not be conflated with a single `120`-row route. |
| `sqlglot_optimize_same_dialect` | `route_level_proposed_row_only` | `route_level_appendix` | Explicit `common_core_v0_40_same_engine_120_optimize_route`. | Timing exists only on `timing_success_65_on_optimize_route`. | Clear retained same-engine route packet, but still route-only. |
| `sqlglot_transpile_same_dialect_noop` | `route_level_proposed_row_only` | `route_level_appendix` | Explicit `common_core_v0_40_same_engine_120_transpile_noop_route`. | Timing exists only on `timing_success_72_on_transpile_noop_route`. | Clear retained same-engine route packet, but still route-only. |
| `direct_llm_same_engine_rewrite` | `same_engine_method_evidence_candidate` | `main_same_engine_evidence_table` | Explicit `common_core_v0_40` same-engine denominator retained in canonical ledger. | Timing exists only on the explicit timing-success subset. | Strong same-engine evidence row with explicit failure accounting. |
| `r_bot_same_engine_rewrite` | `bounded_subset_evidence_only` | `bounded_subset_appendix` | Explicit PG-only subset denominator retained. | Timing exists only on the PG15 match-exact subset. | Safe only as bounded subset evidence, not tri-engine method row. |
| `llm_r2` | `bounded_subset_evidence_only` | `bounded_subset_appendix` | Bounded `10`-case smoke denominator retained only in scratch evidence. | Bounded PG-only timing slice. | Too small for main table but valid as bounded appendix evidence. |
| `learnedrewrite` | `bounded_subset_evidence_only` | `bounded_subset_appendix` | Bounded `10`-case smoke denominator retained only in scratch evidence. | Bounded PG-only timing slice. | Too small and mostly no-op for main table, but still bounded evidence. |
| `sqlsolver` | `support_or_verifier_only` | `verifier_support_table` | Explicit verifier smoke denominator of `4` query pairs. | No rewrite timing claim allowed. | Support-verifier role is explicit and should remain separated. |
| `verieql` | `support_or_verifier_only` | `verifier_support_table` | Explicit bounded support-canary denominator. | No rewrite timing claim allowed. | Support-verifier role is explicit and should remain separated. |
| `sqlglot_cross_dialect_transpile_portability` | `portability_route_only` | `portability_table` | Explicit bounded `PORT` route denominator retained only in scratch evidence. | `SpeedupTransferRate` remains `NA_not_computed`. | Portability route evidence is real but belongs in a separate table. |
| `llm_translate_portability` | `portability_route_only` | `portability_table` | Explicit bounded `PORT` route denominator retained only in scratch evidence. | `SpeedupTransferRate` remains `NA_not_computed`. | Portability route evidence is real but belongs in a separate table. |
| `native_identity_control` | `control_reference_or_guard_only` | `controls_table` | Explicit control denominator retained only in scratch evidence. | Control-only timing boundary. | Control line, not a rewrite method. |
| `human_positive_reference` | `control_reference_or_guard_only` | `controls_table` | Explicit control denominator retained only in scratch evidence. | Control-only timing boundary. | Positive reference, not a rewrite method. |
| `hard_negative_guard` | `control_reference_or_guard_only` | `controls_table` | Explicit control denominator retained only in scratch evidence. | Guard-only timing boundary. | Guard line, not a rewrite method. |

## Review Boundary

This draft does not:

- promote any proposed row into canonical status
- update `method_comparison_summary_v2`
- create a leaderboard table
- freeze a final admission policy
- alter denominator scope, checker semantics, or benchmark rules

Human review is still required before any of these categories can become
source-of-truth policy.
