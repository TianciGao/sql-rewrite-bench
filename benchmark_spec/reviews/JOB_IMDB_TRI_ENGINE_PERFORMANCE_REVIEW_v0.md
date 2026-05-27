# JOB / IMDB Tri-Engine Performance Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the current registered JOB / IMDB-derived tri-engine performance draft set.

Current scope:

- `PERF_0077`
- `PERF_0078`
- `PERF_0080`
- `PERF_0081`
- `PERF_0082`
- `PERF_0083`
- `PERF_0084`
- `PERF_0085`
- `PERF_0086`
- `PERF_0090`
- `PERF_0091`
- `PERF_0093`
- `PERF_0094`
- `PERF_0095`
- `PERF_0096`
- `PERF_0097`
- `PERF_0101`
- `PERF_0102`
- `PERF_0103`
- `PERF_0104`
- `PERF_0105`
- `PERF_0106`
- `PERF_0107`
- `PERF_0108`
- `PERF_0109`

These 25 cases are registry-backed tri-engine performance drafts. Live case facts remain in:

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

It summarizes current package and artifact evidence only, so it answers a narrower question:

> How should the current JOB / IMDB tri-engine evidence-complete draft set be organized for a later human review pass?

---

## 3. Batch summary table

| case_id | JOB source query | draft/source origin | validation state | plan artifact state | package status | review-prep note |
| --- | --- | --- | --- | --- | --- | --- |
| `PERF_0077` | `JOB 3a.sql` | `JOB_DRAFT_0003` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft; use as wave-02 anchor |
| `PERF_0078` | `17a.sql` | `JOB_DRAFT_0017` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft; source identity should be reviewed carefully because registry wording is more generic than later rows |
| `PERF_0080` | `1b.sql` | `JOB_DRAFT_0001` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft |
| `PERF_0081` | `4a.sql` | `JOB_DRAFT_0004` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft |
| `PERF_0082` | `5a.sql` | `JOB_DRAFT_0005` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft |
| `PERF_0083` | `6a.sql` | `JOB_DRAFT_0006` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft |
| `PERF_0084` | `12a.sql` | `JOB_DRAFT_0012` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | early promoted JOB draft |
| `PERF_0085` | `7a.sql` | `JOB_DRAFT_0007` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | later registry reconciliation after artifact repair; keep an eye on evidence provenance notes |
| `PERF_0086` | `8a.sql` | `JOB_DRAFT_0008` | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | end of initial promoted-draft cohort |
| `PERF_0090` | `10a.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0091` | `13b.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0093` | `16a.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0094` | `18b.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0095` | `20a.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0096` | `32b.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0097` | `33a.sql` | local corpus wave 05 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | first direct local corpus cohort |
| `PERF_0101` | `16d.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0102` | `17a.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0103` | `18a.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0104` | `21b.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0105` | `22c.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0106` | `23b.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0107` | `27c.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0108` | `30a.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |
| `PERF_0109` | `31c.sql` | local corpus wave 06 | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | formal skeleton complete; release-grade incomplete | second direct local corpus cohort |

---

## 4. Evidence matrix

| case_id | PG result | PG plan | MySQL result | MySQL plan | Spark result | Spark plan | registry tri_engine_closure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0077` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0078` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0080` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0081` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0082` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0083` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0084` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0085` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0086` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0090` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0091` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0093` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0094` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0095` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0096` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0097` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0101` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0102` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0103` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0104` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0105` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0106` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0107` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0108` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0109` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |

---

## 5. Coverage summary

Relative to the current TPC-H and TPC-DS performance lines, the JOB / IMDB packet adds a different style of tri-engine evidence:

- more join-heavy query shapes over many smaller schema fragments rather than a smaller number of canonical benchmark stars
- stronger emphasis on old-style comma-join source SQL that is normalized into explicit join form in the positive rewrite
- broader IMDB-style entity linking across title, cast, company, keyword, info, and relationship-oriented tables
- more cases where the negative rewrite is a deliberate join/filter perturbation rather than a simpler aggregate-only divergence

In practical review terms, this line helps broaden:

- join normalization coverage
- multi-table selective join coverage
- case-local witness design for hard negatives
- cross-engine package patterns for real-world SQL that is less templated than TPC-H/TPC-DS

The line therefore looks useful as a complementary paper-table group, not as a replacement for TPC-H or TPC-DS.

---

## 6. Backlog / excluded cases

Explicitly excluded from this packet:

- `PERF_0003`: legacy JOB case; PG + MySQL only; Spark closure still missing in registry
- `PERF_0004`: legacy JOB case; PG-only; MySQL / Spark closure still missing in registry
- `PERF_0079`: unresolved; not registered in the JOB / IMDB tri-engine set
- `PERF_0087`: unresolved; not registered in the JOB / IMDB tri-engine set
- `PERF_0092`: failed / not registered; wave-05 batch history records failure at `mysql_validation`
- `PERF_0100`: failed / not registered; wave-06 batch history records failure at `mysql_validation`

These exclusions are intentional. This packet is limited to the 25 registry-backed JOB / IMDB tri-engine drafts only.

---

## 7. Caveats and risks

- Witness data is small and case-local; it is enough for controlled divergence checks, not for any stronger semantic completeness claim.
- Text-like and collation-sensitive behavior may still need later human review.
- Generated or promoted packages are evidence-complete for current tri-engine draft purposes, but they are not yet formally reviewed.
- This packet does not claim release-grade admission or any stronger benchmark-line movement.

---

## 8. Open questions for human reviewer

- Which JOB / IMDB cases should enter a later formal review pass first?
- Should later review be grouped by query family, by cohort, or by rewrite pattern?
- Which unresolved backlog cases, if any, are worth repairing later?
- Should taxonomy or mapping backfill be done before the first human review pass on this line?

---

## 9. Bottom line

The current repository now has **25 JOB / IMDB-derived registry-backed tri-engine performance drafts**.

They are suitable for:

- paper-table preparation
- later human review-prep ordering
- comparison against the already established TPC-H and TPC-DS tri-engine groups

They are **not** being advanced here beyond current registry facts. This document records evidence organization only.
