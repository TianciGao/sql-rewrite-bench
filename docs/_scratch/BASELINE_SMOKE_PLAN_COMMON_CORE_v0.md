# Baseline Smoke Plan Common-Core v0

- Status: scratch planning document only
- Scope: first very small baseline smoke run on a controlled common-core-style subset
- This file is not a formal experiment protocol, not a full baseline comparison, not a leaderboard declaration, not registry writeback, and not a live status change.

## 1. Purpose and Non-Goals

This document defines a minimal execution-facing smoke plan for baseline readiness on a small subset of the current health-gated common-core review slate.

Its purpose is to:

- bind a small baseline set to a clean and interpretable case subset
- define expected output fields before any runner implementation
- make baseline eligibility and failure logging explicit
- reduce ambiguity before the first very small smoke run

This document does not do the following:

- define a formal experiment protocol
- define a full baseline comparison package
- claim leaderboard readiness
- treat the current `35`-case possible slate as admitted common-core
- change registry facts
- change review status
- change common-core admission state
- authorize a `130+` extended run

## 2. Candidate Case Roster

The roster below is intentionally conservative.
It uses `12` cases from the current health-gated keep-for-review subset, with:

- `7` PERF cases
- `3` PORT cases
- `2` CONS cases

Excluded by design:

- `PERF_0038`
- `PERF_0076`

Avoided for this first smoke because of extra caveat load:

- `PERF_0022`
- `PORT_0003`
- `PORT_0016`
- `CONS_0034`

| case_id | pool | why selected | caveat | smoke role |
| --- | --- | --- | --- | --- |
| `PERF_0006` | performance | canonical governed analytical baseline; clean tri-engine evidence | ordinary staged-not-admitted caveat only | `identity_check` |
| `PERF_0008` | performance | clean join/report representative; simple positive reference candidate | ordinary staged-not-admitted caveat only | `positive_reference` |
| `PERF_0013` | performance | stable join/aggregate denominator with clean evidence | ordinary staged-not-admitted caveat only | `negative_guard` |
| `PERF_0017` | performance | anchor-quality grouped reporting case; good LLM smoke target | ordinary staged-not-admitted caveat only | `llm_candidate` |
| `PERF_0024` | performance | clean correlated-subquery coverage; good rule/tool target | ordinary staged-not-admitted caveat only | `sqlglot_candidate` |
| `PERF_0033` | performance | clean governed TPC-DS starter; tests beyond TPC-H | ordinary staged-not-admitted caveat only | `identity_check` |
| `PERF_0054` | performance | join-reorder coverage with clean evidence; useful for rewrite-sensitive smoke | ordinary staged-not-admitted caveat only | `llm_candidate` |
| `PORT_0004` | portability | clean MySQL-reference datetime/type case; low-caveat portability anchor | still PARROT-derived; staged-not-admitted | `identity_check` |
| `PORT_0012` | portability | dense PostgreSQL-reference datetime/type case; useful same-dialect and LLM smoke target | still PARROT-derived; staged-not-admitted | `sqlglot_candidate` |
| `PORT_0022` | portability | clean datetime/type case on different schema; portability coverage without the heaviest endpoint caveats | still PARROT-derived; staged-not-admitted | `llm_candidate` |
| `CONS_0007` | consistency | compact correlated `EXISTS` semantic baseline; easy negative-guard smoke | semantic addendum case, not main PERF/PORT denominator | `negative_guard` |
| `CONS_0012` | consistency | clear `LIMIT` / `OFFSET` threshold rewrite; good positive-reference smoke | semantic addendum case, not main PERF/PORT denominator | `positive_reference` |

## 3. Baseline Roster

Only the following baselines are in scope for the first smoke.
All others remain out of scope for this first run.

| baseline_id | boss_group | leaderboard_role | smoke role | expected input | expected output | can_run_this_smoke | blocker | required adapter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NATIVE_IDENTITY` | `P0_control_or_tool` | `control_only` | establish source-SQL denominator and runtime/result baseline | `source.sql`, schema, engine config | runtime, result artifact, source plan artifact if collected | `yes` | engine choice must be fixed first | existing harness only |
| `HUMAN_REFERENCE_POSITIVE` | `P0_control_or_tool` | `reference_or_guard` | confirm benchmark slice has valid optimization opportunities | `rewrite_pos_*.sql`, `source.sql`, schema, witness/checker context | validated positive rewrite result and plan delta | `yes` | only meaningful on cases with clean positive rewrites | existing harness only |
| `HARD_NEGATIVE_GUARD` | `P0_control_or_tool` | `reference_or_guard` | verify plausible-but-wrong rewrites are rejected | `rewrite_neg_*.sql`, `source.sql`, witness/checker context | negative rejection outcome / false-accept signal | `yes` | only meaningful on cases with negative rewrites | existing checker path only |
| `SQLGLOT_OPT_SAME_DIALECT` | `P0_control_or_tool` | `speedup_leaderboard` | lightweight rule/tool smoke on same-dialect cases | `source.sql`, dialect tag, optional schema hint | optimized SQL candidate plus parse status | `maybe` | SQLGlot adapter command and SQL acceptance policy not frozen | SQLGlot CLI or Python adapter |
| `LLM_DIRECT_REWRITE_STRONG` | `P0_control_or_tool` | `speedup_leaderboard` | minimal direct LLM rewrite smoke | `source.sql`, schema context, target engine, prompt template | rewritten SQL candidate plus token/cost log | `maybe` | prompt freeze, cost logging, model/version freeze not yet set | prompt template + model call wrapper |

Optional next smoke baselines, explicitly not first run:

- `SQLGLOT_TRANSPILE`
- `LLM_DIRECT_TRANSLATE`
- `LLM_DIRECT_REWRITE_SMALL`

Explicitly excluded from the first smoke:

- `CALCITE_HEP_RULES`
- `LEARNED_REWRITE`
- `GENREWRITE`
- `R_BOT`
- `LLM_R2`
- `SLABCITY`
- verifier/support-only methods
- all `P3` appendix methods

## 4. Smoke Execution Contract

Each smoke-run record should be able to emit at least the following fields.
This section defines output shape only; it does not implement any runner.

| field | meaning |
| --- | --- |
| `baseline_id` | baseline method identifier |
| `case_id` | case package identifier |
| `variant_id` | `source`, `rewrite_pos_01`, `rewrite_neg_01`, or baseline-generated variant label |
| `generated_sql_path` | path to generated or selected SQL artifact |
| `execution_status` | `success`, `failed`, `skipped`, or comparable machine-readable status |
| `result_consistency_status` | whether output matches the accepted consistency contract for that case |
| `negative_rejection_status` | whether a negative rewrite was correctly rejected when applicable |
| `plan_collection_status` | whether plan artifacts were captured or intentionally skipped |
| `failure_category` | normalized failure label from the list below |
| `runtime_ms` | runtime in milliseconds if available |
| `token_count` | total token count for LLM baselines when available |
| `estimated_cost_usd` | estimated API cost for LLM baselines when available |
| `notes` | free-form short note for adapter or case-specific context |

## 5. Failure Categories

Initial normalized failure categories:

- `parse_error`
- `unsupported_dialect`
- `execution_error`
- `result_mismatch`
- `timeout`
- `no_rewrite_generated`
- `invalid_negative_acceptance`
- `plan_collection_failed`
- `llm_refusal_or_empty`
- `cost_limit_exceeded`
- `unknown`

## 6. Minimal Run Order

Run order for the first smoke should be fixed and simple:

1. `NATIVE_IDENTITY`
2. `HUMAN_REFERENCE_POSITIVE`
3. `HARD_NEGATIVE_GUARD`
4. `SQLGLOT_OPT_SAME_DIALECT`
5. `LLM_DIRECT_REWRITE_STRONG`

Reason:

- establish reference execution and expected outputs first
- confirm positives and negatives before introducing generated rewrites
- add deterministic tool baseline before LLM variability
- keep debugging order obvious

## 7. Eligibility Rules

Eligibility should be explicit before any smoke run starts.

General rules:

- `NATIVE_IDENTITY` can run on every selected case.
- `HUMAN_REFERENCE_POSITIVE` can run only where an accepted positive rewrite already exists.
- `HARD_NEGATIVE_GUARD` can run only where an accepted negative rewrite already exists.
- `SQLGLOT_OPT_SAME_DIALECT` should run only on cases whose source SQL is accepted by the same-dialect SQLGlot path for the selected engine.
- `LLM_DIRECT_REWRITE_STRONG` should run only on cases where the prompt package can be constructed without special-case hidden context.

Case-type interpretation:

- PERF cases are the main same-engine rewrite smoke substrate.
- PORT cases may be included in the first smoke only as controlled same-engine or cross-dialect-aware planning targets, not as a full translation leaderboard.
- CONS cases are included only as compact semantic addendum checks, not as a broad semantic stress suite.

Explicitly out of scope for the first smoke:

- support-only baselines
- verifier-only baselines
- subset-only prior methods needing substantial adapters
- broad extended-evaluation coverage

## 8. Overclaim Guardrails

The following claims must not be made from this smoke:

- that the results constitute a final leaderboard
- that subset-only methods can be mixed into a main ranking without denominator labeling
- that any extended result should be reported as common-core
- that the baseline inventory scratch CSV is a formal benchmark protocol
- that the `35`-case slate is admitted common-core
- that this smoke implies full pilot-scale baseline readiness

Any future report from this smoke should:

- label methods by capability boundary
- label subset-only methods explicitly
- separate same-engine and translation-oriented outputs
- keep common-core-style smoke results separate from any later extended run

## 9. Open Blockers Before Running

Human decisions or engineering clarifications still needed before execution:

- final `10–15` case roster confirmation
- SQLGlot adapter command definition
- LLM prompt freeze
- token / cost logging format
- output directory convention
- failure logging schema
- engine selection for first smoke
- whether the first smoke is `PG-only` or `tri-engine`

Recommended interpretation of blocker priority:

- first decide the roster
- then decide `PG-only` versus `tri-engine`
- then freeze output schema and prompt/cost logging

## 10. Recommended Immediate Next Step

Human confirms the `10–15` case smoke roster and whether the first smoke is `PG-only` or `tri-engine`.
