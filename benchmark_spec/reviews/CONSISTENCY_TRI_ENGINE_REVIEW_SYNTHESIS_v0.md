# CONSISTENCY Tri-Engine Review Synthesis v0

## 1. Document role and scope

This document is a short **review-prep synthesis note** over the current registry-backed consistency review-prep packets for:

- Calcite-derived consistency drafts
- VeriEQL-derived consistency drafts

Its role is limited to:

- cross-packet comparison
- review-prep ordering support
- conservative paper-table planning

Live case facts remain in:

- `inventory/case_registry.csv`

This document is **not** a formal admission review, promotion decision, `common-core` movement, `extended-line` movement, or formal-review completion claim.

---

## 2. Methodological boundary

This synthesis does **not** make:

- admission judgments
- promotion judgments
- `common-core` movement judgments
- `extended-line` movement judgments
- formal review completion claims

It summarizes current registry-backed draft status only. The narrower question is:

> How should the current Calcite and VeriEQL consistency draft lines be read together before a later human review pass?

---

## 3. Count summary

| group | count | notes |
| --- | --- | --- |
| all CONS registry rows | `40` | current registry-backed CONS population |
| tri-engine CONS rows | `37` | `tri_engine_closure=yes` |
| Calcite tri-engine drafts | `26` | `CONS_0005` through `CONS_0030` |
| VeriEQL tri-engine drafts | `10` | `CONS_0031` through `CONS_0040` |
| manual / legacy anchor | `1` | `CONS_0001` |
| partial / legacy backlog | `3` | `CONS_0002`, `CONS_0003`, `CONS_0004` |

---

## 4. Packet summary

| packet | covered cases | source family | current role | evidence state | caveats |
| --- | --- | --- | --- | --- | --- |
| `benchmark_spec/reviews/CONSISTENCY_CALCITE_TRI_ENGINE_REVIEW_v0.md` | `CONS_0005`–`CONS_0030` | `Calcite` | registry-backed Calcite consistency tri-engine draft line | PG/MySQL/Spark result checks and plan artifacts present across all covered cases | broader line, but still draft-only; some cases required narrow cross-engine compatibility repairs |
| `benchmark_spec/reviews/CONSISTENCY_VERIEQL_TRI_ENGINE_REVIEW_v0.md` | `CONS_0031`–`CONS_0040` | `VeriEQL` | registry-backed VeriEQL consistency tri-engine draft line | PG/MySQL/Spark result checks and plan artifacts present across all covered cases | smaller and newer line; still draft-only; some cases required narrow compatibility or witness-design repairs |

---

## 5. Coverage comparison

The Calcite line contributes the broader consistency substrate. It covers a larger spread of Calcite SQL test-resource shapes, with strong representation of correlated subqueries, `EXISTS`, `NOT EXISTS`, `IN`, `NOT IN`, aggregation-sensitive patterns, and alias-, predicate-, and join-sensitivity cases.

The VeriEQL line contributes an independently sourced equivalence-style supplement built from the VeriEQL / Calcite-397 subset. Its emphasis is still semantic preservation, but it adds a distinct source family and more controlled equivalence-style patterns around alias-scope, predicate-scope, projection-scope, join-sensitive, and aggregation-sensitive behaviors.

Taken together, the two lines are complementary rather than redundant:

- Calcite provides the broader and more mature consistency draft line
- VeriEQL adds an independently sourced correctness line with a different construction history
- both lines strengthen semantic-preservation coverage in ways that the performance-oriented packets do not target directly

---

## 6. Evidence status comparison

Across both packets, the common evidence pattern is:

- registry-backed tri-engine witness-validated draft status
- PostgreSQL result checks present
- PostgreSQL plan artifacts present
- MySQL result checks present
- MySQL plan artifacts present
- Spark result checks present
- Spark plan artifacts present

Additionally, the first CONS current-generation governance batch now covers `8` cases:

- `5` Calcite cases: `CONS_0005`, `CONS_0007`, `CONS_0010`, `CONS_0011`, `CONS_0024`
- `3` VeriEQL cases: `CONS_0031`, `CONS_0034`, `CONS_0037`

For these `8` cases:

- case-root `runs/result_check.json` is present with `validation_model=engine_local_witness`, `ok=true`, and `draft_only=true`
- case-root `runs/plan_check.json` is present with `validation_model=engine_local_plan_artifacts`, `status=complete`, and `draft_only=true`
- registry `notes_link` now points to `cases/CONS/<CASE>/runs/plan_check.json`
- they remain `staged_not_yet_admitted` / not admitted drafts
- plan semantics are not formally reviewed
- this does not imply admission, common-core promotion, formal review closure, or release-grade closure

What that does **not** imply by default:

- admitted status
- promoted status
- `common-core` movement
- `extended-line` movement
- formal review completion

These are evidence-complete draft lines, with case-local artifacts and registry-backed closure, not finalized review outcomes.

---

## 7. Backlog and exclusions

Items outside the two current packets:

- `CONS_0001`: manual legacy tri-engine anchor; useful as a correctness anchor, but not part of the Calcite or VeriEQL review-prep packets
- `CONS_0002`: Calcite PG-only legacy / pre-skeleton backlog
- `CONS_0003`: VeriEQL PG+MySQL partial with older package layout
- `CONS_0004`: VeriEQL PG+MySQL partial with older package layout

Additional scope note:

- no constructed-but-unregistered Calcite or VeriEQL wave backlog remains after the current repair passes
- broader CONS pool still needs taxonomy tagging and may still need additional governance normalization outside the first 8-case current-generation batch

---

## 8. Recommended paper-table usage

Conservative paper-table shells that this synthesis can support:

- consistency source-family count table
- tri-engine evidence table
- semantic coverage table
- backlog / legacy caveat table

These tables can describe current benchmark readiness and source-family composition without implying that all cases have already passed a formal review gate.

---

## 9. Open questions before formal review

- Should taxonomy calibration be completed before the first formal consistency review pass?
- Should `CONS_0002`, `CONS_0003`, and `CONS_0004` be backfilled into newer package layouts, or retired as legacy backlog?
- Which subset should enter formal review first: the broader Calcite line, the newer VeriEQL line, or a mixed pilot subset?
- Should remaining VeriEQL candidates become a later wave-02?
- Does manual anchor `CONS_0001` need package-layout hardening before it is used as a stronger review reference point?

---

## 10. Bottom line

The current consistency pool now has a substantial registry-backed tri-engine draft core:

- `26` Calcite-derived tri-engine drafts
- `10` VeriEQL-derived tri-engine drafts
- `37` tri-engine CONS cases overall when the manual anchor is included

Calcite and VeriEQL provide complementary correctness and semantic-preservation coverage.

This document records no status movement beyond registry-backed witness-validated draft facts.
