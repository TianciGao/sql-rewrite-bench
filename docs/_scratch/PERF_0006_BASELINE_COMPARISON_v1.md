# PERF_0006_BASELINE_COMPARISON_v1

## 0. Purpose And Boundary
This is a case-level baseline comparison for `PERF_0006` only. It is read-only, runs no new experiment, is not leaderboard evidence, and is not registry writeback.

## 1. Case Context
- `case_id`: `PERF_0006`
- pool: `performance`
- source family / dataset: `TPC-H`, seed `TPC-H-Q1`, manually frozen source instance
- why this case matters for the current comparison:
  - R-Bot / LLM4Rewrite reached bounded candidate-generation smoke and checker handoff here
  - LearnedRewrite via the embedded LLM4Rewrite path also reached bounded candidate generation and checker handoff here
  - Calcite HEP bounded subset explicitly includes `PERF_0006`
  - SQLGlot optimize and Direct LLM both have report-local checker-backed case artifacts for this case
  - control artifacts already exist for source, human positive, and hard negative guard

## 2. Evidence Inventory

### Native/source
- case-specific artifacts:
  - `cases/PERF/PERF_0006/runs/pg/source.tsv`
  - `cases/PERF/PERF_0006/runs/pg/result_check.json`
  - `reports/formal_common_core/native_identity_v0.json`
- evidence type: case-specific control evidence
- checker evidence exists: yes
- speedup evidence exists: source reference only, not a scored candidate route

### Human positive
- case-specific artifacts:
  - `cases/PERF/PERF_0006/rewrite_pos_01.sql`
  - `cases/PERF/PERF_0006/runs/pg/rewrite_pos_01.tsv`
  - `cases/PERF/PERF_0006/runs/result_check.json`
  - `reports/formal_common_core/human_reference_positive_v0.json`
- speedup evidence:
  - `reports/formal_common_core/human_positive_speedup_run_v0.json`
  - `docs/_scratch/FORMAL_COMMON_CORE_HUMAN_POSITIVE_SPEEDUP_RUN_SUMMARY_v0.md`
- evidence type: case-specific
- checker evidence exists: yes
- speedup evidence exists: yes

### Hard negative guard
- case-specific artifacts:
  - `cases/PERF/PERF_0006/rewrite_neg_01.sql`
  - `cases/PERF/PERF_0006/runs/pg/rewrite_neg_01.tsv`
  - `cases/PERF/PERF_0006/runs/result_check.json`
  - `docs/_scratch/FORMAL_COMMON_CORE_RUNTIME_OBSERVATION_SNAPSHOT_v0.md`
- evidence type: case-specific guard/control evidence
- checker evidence exists: yes, as negative-diff guard evidence in the case-local result check
- speedup evidence exists: observed single-run runtime only, not correctness-gated speedup scoring

### SQLGlot optimize
- case-specific artifacts:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/perf_0006.json`
  - `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/perf_0006.tsv`
  - `reports/formal_common_core/method_consistency_scoring_v0.json`
- evidence type: case-specific checker-backed report-local materialization
- checker evidence exists: yes
- speedup evidence exists: only aggregate / preflight / single-run observation, not finalized case-specific speedup scoring

### SQLGlot no-opt
- located evidence:
  - aggregate-only references in Batch 2A / expansion notes
- case-specific `PERF_0006` checker artifact found: no
- evidence type: aggregate-only or absent for this case
- checker evidence exists: no case-specific artifact found
- speedup evidence exists: no case-specific artifact found
- uncertainty: do not overclaim `PERF_0006` success from slice-level summaries that do not explicitly include this case

### Direct LLM rewrite
- case-specific artifacts:
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/perf_0006.json`
  - `reports/formal_common_core/result_materialization/llm_direct_rewrite/perf_0006.tsv`
  - `reports/formal_common_core/method_consistency_scoring_v0.json`
- evidence type: case-specific checker-backed report-local materialization
- checker evidence exists: yes
- speedup evidence exists: only aggregate / preflight / single-run observation, not finalized case-specific speedup scoring

### Calcite HEP
- case-specific artifacts:
  - `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json`
  - `reports/formal_expansion/calcite_hep_pg_checker_run_v0.json`
  - `docs/_scratch/CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0.md`
- evidence type: case-specific checker-backed evidence plus bounded speedup subset evidence
- checker evidence exists: yes
- speedup evidence exists: yes

### R-Bot / LLM4Rewrite
- case-specific artifacts:
  - `docs/_scratch/RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v3.md`
  - `docs/_scratch/RBOT_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md`
  - `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql`
- evidence type: bounded 1-case case-specific smoke and checker handoff
- checker evidence exists: yes
- speedup evidence exists: no

### LearnedRewrite / embedded LLM4Rewrite
- case-specific artifacts:
  - `docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v1.md`
  - `docs/_scratch/LEARNEDREWRITE_LLM4REWRITE_CHECKER_HANDOFF_PERF_0006_v1.md`
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v1.sql`
- evidence type: bounded 1-case case-specific smoke and checker handoff
- checker evidence exists: yes
- speedup evidence exists: no
- interpretation: checker-consistent, but the candidate is source-like / no-op, `used_rules` was empty, and `output_cost` was `-1`

## 3. Case-level Comparison Table

| route | candidate_generated | candidate_executed | checker_status | consistency_status | failure_category | speedup_status | speedup_comparable | evidence_scope | claim_boundary |
|---|---|---|---|---|---|---|---|---|---|
| Native/source | not_applicable | yes | consistent | consistent | none | not_applicable | not_applicable | case_specific_control | formal_control_summary_only |
| Human positive | yes | yes | consistent | consistent | none | run_complete | yes | case_specific | positive_control_speedup_only |
| Hard negative guard | yes | yes | consistent | inconsistent | intentional_negative_guard | not_run | no | case_specific_control | guard_only_not_candidate |
| SQLGlot optimize | yes | yes | consistent | consistent | none | not_run | yes | case_specific | perf_only_method_checker_backed_consistency |
| SQLGlot no-opt | unknown | unknown | unknown | unknown | no_case_specific_perf_0006_evidence | not_run | no | aggregate_only_or_absent | aggregate_only_or_unknown |
| Direct LLM rewrite | yes | yes | consistent | consistent | none | not_run | yes | case_specific | perf_only_method_checker_backed_consistency |
| Calcite HEP | yes | yes | consistent | consistent | none | run_complete | yes | case_specific_bounded_subset | calcite_hep_checker_backed_and_speedup_scored_subset |
| R-Bot / LLM4Rewrite | yes | yes | inconsistent | inconsistent | result_mismatch_numeric_avg_precision | not_run | no | bounded_1_case | checker_smoke_failed_not_speedup |
| LearnedRewrite / embedded LLM4Rewrite | yes | yes | consistent | consistent | none | not_run | no | bounded_1_case | checker_smoke_source_like_noop_not_speedup |

For R-Bot / LLM4Rewrite specifically:
- candidate_generated: yes
- candidate_executed: yes
- checker_status: inconsistent
- consistency_status: inconsistent
- failure_category: `result_mismatch_numeric_avg_precision`
- speedup_status: `not_run`
- speedup_comparable: no
- evidence_scope: `bounded_1_case`
- claim_boundary: `checker_smoke_failed_not_speedup`

For LearnedRewrite / embedded LLM4Rewrite specifically:
- candidate_generated: yes
- candidate_executed: yes
- checker_status: consistent
- consistency_status: consistent
- failure_category: none
- speedup_status: `not_run`
- speedup_comparable: no
- evidence_scope: `bounded_1_case`
- candidate_type: `source_echo_or_noop_candidate`
- claim_boundary: `checker_smoke_source_like_noop_not_speedup`

## 4. Correctness-gated Ranking For PERF_0006

### Reference/control
- Native/source
- Human positive
- Hard negative guard

### Checker-consistent and speedup-comparable
- Human positive
- Calcite HEP
- SQLGlot optimize
- Direct LLM rewrite

### Checker-consistent but not speedup-evaluated / not useful rewrite evidence
- LearnedRewrite / embedded LLM4Rewrite

### Generated/executed but checker-failed
- R-Bot / LLM4Rewrite

### Blocked / no case-specific evidence / aggregate-only
- SQLGlot no-opt

Interpretation:
- R-Bot is below checker-consistent routes on this case because it fails correctness.
- R-Bot cannot enter speedup comparison for `PERF_0006`.
- LearnedRewrite is checker-consistent on this case, but the bounded artifact is source-like / no-op and therefore should not be presented as useful rewrite improvement or as a speedup result.
- SQLGlot no-opt is not credited with case-specific success because no explicit `PERF_0006` checker-backed artifact was found.

## 5. R-Bot Failure Interpretation
- R-Bot produced executable SQL
- source and candidate row counts both equaled `2`
- normalized outputs differed
- decisive mismatch: `avg_disc 0.075...` vs `0.08`
- failure type: numeric precision / average rewrite semantic drift
- this is exactly the kind of plausible-but-wrong rewrite that correctness-gated RewriteBench is designed to catch

## 6. LearnedRewrite Interpretation
- LearnedRewrite produced executable SQL and passed the PostgreSQL checker on `PERF_0006`
- but the candidate appears source-like / no-op rather than a useful rewrite
- the smoke artifact reported `used_rules = []`
- the smoke artifact reported `output_cost = -1`
- this should be counted as correctness evidence for source-like output, not as evidence of rewrite gain
- the contrast with R-Bot is instructive:
  - R-Bot produced a nontrivial-looking candidate that executed but failed correctness
  - LearnedRewrite produced a source-like / no-op candidate that remained checker-consistent

## 7. Paper-facing Wording
Accepted wording:

“On PERF_0006, R-Bot / LLM4Rewrite reached bounded candidate generation and PostgreSQL execution, but failed the checker because the generated SQL changed average/decimal semantics. It is therefore counted as a correctness failure and excluded from speedup comparison.”

Required contrast wording:

“On PERF_0006, LearnedRewrite via the embedded LLM4Rewrite path emitted a source-like/no-op candidate that passed the PostgreSQL checker, while R-Bot emitted a nontrivial-looking candidate that executed but failed consistency due to average/decimal semantic drift. This illustrates why RewriteBench separates candidate generation, execution, semantic consistency, and speedup eligibility.”

Forbidden wording:
- LearnedRewrite speedup result
- LearnedRewrite useful rewrite improvement
- LearnedRewrite leaderboard win
- R-Bot passed PERF_0006
- R-Bot speedup result
- full R-Bot coverage

## 8. Recommended Next Step
`stop expanding PERF_0006 for these two baselines and record the contrast as failure/behavior evidence`

Reason:
- the bounded 1-case evidence already captures the useful contrast
- R-Bot shows candidate-generation reachability plus semantic failure
- LearnedRewrite shows checker-consistent but source-like / no-op behavior
- neither result is a basis for claiming useful speedup on this case

## 9. Non-Modification Note
No experiments were run. No repo state changed except this note.
