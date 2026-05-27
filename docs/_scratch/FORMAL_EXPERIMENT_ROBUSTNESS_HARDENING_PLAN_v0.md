# FORMAL_EXPERIMENT_ROBUSTNESS_HARDENING_PLAN_v0

## 1. Status

This is a tracked scratch hardening plan for the current formal experiment packet.

Its purpose is to classify current results by paper-readiness level and define the closure work required before final paper claims.

It is not a new experiment result.

## 2. Current Completed Result Inventory

Current completed or formalized result lines:

- formal common-core control execution and checker-backed scoring
- SQLGlot same-dialect formal execution and scoring snapshot
- Direct LLM rewrite formal execution and scoring snapshot
- formal common-core method plan collection for SQLGlot and Direct LLM
- formal common-core plan parse summary
- formal common-core plan operator-delta preflight
- formal common-core plan operator-delta summary
- formal common-core runtime observation snapshot
- HUMAN_REFERENCE_POSITIVE PERF-only formal speedup run
- SQLGlot PERF-only exploratory row-count-gated speedup appendix
- Direct LLM PERF-only exploratory row-count-gated speedup appendix
- formal PORT current results snapshot
- paper experiment dashboard and rollup notes

## 3. Main-Paper Eligible Results

The following are currently strong enough for main-paper reporting, with bounded wording:

### RQ1

- control-route correctness / validity results
- checker-backed control scoring:
  - `result_consistency_rate_observed_existing_artifacts=1.0`
  - `negative_rejection_rate_observed_existing_artifacts=1.0`
  - `false_accept_rate_observed_existing_artifacts=0.0`

### RQ2

- plan observability readiness across common-core:
  - control plans parseable `9 / 9`
  - SQLGlot method plans parseable `9 / 9`
  - Direct LLM method plans parseable `9 / 9`
  - source-paired plan readiness `9 / 9`
- lightweight operator-delta observation:
  - source-positive top-node changes `2`
  - source-negative top-node changes `2`
  - source-SQLGlot top-node changes `0`
  - source-LLM top-node changes `1`
- HUMAN_REFERENCE_POSITIVE PERF-only positive-control speedup:
  - `GM_Speedup=0.96159127168004`
  - `Win/Tie/Loss=1/2/4`
  - `RegressionRate@20%=0/7`

### RQ3

- bounded current PORT snapshot:
  - SQLGlot Transpile preflight `3 / 3`, PG execution `2 / 3`
  - LLM Translate clean subset `2 / 2`
  - `PORT_0012` documented holdout / failure-analysis case

Main-paper caveat:

- RQ3 is eligible only as a bounded current-status portability snapshot, not as full portability closure

## 4. Appendix-Only Exploratory Results

The following should remain appendix-only unless stronger gating artifacts are built:

- SQLGlot PERF-only exploratory row-count-gated speedup appendix
  - `GM=0.9709643241218479`
  - `WTL=1/2/4`
  - `RegressionRate@20%=0/7`
- Direct LLM PERF-only exploratory row-count-gated speedup appendix
  - `GM=1.0023345046000625`
  - `WTL=1/5/1`
  - `RegressionRate@20%=0/7`
  - `total_token_usage=4487`

Reason:

- both method routes still lack route-specific checker-backed consistency
- current admission to speedup is row-count-gated only
- these results are useful as appendix evidence, not as correctness-gated leaderboard claims

## 5. Not-Yet-Claimable Results

The following are not ready for final paper claims:

- correctness-gated SQLGlot method consistency
- correctness-gated Direct LLM method consistency
- correctness-gated generated-method leaderboard speedup
- generated-method `GM_Speedup` comparisons in main text
- plan attribution / operator-causal explanation
- full portability closure across a stable PORT denominator
- RQ4 taxonomy / failure-slicing conclusions

## 6. Robustness Gaps By RQ

### RQ1

- missing route-specific checker-backed consistency for SQLGlot
- missing route-specific checker-backed consistency for Direct LLM
- current row-count agreement is insufficient for semantic correctness claims

### RQ2

- operator-delta exists only as observation, not attribution
- generated-method speedup is not correctness-gated
- runtime policy is frozen for the first pass, but generated-method leaderboard eligibility is still blocked by consistency gaps

### RQ3

- current clean denominator is only `PORT_0004` and `PORT_0022`
- `PORT_0012` remains unresolved and keeps the line from full closure
- cross-engine / cross-dialect consistency is not yet formalized as a closed result packet

### RQ4

- taxonomy and failure slicing are still future work
- no consolidated robustness / failure-family table exists yet

## 7. Required Hardening Actions

Required before stronger paper claims:

1. Build method-specific checker-backed consistency preflight for SQLGlot and Direct LLM.
2. If viable, build route-specific checker-backed consistency artifacts for SQLGlot.
3. If viable, build route-specific checker-backed consistency artifacts for Direct LLM.
4. Reclassify SQLGlot and Direct LLM from row-count-only execution evidence to checker-backed method validity where supported.
5. Decide whether generated-method speedup can move from appendix-only to correctness-gated leaderboard reporting.
6. Separate operator-delta observation from any future attribution layer with its own protocol.
7. Decide whether `PORT_0012` gets a targeted follow-up run or remains an explicit holdout in the first paper packet.
8. Build at least a first bounded RQ4 failure-slicing summary so coverage / failure discussion is not entirely deferred.

## 8. Priority Order

Priority order for hardening:

1. method-specific checker-backed consistency preflight for SQLGlot and Direct LLM
2. route-specific checker-backed consistency artifact construction, if the preflight says it is feasible
3. re-evaluate generated-method leaderboard speedup eligibility after consistency closure
4. targeted PORT denominator decision around `PORT_0012`
5. operator-delta summary / attribution design separation
6. first bounded RQ4 failure-slicing packet

## 9. Next Concrete Task

- implement method-specific checker-backed consistency preflight for SQLGlot and Direct LLM

## 10. Working Claim Boundary

Until the above hardening closes:

- control-route correctness is strong enough for main-paper use
- HUMAN_REFERENCE_POSITIVE PERF-only speedup is strong enough as a bounded positive-control result
- SQLGlot and Direct LLM speedup remain appendix-only exploratory material
- SQLGlot and Direct LLM row-count match is not semantic equivalence
- no final generated-method leaderboard claim should be made
- no registry or formal review update should be tied to these scratch materials
