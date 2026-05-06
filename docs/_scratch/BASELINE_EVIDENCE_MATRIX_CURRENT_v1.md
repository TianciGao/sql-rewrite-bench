# BASELINE_EVIDENCE_MATRIX_CURRENT_v1

## 0. Purpose And Boundary

This document is a current baseline evidence matrix for RewriteBench.

- documentation / aggregation only
- no new experiment
- not a leaderboard
- separates rewrite-generation, support/verifier, and portability/transfer baselines

The matrix below is an evidence-status table, not a ranking table. Rewrite-generation rows summarize checker-backed generation and bounded same-engine speedup evidence. Support/verifier rows summarize artifact-support evidence only. Portability/transfer rows summarize bounded translation-route evidence only. Support metrics are artifact-support metrics and cannot substitute rewrite leaderboard primary metrics.

## 1. Executive Summary

Current strength is highest for three rewrite-generation prior methods and the core control lines. R-Bot / LLM4Rewrite, LearnedRewrite / embedded LLM4Rewrite, and LLM-R2 all now have bounded 10-case rewrite smoke evidence plus correctness-gated PG-only witness-scale speedup slices. SQLSolver also has a bounded support smoke rollup, and VeriEQL has bounded support-canary / availability evidence.

Current partial areas remain transfer-oriented baselines and older bounded rewrite lines. Calcite HEP now has 10/10 PG-only checker+speedup measured evidence on the target denominator, with witness-scale and non-leaderboard caveats. SQLGlot Transpile and LLM Translate now have a bounded 4-case cross-engine closed PORT subset within a 6-case PG-side route packet, but `PORT_0012` and `PORT_0013` remain PG-route / dialect blocked and `SpeedupTransferRate` remains uncomputed. SQLGlot optimize and Direct LLM rewrite have earlier bounded evidence, but they are not yet summarized in the same shared-denominator style as the strongest current rewrite lines.

Blocked baselines remain blocked for substrate reasons. GenRewrite has no public runnable substrate. SlabCity remains blocked on runner or service-contract acquisition. This matrix is therefore not a ranking table because rows do not share one denominator, one role, one execution contract, or one metric family.

## 2. Unified Baseline Evidence Matrix

| baseline | role | intended_task | substrate_status | runnable_status | current_denominator | evidence_level | consistency_or_support_result | speedup_result | transfer_result | claim_boundary | blockers | next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Native / identity control | rewrite_generation | same-engine identity control | implemented control route | runnable | expanded common-core PG 46 | completed_control | control reference available | control-only | not_applicable | control_only_not_rewrite_baseline_ranking | none | maintain as identity control |
| Human positive reference | rewrite_generation | same-engine positive control | implemented control route | runnable | expanded common-core PG 46; PERF speedup slices 7+19+11+4 | completed_control | control reference available | bounded control speedup available | not_applicable | positive_control_not_prior_method_leaderboard | none | maintain as positive control |
| Hard negative guard | rewrite_generation | same-engine negative guard control | implemented guard route | runnable | expanded common-core PG 46 | completed_control | guard evidence available | guard-only | not_applicable | guard_only_not_speedup_baseline | none | maintain as negative guard |
| SQLGlot no-op / same-dialect baseline | rewrite_generation | same-engine low-transformation baseline | implemented | runnable | expanded PERF PG 34; bounded speedup slices 19+11+4 | bounded_speedup_slice | bounded checker-backed PERF evidence | bounded PG-only speedup slices measured; not final unified denominator | separate from portability transpile route | bounded_pg_only_sqlglot_noop_speedup_slices_not_leaderboard | full unified same-engine summary not rolled into current prior-method slice | retain as existing same-engine reference baseline |
| SQLGlot optimize same-dialect | rewrite_generation | deterministic same-engine optimizer baseline | implemented | runnable | common-core PG 43; bounded PERF checker-backed subset | bounded_checker_backed_smoke | PERF-only 7/7 checker-backed consistency in bounded summary | not closed as current primary slice | not_applicable | bounded_checker_backed_same_engine_optimizer_evidence | no current @10-style unified speedup slice | keep as partial same-engine deterministic baseline evidence |
| Direct LLM rewrite | rewrite_generation | same-engine direct model rewrite baseline | implemented | runnable | seed common-core PG 9; expanded PERF PG 34 | bounded_speedup_slice | PERF-only 7/7 checker-backed consistency in bounded summary | bounded PERF speedup evidence; not current prior-method 10-case slice | not_applicable | bounded_pg_only_direct_llm_rewrite_evidence_not_leaderboard | not consolidated into current shared 10-case prior-method slice | retain as bounded earlier rewrite baseline evidence |
| Calcite HEP | rewrite_generation | same-engine rule-based rewrite baseline | implemented with bounded 10/10 measured evidence | runnable | target @10; measured 10/10 | bounded_speedup_slice | 10/10 checker-consistent | PG-only witness-scale GM 0.9442674761138092; W/T/L 0/7/3; regression@20=2 | not_computed | calcite_hep_10of10_checker_speedup_rollup_not_leaderboard | none | retain as deterministic same-engine baseline evidence; do not treat as leaderboard |
| R-Bot / LLM4Rewrite | rewrite_generation | same-engine rewrite generation baseline | bounded runnable substrate with extracted candidate artifacts | runnable in bounded workflow | 10-case smoke; 7 speedup-eligible | bounded_speedup_slice | checker-consistent nontrivial 7/10 | GM 0.8804340264675553; W/T/L 0/2/5; regression@20=2 | not_computed | bounded_pg_only_rbot_speedup_slice_not_leaderboard | witness-scale only; no cross-engine transfer; no larger-data confirmation | retain in prior-method rewrite summary; no ranking beyond slice |
| LearnedRewrite / embedded LLM4Rewrite | rewrite_generation | same-engine learned rewrite generation baseline | bounded runnable substrate with extracted candidate artifacts | runnable in bounded workflow | 10-case smoke; 2 speedup-eligible non-noop | bounded_speedup_slice | checker-consistent 10/10 but mostly source-like/no-op | GM 0.6295872209675301; W/T/L 0/0/2; regression@20=2 | not_computed | bounded_pg_only_learnedrewrite_speedup_slice_not_leaderboard | very small non-noop denominator; witness-scale only | retain with explicit no-op caveat |
| LLM-R2 | rewrite_generation | same-engine rewrite generation baseline | bounded runnable substrate with clean extracted candidate artifacts | runnable in bounded workflow | 10-case smoke; 9 speedup-eligible | bounded_speedup_slice | checker-consistent clean candidates 9/10 | GM 0.9592371433387649; W/T/L 1/6/2; regression@20=1 | not_computed | bounded_pg_only_llmr2_speedup_slice_not_leaderboard | witness-scale only; no cross-engine transfer; one generation-stage failure remains | retain in prior-method rewrite summary; no ranking beyond slice |
| GenRewrite | rewrite_generation | same-engine rewrite generation baseline | no public substrate found | not_runnable | 0 | blocked_no_public_substrate | not_available | not_run | not_applicable | external_discovery_only_no_public_runnable_substrate | no recoverable public runnable source/binary/service contract | stop unless new public substrate appears |
| SlabCity | rewrite_generation | same-engine rewrite generation baseline | runner or service contract unavailable | blocked | 0 | blocked_runner_or_service_contract | not_available | not_run | not_applicable | blocked_service_or_runner_contract_no_bounded_execution | missing local runner/service contract | acquire runner/service contract before any preflight |
| SQLSolver | support_verifier | equivalence/refutation support smoke | public repo acquired; tmp build complete; bounded smoke executed | runnable for bounded support smoke | 4 query pairs across CONS_0007 / CONS_0035 | support_smoke | verifier_support_rate 3/4 | not_applicable | not_applicable | bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard | only 4-pair support denominator; one unexpected positive-pair NEQ | expand support smoke only if broader support table is needed |
| VeriEQL | support_verifier | support-canary / availability verifier evidence | availability/readiness path partially demonstrated | constraint_sensitive_limited | availability/readiness plus bounded 1-case canary on CONS_0035 | support_canary | negative refutation evidence usable; positive proof closure not complete | not_applicable | not_applicable | verieql_support_canary_availability_only_not_rewrite_not_speedup | positive proof not closed; broader wrapper coverage absent | deepen support audit only if expanded verifier table is required |
| SQLGlot Transpile | portability_transfer | cross-engine / cross-dialect transpile baseline | bounded PORT route implemented on PG-side subset | partially_runnable | PORT PG-side 6; bounded cross-engine closed subset 4/6 | bounded_checker_backed_smoke | bounded PORT route packet now has 4 cross-engine closed cases: PORT_0004, PORT_0022, PORT_0024, PORT_0025 | not_run | bounded 4/6 cross-engine closed subset; PORT_0012 / PORT_0013 still PG-route blocked | bounded_port_cross_engine_subset_not_transfer_metric | no full PORT closure; `SpeedupTransferRate` not computed | diagnose/repair PORT_0012 and PORT_0013 PG-route dialect blockers |
| LLM Translate | portability_transfer | cross-engine / cross-dialect translation baseline | bounded PORT route implemented on PG-side subset | partially_runnable | PORT PG-side 6; bounded cross-engine closed subset 4/6 | bounded_checker_backed_smoke | bounded PORT route packet now has 4 cross-engine closed cases: PORT_0004, PORT_0022, PORT_0024, PORT_0025 | not_run | bounded 4/6 cross-engine closed subset; PORT_0012 / PORT_0013 still PG-route blocked | bounded_port_cross_engine_subset_not_transfer_metric | no full PORT closure; `SpeedupTransferRate` not computed | diagnose/repair PORT_0012 and PORT_0013 PG-route dialect blockers |

## 3. Rewrite-generation Baselines

The strongest rewrite-generation evidence now sits with the integrated prior-method trio plus the control lines. Native / identity, human positive, and hard negative controls are implemented and usable. R-Bot / LLM4Rewrite, LearnedRewrite / embedded LLM4Rewrite, and LLM-R2 each have bounded rewrite-generation evidence, checker-backed gating, and PG-only witness-scale speedup evidence. That is the most complete currently summarized rewrite-baseline family.

SQLGlot and Direct LLM lines remain partially strong but not equally normalized. SQLGlot no-op has bounded same-engine speedup evidence across earlier PERF slices. SQLGlot optimize and Direct LLM rewrite each have bounded checker-backed or bounded speedup evidence, but not yet in the same shared-denominator prior-method rollup structure used for R-Bot, LearnedRewrite, and LLM-R2.

Calcite HEP is no longer just a 4-case subset line. It now has 10/10 PG-only checker-consistent and speedup-measured evidence on the shared target denominator, which makes it a complete bounded deterministic rewrite baseline line in the current matrix. That evidence remains witness-scale, same-engine only, not cross-engine transfer, and not production-scale speedup evidence. GenRewrite and SlabCity remain blocked for substrate reasons rather than checker or speedup reasons: GenRewrite has no public runnable substrate, and SlabCity lacks a usable local runner or service contract.

## 4. Support / Verifier Baselines

SQLSolver and VeriEQL belong in a separate support/verifier family. SQLSolver has the stronger current evidence: public substrate acquired, tmp build completed, and bounded 4-pair CONS support smoke executed, with `verifier_support_rate = 3/4`. VeriEQL remains more limited: it has support-canary / availability evidence, is constraint-sensitive, and still lacks closed positive-proof coverage.

These rows are intentionally not speedup rows. They do not generate rewrites, they do not belong in rewrite-method denominator tables, and their metrics are artifact-support metrics rather than method-ranking speedup metrics. This role separation is required by the current benchmark metric design.

## 5. Portability / Transfer Baselines

SQLGlot Transpile and LLM Translate currently represent bounded portability / transfer evidence rather than closed transfer baselines. Both now have a materially stronger bounded cross-engine closed subset: `PORT_0004`, `PORT_0022`, `PORT_0024`, and `PORT_0025` are cross-engine closed within the current 6-case PG-side route packet. However, `PORT_0012` and `PORT_0013` remain PG-route / dialect blocked, so the route denominator is still not fully closed. Because of that, transfer metrics such as `SpeedupTransferRate` should remain uncomputed.

The current matrix therefore treats portability rows as bounded route-closure evidence only, not transfer-metric evidence. They are useful for route readiness and bounded cross-engine status tracking, but they are not yet comparable to same-engine rewrite-generation rows or support/verifier rows.

## 6. Gaps And Priority Order

| gap | severity | current evidence | next action | why now / why later |
|---|---|---|---|---|
| Calcite HEP final-closure gap | resolved-partial | 10/10 PG-only checker-consistent and speedup-measured evidence on the target denominator; still witness-scale and non-leaderboard | maintain current bounded same-engine evidence line and do not overstate it as transfer or leaderboard evidence | now resolved for same-engine denominator closure; later work should move to transfer closure rather than reopening Calcite denominator work |
| SlabCity substrate / service contract | high | blocked runner_or_service_contract | acquire service/runner contract or stop path | later unless an external runnable contract becomes available |
| GenRewrite no public substrate | high | external discovery found no public runnable substrate | stop path unless new public artifact appears | later because there is no bounded runnable path to deepen now |
| full PORT cross-engine closure | high | bounded 4/6 cross-engine closed subset; `PORT_0012` / `PORT_0013` still PG-route blocked | diagnose/repair `PORT_0012` and `PORT_0013` PG-route dialect blockers | now because the bounded cross-engine closed subset materially improved from 2 to 4 cases and the remaining blockers are narrower dialect/route holdouts |
| SpeedupTransferRate not computed | medium | bounded cross-engine closure improved, but aligned route denominator and target-engine speedup/benefit evidence are still missing | hold until aligned route denominator and target-engine speedup/benefit evidence exist | later because current transfer rows still cannot support a valid transfer metric |
| Plan attribution incomplete | medium | runtime observation snapshots exist but cross-baseline attribution is incomplete | defer until baseline denominator closure is stronger | later because stable baseline evidence should come before broader attribution synthesis |
| RQ4 taxonomy not full closure | medium | taxonomy-related closure remains partial | continue selective deepening after baseline evidence matrix and Calcite HEP preflight | later because current benchmark phase prioritizes consolidation over taxonomy expansion |
| SQLSolver support smoke only 4 pairs | medium | bounded support smoke with verifier_support_rate 3/4 | expand only if broader support denominator is needed | later because support evidence already exists and rewrite-baseline denominator gaps are more pressing |
| VeriEQL positive proof not closed | medium | support-canary / availability evidence with constraint-sensitive positive side still open | deepen VeriEQL support audit only if support table expansion matters | later because VeriEQL is support-only and not on the rewrite speedup critical path |

## 7. Recommended Next Step

`diagnose/repair PORT_0012 and PORT_0013 PG-route dialect blockers`

Same-engine rewrite baseline evidence is now materially stronger, and the bounded PORT cross-engine closed subset improved from two cases to four. The next narrow blocker is the PG-route / dialect holdout pair `PORT_0012` and `PORT_0013`; transfer-oriented metrics such as `SpeedupTransferRate` should remain blocked until that route denominator is better aligned and target-engine speedup evidence exists.

## 8. Non-Modification Note

No experiments were run for this matrix. No DB, checker, speedup, or model/API activity occurred. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were modified. The taxonomy note files remained untouched.
