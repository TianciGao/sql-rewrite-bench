# TPC-DS Tri-Engine Performance Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the current registered TPC-DS-derived tri-engine performance draft set.

Current scope:

- `PERF_0002`
- `PERF_0033`
- `PERF_0034`
- `PERF_0035`
- `PERF_0036`
- `PERF_0038`
- `PERF_0043`
- `PERF_0044`
- `PERF_0047`
- `PERF_0050`
- `PERF_0052`
- `PERF_0053`
- `PERF_0054`
- `PERF_0056`
- `PERF_0062`
- `PERF_0063`
- `PERF_0065`
- `PERF_0066`
- `PERF_0071`
- `PERF_0072`
- `PERF_0073`
- `PERF_0074`
- `PERF_0075`
- `PERF_0076`

These 24 cases are the current registry-backed TPC-DS tri-engine performance set. Live case facts remain in:

- `inventory/case_registry.csv`

This document is **review-prep only**.

Current governance split inside this 24-case tri-engine review-prep set:

- 18 governed cases now have tracked current-generation `runs/result_check.json` and `runs/plan_check.json`, and registry `notes_link` now points to `cases/PERF/<CASE>/runs/plan_check.json`:
  - standard-checker batch: `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0036`, `PERF_0038`, `PERF_0043`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0063`, `PERF_0066`, `PERF_0076`
  - case-specific-normalization batch: `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0053`, `PERF_0065`
- 5 tri-engine cases remain deferred from current-generation governance backfill because positive-output mismatch still needs human review:
  - `PERF_0071`, `PERF_0072`, `PERF_0073`, `PERF_0074`, `PERF_0075`

---

## 2. Methodological boundary

This packet does **not** make:

- admission judgments
- promotion judgments
- `common-core` movement judgments
- `extended-line` movement judgments
- formal review completion claims

It summarizes current registry-backed package and artifact evidence only. The narrower question is:

> How should the current TPC-DS tri-engine performance set be organized for a later human review pass?

---

## 3. Batch summary table

| case_id | TPC-DS query/template identity | validation state | plan artifact state | package status | review-prep note |
| --- | --- | --- | --- | --- | --- |
| `PERF_0002` | `query53.tpl` materialized instance | tri-engine closure is registry-backed; current case-local six-check JSON bundle is not laid out under the later `runs/` pattern | tri-engine closure is registry-backed; current case-local six-check JSON bundle is not laid out under the later `runs/` pattern | formal skeleton complete; release-grade incomplete | legacy admitted external common-core case; treat separately from the later staged-draft cohort |
| `PERF_0033` | `query55.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0034` | `query56.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0035` | `query57.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0036` | `query58.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0038` | `query10a.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0043` | `query35a.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0044` | `query36a.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | case-specific-normalization governed staged draft; normalization limited to documented engine formatting only; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0047` | `query70a.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | case-specific-normalization governed staged draft; normalization limited to documented engine formatting only; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0050` | `query86a.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | case-specific-normalization governed staged draft; normalization limited to documented engine formatting only; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0052` | `query1.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0053` | `query2.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | case-specific-normalization governed staged draft; normalization limited to documented engine formatting only; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0054` | `query3.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0056` | `query6.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0062` | `query13.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0063` | `query15.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0065` | `query17.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | case-specific-normalization governed staged draft; normalization limited to documented engine formatting only; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0066` | `query19.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |
| `PERF_0071` | `query25.tpl` materialized instance | tri-engine closure remains registry-backed, but current-generation governance backfill stays deferred because positive-output mismatch needs human review | existing tri-engine plan artifacts remain part of review-prep evidence; no current-generation governance upgrade claimed here | formal skeleton complete; release-grade incomplete | deferred from governance backfill; keep out of governed staged subset until mismatch is resolved |
| `PERF_0072` | `query26.tpl` materialized instance | tri-engine closure remains registry-backed, but current-generation governance backfill stays deferred because positive-output mismatch needs human review | existing tri-engine plan artifacts remain part of review-prep evidence; no current-generation governance upgrade claimed here | formal skeleton complete; release-grade incomplete | deferred from governance backfill; keep out of governed staged subset until mismatch is resolved |
| `PERF_0073` | `query28.tpl` materialized instance | tri-engine closure remains registry-backed, but current-generation governance backfill stays deferred because positive-output mismatch needs human review | existing tri-engine plan artifacts remain part of review-prep evidence; no current-generation governance upgrade claimed here | formal skeleton complete; release-grade incomplete | deferred from governance backfill; keep out of governed staged subset until mismatch is resolved |
| `PERF_0074` | `query29.tpl` materialized instance | tri-engine closure remains registry-backed, but current-generation governance backfill stays deferred because positive-output mismatch needs human review | existing tri-engine plan artifacts remain part of review-prep evidence; no current-generation governance upgrade claimed here | formal skeleton complete; release-grade incomplete | deferred from governance backfill; keep out of governed staged subset until mismatch is resolved |
| `PERF_0075` | `query30.tpl` materialized instance | tri-engine closure remains registry-backed, but current-generation governance backfill stays deferred because positive-output mismatch needs human review | existing tri-engine plan artifacts remain part of review-prep evidence; no current-generation governance upgrade claimed here | formal skeleton complete; release-grade incomplete | deferred from governance backfill; keep out of governed staged subset until mismatch is resolved |
| `PERF_0076` | `query31.tpl` materialized instance | tracked current-generation `runs/result_check.json` with `ok=true`, `draft_only=true` | tracked current-generation `runs/plan_check.json` with `status=complete`, `draft_only=true` | formal skeleton complete; release-grade incomplete | standard-checker governed staged draft; registry `notes_link` now points to `runs/plan_check.json` |

---

## 4. Evidence matrix

| case_id | PG result | PG plan | MySQL result | MySQL plan | Spark result | Spark plan | registry tri_engine_closure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0002` | registry-backed tri-engine case | registry-backed tri-engine case | registry-backed tri-engine case | registry-backed tri-engine case | registry-backed tri-engine case | registry-backed tri-engine case | `yes` |
| `PERF_0033` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0034` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0035` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0036` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0038` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0043` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0044` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0047` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0050` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0052` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0053` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0054` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0056` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0062` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0063` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0065` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0066` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0071` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0072` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0073` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0074` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0075` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |
| `PERF_0076` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `ok=true` | `yes` |

For the 18 governed cases listed above, the current review-prep evidence now also includes tracked case-root `runs/result_check.json` and `runs/plan_check.json`, and registry `notes_link` now points to `cases/PERF/<CASE>/runs/plan_check.json`. For `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0053`, and `PERF_0065`, the result check uses documented case-specific normalization limited to engine output formatting differences only. `PERF_0071`–`PERF_0075` remain outside this governed subset because their positive-output mismatch still needs human review.

---

## 5. Coverage summary

Relative to the current TPC-H and JOB / IMDB performance lines, TPC-DS adds a different kind of review-prep value:

- template-derived analytical diversity rather than a smaller fixed set of hand-recognizable benchmark query names
- broader parameterized reporting shapes across year, month, week, state, county, education, and market-like dimensions
- more visible aggregate-heavy and grouped-reporting variants, with some source-detail signals for windows, ordering, and set-style reporting families
- a higher-volume template family where source/positive equivalence and source/negative divergence can be reviewed as a repeated package pattern rather than as one-off query engineering

At a high level, the TPC-DS line contributes:

- broader template-family coverage than TPC-H
- more analytical-template regularity than JOB / IMDB
- a useful middle ground between stable benchmark templates and tri-engine package engineering reuse

This makes it suitable as a paper-table group in its own right, while still remaining complementary to TPC-H and JOB / IMDB.

---

## 6. Backlog / excluded cases

Explicitly excluded from this packet:

- `PERF_0005`
- `PERF_0032`
- `PERF_0037`
- `PERF_0039`
- `PERF_0040`
- `PERF_0041`
- `PERF_0042`
- `PERF_0045`
- `PERF_0046`
- `PERF_0048`
- `PERF_0049`
- `PERF_0051`
- `PERF_0055`
- `PERF_0057`
- `PERF_0058`
- `PERF_0059`
- `PERF_0060`
- `PERF_0061`
- `PERF_0064`
- `PERF_0067`
- `PERF_0068`
- `PERF_0069`
- `PERF_0070`

Grouped by reason:

### 6.1 PG-only cases

- `PERF_0005`
- `PERF_0032`
- `PERF_0037`
- `PERF_0039`
- `PERF_0040`
- `PERF_0041`
- `PERF_0042`
- `PERF_0045`
- `PERF_0049`
- `PERF_0051`
- `PERF_0055`
- `PERF_0057`
- `PERF_0058`
- `PERF_0059`
- `PERF_0060`
- `PERF_0061`
- `PERF_0064`
- `PERF_0067`
- `PERF_0068`
- `PERF_0069`
- `PERF_0070`

These remain outside the tri-engine packet because registry facts still show `validated_engines=pg` and no tri-engine closure.

### 6.2 PG + MySQL but Spark-open cases

- `PERF_0046`
- `PERF_0048`

These remain outside the tri-engine packet because registry facts still show `validated_engines=pg|mysql` and `tri_engine_closure=no`.

### 6.3 Known deferred / human-decision cases

- `PERF_0032`

`docs/EXECUTION_STATUS.md` still calls out `PERF_0032` as pending a separate human SQL normalization decision, so it should not be treated as routine tri-engine backlog.

### 6.4 Data-quality note

The earlier malformed-row issue on `PERF_0005` has already been repaired in `inventory/case_registry.csv`. It is therefore excluded here because it is PG-only, not because of any remaining CSV parse problem.

---

## 7. Caveats and risks

- Witness data is small and case-local.
- Template parameters and portability-sensitive functions may still need later human review.
- Generated packages are evidence-complete drafts, not formally reviewed cases.
- This packet does not claim release-grade admission beyond current registry facts.

---

## 8. Open questions for human reviewer

- Which TPC-DS cases should enter a later formal review pass first?
- Should later review be grouped by template family or by rewrite pattern?
- Which remaining deferred or PG-only cases are worth repairing later?
- Should taxonomy or mapping backfill be done before the first human review pass on this line?

---

## 9. Bottom line

TPC-DS now has a substantial registered tri-engine performance set at **24 cases**.

That set is suitable for:

- paper-table preparation
- later human review-prep ordering
- comparison against the current TPC-H and JOB / IMDB groups

This document records no status movement beyond current registry facts.
