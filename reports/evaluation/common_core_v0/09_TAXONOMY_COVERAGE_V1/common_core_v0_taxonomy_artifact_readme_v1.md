# Common-core v0 Taxonomy Artifact Readme v1

## Inputs inspected

- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_all_registry_cases_v1.csv`
- `reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_existing_values_patch_v1.csv`
- `inventory/case_registry.csv` for `source_family` only
- `taxonomy/*.yaml` for formal taxonomy-axis definitions only

## Outputs created

- `common_core_v0_taxonomy_coverage_v1.csv`
- `common_core_v0_taxonomy_coverage_v1.md`
- `common_core_v0_taxonomy_by_pool_v1.csv`
- `common_core_v0_case_tag_matrix_v1.csv`
- `common_core_v0_taxonomy_artifact_readme_v1.md`

## Exact aggregation rules

- Canonical unit: retained `normalized_tags`.
- A case is covered by an axis if at least one normalized tag begins with `axis:`.
- Distinct tags are counted as distinct normalized tag strings within the axis.
- Top tags are sorted by descending frequency, with alphabetical tie-breaks, and truncated to top 5.
- Pool tables use only the 40-case Common-core denominator, not all-registry rows.

## How primary vs secondary were detected

- Primary tags were counted when the second namespace component was exactly `primary`.
- Secondary tags were counted when the second namespace component was exactly `secondary`.
- No additional primary/secondary inference was applied.

## How confirmed vs suspected portability were detected

- Confirmed portability tags were counted when the namespace matched `portability:confirmed:*`.
- Suspected portability tags were counted when the namespace matched `portability:suspected:*`.
- No portability severity or merge layer was invented beyond the retained normalized strings.

## Limitations

- These artifacts characterize a controlled 40-case surface, not production query frequency.
- Tag frequency should not be read as semantic importance.
- The case matrix preserves retained normalized strings; it does not reconcile ambiguities beyond existing normalization.
- Empty namespace cells mean no retained tag in that namespace for that case; they do not imply the construct is impossible or absent outside retained tagging.
- All-registry tag coverage was inspected for context, but the paper-facing denominator here remains Common-core v0 only.

## Whether source-of-truth writeback is needed

- No. These are aggregation artifacts built from retained freeze inputs and formal taxonomy files only.
