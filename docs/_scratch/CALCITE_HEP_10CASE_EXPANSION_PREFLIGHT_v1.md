# CALCITE_HEP_10CASE_EXPANSION_PREFLIGHT_v1

## 0. Purpose And Boundary
This is a no-execution Calcite HEP @10 expansion preflight. It does not run Calcite HEP, run any database, run checker, run speedup, or perform any registry writeback.

## 1. Existing Calcite HEP Evidence
Current Calcite HEP evidence is bounded subset evidence only.

- existing checker denominator: `4`
- existing checker result: `4/4` checker-consistent on the bounded subset
- existing speedup denominator: `4`
- existing speedup result: `GM_Speedup=0.9588741913559858` when available from subset reports
- claim boundary: `calcite_hep_pg_checker_postgres_only_not_speedup_not_final_baseline` and bounded speedup subset only
- current evidence is subset-only because the runnable checker and speedup records are limited to the verified four-case set rather than the shared 10-case denominator

## 2. Target Denominator
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

## 3. Per-case Readiness Table
| case_id | source_sql_exists | pg_schema_exists | pg_witness_exists | existing_calcite_hep_candidate | existing_checker_evidence | existing_speedup_evidence | input_contract_ready | output_capture_contract_ready | checker_handoff_contract_ready | speedup_handoff_contract_ready | readiness_status | risk | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0006 | True | True | True | True | True | True | True | True | True | True | already_measured_subset_case | low | bounded subset checker/speedup evidence already exists; earlier parse-readiness risk=low; earlier readiness recommendation=first_subset_candidate |
| PERF_0008 | True | True | True | True | True | True | True | True | True | True | already_measured_subset_case | low | bounded subset checker/speedup evidence already exists; earlier parse-readiness risk=low; earlier readiness recommendation=first_subset_candidate |
| PERF_0013 | True | True | True | False | False | False | True | True | True | True | ready_for_calcite_hep_generation | medium | earlier parse-readiness risk=medium; earlier readiness recommendation=maybe_later |
| PERF_0017 | True | True | True | False | False | False | True | True | True | True | ready_for_calcite_hep_generation | medium | earlier parse-readiness risk=medium; earlier readiness recommendation=maybe_later |
| PERF_0019 | True | True | True | False | False | False | True | True | True | True | ready_for_calcite_hep_generation | medium | no prior Calcite HEP case-specific readiness record found |
| PERF_0024 | True | True | True | False | False | False | True | True | True | True | ready_for_calcite_hep_generation | medium | earlier parse-readiness risk=medium; earlier readiness recommendation=maybe_later |
| PERF_0033 | True | True | True | True | True | True | True | True | True | True | already_measured_subset_case | low | bounded subset checker/speedup evidence already exists; earlier parse-readiness risk=low; earlier readiness recommendation=first_subset_candidate |
| PERF_0052 | True | True | True | False | False | False | True | True | True | True | ready_for_calcite_hep_generation | medium | no prior Calcite HEP case-specific readiness record found |
| PERF_0054 | True | True | True | True | True | True | True | True | True | True | already_measured_subset_case | low | bounded subset checker/speedup evidence already exists; earlier parse-readiness risk=low; earlier readiness recommendation=first_subset_candidate |
| PERF_0063 | True | True | True | False | False | False | True | True | True | True | ready_after_minor_adapter_patch | high | not included in earlier calcite pg-native-9 parse-readiness report |

## 4. Expansion Plan
Already-covered subset cases:
- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Missing cases ready for generation:
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0052`

Cases needing adapter patch:
- `PERF_0063`

Blocked cases:
- none

## 5. Metrics To Report Later
- `candidate_generation_rate@10`
- `executable_rate@10`
- `result_consistency_rate@10`
- `gm_speedup`
- `win/tie/loss`
- `regression_rate@20`
- `measurement_failure_count`
- `timeout_count`

No metrics are computed in this preflight.

## 6. Claim Boundary
- `bounded_calcite_hep_10case_expansion_preflight_only_not_execution`

## 7. Recommended Next Step
- `execute Calcite HEP missing-case generation/checker batch`

## 8. Non-Modification Note
Confirm no Calcite HEP run, no DB/checker/speedup, no model/API, no registry/review/rules/EXECUTION_STATUS/case changes, and taxonomy notes untouched.
