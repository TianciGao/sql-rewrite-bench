# TAXONOMY_METADATA_HARDENING_PLAN_FOR_RQ4_v0

## 1. Status

This is a tracked scratch metadata hardening plan for the current RQ4 sliced experiment cases.

It is a hardening plan only, not taxonomy writeback.

## 2. Why This Exists

The current paper-facing RQ4 table draft already exists, but feature-level RQ4 rates are only as reliable as the metadata behind them.

Current taxonomy slicing coverage is complete at the case level, but the evidence is mixed:

- some cases rely mainly on manifest tags
- some cases have missing `taxonomy_trial*.yaml`
- some cases have placeholder or provisional taxonomy trial files
- `taxonomy_trial_v0.3.yaml` parsing now correctly distinguishes explicit-empty tags from missing tags

Before treating feature-level RQ4 rates as final paper claims, these metadata gaps need to be hardened explicitly.

## 3. Current Metadata Caveat Summary

- `sql_feature_gap_count=0`
- `portability_tag_gap_count=1`
- `workload_realism_gap_count=2`
- `taxonomy_trial_missing_count=4`
- `taxonomy_trial_placeholder_or_empty_count=5`
- `taxonomy_trial_provisional_count=1`

Interpretation:

- all 12 sliced cases have usable metadata for the current draft
- current coverage depends heavily on manifest tags
- feature-level rates are not yet final-quality until the missing / placeholder / provisional taxonomy metadata is normalized

## 4. Per-Case Hardening Table

| case_id | pool | source_family | taxonomy_trial_status | missing tag categories | current claim risk | recommended hardening action |
|---|---|---|---|---|---|---|
| `PERF_0006` | performance | `TPC-H` | `placeholder_or_empty` | none | medium | `replace_placeholder_taxonomy_trial` |
| `PERF_0008` | performance | `TPC-H` | `placeholder_or_empty` | none | medium | `replace_placeholder_taxonomy_trial` |
| `PERF_0013` | performance | `TPC-H` | `placeholder_or_empty` | none | medium | `replace_placeholder_taxonomy_trial` |
| `PERF_0017` | performance | `TPC-H` | `placeholder_or_empty` | none | medium | `replace_placeholder_taxonomy_trial` |
| `PERF_0024` | performance | `TPC-H` | `placeholder_or_empty` | none | medium | `replace_placeholder_taxonomy_trial` |
| `PERF_0033` | performance | `TPC-DS` | `usable_for_current_slicing` | none | low | `no_action_needed` |
| `PERF_0054` | performance | `TPC-DS` | `usable_for_current_slicing` | none | low | `no_action_needed` |
| `CONS_0007` | consistency | `Calcite` | `missing` | `portability_tags`, `workload_realism_tags` | medium | `create_taxonomy_trial_from_manifest_tags`; `fill_missing_portability_tags`; `fill_missing_workload_realism_tags` |
| `CONS_0012` | consistency | `Calcite` | `missing` | `workload_realism_tags` | medium | `create_taxonomy_trial_from_manifest_tags`; `fill_missing_workload_realism_tags` |
| `PORT_0004` | portability | `PARROT` | `provisional` | none | medium | `review_provisional_taxonomy_trial` |
| `PORT_0012` | portability | `PARROT` | `missing` | none | medium | `create_taxonomy_trial_from_manifest_tags` |
| `PORT_0022` | portability | `PARROT` | `missing` | none | low | `create_taxonomy_trial_from_manifest_tags` |

Notes:

- `PERF_0033` and `PERF_0054` are now cleared as P0 hardening targets.
- both cases now parse as `usable_for_current_slicing`, carry `metadata_missing_flags=[]`, and no longer contribute to portability tag gaps.
- both cases still appear in the SQL-feature `untagged` bucket because their `sql_feature_tags=[]` is an explicit-empty assignment rather than a missing tag.
- `CONS_0007` and `CONS_0012` do not block the current common-core correctness packet, but they still weaken final RQ4 feature-level coverage if left manifest-only.
- `PORT_0004` already has a trial file, but it is still marked provisional and should not be treated as fully hardened metadata.

## 5. Priority Order

### P0: Cases blocking final RQ4 feature-level rates

- cleared in the current patch cycle

Reason:

- no unresolved P0 blocker remains after the v0.3 parser fix plus the bounded `PERF_0033` / `PERF_0054` trial-file patch
- the next remaining hardening pressure is on placeholder / provisional trial quality rather than P0 missing-tag gaps

### P1: Cases with placeholder or provisional taxonomy_trial

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PORT_0004`

Reason:

- the tags are present enough for current slicing
- the trial files are not yet in a stable final-quality state

### P2: Cases where manifest tags are adequate but taxonomy_trial should be normalized later

- `CONS_0007`
- `CONS_0012`
- `PORT_0012`
- `PORT_0022`

Reason:

- current slicing can still use manifest-derived metadata
- taxonomy trial normalization is still needed before treating feature-level rates as fully hardened

## 6. Recommended Hardening Policy

- do not edit registry yet
- do not treat scratch taxonomy notes as writeback
- harden case-local `taxonomy_trial*.yaml` first
- rerun taxonomy slicing after the case-local metadata is hardened
- only after that consider whether any registry or formal review layer needs synchronized writeback

This keeps the hardening order aligned with the repository’s governance separation:

- case-local taxonomy evidence first
- aggregate slicing refresh second
- narrative or governance propagation only after evidence is stable

## 7. Concrete Next Action

- create a bounded taxonomy hardening patch plan for the P1 placeholder / provisional cases only, without applying it yet

## 8. Claim Boundaries

- no taxonomy writeback
- no registry writeback
- no case modification
- no final RQ4 result
- no formal review update

## 9. Verification / Non-Modification Note

- only this plan was created
- no SQL or database workload was run
- no model or LLM call was made
- no SQLGlot execution or generation was run
- no checker was run
- no registry was changed
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- no taxonomy files were changed
- taxonomy calibration notes were untouched
