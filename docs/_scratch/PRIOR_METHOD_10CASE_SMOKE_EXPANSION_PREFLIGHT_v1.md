# PRIOR_METHOD_10CASE_SMOKE_EXPANSION_PREFLIGHT_v1

## 0. Purpose And Boundary
This note is a bounded case-selection preflight only for expanding the current prior-method smoke subset from the executed 3-case base and proposed 6-case denominator to a future 10-case denominator. It does not execute `R-Bot`, `LearnedRewrite`, any database, any checker, any model/API route, or any speedup workflow.

## 1. Existing Evidence
Executed 3-case subset:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

Current proposed 6-case denominator:
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

Why expand to 10:
- the 3-case execution subset already showed meaningful behavior diversity
- the 6-case proposal extends that into one broader TPC-H date/interval case, one correlated-subquery case, and one clean TPC-DS analytical case
- a 10-case denominator can add more stress diversity across grouped reporting, outer-join/materialization, CTE/decorrelation, and string/filter analytical patterns

Why this remains non-leaderboard:
- this is still preflight only
- even if later executed, the planned denominator remains a bounded smoke subset rather than full prior-method coverage
- no speedup is included in this planning step

## 2. Candidate Pool
Broad `cases/PERF/*` structure and report-local artifact coverage were inspected. The table below records the current denominator plus the strongest next-layer candidates and backups after excluding the already-selected 6-case set.

| case_id | source_sql_exists | pg_schema_exists | pg_witness_exists | pg_control_evidence_exists | existing_method_artifacts | feature_or_behavior_diversity | known_blockers | eligibility_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | TPC-H aggregate/reporting | already_in_current_denominator | excluded_existing | executed base case |
| `PERF_0008` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | TPC-H join/aggregate/order/limit | already_in_current_denominator | excluded_existing | executed base case |
| `PERF_0013` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker` | date/interval join-aggregate | already_in_current_denominator | excluded_existing | proposed 6-case addition |
| `PERF_0017` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker`, `learnedrewrite_input_readiness`, `rbot_retrieval_readiness` | grouped reporting plus interval-month semantics | interval_month_grouped_reporting_risk | eligible | strongest remaining common-core-style addition |
| `PERF_0019` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch2a_pg_execution`, `human_positive_case_local` | outer join plus derived-table/materialization distribution query | none_known_at_preflight | eligible | adds outer-join/materialization variety |
| `PERF_0022` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch2a_pg_execution`, `human_positive_case_local` | richer aggregation with subquery and reporting complexity | taxonomy_metadata_cleanup_caveat | eligible_backup | strong structural candidate, but carries explicit metadata caveat in review notes |
| `PERF_0024` | yes | yes | yes | yes | `sqlglot_opt`, `direct_llm`, `human_positive`, `common_core_checker` | correlated nested subquery | already_in_current_denominator | excluded_existing | proposed 6-case addition |
| `PERF_0033` | yes | yes | yes | yes | `rbot`, `learnedrewrite`, `sqlglot_opt`, `direct_llm`, `calcite_hep`, `human_positive` | TPC-DS aggregate/order/limit | already_in_current_denominator | excluded_existing | executed base case |
| `PERF_0052` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch3a_pg_execution`, `human_positive_case_local` | CTE plus decorrelation / correlated aggregate thresholding | none_known_at_preflight | eligible | compact TPC-DS decorrelation case with clean execution scaffolding |
| `PERF_0054` | yes | yes | yes | yes | `calcite_hep`, `sqlglot_opt`, `direct_llm`, `human_positive`, `prior_baseline_feasibility` | TPC-DS join/aggregate/order/limit | already_in_current_denominator | excluded_existing | proposed 6-case addition |
| `PERF_0056` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch3a_pg_execution`, `human_positive_case_local` | another decorrelation / existence-style analytical case | overlap_with_perf_0052 | eligible_backup | structurally strong, but more redundant if `PERF_0052` is selected |
| `PERF_0062` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch3a_pg_execution`, `human_positive_case_local` | straightforward aggregate/reporting analytical case | lower_behavior_novelty | eligible_backup | stable but less behavior-diverse than selected alternatives |
| `PERF_0063` | yes | yes | yes | yes | `expanded_direct_llm`, `sqlglot_no_opt_checker`, `batch3a_pg_execution`, `human_positive_case_local` | string function plus disjunctive filter plus grouped aggregation | none_known_at_preflight | eligible | adds string/filter analytical diversity absent from the current denominator |

## 3. Recommended 4 Additional Cases
Recommended additions:
- `PERF_0017`
- `PERF_0019`
- `PERF_0052`
- `PERF_0063`

### `PERF_0017`
- why selected:
  - already overlaps with the formal common-core control/method artifact lattice
  - adds grouped reporting plus interval-month semantics that are not otherwise present in the proposed 6-case denominator
- why safe for `R-Bot` smoke:
  - structurally complete PG package and prior retrieval-readiness notes already mention it as plausible
- why safe for `LearnedRewrite` smoke:
  - bounded adapter contract is comparable to already-connected TPC-H cases
- expected risk:
  - medium
- feature/behavior contribution:
  - grouped reporting
  - interval/date arithmetic
  - join-aggregate with ordering
- existing evidence paths:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/perf_0017.json`
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/perf_0017.json`
  - `docs/_scratch/FORMAL_COMMON_CORE_HUMAN_POSITIVE_SPEEDUP_RUN_SUMMARY_v0.md`

### `PERF_0019`
- why selected:
  - adds left-outer-join plus derived-table/materialization style not already represented in the proposed 6-case denominator
  - has full PG package, case-local result-check evidence, and expanded-slice Direct LLM / SQLGlot no-opt artifacts
- why safe for `R-Bot` smoke:
  - structurally complete PG package and no package-level blocker was found
- why safe for `LearnedRewrite` smoke:
  - input contract remains simple single-statement SQL despite richer shape
- expected risk:
  - medium
- feature/behavior contribution:
  - left outer join
  - grouped derived table
  - distribution-style reporting
- existing evidence paths:
  - `reports/formal_expansion/result_checks/expanded_perf/llm_direct_rewrite/perf_0019.json`
  - `reports/formal_expansion/result_checks/batch2a/sqlglot_transpile_same_dialect_no_opt/perf_0019.json`
  - `docs/_scratch/BATCH2A_SPEEDUP_RUN_SUMMARY_v0.md`

### `PERF_0052`
- why selected:
  - adds a compact TPC-DS CTE/decorrelation pattern
  - has case-local result-check evidence plus expanded Direct LLM / SQLGlot no-opt / PG execution artifacts
- why safe for `R-Bot` smoke:
  - PG package is complete and the SQL shape is complex enough to be informative without being unusually exotic
- why safe for `LearnedRewrite` smoke:
  - single-statement analytical structure remains compatible with the already recovered Java/JAR path
- expected risk:
  - medium
- feature/behavior contribution:
  - CTE
  - correlated aggregate threshold
  - decorrelation-style rewrite opportunity
- existing evidence paths:
  - `reports/formal_expansion/result_checks/expanded_perf/llm_direct_rewrite/perf_0052.json`
  - `reports/formal_expansion/result_checks/batch3a/sqlglot_transpile_same_dialect_no_opt/perf_0052.json`
  - `docs/_scratch/BATCH3A_PERF_PG_EXECUTION_SUMMARY_v0.md`

### `PERF_0063`
- why selected:
  - adds string-function and disjunctive-filter behavior not covered by the existing 6-case proposal
  - has full PG package, case-local result-check evidence, and expanded Direct LLM / SQLGlot no-opt / PG execution artifacts
- why safe for `R-Bot` smoke:
  - structurally complete analytical case with prior expanded-slice method artifacts already materialized
- why safe for `LearnedRewrite` smoke:
  - no package-level blocker was found and the query remains within the same bounded analytical family as already connected TPC-DS cases
- expected risk:
  - medium
- feature/behavior contribution:
  - string function
  - disjunctive filter
  - grouped aggregation
- existing evidence paths:
  - `reports/formal_expansion/result_checks/expanded_perf/llm_direct_rewrite/perf_0063.json`
  - `reports/formal_expansion/result_checks/batch3a/sqlglot_transpile_same_dialect_no_opt/perf_0063.json`
  - `docs/_scratch/BATCH3A_PERF_PG_EXECUTION_SUMMARY_v0.md`

## 4. Proposed 10-case Denominator
Executed 3:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

6-case proposed additions:
- `PERF_0013`
- `PERF_0024`
- `PERF_0054`

New 4:
- `PERF_0017`
- `PERF_0019`
- `PERF_0052`
- `PERF_0063`

Final proposed denominator:
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

## 5. Execution Plan For Later
For each of the 7 not-yet-run cases and each method:

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

## 6. Metrics To Report Later
For the eventual 10-case smoke subset, report:
- `candidate_generation_rate@10`
- `executable_rate@10`
- `result_consistency_rate@10`
- `checker_failed_count`
- `failure_categories`
- `source_like_or_noop_count`
- `nontrivial_checker_consistent_count`
- `speedup_status = not_run`

Do not compute:
- `gm_speedup`
- `regression_rate@20`
- leaderboard rank

## 7. Claim Boundary
`bounded_10case_prior_method_smoke_subset_not_leaderboard`

## 8. Recommended Next Step
`execute the 7 not-yet-run cases for R-Bot and LearnedRewrite`

Reason:
- the four new additions are structurally eligible
- they extend the denominator without obvious cherry-picking
- they add real behavior diversity beyond the current and proposed subsets
- they remain bounded enough to review before any further expansion

## 9. Non-Modification Note
No experiments were run. No repo state changed except this note and the machine-readable preflight summary.
