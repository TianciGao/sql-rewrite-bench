# PAPER_RESULTS_TABLES_DRAFT_v0

## 1. Status

This is a paper results table draft for the current expanded experiment state.

## 2. How To Use This Draft

These tables are paper-facing draft material assembled from the current expanded evidence packets.

They should be used with four constraints in mind:

- they are not a final leaderboard
- route denominators differ by packet and should not be collapsed into one uniform denominator
- PORT results are PostgreSQL-side only
- taxonomy slicing reflects current metadata quality, not final taxonomy closure

## 3. Table 1: Denominator Composition

| packet | cases | pool / source | role | current claim boundary |
| --- | ---: | --- | --- | --- |
| seed common-core | `9` | mixed `PERF` + `CONS`; `TPC-H`, `TPC-DS`, `Calcite` | seed end-to-end common-core packet | full seed pipeline only |
| Batch 2A PERF | `19` | `PERF`; PostgreSQL analytical expansion | expanded PERF execution / checker / speedup packet | route coverage differs; not final leaderboard |
| Batch 2B CONS | `3` | `CONS`; PostgreSQL consistency expansion | checker-backed consistency expansion | narrow CONS extension only |
| Batch 3A PERF | `11` | `PERF`; PostgreSQL later ready-lane expansion | later PERF execution + speedup packet | route coverage differs; not final leaderboard |
| Batch 3B PERF | `4` | `PERF`; PostgreSQL paper-draft override slice | bounded PERF execution + checker + speedup packet | paper-draft override only; registry unchanged |
| seed PORT | `3` | `PORT`; bounded PostgreSQL seed packet | initial portability route / stress packet | PostgreSQL-only; not cross-engine closure |
| Batch 2C PORT | `3` | `PORT`; bounded PostgreSQL expansion | portability route-matrix and policy-consistency expansion | PostgreSQL-only; no denominator expansion by itself |

Current expanded evidence totals:

- expanded common-core: `46` cases
- expanded PORT: `6` PostgreSQL-side cases

## 4. Table 2: RQ1 Correctness / Validity

| method / route | denominator | executable | consistency / guard metric | failure mode if any | claim boundary |
| --- | --- | --- | --- | --- | --- |
| seed controls | seed common-core `9` | complete | control correctness / guard complete | none | seed packet only |
| `SQLGLOT_OPT_SAME_DIALECT` | seed common-core `9` | `9 / 9` | generated-method consistency `9 / 9` | none on seed | seed-only generated-method evidence |
| `LLM_DIRECT_REWRITE_STRONG` | seed common-core `9` | `9 / 9` | generated-method consistency `9 / 9` | none on seed | seed-only generated-method evidence |
| Batch 2B CONS controls | Batch 2B CONS `3` | native `3 / 3`, positive `3 / 3`, negative `3 / 3` | `ResultConsistencyRate=1.0`, `NegativeRejectionRate=1.0`, `FalseAcceptRate=0.0` | none | consistency expansion only |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 2A PERF `19` | generation `19 / 19`, PG execution `19 / 19` | exact TSV consistency `19 / 19`, `ResultConsistencyRate=1.0` | none on Batch 2A | separate baseline candidate, not replacement |
| `SQLGLOT_OPT_SAME_DIALECT` | Batch 2A PERF `19` | success `4 / 19`, failed `15 / 19` | capability boundary exposed rather than closed consistency | `OptimizeError=13`, `UndefinedColumn=2` | boundary evidence only |
| Batch 3B PERF controls | Batch 3B PERF `4` | native `4 / 4`, positive `4 / 4`, negative `4 / 4` | positive equality `4 / 4`, negative differs `4 / 4` | none | paper-draft override slice only |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 3B PERF `4` | generation `4 / 4`, PG execution `4 / 4` | checker consistency `4 / 4`, `ResultConsistencyRate=1.0` | none on Batch 3B | separate baseline candidate, not replacement |
| `SQLGLOT_OPT_SAME_DIALECT` | Batch 3B PERF `4` | success `1 / 4`, failed `3 / 4` | capability boundary persists rather than closed consistency | `OptimizeError=3` | paper-draft boundary evidence only |

## 5. Table 3: RQ2 Performance

| method / route | denominator | GM_Speedup | W / T / L | RegressionRate@20% | notes |
| --- | --- | ---: | --- | --- | --- |
| `HUMAN_REFERENCE_POSITIVE` | seed PERF `7` | `0.96159127168004` | `1 / 2 / 4` | `0 / 7` | seed positive-control runtime |
| `SQLGLOT_OPT_SAME_DIALECT` | seed PERF `7` | `0.9709643241218479` | `1 / 2 / 4` | `0 / 7` | seed-only optimize route |
| `LLM_DIRECT_REWRITE_STRONG` | seed PERF `7` | `1.0023345046000625` | `1 / 5 / 1` | `0 / 7` | seed-only method runtime |
| `HUMAN_REFERENCE_POSITIVE` | Batch 2A PERF `19` | `0.9733` | `4 / 9 / 6` | `3 / 19` | expanded PERF positive-control runtime |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 2A PERF `19` | `1.0119` | `4 / 13 / 2` | `0 / 19` | separate SQLGlot no-opt baseline candidate |
| `HUMAN_REFERENCE_POSITIVE` | Batch 3A PERF `11` | `0.9984` | `0 / 10 / 1` | `0 / 11` | later ready-PERF runtime slice; Batch 3A route-record execution `22 / 22` with row-count match `22 / 22` |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 3A PERF `11` | `1.0023` | `2 / 7 / 2` | `0 / 11` | later ready-PERF runtime slice; still a separate SQLGlot baseline candidate |
| `HUMAN_REFERENCE_POSITIVE` | Batch 3B PERF `4` | `0.9853` | `1 / 1 / 2` | `0 / 4` | bounded paper-draft runtime slice; registry unchanged |
| `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` | Batch 3B PERF `4` | `0.9841` | `1 / 2 / 1` | `0 / 4` | bounded paper-draft runtime slice; still a separate SQLGlot baseline candidate |

## 6. Table 4: RQ2 Plan Observability

| plan role / pair | readiness | top-node change count | attribution status | notes |
| --- | --- | ---: | --- | --- |
| source plans | `9 / 9` parseable | n/a | not computed | seed common-core only |
| human positive plans | `9 / 9` parseable | `2 / 9` | not computed | source-positive pair ready `9 / 9` |
| hard negative plans | `9 / 9` parseable | `2 / 9` | not computed | source-negative pair ready `9 / 9` |
| SQLGlot method plans | `9 / 9` parseable | `0 / 9` | not computed | source-SQLGlot pair ready `9 / 9` |
| Direct LLM method plans | `9 / 9` parseable | `1 / 9` | not computed | source-LLM pair ready `9 / 9` |

## 7. Table 5: RQ3 Portability

| route | packet | PG success | PG failure | consistency / diagnostic result | token usage | failure highlights | claim boundary |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `SQLGLOT_TRANSPILE` | seed PORT `3` | `2` | `1` | executable seed reference consistency: exact consistent `0`, exact inconsistent `2` | n/a | `PORT_0012 InvalidDatetimeFormat` | PostgreSQL-only route evidence |
| `LLM_DIRECT_TRANSLATE` | seed PORT `3` | `3` | `0` | `PORT_0004` exact consistent; `PORT_0022` normalized-consistent; `PORT_0012` report-local PG-normalized-reference consistent | `1317` seed matrix, plus `480` targeted canary | stress-case success on `PORT_0012` | PostgreSQL-only route evidence |
| `SQLGLOT_TRANSPILE` | Batch 2C PORT `3` | `2` | `1` | policy-consistent `2 / 3` | n/a | `PORT_0013 UndefinedFunction / SUM(boolean)` | bounded PostgreSQL slice only |
| `LLM_DIRECT_TRANSLATE` | Batch 2C PORT `3` | `3` | `0` | checker-consistent `3 / 3` under selected policy | `1278` | `PORT_0024` closes under normalized TSV policy | bounded PostgreSQL slice only |

Combined current PostgreSQL-side PORT summary:

- SQLGlot: PG success `4 / 6`, PG failure `2 / 6`
- Direct LLM: PG success `6 / 6`, PG failure `0 / 6`
- combined Direct LLM token usage across seed matrix + Batch 2C: `2595`

## 8. Table 6: RQ4 Coverage / Failure Slicing

### 8.1 Coverage / Composition

| slice | count | note |
| --- | ---: | --- |
| total sliced cases | `12` | current metadata-backed slice |
| common-core | `9` | main common-core evidence line |
| PORT snapshot | `3` | bounded portability slice |
| common-core performance | `7` | PERF speedup denominator |
| common-core consistency | `2` | consistency line outside first-pass GM speedup |
| `TPC-H` | `5` | dominant current common-core source family |
| `TPC-DS` | `2` | smaller analytical block |
| `Calcite` | `2` | consistency subline |
| `PARROT` | `3` | current bounded portability source family |

### 8.2 SQL Feature Buckets

| bucket | count |
| --- | ---: |
| `date_time_function` | `8` |
| `correlated_subquery` | `3` |
| `expression_complexity` | `3` |
| `subquery_in_from` | `2` |
| `untagged` | `2` |

### 8.3 Rewrite Opportunity Buckets

| bucket | count |
| --- | ---: |
| `predicate_pushdown` | `7` |
| `join_reorder` | `4` |
| `dialect_adaptation` | `3` |
| `function_normalization` | `3` |
| `materialization_strategy` | `3` |
| `subquery_decorrelation` | `3` |
| `expression_simplification` | `2` |
| `order_limit_simplification` | `1` |

### 8.4 Metadata Caveats

| caveat | count |
| --- | ---: |
| `sql_feature_gap_count` | `0` |
| `portability_tag_gap_count` | `1` |
| `workload_realism_gap_count` | `2` |
| `taxonomy_trial_missing_count` | `4` |
| `taxonomy_trial_placeholder_or_empty_count` | `5` |
| `taxonomy_trial_provisional_count` | `1` |

## 9. Cross-Cutting Interpretation Bullets

- the expanded denominator exposed a major `SQLGLOT_OPT_SAME_DIALECT` capability boundary that the seed packet did not reveal
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remains broadly executable / consistent across Batch 2A, Batch 3A, and Batch 3B, but speedup gains remain close to neutral
- Direct LLM shows stronger PostgreSQL-side PORT coverage than SQLGlot on the current bounded six-case sample
- human positive and SQLGlot no-opt both remain close to neutral, with tie-heavy runtime behavior on the expanded PERF slices
- the `SQLGLOT_OPT_SAME_DIALECT` capability boundary persists from Batch 2A into Batch 3A and Batch 3B
- feature-level slicing is already useful for paper analysis, but metadata hardening is still incomplete

## 10. Non-Claim Boundaries

- no final benchmark leaderboard
- no registry / admission decision
- no full cross-engine PORT closure
- no attribution
- no final taxonomy writeback
- no uniform denominator across all routes yet

## 11. Recommended Next Action

- use this table draft to write the paper results section, while separately deciding whether to stop at `46 + 6` or run one last small bounded PORT or CONS expansion only if it can be completed quickly

## 12. Verification / Non-Modification Note

- only this table draft was created
- no SQL / database / model / SQLGlot / checker execution
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched
