# PAPER_RQ_NARRATIVE_STAGING_v1_1

## 0. Purpose And Boundary

This is a staging note, not final manuscript text.

`paper-draft-v1` remains the base evidence packet.

`v1.1` adds bounded PORT cross-engine evidence.

No new experiment is performed by this note.

No final denominator is frozen by this note.

This note is intended to stage current RQ1/RQ2/RQ3/RQ4 narrative choices, mark which claims already look stable, and separate checkpoint-only numbers from claims that should wait for later experiments or final paper freeze.

## 1. Current Evidence View

Current evidence view:

- `46` common-core evidence cases
- `6` PostgreSQL-side PORT cases
- bounded `3`-case x `2`-engine MySQL/Spark execution sub-slice
- only `PORT_0024` closed on both MySQL and Spark
- `PORT_0022` and `PORT_0025` remain execution-blocked before checker comparison
- not full PORT closure
- not final cross-engine matrix

Interpretation:

- the `46`-case packet remains the main same-engine evidence base
- the `6`-case PORT packet remains a PostgreSQL-side portability layer
- the bounded MySQL/Spark slice is additive checkpoint evidence, not a new frozen denominator

## 2. Stable Narrative Claims

The following claims are stable enough to carry forward:

1. seed-only evaluation can overestimate rewrite-route robustness
2. correctness-valid rewrites are not automatically stable speedup wins
3. portability evidence must be layered
4. cross-engine portability can fail before semantic checking

These are higher-confidence narrative claims than any single checkpoint number, because they are supported by repeated bounded observations across multiple packets rather than by one isolated table.

## 3. RQ1 Staging: Route Robustness / Applicability

Current staging narrative:

- `SQLGlot optimize` passes the seed packet at `9 / 9`
- it fails repeatedly on expanded PERF slices:
  - Batch 2A: `4 / 19`
  - Batch 3A: `2 / 11`
  - Batch 3B: `1 / 4`
- the repeated later-wave failures indicate that the seed packet materially overestimates route robustness
- the clean controls and the broader no-opt route closure indicate that this is a method-route capability boundary rather than a generic package-health problem

Staging judgment:

- stable claim: yes
- final table numbers: checkpoint-only until paper freeze

Suggested narrative direction:

- use RQ1 to argue that small seed or workload-only evaluation can hide capability boundaries
- keep the later PERF-wave numbers explicit in staging materials, but do not yet treat any single table layout as final manuscript structure

## 4. RQ2 Staging: Correctness-Gated Speedup

Current staging narrative:

- Human positive, SQLGlot no-opt, Direct LLM rewrite, and Calcite HEP are checker-consistent where evaluated
- speedup remains near-neutral, tie-heavy, or mildly negative across the bounded scored packets
- correctness-valid rewrite therefore does not imply a stable speedup win
- the more defensible paper direction is to emphasize correctness-gated evaluation rather than raw speedup optimism

Staging judgment:

- stable claim: yes
- final leaderboard wording: not yet
- final speedup table: checkpoint-only

Suggested narrative direction:

- use RQ2 to argue that executable and checker-consistent rewrites may still produce limited or non-positive runtime gains
- keep Calcite HEP explicitly bounded and separate from the main common-core denominator

## 5. RQ3 Staging: Portability / Cross-engine Evidence

Current staging narrative must remain explicitly layered.

Layer A:

- PG-side PORT evidence: `6` cases
- SQLGlot Transpile PG success `4 / 6`
- Direct LLM Translate PG success `6 / 6`
- PG-side only, not cross-engine closure

Layer B:

- cross-engine feasibility preflight: `6` cases
- `3 / 6` MySQL-ready
- `3 / 6` Spark-ready
- `3 / 6` both-engine-ready

Layer C:

- bounded MySQL+Spark execution attempt
- `3` approved cases x `2` engines
- `PORT_0022`, `PORT_0024`, `PORT_0025`
- only `PORT_0024` closed on both engines
- `PORT_0022` and `PORT_0025` blocked before checker comparison

Required accepted wording:

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

Staging judgment:

- stable claim: portability must be layered
- checkpoint-only number: `1 / 3` both-engine success
- not computed: `SpeedupTransferRate`

Suggested narrative direction:

- use RQ3 to show that portability has at least three separate evidence layers: same-engine route evidence, cross-engine readiness, and bounded cross-engine execution
- emphasize that failure can happen before checker comparison, which means execution-layer failure categories matter directly for portability analysis
- do not compress the current PORT packet into a single success-rate claim

## 6. RQ4 Staging: Coverage / Failure Analysis

Current staging narrative:

- current coverage and failure slicing should remain careful rather than totalizing
- metadata-backed coverage evidence is useful, but it is not yet final full `46`-case taxonomy closure
- PORT now adds execution-layer failure categories:
  - `rewrite_execution_failed`
  - `source_execution_failed`
- the paper should emphasize failure taxonomy, not only success rates
- bounded support evidence and bounded method-specific subsets are informative, but they do not yet justify a final full coverage map

Staging judgment:

- stable claim: failure analysis is central
- final coverage map: not yet
- taxonomy closure: not yet

Suggested narrative direction:

- use RQ4 to argue that benchmark interpretation should account for route failure modes, blocked baselines, and execution-layer portability failures rather than only closed successes

## 7. Claims To Avoid In Manuscript For Now

Avoid the following claims for now:

- final leaderboard
- full prior-method coverage
- full PORT cross-engine closure
- `6`-case PORT closure
- final cross-engine matrix
- `SpeedupTransferRate` result
- registry/admission/common-core promotion
- Calcite HEP full baseline
- VeriEQL rewrite or speedup baseline

## 8. What Should Wait For Future Experiments

The following should wait for future experiments or final freeze work:

- final denominator
- final method leaderboard
- `SpeedupTransferRate`
- full `6`-case PORT cross-engine closure
- broader prior-method runnable coverage
- plan attribution
- final RQ4 full taxonomy coverage map

## 9. Recommended Stop / Freeze Decision

- do not expand PORT further for this paper draft
- keep `PORT_0022` and `PORT_0025` as portability failure-analysis evidence
- use `v1.1` to update RQ3 narrative later, not final manuscript now
- next manuscript work should be staged, not final rewrite

## 10. One-paragraph Draft Abstract Update Candidate

Candidate only, not final abstract:

RewriteBench currently supports a staged evidence packet that combines `46` common-core evidence cases with a bounded portability packet of `6` PostgreSQL-side PORT cases and an additional bounded `3`-case x `2`-engine MySQL/Spark execution sub-slice. Across this packet, the current evidence suggests that seed-only evaluation can overestimate route robustness, that correctness-valid rewrites do not automatically yield stable speedup gains, and that portability must be evaluated in layered form rather than as a single success rate. In particular, a bounded MySQL+Spark follow-up closed only `PORT_0024` on both engines, while `PORT_0022` and `PORT_0025` remained execution-blocked before checker comparison, indicating that cross-engine portability failure can arise before semantic comparison and should be treated as first-class benchmark evidence rather than collapsed into final closure claims.

## 11. One-paragraph RQ3 Draft Candidate

Candidate only, not final manuscript text:

The current portability evidence should be read in three layers rather than as a single closure claim. First, the PostgreSQL-side PORT packet now covers six cases, with SQLGlot Transpile succeeding on four of six and Direct LLM Translate succeeding on six of six, but this remains same-engine evidence only. Second, a read-only cross-engine feasibility preflight shows that only three of the six cases are currently ready for both MySQL and Spark execution. Third, a bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix. The current RQ3 lesson is therefore not that portability is solved, but that portability evidence must separate same-engine route success, cross-engine readiness, and execution-layer failure before semantic checking.

## Source Basis

- `docs/_scratch/RewriteBench_checkpoint_summary_v1_1.md`
- `docs/_scratch/EXPANDED_PORT_RESULTS_CLOSEOUT_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_CLOSEOUT_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_BOUNDED_EXECUTION_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_FEASIBILITY_PREFLIGHT_v0.md`
- `docs/_scratch/PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0.md`
- `docs/_scratch/PAPER_EXPERIMENT_RESULTS_ROLLUP_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/EXPANDED_COMMON_CORE_RESULTS_ROLLUP_v0.md`
- `paper/outline.md`

## Non-Modification Note

- no DB execution was performed while producing this note
- no model calls were performed while producing this note
- no SQLGlot execution was performed while producing this note
- no case files were modified
- no `result_check.json` files were modified
- no report JSON files were modified
- no registry files were modified
- no review files were modified
- no benchmark protocol, taxonomy, admission, or common-core rules were modified
- no final manuscript files were modified
- `docs/EXECUTION_STATUS.md` was not modified
- the three long-standing untracked taxonomy notes were left untouched
