# LONGTAIL SQLStorm Tri-Engine Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the current registry-backed LONGTAIL tri-engine draft set, with emphasis on the SQLStorm-derived longtail line.

Current scope:

- `LONGTAIL_0001`
- `LONGTAIL_0003`
- `LONGTAIL_0004`
- `LONGTAIL_0005`
- `LONGTAIL_0007`
- `LONGTAIL_0008`
- `LONGTAIL_0009`
- `LONGTAIL_0010`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0014`
- `LONGTAIL_0015`
- `LONGTAIL_0016`
- `LONGTAIL_0018`
- `LONGTAIL_0019`
- `LONGTAIL_0020`
- `LONGTAIL_0021`

These cases are the current registry-backed LONGTAIL tri-engine draft subset. Live case facts remain in:

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

> How should the current LONGTAIL tri-engine draft subset be organized for a later human review pass?

---

## 3. Count summary

| group | count | notes |
| --- | --- | --- |
| all LONGTAIL registry rows | `19` | current registry-backed LONGTAIL population |
| tri-engine LONGTAIL rows | `18` | `tri_engine_closure=yes` |
| SQLStorm tri-engine draft rows | `17` | current SQLStorm-derived witness-validated longtail draft set |
| manual / legacy anchor | `1` | `LONGTAIL_0001` |
| PG-only registered backlog | `1` | `LONGTAIL_0002` remains registered but not tri-engine |

---

## 4. Case summary table

| case_id | source family | SQLStorm source query / source_detail | validation state | plan artifact state | package status | review-prep note |
| --- | --- | --- | --- | --- | --- | --- |
| `LONGTAIL_0001` | `manual_seed` | manual long-tail anchor; non-external package | registry-backed tri-engine anchor | registry-backed tri-engine anchor | anchor package; older package layout | keep separate from SQLStorm cohort in later human review |
| `LONGTAIL_0003` | `SQLStorm` | `8708.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 success; early SQLStorm longtail cohort |
| `LONGTAIL_0004` | `SQLStorm` | `13845.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 success; early SQLStorm longtail cohort |
| `LONGTAIL_0005` | `SQLStorm` | `16141.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 success; lower-complexity SQLStorm draft |
| `LONGTAIL_0007` | `SQLStorm` | `12771.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-01 success; aggregation-focused SQLStorm draft |
| `LONGTAIL_0008` | `SQLStorm` | `12754.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after initial Spark-open state |
| `LONGTAIL_0009` | `SQLStorm` | `10183.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 success |
| `LONGTAIL_0010` | `SQLStorm` | `10923.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL parser-compatibility issue |
| `LONGTAIL_0011` | `SQLStorm` | `6625.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 success |
| `LONGTAIL_0012` | `SQLStorm` | `7247.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL-open state |
| `LONGTAIL_0013` | `SQLStorm` | `1298.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL-open state |
| `LONGTAIL_0014` | `SQLStorm` | `3369.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-02 success |
| `LONGTAIL_0015` | `SQLStorm` | `10979.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 success |
| `LONGTAIL_0016` | `SQLStorm` | `10426.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL parser-compatibility issue |
| `LONGTAIL_0018` | `SQLStorm` | `11204.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after MySQL-open state |
| `LONGTAIL_0019` | `SQLStorm` | `11951.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-03 success |
| `LONGTAIL_0020` | `SQLStorm` | `11294.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | wave-04 success |
| `LONGTAIL_0021` | `SQLStorm` | `11502.sql` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | repaired after earlier artifact-identity mismatch and MySQL-open state |

---

## 5. Evidence matrix

| case_id | PG result | PG plan | MySQL result | MySQL plan | Spark result | Spark plan | registry tri_engine_closure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LONGTAIL_0001` | registry-backed tri-engine anchor | registry-backed tri-engine anchor | registry-backed tri-engine anchor | registry-backed tri-engine anchor | registry-backed tri-engine anchor | registry-backed tri-engine anchor | `yes` |
| `LONGTAIL_0003` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0004` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0005` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0007` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0008` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0009` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0010` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0011` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0012` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0013` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0014` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0015` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0016` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0018` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0019` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0020` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `LONGTAIL_0021` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |

---

## 6. Coverage summary

Relative to the current performance-oriented TPC-H, TPC-DS, and JOB / IMDB groups, the LONGTAIL line contributes a different kind of review-prep value:

- more structurally irregular SQL than benchmark-template families
- more SQLStorm / StackOverflow-style analytical shapes built around outer joins, grouped summaries, CTEs, windows, and nullable attachment patterns
- stronger emphasis on controlled long-tail query shapes that are useful for cross-engine package hardening even when they are not canonical benchmark queries
- a visible construction history through SQLStorm waves plus targeted repairs, which makes the line useful for workflow and repair-discipline review as well as for query-shape coverage

At a high level, this line broadens:

- long-tail structural diversity
- outer-join-preservation and null-sensitive negative design
- case-local witness engineering over more irregular StackOverflow-style schemas
- cross-engine repair patterns for parser and artifact-identity issues

This remains useful even without formal review or admission because it strengthens later benchmark characterization and coverage discussion beyond the performance families alone.

---

## 7. Backlog / excluded cases

Explicitly excluded from the current tri-engine LONGTAIL packet:

- `LONGTAIL_0002`: registered PG-only legacy SQLStorm case
- `LONGTAIL_0006`: constructed but PG validation failed
- `LONGTAIL_0017`: constructed but PG validation failed

The remaining SQLStorm candidate pool also looks materially thinner than earlier waves:

- fewer low / medium-risk candidates remain
- later expansion should be deliberate rather than broad-wave by default
- remaining work is more likely to come from careful backlog repair or new longtail-source acquisition than from a large additional SQLStorm-only wave

---

## 8. Caveats and risks

- Witness data is small and case-local.
- Some repaired cases required narrow alias-compatibility changes to keep SQL text executable across engines.
- SQLStorm-derived cases are evidence-complete drafts, not formally reviewed cases.
- `LONGTAIL_0001` remains a legacy/manual anchor with an older package layout than the later SQLStorm cohort.
- This packet does not claim release-grade admission or any stronger benchmark-line movement.

---

## 9. Open questions for human reviewer

- Which LONGTAIL cases should enter a later formal review pass first?
- Should `LONGTAIL_0006` and `LONGTAIL_0017` be repaired, or left deferred?
- Should taxonomy tags be backfilled before the first human review pass on this line?
- Is additional longtail-source acquisition needed beyond the current SQLStorm candidate pool?

---

## 10. Bottom line

The current LONGTAIL pool now has a substantial registry-backed tri-engine draft subset:

- `18` tri-engine LONGTAIL cases overall
- `17` SQLStorm-derived tri-engine longtail drafts

That subset is useful for:

- benchmark coverage broadening
- later paper characterization
- later human review-prep ordering

This document records no status movement beyond registry-backed witness-validated draft facts.
