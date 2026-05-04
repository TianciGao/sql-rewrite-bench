# TAXONOMY_SOURCE_OF_TRUTH_ALIGNMENT_NOTE_v0

## 1. Status

This is a scratch governance alignment note for RQ4 taxonomy handling.

It is not taxonomy writeback.

It is not registry writeback.

## 2. Source-of-Truth Hierarchy

The intended governance hierarchy is:

- `taxonomy/*.yaml`
  - vocabulary and definition layer
  - defines allowed tag families, tag IDs, and semantic meaning
  - this is the controlled vocabulary source of truth
- `manifest.yaml` case tags
  - intended stable case-level annotation layer
  - this is where durable case taxonomy should ultimately live once reviewed
  - these tags should be stable enough to support paper-facing aggregation without relying on temporary draft files
- `taxonomy_trial_v0.x.yaml`
  - draft / review / calibration / hardening layer
  - used to propose, test, and harden case-level taxonomy before stable writeback
  - useful for bounded experimentation on metadata quality, but not itself the final governance destination
- `inventory/case_registry.csv`
  - live status / governance facts layer
  - should track case status, maturity, role, admission posture, and related governance facts
  - should not become the full case-level taxonomy payload store

## 3. Why `taxonomy_trial` Was Used

`taxonomy_trial_v0.x.yaml` was used because the project needed a bounded way to:

- harden specific case metadata without immediately overwriting stable case annotation
- test slicer behavior on draft tags
- capture reviewer-facing proposals for cases such as `PERF_0033` and `PERF_0054`

This makes `taxonomy_trial` operationally useful for RQ4 hardening, but it does not make `taxonomy_trial` equal to final case metadata.

## 4. Explicit Empty vs Missing

The current parser fix establishes an important governance distinction:

- `sql_feature_tags: []`
  - explicit empty
  - means the case was reviewed and no high-signal SQL feature tag from the current vocabulary was judged appropriate
  - this is a valid annotation outcome
- missing `sql_feature_tags`
  - metadata gap
  - means the case still lacks reviewed annotation for that category

The slicer must distinguish these two states.

Otherwise, reviewer-approved "no-feature" judgments would be incorrectly counted as unresolved metadata gaps.

## 5. Current P0 State

Current P0 state is:

- `PERF_0033` and `PERF_0054` now have `taxonomy_trial_v0.3.yaml` drafts
- those drafts are now usable for current draft slicing
- the parser now treats their explicit-empty `sql_feature_tags` as explicit-empty rather than missing
- both cases are no longer counted as portability-tag gaps because `limit_fetch_gap` is now parsed correctly

Boundary:

- this is not registry writeback
- this is not formal admission
- this is not final stable case annotation

The next governance question is whether the reviewed P0 tags should be written into stable `manifest.yaml` tags.

## 6. Policy For RQ4 Draft vs Final

Draft RQ4 slicing may read `taxonomy_trial` files with explicit provisional caveats.

Final paper-facing RQ4 feature-level rates should rely on:

- stable `manifest.yaml` case tags, or
- another explicitly approved stable case-metadata layer

Any rate that depends materially on `taxonomy_trial` should be labeled draft / provisional until stable case metadata is updated.

## 7. What Not To Do

- do not keep accumulating trial files indefinitely without deciding whether tags should be promoted into stable case metadata
- do not treat `case_registry.csv` as the full taxonomy label store
- do not write taxonomy tag payloads into the registry
- do not treat scratch calibration notes as applied metadata

## 8. Recommended Next Action

- create a bounded manifest tag writeback proposal for P0 cases `PERF_0033` and `PERF_0054`, without applying it yet

## 9. Claim Boundaries

- no taxonomy writeback
- no manifest changes
- no registry writeback
- no formal review update
- no final RQ4 claim

## 10. Verification / Non-Modification Note

- only this note was created
- no case files were modified
- no taxonomy files were modified
- no registry files were modified
- no SQL or database workload was run
- no model or LLM call was made
- no SQLGlot execution or generation was run
- no checker was run
- `docs/EXECUTION_STATUS.md` was not changed
- taxonomy calibration notes were untouched
