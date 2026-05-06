# CALCITE_HEP_9OF10_CHECKER_SPEEDUP_ROLLUP_v1

## 0. Purpose And Boundary
This is a Calcite HEP checker+speedup rollup for a 9/10 measured subset. It is PG-only, witness-scale, not a final @10 baseline, and records no new experiment.

## 1. Evidence Timeline
- original 4-case subset established bounded checker+speedup evidence for `PERF_0006`, `PERF_0008`, `PERF_0033`, and `PERF_0054`
- `CALCITE_HEP_10CASE_EXPANSION_PREFLIGHT_v1` established that six additional cases were mostly runnable, with `PERF_0063` higher risk
- the first missing-case checker batch generated candidates but failed checker handoff on five cases because of a readiness/report-path contract mismatch
- `CALCITE_HEP_MISSING_FAILURE_DIAGNOSTIC_v1` isolated that shared wrapper failure and separated it from the `PERF_0063` function-signature blocker
- checker rerun after the readiness fix produced five new checker-consistent cases: `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0052`
- the five-case speedup batch then measured those newly checker-consistent cases and the sanity audit passed with a witness-scale caveat
- `PERF_0063` remains blocked by `generation_failed_function_signature_mismatch`

## 2. Coverage Summary
| target_10case_denominator | checker_consistent_count | speedup_measured_count | remaining_blocker | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| 10 | 9 | 9 | `PERF_0063:generation_failed_function_signature_mismatch` | `measured_for_9of10_only` | `calcite_hep_9of10_checker_speedup_rollup_not_final_baseline` |

## 3. Subset Metrics
| subset | cases | checker_consistent | speedup_measured | gm_speedup | win/tie/loss | regression_count@20 | measurement_failure_count | timeout_count | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| existing_4case_subset | `PERF_0006, PERF_0008, PERF_0033, PERF_0054` | 4/4 | 4/4 | `0.9588741913559858` | `0/3/1` | `0` | `0` | `0` | bounded PG-only subset, not final baseline |
| fixed_5case_missing_batch | `PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0052` | 5/5 | 5/5 | `0.9588328711588356` | `0/4/1` | `1` | `0` | `0` | bounded PG-only witness-scale batch after readiness fix |
| combined_9of10_measured_subset | `PERF_0006, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0052, PERF_0054` | 9/10 | 9/10 | `0.9588512354710723` | `0/7/2` | `1` | `0` | `0` | PG-only witness-scale rollup, still not a final @10 baseline |

## 4. Per-case Matrix
| case_id | status | checker_status | speedup_status | speedup | win_tie_loss | regression_at_20 | artifact_source | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0006 | measured_existing_subset | consistent | measured | `0.9507767598019691` | `tie` | `false` | `docs/_scratch/CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0.md` | existing bounded 4-case PG-only subset |
| PERF_0008 | measured_existing_subset | consistent | measured | `0.9969231920515313` | `tie` | `false` | `docs/_scratch/CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0.md` | existing bounded 4-case PG-only subset |
| PERF_0013 | measured_missing_batch_after_fix | consistent | measured | `0.9738323007586009` | `tie` | `false` | `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json` | newly checker-consistent after readiness/report-path fix |
| PERF_0017 | measured_missing_batch_after_fix | consistent | measured | `1.017780453645755` | `tie` | `false` | `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json` | newly checker-consistent after readiness/report-path fix |
| PERF_0019 | measured_missing_batch_after_fix | consistent | measured | `1.01548648757718` | `tie` | `false` | `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json` | newly checker-consistent after readiness/report-path fix |
| PERF_0024 | measured_missing_batch_after_fix | consistent | measured | `0.9977679352963833` | `tie` | `false` | `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json` | newly checker-consistent after readiness/report-path fix |
| PERF_0033 | measured_existing_subset | consistent | measured | `0.9382440670018497` | `loss` | `false` | `docs/_scratch/CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0.md` | existing bounded 4-case PG-only subset |
| PERF_0052 | measured_missing_batch_after_fix | consistent | measured | `0.8069982593767138` | `loss` | `true` | `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json` | newly checker-consistent after readiness/report-path fix |
| PERF_0054 | measured_existing_subset | consistent | measured | `0.950583855886198` | `tie` | `false` | `docs/_scratch/CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0.md` | existing bounded 4-case PG-only subset |
| PERF_0063 | blocked | not_run_generation_failed | not_run | `n/a` | `not_applicable` | `n/a` | `docs/_scratch/CALCITE_HEP_MISSING_FAILURE_DIAGNOSTIC_v1.md` | blocked by function-signature mismatch on `substr(ca_zip, 1, 5)` |

## 5. Interpretation
Calcite HEP is no longer merely a 4-case checker/speedup line. It now has 9/10 PG-only checker-consistent and speedup-measured evidence across the shared target denominator. That said, it is still not a final @10 baseline because `PERF_0063` remains blocked by function-signature validation. This evidence remains PG-only, witness-scale, not cross-engine transfer, and not a final leaderboard.

## 6. Recommended Next Step
- `update baseline evidence matrix with Calcite HEP 9/10 rollup`

## 7. Non-Modification Note
No experiments were run for this rollup. No DB/checker/speedup activity occurred, no `PERF_0063` work occurred, and no registry/review/rules/EXECUTION_STATUS/case changes were made. The taxonomy note files remained untouched.
