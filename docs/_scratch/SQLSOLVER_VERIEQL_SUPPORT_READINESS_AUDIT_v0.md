# SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0

## 1. Executive Summary

This is a tracked scratch readiness audit for SQLSolver / VeriEQL support analysis.

SQLSolver and VeriEQL should be treated as support analysis tools, not as main leaderboard baselines and not as speedup routes.

Current audit conclusion:

- SQLSolver / VeriEQL support does not exist in runnable form in this repository.
- No solver/equivalence-checker runner, adapter, CLI command, or wrapper was found.
- No local Z3 / SMT / CVC5 dependency path or solver artifact path was found.
- The baseline inventory frames both tools as `support_only`.
- Both tools are subset-only in practice and are not execution-ready in this repo.

Recommended posture:

- support-only / subset-only verifier
- not execution-ready
- bounded correctness / semantic-stress / failure-analysis use only after a local support path exists

## 2. Files / Signals Found

| file path or signal | what it indicates | relevance to readiness |
|---|---|---|
| `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md` | Step 9 is a support / analysis line, not a main leaderboard route | sets intended route role |
| `docs/_scratch/baseline_inventory_boss_requirements.csv` | explicit `SQLSOLVER_SUPPORT` and `VERIEQL_SUPPORT` rows exist | strongest source-of-truth signal |
| repo search for `SQLSOLVER`, `VeriEQL`, `Z3`, `CVC5`, `SMT`, `equivalence`, `counterexample`, `verifier` | no runnable solver/verifier toolchain found | main blocker signal |
| `scripts/cli.py` | no SQLSolver / VeriEQL command or adapter path | no local execution entrypoint |
| `cases/**/validation/checker.yaml` patterns | checker-oriented case artifacts exist | adjacent support context, but not a symbolic solver stack |
| dependency scan | no `requirements*.txt`, `pyproject.toml`, `setup.py`, `environment.yml`, or solver artifacts found | no local solver runtime contract |

## 3. Baseline Inventory Finding

### `SQLSOLVER_SUPPORT`

| field | value |
|---|---|
| `baseline_id` | `SQLSOLVER_SUPPORT` |
| `baseline_method` | `SQLSolver support analysis` |
| `boss_group` | `P2_support_or_secondary` |
| `leaderboard_role` | `support_only` |
| `token_cost_class` | `None` |
| `common_core_fit` | `Subset support analysis` |
| `subset_only` | `Yes - prover-supported SQL fragment` |
| `environment` | `Ubuntu, Java 17, Gradle, Z3/ANTLR as repo requirements` |
| `source_urls` | `https://github.com/SJTU-IPADS/SQLSolver; https://www.researchgate.net/publication/376475433_Proving_Query_Equivalence_Using_Linear_Integer_Arithmetic` |
| current interpretation | formal verifier support metric for subset analysis, not speedup leaderboard |
| blockers | no local runner, no Java/Gradle/Z3 stack, no wrapper, no subset/timeout implementation |

Inventory note:

- report `VerifierSupportRate`, `UnknownRate`, and `TimeoutRate`

### `VERIEQL_SUPPORT`

| field | value |
|---|---|
| `baseline_id` | `VERIEQL_SUPPORT` |
| `baseline_method` | `VeriEQL support analysis` |
| `boss_group` | `P2_support_or_secondary` |
| `leaderboard_role` | `support_only` |
| `token_cost_class` | `None` |
| `common_core_fit` | `Subset support analysis` |
| `subset_only` | `Yes - bounded SQL/features supported` |
| `environment` | `Verifier tool, constraint/bound setup, likely solver stack` |
| `source_urls` | ResearchGate citation links in inventory |
| current interpretation | bounded verifier support / appendix-style correctness aid |
| blockers | no local verifier toolchain, no constraint setup, no wrapper, no bounded-support contract in repo |

Inventory note:

- useful for correctness claim even if not cited `20+`

## 4. Dependency / Solver Readiness

- solver dependencies present: no
- equivalence checker wrapper present: no
- symbolic execution path present: no
- schema / constraint extraction present: no explicit solver-targeted path found
- timeout policy present: not implemented locally
- SQL subset policy present: implied in inventory only, not implemented in repo code
- artifact / license / reproducibility signals:
  - inventory source URLs exist
  - no local packaged artifact path was found
  - no runnable reproducibility packet was found

Bottom line:

- the repository records SQLSolver and VeriEQL as support analysis concepts
- it does not contain the local machinery required to run them

## 5. Current 9-Case Compatibility Table

| case_id | pool | likely solver support risk | likely support usefulness | reason | recommended inclusion status |
|---|---|---:|---:|---|---|
| `PERF_0006` | PERF | medium | medium | straightforward analytical SQL, but aggregate and bag-semantics support is unclear | maybe |
| `PERF_0008` | PERF | medium | medium | clean join/aggregate/order/limit shape, but solver subset support is unproven | maybe |
| `PERF_0013` | PERF | high | medium | interval and date semantics raise symbolic encoding risk | exclude |
| `PERF_0017` | PERF | high | medium | interval syntax plus grouped logic increases subset risk | exclude |
| `PERF_0024` | PERF | high | high | correlated nested subqueries are useful semantic stress, but solver difficulty is likely high | maybe |
| `PERF_0033` | PERF | medium | medium | clean TPC-DS aggregate query, still dependent on aggregate semantics support | maybe |
| `PERF_0054` | PERF | medium | medium | bounded analytical structure, but subset support remains uncertain | maybe |
| `CONS_0007` | CONS | medium | high | compact semantic case from Calcite-derived consistency pool; good verifier-style support target | support_candidate |
| `CONS_0012` | CONS | high | high | strong semantic-interest case, but `LIMIT/OFFSET` and correlation are difficult for solver subsets | maybe |

Interpretation:

- `CONS` cases are the strongest bounded support candidates
- cleaner `PERF` cases may be usable later if aggregate and bag semantics are supported
- interval/date and nested correlated forms are higher risk

## 6. PORT / Translation-Route Assessment

High-level assessment:

- SQLSolver / VeriEQL could be useful for translation-correctness support and non-equivalence analysis.
- `PORT_0012` is a good later support-only failure-analysis target because it already carries known execution-layer failure context.
- Direct cross-dialect support is unlikely to be realistic without dialect normalization.
- These tools should only be considered after translation output is normalized into a supported SQL fragment.

Practical interpretation:

- support-only failure analysis: yes
- counterexample-style investigation: potentially yes
- direct cross-dialect verifier path: no
- use after dialect normalization: yes

## 7. 35-Case High-Level Compatibility

High-level only:

- `CONS`: best fit
  - semantic-stress and correctness-support use is most natural here
- `PERF`: limited subset fit
  - only cleaner analytical cases look plausible
- `PORT`: high risk
  - dialect and normalization issues likely dominate
- `LONGTAIL`: high risk
  - feature diversity likely exceeds a prover-supported fragment quickly

Current interpretation:

- SQLSolver / VeriEQL are subset-only support tools
- they are not broad all-35 support routes today
- they are best used on a bounded semantic-support denominator

## 8. Risk / Blocker List

- SQL subset limitations
- NULL semantics uncertainty
- bag semantics uncertainty
- aggregate support uncertainty
- date / interval semantics risk
- cross-dialect semantics risk
- schema / constraint extraction missing
- solver timeout risk
- dependency / artifact availability missing
- false positive / false negative risk if subset assumptions are violated
- no local wrapper or reproducible execution contract

## 9. Recommendation

Recommendation:

- support-only / subset-only verifier
- not execution-ready

Use SQLSolver / VeriEQL only as bounded correctness / semantic-stress / failure-analysis support after a local support path exists.

Do not treat SQLSolver / VeriEQL as:

- a main leaderboard baseline
- a speedup route

## 10. Next Action

- implement a no-execution SQLSolver / VeriEQL support-readiness scaffold

## 11. Verification / Non-Modification Note

- files modified for the completed audit: none
- files created for the completed audit: none
- database workloads run: no
- LLM calls: no
- dependency installs/downloads: no
- registry/docs/formal review/live status changed: no
- taxonomy calibration notes touched: no

Commands used for the completed read-only audit:

- `pwd`
- `git status --short`
- `rg -n -i "SQLSOLVER|SQL Solver|SQLSolver|VERIEQL|VeriEQL|equivalence checker|symbolic equivalence|SMT|Z3|CVC5|solver|theorem prover|constraint solver|counterexample|verifier|semantic checker" .`
- `rg --files | rg -i "(sqlsolver|verieql|solver|smt|z3|cvc5|equivalence|counterexample|verifier|checker|baseline|inventory|requirements|pyproject|setup.py|environment.yml)"`
- `find . -maxdepth 4 \( -name 'requirements*.txt' -o -name 'pyproject.toml' -o -name 'setup.py' -o -name 'environment.yml' -o -name '*z3*' -o -name '*smt*' \) | sort`
- `python - <<'PY' ...` to read `SQLSOLVER_SUPPORT` and `VERIEQL_SUPPORT` inventory rows
- `python - <<'PY' ...` to read selected `inventory/case_registry.csv` rows
- `sed -n '1,220p' docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`
- `sed -n '1,260p' docs/_scratch/BASELINE_SMOKE_READINESS_ROLLUP_v0.md`
- `sed -n '1,220p' docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md`
- `sed -n '1,220p' docs/_scratch/PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md`
- `sed -n '1,220p' docs/PROJECT_PLAN.md`
- `sed -n '1,220p' docs/EXECUTION_STATUS.md`
- `sed -n '1,220p' benchmark_spec/decision_log.md`
- `sed -n '1,220p' benchmark_spec/benchmark_spec_v0.md`
- `sed -n '1,120p'` on representative SQL files including `PERF_0024`, `CONS_0012`, and `PORT_0012`
