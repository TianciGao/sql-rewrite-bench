# PRIOR_METHOD_6CASE_SMOKE_EXPANSION_PREFLIGHT_v1

## 0. Purpose And Boundary
This note is a bounded case-selection preflight only for expanding the current prior-method smoke subset from 3 PERF cases to 6 PERF cases. It does not execute `R-Bot`, `LearnedRewrite`, any database, any checker, any model/API route, or any speedup workflow.

## 1. Existing 3-case Subset
Current denominator:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

Current interpretation from the bounded 3-case smoke:
- `R-Bot / LLM4Rewrite` showed one checker-consistent nontrivial candidate, one checker-inconsistent candidate, and one generation-path failure.
- `LearnedRewrite / embedded LLM4Rewrite` showed three checker-consistent candidates, but two were source-like / no-op outputs.

## 2. Candidate Pool
Broad `cases/PERF/*` structure and report-local artifact coverage were inspected. The table below records the highest-overlap PERF cases after excluding the current denominator.

| case_id | source_sql_exists | pg_schema_exists | pg_witness_exists | pg_control_evidence_exists | existing_method_artifacts | known_blockers | eligibility_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | already_in_current_subset | excluded_current_subset | retained as existing denominator case only |
| `PERF_0008` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | already_in_current_subset | excluded_current_subset | retained as existing denominator case only |
| `PERF_0033` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | already_in_current_subset | excluded_current_subset | retained as existing denominator case only |
| `PERF_0013` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker`, `learnedrewrite_input_readiness`, `rbot_retrieval_readiness` | interval_year_date_syntax_risk | eligible | stable common-core case with existing checker/materialization coverage |
| `PERF_0017` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker`, `learnedrewrite_input_readiness`, `rbot_retrieval_readiness` | interval_month_grouped_reporting_risk | eligible_backup | structurally clean, but less behavior-diverse than the selected correlated-subquery candidate |
| `PERF_0024` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker`, `learnedrewrite_input_readiness`, `rbot_retrieval_readiness` | correlated_subquery_high_complexity | eligible | useful semantic-stress case with existing common-core evidence |
| `PERF_0054` | yes | yes | yes | yes | `calcite_hep`, `sqlglot_opt`, `direct_llm`, `human_positive`, `prior_baseline_feasibility`, `learnedrewrite_input_readiness`, `rbot_retrieval_readiness` | none_known_at_preflight | eligible | explicitly named in earlier prior-baseline readiness notes as the clean next candidate beyond the current 3-case set |

## 3. Recommended 3 Additional Cases
Recommended additions:
- `PERF_0013`
- `PERF_0024`
- `PERF_0054`

### `PERF_0013`
- why selected:
  - already sits inside the formal common-core method/control artifact lattice
  - has `source.sql`, `schema/ddl_pg.sql`, `validation/pg_witness_data.sql`, and case-local `runs/result_check.json`
  - adds interval/date semantics that differ from the current 3-case subset
- why safe for `R-Bot` smoke:
  - structurally complete PG package
  - prior retrieval-readiness artifacts already mention it as a plausible bounded candidate
- why safe for `LearnedRewrite` smoke:
  - bounded adapter input contract is present and similar to already-connected TPC-H cases
- expected risk:
  - medium
  - interval/date syntax could stress retrieval or Java-side rule handling
- existing evidence paths:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/perf_0013.json`
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/perf_0013.json`
  - `docs/_scratch/FORMAL_COMMON_CORE_HUMAN_POSITIVE_SPEEDUP_RUN_SUMMARY_v0.md`

### `PERF_0024`
- why selected:
  - adds correlated nested-subquery behavior not covered by the current 3-case denominator
  - has full PG package and existing common-core checker/materialization evidence
  - improves behavior diversity rather than selecting only easier analytical cases
- why safe for `R-Bot` smoke:
  - package closure and report-local control evidence already exist
  - retrieval-readiness work already indexed it as a plausible target
- why safe for `LearnedRewrite` smoke:
  - adapter inputs are structurally complete and already recognized in LearnedRewrite input-readiness artifacts
- expected risk:
  - medium-high
  - correlated subqueries raise candidate-generation and semantic-consistency risk
- existing evidence paths:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/perf_0024.json`
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/perf_0024.json`
  - `docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md`

### `PERF_0054`
- why selected:
  - explicitly identified in earlier prior-baseline feasibility notes as the clean next case beyond `PERF_0006`, `PERF_0008`, and `PERF_0033`
  - has full PG package plus existing Calcite HEP, SQLGlot, Direct LLM, and human-positive report-local evidence
  - adds a TPC-DS analytical join/aggregate/order/limit shape with cleaner bounded readiness than most alternatives
- why safe for `R-Bot` smoke:
  - previous readiness notes singled it out as a clean first-subset case for retrieval-style baselines
- why safe for `LearnedRewrite` smoke:
  - input-readiness artifacts already include it, and the package has no unresolved PG substrate gap at preflight level
- expected risk:
  - medium
  - still a real rewrite-sensitive analytical case, so candidate generation may not remain source-like
- existing evidence paths:
  - `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0054.json`
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/perf_0054.json`
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/perf_0054.json`
  - `docs/_scratch/REMAINING_PRIOR_BASELINES_FEASIBILITY_v0.md`

## 4. Proposed 6-case Denominator
Existing 3:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

New 3:
- `PERF_0013`
- `PERF_0024`
- `PERF_0054`

Final proposed denominator:
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

## 5. Execution Plan For Later
For each new case and method, later execution should remain bounded and correctness-gated.

For `R-Bot / LLM4Rewrite`:
- adapter / smoke preflight if missing
- single-case dry-run
- single-case smoke with fresh run name and vector-alignment patch
- PG checker handoff only if `output_sql` is captured
- no speedup

For `LearnedRewrite / embedded LLM4Rewrite`:
- adapter preflight if missing
- single-case dry-run
- single-case smoke using the recovered unsigned/repacked classpath path
- PG checker handoff only if `output_sql` is captured
- no speedup

## 6. Claim Boundary
`bounded_6case_prior_method_smoke_subset_not_leaderboard`

## 7. Recommended Next Step
`execute the 3 additional cases for R-Bot and LearnedRewrite`

Reason:
- the three recommended additions are structurally eligible
- they already overlap with existing control/method artifact coverage
- they add behavior diversity without selecting only apparently favorable cases
- they preserve a bounded, auditable denominator

## 8. Non-Modification Note
No experiments were run. No repo state changed except this note and the machine-readable preflight summary.
