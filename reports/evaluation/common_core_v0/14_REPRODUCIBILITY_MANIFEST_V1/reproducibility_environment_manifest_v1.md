# Reproducibility Environment Manifest v1

## Purpose

This manifest records which reproducibility-environment fields are already frozen in retained Common-core v0 artifacts, which are only route-local or bounded-subset values, and which still need explicit submission-time capture. No DB, model, or verifier run was performed.

## Retained Exact Or Route-Local Values

### retained_partial

| category | field | retained_value | source_artifact | notes |

| --- | --- | --- | --- | --- |

| hardware | OS | Primary convention: WSL Ubuntu; retained exact bounded runtime snapshot: Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39 | AGENTS.md|reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_verify_report_v1.md | Repo-wide submission OS is not frozen, but a bounded exact runtime snapshot exists for the R-Bot formal lock. |

| runtime | Python version | 3.12.3 exact in retained R-Bot runtime lock snapshot; repo-wide interpreter pin not frozen | reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_verify_report_v1.md|reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json | Exact for one bounded prior-method environment only. |

| engine | MySQL version | mysql:8.4 retained in bootstrap docker-compose only | env/docker-compose.yml | Bootstrap container image is retained, but this is not a full benchmark-wide engine-version freeze. |

| dependency | SQLGlot version | 30.7.0 exact in retained R-Bot formal runtime lock only | reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt|reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json | Useful package pin evidence exists, but not as a repo-wide lock for every Common-core route. |

| policy | timeout policy | 30s per query attempt on retained timing packets; 60s statement_timeout on PG plan attribution frontier | reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_policy_v1.md|reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/README.md|reports/evaluation/common_core_v0/runs/pg_plan_attribution_113_01/pg_plan_attribution_113_policy_v1.md | Policy is packet-local rather than one repo-wide frozen submission field. |

| policy | warmup policy | warmup_count=1 on retained timing packets | reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_policy_v1.md|reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/README.md | Retained for timing packets only. |

| policy | repetitions | repeat_count=3 on retained timing packets | reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_policy_v1.md|reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/README.md | Retained for timing packets only. |

| policy | checker normalization policy | Route-level normalized checker / backfill behavior retained, but no single consolidated repo-wide normalization field frozen | reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/sqlglot_result_check_backfill_summary_v1.csv | Exact normalization behavior exists in route artifacts, but not in one submission manifest. |

| policy | NULL/date handling | Retained as route-specific normalization caveats and portability tags, not one repo-wide execution policy | reports/evaluation/common_core_v0/09_TAXONOMY_COVERAGE_V1/common_core_v0_case_tag_matrix_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv | Important for interpretation, but not frozen as one canonical runtime flag set. |

| llm | LLM model/checkpoint | gpt-4o-mini exact for Direct LLM original and Direct LLM + Repair-1; bounded prior-method checkpoints remain unrecovered or outside main-track freeze | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | Exact for Direct LLM packets only. |

| llm | provider | api.gptsapi.net exact for Direct LLM original/repair and bounded R-Bot runtime lock | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md|reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_verify_report_v1.md | Provider is not a repo-wide guarantee for all historical/bounded routes. |

| llm | prompt template path/hash | Original prompt: reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md sha256=55561656591c9ebd4c02192ee1b3802cdd8cda433acb7e19cc80c9fc17e5d986; Repair prompt: reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_prompt_template_v1.md sha256=5192c1c6ce9e7a370556846a2a04b29372094f1e7c02f567191d6d9f18ea33db | reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_prompt_template_v1.md | Exact paths and computed hashes are available for Direct LLM routes only. |

| llm | temperature | 0 exact for Direct LLM original and repair | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | Symbolic routes are not temperature-driven. |

| llm | top-p | 1 exact for Direct LLM original and repair | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | Symbolic routes are not top-p driven. |

| llm | max tokens | 2048 exact for Direct LLM original and repair | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | Symbolic routes are not max-token driven. |

| llm | candidate count | 1 candidate per row exact for Direct LLM original and repair | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | No multi-candidate decode policy is frozen for the main Direct LLM routes. |

| llm | retry policy | Original route: single generation call per row with no explicit retry loop retained; repair route: repair_attempts=1 | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/run_results.json | Retained per Direct LLM route, not as a repo-wide global field. |

| llm | extraction rule | Original route captures direct message content with SQL-like first-line / no-markdown / no-prose gating; repair route uses the same acceptance family | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_original_model_metadata_audit_v1.md|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_policy_v1.md | Exact for Direct LLM routes only. |

| llm | call date | Original run_timestamp=2026-05-07T21:16:12+00:00; repair run_timestamp=2026-05-11T09:57:49+00:00 retained as closest call-date proxies | reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/run_results.json|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/run_results.json | Per-row API call timestamps are not frozen. |

| packaging | table regeneration commands | Packet-level run scripts are retained for several upstream artifacts, but no single final Section 8 render command or 13_SECTION8_FINAL_RENDER_V1 directory is retained | scripts/cli.py|reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_01/run_manual_direct_llm_timing.sh|reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/run_manual_sqlglot_full_per_case_timing.sh|reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/run_manual_calcite_hep_93_exact_timing.sh|reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/run_manual_package_hard_negative_closure.sh|reports/evaluation/common_core_v0/runs/pg_plan_attribution_113_01/run_manual_pg_plan_attribution_113.sh | Manifest can point to retained packet-level commands, but not to one frozen end-to-end Section 8 render entrypoint. |


### human_review_needed

| category | field | retained_value | source_artifact | notes |

| --- | --- | --- | --- | --- |

| dependency | Calcite version or commit/hash | NA_not_retained | reports/evaluation/common_core_v0/calcite_hep_120_fail_closed_synthesis_v1.csv|reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/README.md | Calcite route evidence is retained, but the exact wrapper / jar version or commit hash is not frozen in the inspected paper artifacts. |

| policy | ordering policy | NA_not_retained | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv|reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_policy_v1.md | Speedup is row-local median based, but a single explicit output-ordering policy for all checker tables was not frozen. |

| policy | numeric tolerance | NA_not_retained | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | Numeric tolerance is referenced implicitly in checker/normalization artifacts, but no single exact tolerance value was frozen here. |


### missing_before_submission

| category | field | retained_value | source_artifact | notes |

| --- | --- | --- | --- | --- |

| hardware | CPU | NA_not_retained | reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json | Machine architecture x86_64 is retained, but CPU model is not frozen in the paper artifact layer. |

| hardware | memory | NA_not_retained | reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json | No retained exact RAM value was found. |

| hardware | storage | NA_not_retained | reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json | No retained storage / disk class value was found. |

| runtime | JVM / Java version | NA_not_retained | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/verifier_support_pair_ledger_v1.csv | Verifier support artifacts do not freeze a submission-grade Java version in the Common-core paper layer. |

| engine | PostgreSQL version | NA_not_retained | AGENTS.md|scripts/cli.py | PostgreSQL access conventions are retained, but no exact benchmark PostgreSQL version was frozen in the inspected artifact layer. |

| engine | Spark SQL version | NA_not_retained | AGENTS.md|scripts/cli.py | Spark local-mode convention is retained, but no exact Spark SQL version was frozen in the inspected artifact layer. |

| policy | cache policy | NA_not_retained | reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.md | No single retained cache-on/cache-off policy was frozen for submission. |


## Key Takeaway

- The strongest retained reproducibility metadata is route-local: Direct LLM model/prompt/decode settings, timing packet policies, PG plan-attribution scripts, and the bounded R-Bot runtime lock.

- Repo-wide submission metadata is still incomplete for hardware and exact engine-version pins.
