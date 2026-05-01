# CONSISTENCY VeriEQL Tri-Engine Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the current registry-backed VeriEQL-derived CONSISTENCY tri-engine draft set.

Current scope:

- `CONS_0031`
- `CONS_0032`
- `CONS_0033`
- `CONS_0034`
- `CONS_0035`
- `CONS_0036`
- `CONS_0037`
- `CONS_0038`
- `CONS_0039`
- `CONS_0040`

These cases are the current registry-backed VeriEQL-derived CONSISTENCY tri-engine draft subset. Live case facts remain in:

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

> How should the current VeriEQL-derived CONSISTENCY tri-engine draft subset be organized for a later human review pass?

---

## 3. Count summary

| group | count | notes |
| --- | --- | --- |
| all CONS registry rows | `40` | current registry-backed CONS population |
| tri-engine CONS rows | `37` | `tri_engine_closure=yes` |
| VeriEQL tri-engine draft rows | `10` | current VeriEQL-derived witness-validated consistency draft set |
| VeriEQL legacy / partial rows | `2` | `CONS_0003`, `CONS_0004` |
| constructed-but-unregistered VeriEQL backlog | `0` | none after wave-01 repairs |

---

First current-generation governance batch note:

- `CONS_0031`, `CONS_0034`, and `CONS_0037` now also have tracked case-root governance artifacts.
- `runs/result_check.json`: `validation_model=engine_local_witness`, `ok=true`, `draft_only=true`
- `runs/plan_check.json`: `validation_model=engine_local_plan_artifacts`, `status=complete`, `draft_only=true`
- registry `notes_link` now points to `cases/CONS/<CASE>/runs/plan_check.json`
- these cases remain `staged_not_yet_admitted` / not admitted / not under review drafts
- plan semantics are not formally reviewed
- this packet remains review-prep only and does not imply common-core promotion, admission, formal review closure, or release-grade closure

---

## 4. Case summary table

| case_id | source family | VeriEQL source query / source_detail | consistency focus if available | validation state | plan artifact state | package status | review-prep note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0031` | `VeriEQL` | `Calcite-397 / 23 EXISTS and NOT EXISTS over EMP` | `subquery_semantics`, `anti_join_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | repaired after alias-compatibility and witness-discrimination issues; registry `notes_link` points to `cases/CONS/CONS_0031/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0032` | `VeriEQL` | `Calcite-397 / 46 correlated NOT IN over derived EMP rows` | `subquery_semantics`, `anti_join_semantics`, `null_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | direct wave-01 success; compact correlated `NOT IN` null-sensitive case |
| `CONS_0033` | `VeriEQL` | `Calcite-397 / 48 correlated NOT IN against DEPT names` | `subquery_semantics`, `anti_join_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after witness ordering / discrimination issue |
| `CONS_0034` | `VeriEQL` | `Calcite-397 / 94 LEFT JOIN CASE aggregation rewrite` | `outer_join_semantics`, `aggregation_semantics`, `projection_scope` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | repaired after narrow Spark alias compatibility issue; registry `notes_link` points to `cases/CONS/CONS_0034/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0035` | `VeriEQL` | `Calcite-397 / 103 COUNT(nullable mgr) simplification` | `aggregation_semantics`, `null_semantics` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | direct wave-01 success; compact null-sensitive aggregate case |
| `CONS_0036` | `VeriEQL` | `Calcite-397 / 124 HAVING predicate pushdown on DEPT names` | `aggregation_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | direct wave-01 success; HAVING / predicate-scope coverage |
| `CONS_0037` | `VeriEQL` | `Calcite-397 / 223 COUNT(DISTINCT joined name) under removable LEFT JOIN` | `duplicate_semantics`, `outer_join_semantics`, `aggregation_semantics` | PG/MySQL/Spark result checks all `ok=true`; case-root `runs/result_check.json` `ok=true` (`engine_local_witness`, `draft_only=true`) | PG/MySQL/Spark plan checks all `ok=true`; case-root `runs/plan_check.json` `status=complete` (`engine_local_plan_artifacts`, `draft_only=true`) | formal skeleton complete; release-grade incomplete | direct wave-01 success; duplicate-sensitive left-join aggregate case; registry `notes_link` points to `cases/CONS/CONS_0037/runs/plan_check.json`; `staged_not_yet_admitted` / not admitted / plan semantics not formally reviewed |
| `CONS_0038` | `VeriEQL` | `Calcite-397 / 319 boolean EXISTS projection over EMP` | `subquery_semantics`, `projection_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after narrow MySQL/Spark compatibility issue in positive rewrite |
| `CONS_0039` | `VeriEQL` | `Calcite-397 / 346 EXISTS disjunction over EMP` | `subquery_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after narrow MySQL/Spark compatibility issue in positive rewrite |
| `CONS_0040` | `VeriEQL` | `Calcite-397 / 359 null-sensitive IN with CASTed deptno` | `null_semantics`, `subquery_semantics`, `predicate_scope` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after narrow cross-engine compatibility cleanup around null-sensitive `IN` |

---

## 5. Evidence matrix

| case_id | PG result | PG plan | MySQL result | MySQL plan | Spark result | Spark plan | registry tri_engine_closure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CONS_0031` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0032` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0033` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0034` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0035` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0036` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0037` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0038` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0039` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `CONS_0040` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |

---

## 6. Coverage summary

Relative to the current performance-oriented TPC-H, TPC-DS, JOB / IMDB, and longtail groups, the VeriEQL CONSISTENCY line adds a different kind of review-prep value:

- primary emphasis on semantic preservation rather than runtime-oriented benchmark behavior
- direct use of Calcite-397 / VeriEQL-derived equivalence patterns that were selected for controlled source-to-positive and source-to-negative discrimination
- concentrated coverage of `EXISTS`, `NOT EXISTS`, `IN`, and `NOT IN` shapes under correlated and null-sensitive conditions
- additional attention to duplicate-sensitive, aggregation-sensitive, outer-join-sensitive, predicate-scope, and projection-scope behaviors
- a compact EMP / DEPT / BONUS-style schema family that makes small witness-data reasoning easier to inspect during later review

At a high level, the current VeriEQL-derived set contributes:

- correlated subquery and anti-join review surfaces that complement the larger Calcite packet
- more explicit null-sensitive `IN` / `NOT IN` and boolean-`EXISTS` projection patterns
- HAVING, COUNT, COUNT(DISTINCT), and nullable aggregate cases with small discriminating witnesses
- additional join-scope, predicate-scope, and projection-scope correctness cases

This complements the Calcite CONSISTENCY packet rather than replacing it. The Calcite line is broader and already more mature as a registry-backed subgroup, while the VeriEQL line contributes a separate controlled source family with its own equivalence patterns and repair history.

---

## 7. Backlog / excluded cases

Explicitly excluded from the current VeriEQL tri-engine packet:

- `CONS_0003`: VeriEQL PG+MySQL partial with older package / evidence layout; not part of this tri-engine packet
- `CONS_0004`: VeriEQL PG+MySQL partial with older package / evidence layout; not part of this tri-engine packet

Additional scope notes:

- constructed VeriEQL wave-01 backlog is now empty after repairs
- remaining VeriEQL candidate drafts may still exist, but they are not part of this registry-backed tri-engine packet

---

## 8. Caveats and risks

- Witness data is small and case-local.
- Some repaired cases required narrow cross-engine compatibility fixes to keep the SQL executable across PostgreSQL, MySQL, and Spark.
- These cases are evidence-complete drafts, not formally reviewed cases.
- This packet does not claim release-grade admission or stronger benchmark-line movement.
- `CONS_0003` and `CONS_0004` still carry older package or evidence-layout caveats relative to the later VeriEQL case-local cohort.

---

## 9. Open questions for human reviewer

- Which VeriEQL consistency cases should enter a later formal review pass first?
- Should `CONS_0003` and `CONS_0004` be backfilled into the newer package and evidence layout, or left as legacy partials?
- Should taxonomy tags be calibrated before the first human review pass on this line?
- Should the remaining VeriEQL candidates become a later wave-02?
- Should this packet later be merged into a consistency-wide synthesis alongside the Calcite packet?

---

## 10. Bottom line

The current VeriEQL consistency line now has a registry-backed tri-engine draft subset of meaningful size:

- `10` VeriEQL-derived tri-engine consistency drafts
- `37` tri-engine CONS cases overall when the manual anchor, Calcite line, and VeriEQL line are viewed together

That subset is useful for:

- correctness / semantic-preservation coverage
- later human review-prep ordering
- cross-family consistency synthesis with the Calcite packet

This document records no status movement beyond registry-backed witness-validated draft facts.
