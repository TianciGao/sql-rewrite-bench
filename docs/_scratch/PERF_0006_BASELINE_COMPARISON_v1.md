# PERF_0006_BASELINE_COMPARISON_v1

## 0. Purpose And Boundary
This is a case-level baseline comparison for `PERF_0006` only. It is read-only, runs no new experiment, is not leaderboard evidence, and is not registry writeback.

## 1. Case Context
- `case_id`: `PERF_0006`
- pool: `performance`
- source family / dataset: `TPC-H`, seed `TPC-H-Q1`, manually frozen source instance
- why this case matters for the current comparison:
  - R-Bot / LLM4Rewrite reached bounded candidate-generation smoke and checker handoff here
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

### Generated/executed but checker-failed
- R-Bot / LLM4Rewrite

### Blocked / no case-specific evidence / aggregate-only
- SQLGlot no-opt

Interpretation:
- R-Bot is below checker-consistent routes on this case because it fails correctness.
- R-Bot cannot enter speedup comparison for `PERF_0006`.
- SQLGlot no-opt is not credited with case-specific success because no explicit `PERF_0006` checker-backed artifact was found.

## 5. R-Bot Failure Interpretation
- R-Bot produced executable SQL
- source and candidate row counts both equaled `2`
- normalized outputs differed
- decisive mismatch: `avg_disc 0.075...` vs `0.08`
- failure type: numeric precision / average rewrite semantic drift
- this is exactly the kind of plausible-but-wrong rewrite that correctness-gated RewriteBench is designed to catch

## 6. Paper-facing Wording
Accepted wording:

“On PERF_0006, R-Bot / LLM4Rewrite reached bounded candidate generation and PostgreSQL execution, but failed the checker because the generated SQL changed average/decimal semantics. It is therefore counted as a correctness failure and excluded from speedup comparison.”

Forbidden wording:
- R-Bot passed PERF_0006
- R-Bot checker-backed success
- R-Bot speedup result
- R-Bot leaderboard result
- full R-Bot coverage

## 7. Recommended Next Step
`perform failure analysis only`

Reason:
- the bounded 1-case evidence already shows that R-Bot can reach candidate generation and PG execution
- the blocker is now semantic correctness, not environment readiness
- speedup is disallowed until a future candidate becomes checker-consistent

## 8. Non-Modification Note
No experiments were run. No repo state changed except this note.
