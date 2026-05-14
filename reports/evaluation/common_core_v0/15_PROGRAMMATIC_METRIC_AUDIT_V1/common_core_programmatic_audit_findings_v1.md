# Common-core v0 Programmatic Metric Audit Findings v1

## 1. Purpose
This audit maps Common-core v0 execution scripts, aggregation artifacts, metric formulas, inputs, outputs, and traceability from retained program/artifact layers to paper-facing Section 8 tables. It does not adjudicate scientific claims.

## 2. Scope and non-goals
Scope was read-only inspection of retained scripts, manifests, reports, and case-package references. No database engines, LLM/model calls, verifier tools, PORT9 experiments, EXPLAIN collection, timing collection, taxonomy edits, case edits, registry edits, protocol edits, code fixes, or paper prose edits were performed.

## 3. Script inventory summary
The retained program layer includes CLI scaffolding in `scripts/cli.py`, validation logic in `scripts/common_core_v0_validation.py`, exact Direct LLM generation/repair Python runners, package hard-negative closure code, selected PG plan-observability code, and many shell/manual run packets under `reports/evaluation/common_core_v0/runs/**`. Several important aggregations are artifact-only: denominator composition, taxonomy coverage, candidate failure accounting, PORT readiness, verifier support, and final Section 8 value mapping.

## 4. Metric formula summary
The strongest code-retained formulas are timing formulas and hard-negative closure formulas. Speedup ratio is retained as `source_median_runtime / rewrite_median_runtime`; GM speedup is `exp(mean(log(speedup_ratio)))` over exact + timing-success rows; Regression@20 is `count(speedup_ratio < 0.8) / timing_denominator`, equivalent to candidate median runtime at least `1.20 * source` in runner code. Hard-negative false accept rate is `false_accept_rows / tested_negative_rows`.

## 5. Table-to-artifact traceability summary
Tables 8 through 20 are traceable to retained artifacts, but not uniformly to retained generator code. Tables 13 and 15 have the strongest code+artifact traceability for main rows. Tables 9, 10, 14, 17, 18, 19, and 20 are mostly artifact-only or policy/artifact mapping layers.

## 6. Metrics that are fully traceable
Fully traceable metrics include package hard-negative planned/tested/rejected/false-accept counts, Direct LLM repair timing formulas, route timing GM/median/W/T/L/Regression@20 where per-case timing rows exist, and selected PG frontier plan availability for retained selected rows.

## 7. Metrics that are artifact-only
Artifact-only metrics include taxonomy coverage aggregates, candidate failure accounting aggregation, bounded PORT6 closure/readiness, verifier support pair summaries, conclusion-evidence mapping, and the final Section 8 value/source map. These are retained and inspectable, but their generator scripts are absent or not clearly retained.

## 8. Metrics with missing code-level formula
Missing or incomplete code-level formulas include full Section 8 table rendering, taxonomy aggregation regeneration, candidate failure-accounting aggregation, SQLGlot combined diagnostic aggregation, full prior-method bounded rows, SpeedupTransferRate, full NodeAlignmentCoverage, and full verifier support rate with clean SQLSolver verdict split.

## 9. Metrics needing independent recomputation
Round 15B should recompute denominator composition, taxonomy coverage, hard-negative guardrail counts, candidate failure buckets, and timing formulas from retained CSV/event artifacts. It should explicitly check executed semantics versus ready-after-preflight semantics for Direct LLM repair and method evidence rows.

## 10. Metrics that are unsupported / NA by design
SpeedupTransferRate is not computed because paired target-engine timing arrays are not retained. Full NodeAlignmentCoverage is not computed because only a selected PG frontier exists. Verifier support is support-layer evidence, not a rewrite baseline. Bounded PORT6 is not full PORT9. Bounded prior methods are appendix evidence, not full-denominator leaderboard rows.

## 11. Potential risks or inconsistencies
The main semantic risk is executed rows versus ready-after-preflight rows: the Direct LLM repair route preserves ready/blocker semantics separately from final executed semantics. Another risk is route-summary-only bounded evidence being read as recomputable per-case timing. SQLGlot no-op/source-like rows must remain visible as method behavior, not silently treated as success or discarded failure. The empty `primary_metrics_v0.md`, `common_core_extended_rules_v0.md`, and `docs/EXECUTION_STATUS.md` files are traceability gaps for policy-level definitions in this branch.

## 12. Recommended Round 15B independent recomputation plan
Run static recomputation only. First, verify denominator manifests and table index path existence. Second, recompute taxonomy counts from retained tag matrices. Third, recompute hard-negative guardrail counts from retained event_long. Fourth, recompute candidate failure buckets for main route rows from retained summary/event artifacts. Fifth, recompute timing GM/median/W/T/L/Regression@20 from retained per-case timing rows where available, and mark route-summary-only rows as artifact-only.

## 13. Source-of-truth writeback judgment
No source-of-truth writeback is needed in this round. The audit does not change source facts, case facts, taxonomy definitions, denominators, primary metrics, admission policy, or paper claims.
