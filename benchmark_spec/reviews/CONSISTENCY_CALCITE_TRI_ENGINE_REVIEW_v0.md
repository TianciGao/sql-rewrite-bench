# CONSISTENCY Calcite Tri-Engine Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the current registry-backed Calcite-derived CONSISTENCY tri-engine draft set.

Current scope:

- `CONS_0005`
- `CONS_0006`
- `CONS_0007`
- `CONS_0008`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0013`
- `CONS_0014`
- `CONS_0015`
- `CONS_0016`
- `CONS_0017`
- `CONS_0018`
- `CONS_0019`
- `CONS_0020`
- `CONS_0021`
- `CONS_0022`
- `CONS_0023`
- `CONS_0024`
- `CONS_0025`
- `CONS_0026`
- `CONS_0027`
- `CONS_0028`
- `CONS_0029`
- `CONS_0030`

These cases are the current registry-backed Calcite-derived CONSISTENCY tri-engine draft subset. Live case facts remain in:

- `inventory/case_registry.csv`

This document is **review-prep only**.

---

## 2. Methodological boundary

This packet does **not** make:

- admission judgments
- promotion judgments
- `common-core` movement judgments
- `extended-line` movement judgments
- formal review completion claims

It summarizes current registry-backed package and evidence status only. The narrower question is:

> How should the current Calcite-derived CONSISTENCY tri-engine draft subset be organized for a later human review pass?

---

## 3. Count summary

| group | count | notes |
| --- | --- | --- |
| all CONS registry rows | `30` | current registry-backed CONS population |
| tri-engine CONS rows | `27` | `tri_engine_closure=yes` |
| Calcite tri-engine draft rows | `26` | current Calcite-derived witness-validated consistency draft set |
| manual / legacy anchor | `1` | `CONS_0001` |
| partial / legacy backlog | `3` | `CONS_0002`, `CONS_0003`, `CONS_0004` |
| constructed-but-unregistered Calcite backlog | `0` | none after wave-01 / wave-02 / wave-03 repairs |

---

First current-generation governance batch note:

- `CONS_0005`, `CONS_0007`, `CONS_0010`, `CONS_0011`, and `CONS_0024` now also have tracked case-root governance artifacts.
- `runs/result_check.json`: `validation_model=engine_local_witness`, `ok=true`, `draft_only=true`
- `runs/plan_check.json`: `validation_model=engine_local_plan_artifacts`, `status=complete`, `draft_only=true`
- registry `notes_link` now points to `cases/CONS/<CASE>/runs/plan_check.json`
- these cases remain `staged_not_yet_admitted` / not admitted / not under review drafts
- plan semantics are not formally reviewed
- this packet remains review-prep only and does not imply common-core promotion, admission, formal review closure, or release-grade closure

---

## 4. Case summary table

| case_id | source family | Calcite source query / source_detail | consistency focus if available | validation state | plan artifact state | package status | review-prep note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0005` | `Calcite` | `blank.iq correlated NOT IN table1/table2` | `null_semantics`, `anti_join_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | wave-01 direct success; useful null-sensitive anti-join anchor; registry `notes_link` points to `cases/CONS/CONS_0005/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0006` | `Calcite` | `blank.iq aggregate CASE seed` | `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after initial PG typing-compatibility issue |
| `CONS_0007` | `Calcite` | `blank.iq tmp_emps correlated EXISTS` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | wave-01 direct success; compact correlated EXISTS case; registry `notes_link` points to `cases/CONS/CONS_0007/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0008` | `Calcite` | `sub-query.iq multi-correlation EXISTS t0/t1/t2` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after initial Spark-open state |
| `CONS_0009` | `Calcite` | `sub-query.iq UNION ALL scalar predicate` | `set_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 direct success; set-op / scalar predicate coverage |
| `CONS_0010` | `Calcite` | `sub-query.iq NOT EXISTS EMP/BONUS duplicate-salary seed` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | repaired after MySQL compatibility issue; registry `notes_link` points to `cases/CONS/CONS_0010/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0011` | `Calcite` | `sub-query.iq LEFT JOIN BONUS NULL-filter EXISTS` | `outer_join_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | repaired after MySQL and Spark compatibility issues; registry `notes_link` points to `cases/CONS/CONS_0011/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0012` | `Calcite` | `sub-query.iq EXISTS LIMIT 1 OFFSET 2 threshold seed` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 direct success; explicit OFFSET-sensitive threshold case |
| `CONS_0013` | `Calcite` | `sub-query.iq alias-shadow NOT IN b1` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 direct success; alias-shadow scope case |
| `CONS_0014` | `Calcite` | `sub-query.iq alias-shadow NOT IN with preserved inner alias` | `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 direct success; paired alias-scope variant |
| `CONS_0015` | `Calcite` | `blank.iq global NOT IN OR i = 1` | `predicate_scope`, `null_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; predicate-scope and null-sensitive OR pattern |
| `CONS_0016` | `Calcite` | `blank.iq global NOT IN OR j = 2` | `predicate_scope`, `null_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; sibling predicate-scope variant |
| `CONS_0017` | `Calcite` | `blank.iq EXISTS boolean projection over tmp_emps` | `projection_scope`, `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; boolean-projection coverage |
| `CONS_0018` | `Calcite` | `sub-query.iq EXISTS over COUNT(*) guaranteed one row` | `subquery_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; aggregate-subquery guaranteed-row case |
| `CONS_0019` | `Calcite` | `sub-query.iq EXISTS over COUNT(*) with always-false filter` | `subquery_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; aggregate-subquery false-filter variant |
| `CONS_0020` | `Calcite` | `sub-query.iq NOT EXISTS over COUNT(*) HAVING FALSE` | `subquery_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; HAVING-based negative design |
| `CONS_0021` | `Calcite` | `sub-query.iq correlated UNION ALL scalar sum` | `set_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 direct success; correlated set-op aggregation case |
| `CONS_0022` | `Calcite` | `sub-query.iq EXISTS LEFT JOIN OR predicate` | `outer_join_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL compatibility issue |
| `CONS_0023` | `Calcite` | `sub-query.iq COMM > correlated join count` | `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL compatibility issue |
| `CONS_0024` | `Calcite` | `sub-query.iq LEFT JOIN EXISTS HAVING SUM` | `outer_join_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | repaired after initial PG witness-discrimination issue; registry `notes_link` points to `cases/CONS/CONS_0024/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0025` | `Calcite` | `sub-query.iq two-level nested dept EXISTS` | `subquery_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after narrow Spark nested-correlation compatibility issue |
| `CONS_0026` | `Calcite` | `sub-query.iq scalar group count from correlated subquery` | `aggregation_semantics`, `subquery_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after narrow Spark correlated-group compatibility issue |
| `CONS_0027` | `Calcite` | `sub-query.iq EXISTS inner join OR predicate` | `subquery_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 direct success; inner-join OR-predicate semantics |
| `CONS_0028` | `Calcite` | `sub-query.iq COMM > left-join correlated count` | `outer_join_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 direct success; correlated left-join count variant |
| `CONS_0029` | `Calcite` | `sub-query.iq LEFT JOIN BONUS EXISTS without NULL filter` | `outer_join_semantics`, `null_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 direct success; left-join EXISTS null-sensitivity variant |
| `CONS_0030` | `Calcite` | `sub-query.iq LEFT JOIN EXISTS HAVING SUM with name condition` | `outer_join_semantics`, `aggregation_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 direct success; HAVING + join + name-condition variant |

---

## 5. Evidence matrix

| case_id | PG result | PG plan | MySQL result | MySQL plan | Spark result | Spark plan | registry tri_engine_closure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0005` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0006` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0007` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0008` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0009` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0010` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0011` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0012` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0013` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0014` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0015` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0016` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0017` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0018` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0019` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0020` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0021` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0022` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0023` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0024` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0025` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0026` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0027` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0028` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0029` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0030` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |

---

## 6. Coverage summary

Relative to the current performance-oriented TPC-H, TPC-DS, and JOB / IMDB groups, the Calcite CONSISTENCY line adds a different kind of review-prep value:

- primary emphasis on semantic preservation rather than runtime-oriented benchmark behavior
- stronger concentration of correlated subqueries, EXISTS / NOT EXISTS, IN / NOT IN, scalar-subquery thresholds, and alias-scope cases
- more direct use of small witness data to prove `source = positive` and `source != negative`
- broader exposure to null-sensitive, duplicate-sensitive, aggregation-sensitive, predicate-scope, projection-scope, and outer-join-sensitive behaviors
- wave-03 additions through `CONS_0030` extend the line with more Spark-closed correlated-subquery, join-scope, OR-predicate, and aggregate-sensitive variants without changing the packet's conservative draft status

At a high level, the current Calcite-derived set contributes:

- subquery semantics as a first-class review surface
- anti-join and null-sensitive NOT IN behavior
- outer-join and null-filter correctness coverage
- aggregate / scalar-predicate and HAVING-sensitive correctness coverage
- alias-shadow, predicate-scope, and join-scope discipline cases that are less central in the performance families

This is useful even without formal review or admission because it strengthens the benchmark's correctness and semantic-preservation coverage in a way that is distinct from the performance-oriented TPC and JOB lines.

---

## 7. Backlog / excluded cases

Explicitly excluded from the current Calcite tri-engine packet:

- `CONS_0002`: registered Calcite PG-only legacy / pre-skeleton backlog
- `CONS_0003`: VeriEQL PG+MySQL partial; not part of this Calcite tri-engine packet
- `CONS_0004`: VeriEQL PG+MySQL partial; not part of this Calcite tri-engine packet

Additional scope notes:

- constructed Calcite wave-01 / wave-02 / wave-03 backlog is now empty after repairs
- remaining candidate pool may still contain unused Calcite drafts, but this packet is limited to the registry-backed tri-engine cases only

---

## 8. Caveats and risks

- Witness data is small and case-local.
- Some repaired cases required narrow cross-engine compatibility fixes to keep the SQL executable across PostgreSQL, MySQL, and Spark.
- These cases are evidence-complete drafts, not formally reviewed cases.
- This packet does not claim release-grade admission or stronger benchmark-line movement.
- `CONS_0001` through `CONS_0004` still carry older package or evidence-layout caveats relative to the later Calcite case-local cohort.

---

## 9. Open questions for human reviewer

- Which Calcite consistency cases should enter a later formal review pass first?
- Should `CONS_0002` be backfilled into the newer package pattern, or replaced by the stronger later Calcite cohort?
- Should `CONS_0003` and `CONS_0004` be Spark-closed, or handled instead in a separate VeriEQL-oriented packet?
- Should taxonomy tags be calibrated before the first human review pass on this line?
- Should the remaining unused Calcite candidates become a later wave beyond the current registry-backed set?

---

## 10. Bottom line

The current Calcite consistency line now has a substantial registry-backed tri-engine draft subset:

- `26` Calcite-derived tri-engine consistency drafts
- `27` tri-engine CONS cases overall when the manual anchor `CONS_0001` is included

That subset is useful for:

- correctness / semantic-preservation coverage
- later human review-prep ordering
- later benchmark characterization distinct from the performance families

This document records no status movement beyond registry-backed witness-validated draft facts.
