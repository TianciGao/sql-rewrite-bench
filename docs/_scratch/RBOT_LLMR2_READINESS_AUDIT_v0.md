# RBOT_LLMR2_READINESS_AUDIT_v0

## 1. Executive Summary

This is a tracked scratch readiness audit for `R_BOT` and `LLM_R2`.

Current conclusion:

- R-Bot / LLM-R2 support does not exist in runnable form in this repository.
- Retrieval/demo/rule-pool infrastructure does not exist in the repository.
- The repository has reusable direct-LLM prompt/call scaffolding, but it does not have:
  - a retrieval module
  - a demo selector
  - a rule pool
  - a rerank path
  - a retrieval or demo reproducibility contract
- `R_BOT` and `LLM_R2` are not execution-ready.

Current recommendation:

- treat them as retrieval-dependent appendix / subset-only candidates
- do not treat them as main baseline candidates now
- next action should be a no-execution retrieval-readiness scaffold

## 2. Files / Signals Found

| file path or signal | what it indicates | relevance to readiness |
| --- | --- | --- |
| `docs/_scratch/baseline_inventory_boss_requirements.csv` | explicit inventory rows exist for `R_BOT` and `LLM_R2` | repository intends both as conceptual candidate baselines |
| `docs/_scratch/BASELINE_SMOKE_PLAN_COMMON_CORE_v0.md` | `R_BOT` and `LLM_R2` were explicitly excluded from first smoke | confirms they are not first-wave runnable baselines |
| `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md` | Step 7 is still not started and is framed as retrieval/demo/rule-pool dependent | current route posture |
| `scripts/cli.py` | direct LLM rewrite/translate prompt, call, extraction, token logging, and reporting paths exist | reusable substrate for future scaffolding |
| repo-wide search for `R_BOT`, `LLM_R2`, `retrieval`, `demo`, `rule pool`, `embedding`, `rerank` | no runnable module or command beyond inventory and scratch docs | strong blocker signal |
| dependency/index scan | no dependency file, vector index, retrieval artifact, or serialized store was found | no retrieval/runtime artifact path |

## 3. Baseline Inventory Finding

### `R_BOT`

| field | value |
| --- | --- |
| `baseline_id` | `R_BOT` |
| `baseline_method` | `R-Bot` |
| `boss_group` | `P1_frontier_exception` |
| `leaderboard_role` | `subset_only_candidate` |
| `token_cost_class` | `High` |
| `common_core_fit` | `PG/common-core subset first` |
| `subset_only` | `Yes - depends on original KB/rules and SQL subset` |
| `environment / dependency notes` | `LLM API, RAG index/KB, CalciteRewrite components, original repo env` |
| `source_urls / citation notes` | `https://dblp.org/rec/journals/corr/abs-2412-01661; https://www.researchgate.net/publication/395559470_R-Bot_An_LLM-Based_Query_Rewrite_System` |
| current interpretation | retrieval-dependent frontier LLM rewrite candidate; potentially useful only if original knowledge base, rules, and retrieval environment can be reproduced |
| blockers | no RAG index/KB, no CalciteRewrite components, no retrieval policy, no demo/rule isolation policy, no adapter |

Inventory note:

- do not let the retrieval index contain test positive rewrites

### `LLM_R2`

| field | value |
| --- | --- |
| `baseline_id` | `LLM_R2` |
| `baseline_method` | `LLM-R2` |
| `boss_group` | `P1_frontier_exception` |
| `leaderboard_role` | `subset_only_candidate` |
| `token_cost_class` | `Medium-High` |
| `common_core_fit` | `Subset/dev-only adaptation possible` |
| `subset_only` | `Yes - rules/demonstrations supported subset` |
| `environment / dependency notes` | `LLM API, demonstration pool, rule applier, possible embedding/contrastive model` |
| `source_urls / citation notes` | `https://huggingface.co/papers/2404.12872` |
| current interpretation | LLM-guided rule-selection candidate for a supported subset only |
| blockers | no demonstration pool, no rule applier, no demo policy, no contrastive or embedding path, no adapter |

Inventory note:

- separate original-demo and repo-dev-demo settings

## 4. Dependency / Retrieval / Cost Readiness

- LLM client path present: yes
  - existing direct LLM routes already handle prompt construction, endpoint configuration, model-call capture, extraction, and token logging
- prompt infrastructure reusable: yes, partially
  - reusable:
    - prompt package construction
    - provider/base-URL handling
    - model-call capture
    - token logging
    - per-case and rollup reporting
- retrieval index present: no
- demo corpus present: no
- rule pool present: no
- embedding/vector dependency present: no
- rerank policy present: no
- demo count / retrieval count frozen: no
- pricing snapshot frozen: no
- artifact / license / reproducibility signals: weak
  - only paper/source URLs are present in inventory
  - no local reproducibility packet, retrieval corpus contract, or artifact freeze exists

Bottom line:

- the repository can support direct LLM baselines
- the repository cannot currently support retrieval-based or demo/rule-pool baselines

## 5. Current 9-Case Compatibility Table

| case_id | pool | likely input risk | likely usefulness | likely retrieval/cost risk | reason | recommended inclusion status |
| --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | performance | low | medium | medium | clean TPC-H aggregate/reporting case; retrieval likely unnecessary but bounded | candidate |
| `PERF_0008` | performance | low | medium | medium | straightforward join/aggregate/order/limit case | candidate |
| `PERF_0013` | performance | medium | medium | medium | interval-year syntax adds normalization pressure to retrieved example/rule matching | maybe |
| `PERF_0017` | performance | medium | medium | medium | interval-month grouped reporting is plausible but less clean for first retrieval scaffolding | maybe |
| `PERF_0024` | performance | medium | high | high | correlated nested subqueries raise both potential value and retrieval-selection cost risk | maybe |
| `PERF_0033` | performance | low | medium | medium | clean TPC-DS aggregate/order/limit shape; good bounded candidate | candidate |
| `PERF_0054` | performance | low | medium | medium | clean TPC-DS join/aggregate/order/limit shape | candidate |
| `CONS_0007` | consistency | medium | high | high | correlated `EXISTS` case could benefit from rule/example retrieval, but fairness and reproducibility are harder | maybe |
| `CONS_0012` | consistency | medium | high | high | `LIMIT` / `OFFSET` threshold semantics are useful later, but demo/rule choice sensitivity is high | maybe |

Interpretation:

- likely prompt/input compatibility is strongest on cleaner PERF analytical cases
- retrieval demos would likely be needed for any meaningful R-Bot / LLM-R2 route
- schema/context is likely required
- PostgreSQL SQL emission is plausible through reused direct LLM infrastructure, but is not established for retrieval/rule-pool methods

## 6. PORT / Translation-Route Assessment

High-level interpretation:

- R-Bot / LLM-R2 should not start as first-wave PORT translation baselines
- they are more naturally retrieval-based rewrite or repair methods than minimal translation baselines
- `PORT_0012` is a useful later retrieval/repair stress case because it already has a known failure-analysis role
- they should wait until the simpler direct LLM translate route is more stable and frozen as the denominator

Practical recommendation:

- first use should be same-dialect rewrite, not translation
- later use could include translation repair or failure analysis
- do not mix retrieval-based methods into the clean PORT 2-case canary subset yet

## 7. 35-Case High-Level Compatibility

High-level only:

- `PERF`: best fit
  - especially cleaner TPC-H and TPC-DS analytical cases
- `CONS`: possible but higher-risk
  - retrieval/rule selection may help, but fairness and reproducibility are harder
- `PORT`: later-stage fit
  - more useful as example-based repair or translation stress, not a first-wave denominator
- `LONGTAIL`: high risk
  - structure diversity raises retrieval and demo-selection instability

Current conclusion:

- R-Bot / LLM-R2 are subset-only in practice
- they are retrieval-dependent appendix candidates in governance terms
- they are not full 35-case baseline routes now

## 8. Risk / Blocker List

- retrieval corpus missing
- demo selection reproducibility is undefined
- rule pool missing
- embedding/vector index missing
- rerank policy missing
- multi-call cost
- prompt freeze missing
- pricing snapshot not frozen
- third-party endpoint reproducibility concern
- fair comparison against direct LLM baseline is not yet defined
- subset denominator risk
- no retrieval contamination policy beyond the inventory note
- no frozen demo-count / retrieval-count / retry policy

## 9. Recommendation

Current recommendation:

- retrieval-dependent appendix / subset-only candidate
- not execution-ready
- not a main baseline candidate now

This route should not be treated as runnable baseline infrastructure at the current repository state.

## 10. Next Action

- implement a no-execution retrieval-readiness scaffold

## 11. Verification / Non-Modification Note

- files modified: none during the audit
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
- `ls -1`
- repo-wide `rg` searches for:
  - `R_BOT`
  - `LLM_R2`
  - retrieval
  - demo
  - rule pool
  - embedding
  - rerank
- dependency/index scan for:
  - `requirements*.txt`
  - `pyproject.toml`
  - `setup.py`
  - `environment.yml`
  - `.faiss`
  - `.index`
  - `.pkl`
- read-only inspection of:
  - `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
  - `docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md`
  - `docs/_scratch/BASELINE_SMOKE_PLAN_COMMON_CORE_v0.md`
  - `docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md`
  - `docs/_scratch/PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md`
  - `docs/_scratch/baseline_inventory_boss_requirements.csv`
  - `inventory/case_registry.csv`
  - `scripts/cli.py`

This document is a scratch readiness note only. It is not:

- a registry writeback
- an admission decision
- a leaderboard claim
- a correctness scoring artifact
- a speedup scoring artifact
- a formal review update
