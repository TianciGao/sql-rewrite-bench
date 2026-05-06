# CALCITE_HEP_PERF_0063_SPEEDUP_SANITY_AUDIT_v1

## 0. Purpose And Boundary
This is a read-only sanity audit for the stored `PERF_0063` Calcite HEP speedup result. It does not execute SQL, does not rerun speedup, does not rerun generation, does not run checker, and does not write back to registries.

## 1. Source Artifacts
- speedup report path: `docs/_scratch/CALCITE_HEP_PERF_0063_SPEEDUP_v1.md`
- speedup JSON path: `/tmp/rewritebench_calcite_hep_perf_0063_speedup_v1.json`
- referenced artifact paths:
  - candidate SQL: `/tmp/calcite-hep-wrapper/real-route/perf_0063.sql`
  - checker output: `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0063.json`
  - candidate result TSV: `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0063.tsv`
  - source result TSV: `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0063.tsv`
- artifacts present/missing:
  - speedup JSON: present
  - candidate SQL: present
  - checker output: present
  - candidate result TSV: present
  - source result TSV: present

## 2. Runtime Array / Repeat Check
- source run count: `5`
- candidate run count: `5`
- warmup policy visible: `yes`
- measured arrays present: `yes`
- warmup runs appear excluded from the stored runtime arrays because the arrays contain exactly five measured runs per side, matching the stated repeat policy

## 3. Metric Recalculation
- source median: recomputed `0.351643`, reported `0.351643`
- candidate median: recomputed `0.427477`, reported `0.427477`
- recomputed speedup: `0.8226009820411391`
- reported speedup: `0.8226009820411391`
- W/T/L check: recomputed `loss`, reported `loss`
- regression@20 check: recomputed `true`, reported `true`

## 4. Witness-scale Caveat
`PERF_0063` remains witness-scale because both source and candidate medians are sub-ms. Paper wording should stay bounded and non-leaderboard. Safe wording:

“PERF_0063 completed Calcite HEP PG-only speedup measurement after substring-surface normalization, but the result remains bounded witness-scale evidence and not a final leaderboard result.”

## 5. Classification
- `measurement_sanity_passed_with_witness_scale_caveat`

## 6. Recommended Next Step
- `create Calcite HEP 10/10 checker+speedup final rollup`

## 7. Non-Modification Note
No generation rerun occurred, no speedup rerun occurred, no DB or checker activity occurred, no existing 9-case rerun occurred, and no registry/review/rules/EXECUTION_STATUS/case changes were made.
