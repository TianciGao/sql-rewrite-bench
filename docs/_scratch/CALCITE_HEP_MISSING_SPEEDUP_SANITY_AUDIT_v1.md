# CALCITE_HEP_MISSING_SPEEDUP_SANITY_AUDIT_v1

## 0. Purpose And Boundary
This is a read-only sanity audit of the Calcite HEP missing-case speedup batch. It does not execute SQL, rerun speedup, rerun generation, rerun checker, or perform any registry writeback.

## 1. Source Artifacts
- speedup report path: `docs/_scratch/CALCITE_HEP_MISSING_SPEEDUP_AFTER_READINESS_FIX_v1.md`
- batch JSON path: `/tmp/rewritebench_calcite_hep_missing_speedup_after_readiness_fix_v1.json`
- per-case result root: runtime arrays are present in the batch JSON; no separate per-case runtime JSON files were discovered under `/tmp`
- expected case list:
  - `PERF_0013`
  - `PERF_0017`
  - `PERF_0019`
  - `PERF_0024`
  - `PERF_0052`
- artifacts present/missing:
  - all 5 expected cases are present in the batch JSON
  - no separate per-case runtime JSON files were found, but this is not blocking because the batch JSON stores per-case runtime arrays directly

## 2. Runtime Array / Repeat Check
| case_id | source run count | candidate run count | warmup policy visible | measured arrays present |
| --- | --- | --- | --- | --- |
| PERF_0013 | 5 | 5 | yes | yes |
| PERF_0017 | 5 | 5 | yes | yes |
| PERF_0019 | 5 | 5 | yes | yes |
| PERF_0024 | 5 | 5 | yes | yes |
| PERF_0052 | 5 | 5 | yes | yes |

Warmup exclusion check:
- the report declares `1` optional warmup per query
- stored runtime arrays contain exactly `5` measured source runs and `5` measured candidate runs for each case
- this is consistent with warmup being excluded from the measured arrays

## 3. Metric Recalculation
| case_id | source median | candidate median | recomputed speedup | reported speedup | W/T/L check | regression@20 check |
| --- | --- | --- | --- | --- | --- | --- |
| PERF_0013 | 0.627483 | 0.644344 | 0.9738323007586009 | 0.9738323007586009 | match (`tie`) | match (`false`) |
| PERF_0017 | 0.393879 | 0.386998 | 1.017780453645755 | 1.017780453645755 | match (`tie`) | match (`false`) |
| PERF_0019 | 0.301961 | 0.297356 | 1.01548648757718 | 1.01548648757718 | match (`tie`) | match (`false`) |
| PERF_0024 | 0.341967 | 0.342732 | 0.9977679352963833 | 0.9977679352963833 | match (`tie`) | match (`false`) |
| PERF_0052 | 0.338447 | 0.41939 | 0.8069982593767138 | 0.8069982593767138 | match (`loss`) | match (`true`) |

## 4. Batch-level Recalculation
- recomputed `gm_speedup` = `0.9588328711588356`
- reported `gm_speedup` = `0.9588328711588356`
- recomputed win/tie/loss counts = `0/4/1`
- recomputed regression count = `1`
- reported measurement failure count = `0`
- reported timeout count = `0`

## 5. Witness-scale Caveat
All five measured cases are sub-ms or near-sub-ms. Paper wording should keep this bounded to witness-scale evidence rather than broader performance claims.

Safe wording:
“Calcite HEP measured 9/10 checker-consistent cases after the readiness fix, but the newly measured 5-case slice remains bounded PG-only witness-scale evidence and is not a final performance leaderboard.”

## 6. Classification
- `measurement_sanity_passed_with_witness_scale_caveat`

## 7. Recommended Next Step
- `create Calcite HEP 9/10 checker+speedup rollup`

## 8. Non-Modification Note
No generation rerun, no speedup rerun, no DB/checker execution, no `PERF_0063` work, and no registry/review/rules/EXECUTION_STATUS/case changes occurred.
