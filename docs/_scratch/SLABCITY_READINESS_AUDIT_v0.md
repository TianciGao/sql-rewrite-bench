# SLABCITY_READINESS_AUDIT_v0

## 1. Executive Summary

This is a tracked scratch readiness audit for `SLABCITY`.

Current conclusion:

- SlabCity support does not exist in runnable form in this repository.
- The repository has no SlabCity runner, adapter, CLI command, API wrapper, or service integration.
- The only concrete signal is the `SLABCITY` inventory row in `docs/_scratch/baseline_inventory_boss_requirements.csv`.
- The inventory frames SlabCity as a synthesis-based frontier exception, not as a currently runnable local baseline.
- SlabCity is not execution-ready in this repository.

Current recommendation:

- defer SlabCity
- do not treat it as a runnable main baseline candidate now
- keep it deferred until a runnable local adapter or a reproducible service/runtime contract exists

## 2. Files / Signals Found

| file path or signal | what it indicates | relevance to readiness |
| --- | --- | --- |
| `docs/_scratch/baseline_inventory_boss_requirements.csv` | explicit `SLABCITY` row exists | repository intends SlabCity as a conceptual frontier candidate |
| `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md` | Step 8 is still not started and already labeled a frontier exception line | current governance posture |
| `docs/_scratch/BASELINE_SMOKE_PLAN_COMMON_CORE_v0.md` | `SLABCITY` is explicitly excluded from first smoke | confirms it was never considered first-wave runnable |
| repo-wide search for `SLABCITY`, `SlabCity`, `synthesis`, `solver`, `service`, `external API` | no SlabCity-specific code or integration found | strong blocker |
| `scripts/cli.py` | no SlabCity command or adapter path exists | no local execution route |
| dependency scan | no `requirements*.txt`, `pyproject.toml`, `setup.py`, or `environment.yml` found | no declared local runtime path |

## 3. Inventory Finding

| field | value |
| --- | --- |
| `baseline_id` | `SLABCITY` |
| `baseline_method` | `SlabCity` |
| `category` | `Program synthesis rewrite` |
| `representative_role` | `Representative synthesis-based whole-query optimization method` |
| `input_output` | `Input: SQL + schema/constraints + synthesizer config; Output: equivalent/faster SQL candidates` |
| `pg` | `Likely original backend/subset; verify` |
| `mysql` | `No/unknown` |
| `spark` | `No/unknown` |
| `cross_dialect` | `No` |
| `environment` | `Synthesis engine, verifier/solver, likely specific DB runtime and workload setup` |
| `common_core_fit` | `Subset only; start PG common-core smoke` |
| `subset_only` | `Yes - synthesis-supported SQL subset and timeouts` |
| `token_cost_class` | `None` |
| `recommended_use` | `Main if boss allows representative exception; otherwise appendix` |
| `boss_group` | `P1_frontier_exception` |
| `leaderboard_role` | `subset_only_candidate` |
| `source_urls` | `https://par.nsf.gov/biblio/10451715-slabcity-whole-query-optimization-using-program-synthesis; https://www.researchgate.net/scientific-contributions/Xinyu-Wang-2242296732` |

Interpretation:

- SlabCity is present as a frontier exception baseline concept only.
- The inventory already suggests subset-only operation and likely dependence on a specific backend/runtime.
- There is no evidence in this repository that the required synthesis engine, verifier/solver stack, or runtime contract has been integrated.

## 4. Dependency / Service / Artifact Readiness

- SlabCity runner present: no
- CLI command present: no
- API wrapper present: no
- external service integration present: no
- synthesis engine present: no
- verifier/solver integration present: no
- proprietary artifact path present: no explicit local artifact
- hosted benchmark / remote execution contract present: no
- reproducible local contract present: no
- dependency files present: no

Interpretation:

- the inventory implies a specialized synthesis stack
- the repository does not contain that stack
- if SlabCity depends on remote or hosted setup, that dependency is not documented here in a reproducible repo-local way

## 5. Compatibility With Current 9-Case And PORT Route

High-level only, without execution:

Current PG-native 9-case set:

- cleaner PERF cases such as `PERF_0006`, `PERF_0008`, `PERF_0033`, and `PERF_0054` would be the only plausible first candidates if a local synthesis adapter existed
- `PERF_0013` and `PERF_0017` add interval-syntax risk
- `PERF_0024` adds nested correlated-subquery complexity
- `CONS_0007` and `CONS_0012` are semantically interesting but likely verifier-sensitive
- the repository has no synthesis/verifier layer to test any of this

PORT route:

- `PORT_0004`, `PORT_0012`, and `PORT_0022` are poor early SlabCity targets
- the inventory already says `cross_dialect = No`
- `PORT_0012` is currently a failure-analysis case, not a clean denominator candidate for a missing synthesis stack
- SlabCity should not be treated as a translation-route method here

Current conclusion:

- at best, SlabCity would be a PG-only subset method if a local adapter existed
- today, no compatibility claim should be operationalized because there is no runnable path

## 6. 35-Case High-Level Compatibility

High-level assessment:

- `PERF`: best hypothetical fit
- `CONS`: possible but high risk due to verifier/semantic sensitivity
- `PORT`: weak fit
- `LONGTAIL`: high risk

Current conclusion:

- SlabCity is subset-only in principle
- SlabCity is a frontier exception in governance terms
- SlabCity should be treated as deferred in practice

## 7. Risks / Blockers

- synthesis engine missing
- verifier / solver integration missing
- likely specific DB/runtime setup missing
- no local adapter
- no reproducible service/runtime contract
- no dependency or environment file
- citation gate risk is already flagged in inventory
- subset denominator risk
- no cross-dialect support
- fairness against completed baselines is undefined without a runnable local contract

## 8. Recommendation

Current recommendation:

- defer SlabCity

Reason:

- it is a frontier exception only in inventory
- there is no runnable local adapter
- there is no reproducible service/runtime contract in the repository
- it is not reasonable to advance beyond audit state without that missing substrate

## 9. Next Action

- keep SlabCity deferred until a runnable local adapter or reproducible service contract exists

## 10. Verification / Non-Modification Note

- files modified during the audit: none
- files created during the audit: none
- database workloads run: no
- LLM calls: no
- dependency installs/downloads: no
- registry changed: no
- `docs/EXECUTION_STATUS.md` changed: no
- formal review files changed: no
- taxonomy calibration notes touched: no

Read-only commands used for the audit included:

- `pwd`
- `git status --short`
- repo-wide `rg` searches for:
  - `SLABCITY`
  - `SlabCity`
  - synthesis
  - solver
  - service
  - external API
- dependency scan for:
  - `requirements*.txt`
  - `pyproject.toml`
  - `setup.py`
  - `environment.yml`
- read-only inspection of:
  - `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
  - `docs/_scratch/BASELINE_SMOKE_PLAN_COMMON_CORE_v0.md`
  - `docs/_scratch/baseline_inventory_boss_requirements.csv`
  - `docs/PROJECT_PLAN.md`
  - `docs/EXECUTION_STATUS.md`
  - `benchmark_spec/decision_log.md`
  - `inventory/case_registry.csv`
  - `scripts/cli.py`
  - representative SQL from `PERF_0024`, `CONS_0012`, and `PORT_0012`

This document is a scratch readiness note only. It is not:

- a registry writeback
- an admission decision
- a leaderboard claim
- a correctness scoring artifact
- a speedup scoring artifact
- a formal review update
