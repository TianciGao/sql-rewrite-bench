# GENREWRITE_READINESS_AUDIT_v0

## 1. Executive Summary

This is a tracked scratch readiness audit for the `GENREWRITE` baseline line.

Current conclusion:

- GenRewrite support does not exist in runnable form in this repository.
- No correction-loop implementation, verifier loop, rerank path, or executor-feedback loop is present.
- No GenRewrite-specific prompt/rule library, retry policy, or correction budget contract is present.
- Existing direct LLM rewrite/translate scaffolding is reusable in part, but it is not sufficient to claim GenRewrite readiness.

Current recommendation:

- treat GenRewrite as a `frontier appendix / subset-only candidate`
- treat it as `not execution-ready`
- do not treat it as a full common-core baseline candidate yet

The practical next step is a no-execution input/cost-readiness scaffold rather than any execution attempt.

## 2. Files / Signals Found

| file or signal | what it indicates | relevance |
|---|---|---|
| `docs/_scratch/baseline_inventory_boss_requirements.csv` | explicit `GENREWRITE` row exists | repository intends GenRewrite as a candidate baseline concept |
| `docs/_scratch/BASELINE_SMOKE_PLAN_COMMON_CORE_v0.md` | `GENREWRITE` was explicitly excluded from the first smoke | confirms it is not part of the current runnable first-wave route |
| `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md` | Step 6 is the next route after LearnedRewrite | confirms sequencing |
| `scripts/cli.py` direct LLM rewrite/translate paths | direct prompt, model-call, extraction, and token logging infrastructure exists | partial substrate is reusable |
| `scripts/cli.py` | no `GENREWRITE` command, no correction loop, no verifier/rerank loop, no retry-budget logic | main implementation gap |
| repo-wide search for `GENREWRITE`, `correction loop`, `repair loop`, `self-correction`, `verifier`, `rerank`, `n-best`, `execution feedback` | only meaningful GenRewrite hit is the inventory row and scratch plan docs | strong signal that runnable machinery is absent |
| repository dependency scan | no `requirements*.txt`, `pyproject.toml`, `setup.py`, or `environment.yml` found | no declared dependency/runtime path for a GenRewrite stack |

## 3. Baseline Inventory Finding

| field | value |
|---|---|
| `baseline_id` | `GENREWRITE` |
| `baseline_method` | `GenRewrite` |
| `boss_group` | `P1_frontier_exception` |
| `leaderboard_role` | `subset_only_candidate` |
| `token_cost_class` | `High` |
| `common_core_fit` | `Yes for LLM-compatible common-core after fixed budget` |
| `subset_only` | `No in principle, but practical parser/checker failures expected` |
| `environment` | `LLM API/local LLM, prompt/rule library, checker feedback loop, token logging` |
| `source_urls` | `https://huggingface.co/papers/2403.09060; https://summarxiv.com/en/paper/2403.09060` |
| `notes` | `Must cap correction rounds fairly.` |

Current interpretation:

- GenRewrite is framed as a representative LLM rewrite method with a correction loop.
- It is treated as a frontier exception and not as a simple first-wave baseline.
- It assumes multiple pieces of control infrastructure that do not currently exist in this repository.

Primary blockers:

- no correction-loop implementation
- no verifier/checker feedback integration for iterative repair
- no retry/sample policy
- no frozen prompt/rule library
- no explicit correction-round cap
- no cost/fairness contract for multi-round LLM use

## 4. Dependency / API / Cost Readiness

Current repository signals:

- LLM client path: present via existing direct LLM baseline code
- prompt infrastructure: partially reusable
- correction-loop infrastructure: absent
- verifier/executor feedback loop: absent for GenRewrite
- rerank / n-best path: absent
- retry/sample policy: absent
- pricing snapshot freeze: absent
- dependency file: none found
- reproducibility note for GenRewrite execution: none found
- local rule library or natural-language rule set: none found
- explicit artifact/license packet for GenRewrite: none found

Interpretation:

- the repository can already run single-call direct LLM baselines
- it cannot yet run a fair, reproducible, bounded correction-loop baseline
- the missing issue is not just API access, but the policy/control layer around iterative generation

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

| case_id | pool | likely GenRewrite input risk | likely usefulness | likely cost risk | reason | recommended inclusion status |
|---|---|---|---|---|---|---|
| `PERF_0006` | PERF | low | medium | medium | simple TPC-H aggregate/reporting shape; existing direct LLM prompt path already fits this structure | candidate |
| `PERF_0008` | PERF | low | medium | medium | clean join/aggregate/order/limit shape; good bounded candidate for a later first canary | candidate |
| `PERF_0013` | PERF | medium | medium | medium | interval year syntax raises parser/normalization risk for a correction loop | maybe |
| `PERF_0017` | PERF | medium | medium | medium | interval month syntax plus grouped reporting makes iterative repair less clean | maybe |
| `PERF_0024` | PERF | medium | high | high | correlated nested subqueries increase both usefulness and likely correction cost | maybe |
| `PERF_0033` | PERF | low | medium | medium | clean TPC-DS aggregate/order/limit case; good bounded analytical candidate | candidate |
| `PERF_0054` | PERF | low | medium | medium | clean TPC-DS join/aggregate/order/limit case; good bounded analytical candidate | candidate |
| `CONS_0007` | CONS | medium | high | high | semantically interesting correlated `EXISTS`; valuable later but not ideal for first correction-loop fairness | maybe |
| `CONS_0012` | CONS | medium | high | high | `LIMIT/OFFSET` threshold semantics are useful, but likely checker-sensitive and costlier | maybe |

Assessment:

- prompt/input compatibility is best on the cleaner PERF analytical cases
- existing direct LLM prompt infrastructure is reusable
- GenRewrite would still need rule/correction/checker budget controls that the repo does not yet have

## 6. PORT / Translation-Route Assessment

High-level interpretation:

- GenRewrite should not start as a general PORT translation baseline.
- It is more naturally aligned with same-dialect rewrite or later repair-loop work than with first-wave translation.
- `PORT_0012` is a useful later repair-loop stress case because SQLGlot transpile already exposed an execution-layer failure there.
- Even so, PORT repair should wait until the simpler direct LLM translate route is considered stable enough as a denominator.

Current route fit:

- not first-wave translation baseline
- potentially useful later for failed translation repair
- potentially useful later for verifier/executor-feedback repair on hard cases

## 7. 35-Case High-Level Compatibility

High-level interpretation only:

- `PERF` is the strongest likely pool for an early bounded GenRewrite subset.
- `CONS` is plausible but higher-risk because semantic edge cases are more likely to require stronger checker and repair policy.
- `PORT` is a later-stage fit, especially for repair-loop analysis rather than first-pass translation.
- `LONGTAIL` is high risk because structure diversity and likely cost blow-up make it a poor initial denominator.

Would GenRewrite likely run across all 35 next human-review cases now?

- no

Current classification:

- subset-only candidate in practice
- frontier appendix candidate in governance terms
- not a full 35-case route candidate at current repository maturity

## 8. Risk / Blocker List

- multi-call cost
- correction-loop reproducibility
- prompt freeze is missing
- natural-language rule library is missing
- retry/sample policy is missing
- correction-round cap is missing
- verifier/executor feedback infrastructure is missing
- output SQL validation policy for iterative repair is missing
- result-checker integration into a repair loop is missing
- subset denominator risk
- pricing snapshot is not frozen
- third-party endpoint reproducibility concern applies to LLM routes
- no `n-best` / rerank path exists
- no fair comparison contract against simpler direct LLM baselines exists yet

## 9. Recommendation

Recommendation:

- `frontier appendix / subset-only candidate, not execution-ready`

Interpretation:

- do not treat GenRewrite as a full common-core baseline candidate now
- do not attempt execution
- keep it in the route as a bounded frontier prior-method line
- first add a no-execution readiness scaffold that makes cost and correction controls explicit

## 10. Next Action

- implement a no-execution GenRewrite input/cost-readiness scaffold

## 11. Verification / Non-Modification Note

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
