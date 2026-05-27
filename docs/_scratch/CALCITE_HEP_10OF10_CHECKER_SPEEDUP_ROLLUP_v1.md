# CALCITE_HEP_10OF10_CHECKER_SPEEDUP_ROLLUP_v1

## 0. Purpose And Boundary
This is a Calcite HEP checker+speedup rollup for the full 10/10 measured target denominator. It is PG-only, witness-scale, not cross-engine transfer, not a leaderboard, and records no new experiment.

## 1. Evidence Timeline
- original 4-case subset established bounded checker+speedup evidence for `PERF_0006`, `PERF_0008`, `PERF_0033`, and `PERF_0054`
- `CALCITE_HEP_10CASE_EXPANSION_PREFLIGHT_v1` established the shared target denominator and identified `PERF_0063` as the main risk
- the first missing 5-case checker batch exposed a readiness/report-path contract issue rather than a SQL-quality issue
- checker rerun after the readiness fix produced five newly checker-consistent cases: `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0052`
- the missing 5-case speedup batch measured those five cases and the sanity audit passed with a witness-scale caveat
- `PERF_0063` first failed under CAST-based `substr` normalization
- `PERF_0063` then succeeded after case-specific adapter-local substring-surface normalization from `substr(ca_zip, 1, 5)` to `substring(ca_zip FROM 1 FOR 5)`
- `PERF_0063` speedup then completed and its sanity audit passed with a witness-scale caveat

## 2. Coverage Summary
| target_10case_denominator | checker_consistent_count | speedup_measured_count | remaining_blockers | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| 10 | 10 | 10 | `[]` | `measured` | `calcite_hep_10of10_checker_speedup_rollup_not_leaderboard` |

## 3. Subset Metrics
| subset | cases | checker_consistent | speedup_measured | gm_speedup | win/tie/loss | regression_count@20 | measurement_failure_count | timeout_count | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| existing_4case_subset | `PERF_0006, PERF_0008, PERF_0033, PERF_0054` | 4/4 | 4/4 | `0.9588741913559858` | `0/3/1` | `0` | `0` | `0` | bounded PG-only subset, not final baseline |
| fixed_5case_missing_batch | `PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0052` | 5/5 | 5/5 | `0.9588328711588356` | `0/4/1` | `1` | `0` | `0` | bounded PG-only witness-scale batch after readiness fix |
| perf_0063_single_case | `PERF_0063` | 1/1 | 1/1 | `0.8226009820411391` | `0/0/1` | `1` | `0` | `0` | case-specific adapter-local substring normalization; still witness-scale |
| combined_10of10_measured_target | `PERF_0006, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0052, PERF_0054, PERF_0063` | 10/10 | 10/10 | `0.9442674761138092` | `0/7/3` | `2` | `0` | `0` | PG-only witness-scale rollup, not cross-engine transfer and not leaderboard evidence |

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
| PERF_0063 | measured_after_substring_surface_fix | consistent | measured | `0.8226009820411391` | `loss` | `true` | `/tmp/rewritebench_calcite_hep_perf_0063_speedup_v1.json` | required case-specific adapter-local substring normalization; case source file unchanged |

## 5. Interpretation
Calcite HEP now has 10/10 PG-only checker+speedup measured evidence on the target denominator. This is materially stronger than the earlier 4-case subset and the intermediate 9/10 boundary. It nevertheless remains PG-only and witness-scale, not cross-engine transfer, and not a final leaderboard. `PERF_0063` required case-specific adapter-local substring normalization without editing the case source package.

## 6. Recommended Next Step
- `update baseline evidence matrix with Calcite HEP 10/10 rollup`

## 7. Non-Modification Note
No experiments were run for this rollup. No DB/checker/speedup activity occurred, no case reruns occurred, and no registry/review/rules/EXECUTION_STATUS/case changes were made. Taxonomy notes remained untouched.
