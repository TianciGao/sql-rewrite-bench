# LEARNED_REWRITE_READINESS_AUDIT_v0

## 1. Executive Summary

This is a tracked scratch readiness audit for the `LEARNED_REWRITE` baseline line.

Current conclusion:

- LearnedRewrite support does not exist in runnable form in this repository.
- No runnable artifacts, checkpoints, or inference wrappers are present.
- No existing adapter, CLI command, or model-call path is present.
- The repository contains a baseline inventory row for `LEARNED_REWRITE`, but not an execution-ready implementation.

Current recommendation:

- treat LearnedRewrite as `subset-only`
- treat it as `not execution-ready`
- do not treat it as a full common-core baseline candidate yet

The practical next step is a no-execution input-readiness scaffold rather than any execution attempt.

## 2. Files / Signals Found

| file or signal | what it indicates | relevance |
|---|---|---|
| `docs/_scratch/baseline_inventory_boss_requirements.csv` | explicit `LEARNED_REWRITE` row exists | repository intends LearnedRewrite as a baseline concept |
| `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md` | Step 5 is the next readiness audit slot | confirms sequencing |
| `docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md` | current completed smoke route is through Step 4b only | LearnedRewrite remains outside the completed smoke path |
| `docs/_scratch/baseline_smoke_common_core_v0.json` | current smoke denominator is a compact PG-native PERF/CONS set plus limited PORT | useful for first compatibility assessment |
| `docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md` | next 35-case human-review slate is dominated by PERF+PORT | useful for high-level subset assessment |
| `docs/_scratch/PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md` | CONS is a compact semantic addendum with Calcite and VeriEQL provenance | useful for consistency-pool risk assessment |
| `scripts/cli.py` | no LearnedRewrite command or adapter path found | no runnable repository integration |
| repo-wide search for `LEARNED_REWRITE`, `LearnedRewrite`, `checkpoint`, `trainer`, `inference`, `torch`, `tensorflow`, `onnx` | only meaningful direct hit is the inventory row | strong signal that implementation is absent |
| repository dependency/artifact scan | no `requirements*.txt`, `pyproject.toml`, `setup.py`, `environment.yml`, `.pt`, `.pth`, `.ckpt`, or `.onnx` files found | no local ML stack or model artifact path |

## 3. Baseline Inventory Finding

| field | value |
|---|---|
| `baseline_id` | `LEARNED_REWRITE` |
| `baseline_method` | `LearnedRewrite / learned query rewrite` |
| `boss_group` | `P1_main_prior_method` |
| `leaderboard_role` | `subset_only_candidate` |
| `token_cost_class` | `None` |
| `common_core_fit` | `Yes for PG/common-core subset after adapter` |
| `subset_only` | `Yes - Calcite-supported SQL and method-supported rules` |
| `environment` | `Java/Calcite, model/checkpoint or training artifacts, statistics/cost model` |
| `source_urls` | `https://pure.bit.edu.cn/en/publications/a-learned-query-rewrite-system-using-monte-carlo-tree-search; https://www.researchgate.net/publication/373966008_A_Learned_Query_Rewrite_System` |
| `notes` | `Run original smoke first; report frozen-transfer vs adapted separately.` |

Current interpretation:

- LearnedRewrite is framed as an important prior-method baseline.
- It is not framed as cross-dialect.
- It is explicitly framed as subset-only and adapter-dependent.
- The inventory assumes external model/checkpoint or training artifacts that are not present in this repository.

Primary blockers:

- no adapter
- no model/checkpoint artifacts
- no inference path
- no dependency path
- no reproducible execution contract in repo

## 4. Dependency / Artifact Readiness

Current repository signals:

- Python dependency support file: none found
- ML framework signal: none found
- checkpoint files: none found
- training entrypoint: none found
- inference entrypoint: none found
- adapter path: none found
- documented runnable artifact URL: none found
- local reproducibility note for LearnedRewrite artifacts: none found
- explicit license note for LearnedRewrite artifacts: none found

Interpretation:

- the repository has a baseline inventory row
- it does not have a runnable LearnedRewrite artifact stack
- execution is blocked before any benchmark-scaffold question about SQL behavior can even start

## 5. Current 9-Case Compatibility Assessment

Current PG-native 9-case smoke set:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

| case_id | pool | likely LearnedRewrite input risk | likely usefulness | reason | recommended inclusion status |
|---|---|---|---|---|---|
| `PERF_0006` | PERF | medium | medium | simple TPC-H aggregate/reporting query; plausible first subset input if adapter exists | candidate |
| `PERF_0008` | PERF | medium | medium | classic join/aggregate/order/limit shape; likely usable if raw SQL can be normalized into expected form | candidate |
| `PERF_0013` | PERF | high | medium | interval year syntax introduces dialect and canonicalization risk | maybe |
| `PERF_0017` | PERF | high | medium | interval month syntax plus grouped reporting and limit adds normalization risk | maybe |
| `PERF_0024` | PERF | high | high | correlated nested subqueries are interesting but likely require stronger canonical form and schema/statistics support | maybe |
| `PERF_0033` | PERF | medium | medium | TPC-DS analytical shape is plausible, but input representation assumptions are unknown | candidate |
| `PERF_0054` | PERF | medium | medium | straightforward TPC-DS join/aggregate/order/limit case; good bounded candidate if adapter exists | candidate |
| `CONS_0007` | CONS | high | high | Calcite-derived correlated `EXISTS`; semantically valuable but likely representation-sensitive | maybe |
| `CONS_0012` | CONS | high | high | Calcite-derived `LIMIT/OFFSET` correlated case; useful but likely sensitive to method assumptions | maybe |

Assessment:

- LearnedRewrite likely expects more than raw SQL alone.
- The inventory explicitly says the method expects SQL plus schema/statistics plus rule set.
- It may also assume Calcite-style canonical representation or rule-application context.
- PostgreSQL SQL emission is unproven in this repository.

## 6. 35-Case High-Level Compatibility

High-level interpretation only:

- `PERF` is the most likely compatible pool for a first bounded subset.
- `CONS` is potentially valuable but higher-risk because semantic and decorrelation-heavy cases may depend more heavily on canonical form and method-specific rule assumptions.
- `PORT` is a weak near-term fit because the inventory already marks LearnedRewrite as not cross-dialect.
- `LONGTAIL` is high risk because it is structurally varied and not a good first subset for an adapter-missing learned baseline.

Would LearnedRewrite likely run across all 35 next human-review cases now?

- no

Current classification:

- subset-only candidate
- not a full 35-case route candidate
- not a full common-core baseline candidate at current repository maturity

## 7. Blocker List

- model/checkpoint artifacts are missing
- no training/inference wrapper exists in the repository
- no Java/Calcite adapter path exists in the repository for this method
- the inventory implies schema/statistics/rule-set inputs that the current smoke scaffold does not provide for LearnedRewrite
- raw SQL vs canonical representation mismatch is unresolved
- Calcite-subset assumptions are likely
- output SQL dialect behavior is unproven
- reproducibility path is missing
- artifact/license/freeze path is missing
- subset denominator risk is high
- no evidence exists that the original method transfers cleanly to the current PG-native smoke denominator without adaptation

## 8. Recommendation

Recommendation:

- `subset-only, not execution-ready`

Interpretation:

- do not treat LearnedRewrite as a full common-core baseline candidate now
- do not attempt execution
- do not defer all structure work either
- keep it in the route as a bounded future prior-method line that first needs a no-execution readiness scaffold

## 9. Next Action

- implement a no-execution LearnedRewrite input-readiness scaffold

## 10. Verification / Non-Modification Note

This audit was read-only.

- files modified: none
- files created by the audit itself: none
- database workloads run: no
- LLM calls: no
- dependency installs/downloads: no
- registry updates: no
- `docs/EXECUTION_STATUS.md` changes: no
- formal review file changes: no
- taxonomy calibration notes touched: no

The audit conclusions here are readiness-layer only. They are not execution evidence, not correctness evidence, not speedup evidence, and not leaderboard evidence.
