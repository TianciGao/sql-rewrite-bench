# Case Package Contract Audit v1

## Scope and method

- Repository branch audited: `artifact/case-package-contract-alignment-clean`.
- Common-core v0 case set source: `reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`.
- The retained manifest has `120` engine rows and `40` unique case packages; this audit de-duplicates by `case_id`.
- This was a read-only audit of existing files. No databases, SQL execution, registry edits, benchmark rule edits, paper evidence edits, deletions, or status changes were performed.

## Aggregate contract snapshot

| Metric | Count |
| --- | ---: |
| case packages audited | 40 |
| has manifest.yaml | 40 |
| has source.sql | 40 |
| has schema/data layer | 40 |
| has checker | 36 |
| has PostgreSQL validation evidence | 40 |
| has MySQL validation evidence | 40 |
| has Spark validation evidence | 40 |
| has manifest taxonomy tags | 40 |
| has standalone taxonomy/trial file | 13 |
| has top-level provenance block | 13 |
| has provenance files | 26 |

## Colleague-reported issue verification

### 1. Provenance consistency

Status: **confirmed**. The Common-core v0 packages are not provenance-uniform: some use a top-level `provenance:` block, many use `source` / `source_*` manifest fields without a top-level provenance block, and some also carry case-local `provenance/` files.

- Cases with top-level `provenance:` block: `PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054, PERF_0056, PERF_0062`.
- Cases with source/source_* fields but no provenance block: `CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037, LONGTAIL_0011, LONGTAIL_0012, LONGTAIL_0013, LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024, PERF_0024, PERF_0077, PERF_0082, PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025`.
- Cases with provenance files/directories: `LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024, PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054, PERF_0056, PERF_0062, PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025`.
- Provenance styles: `{'explicit_manifest_block_and_case_local_files': 13, 'implicit_source_fields_only': 14, 'source_fields_plus_case_local_files_no_manifest_block': 13}`.
- Evidence paths: per-case `manifest.yaml` plus case-local `provenance/` directories where present, e.g. `cases/PERF/PERF_0006/provenance/raw_record.json` and `cases/PORT/PORT_0003/provenance/parrot_source_record.json`.
- Recommended release-facing fix: add a top-level `provenance:` block to every Common-core manifest. Where provenance files already exist, link them from the block; where only source fields exist, migrate those fields into a structured provenance block and optionally add case-local notes/source-record files.
- Blocking issue for public artifact release: **blocking for contract cleanliness / release-facing schema consistency**, but generally not evidence-absence when source fields or provenance files are already present.

### 2. Taxonomy / tags consistency

Status: **confirmed**. Manifest tags and standalone taxonomy trial files coexist inconsistently.

- Cases with manifest tags: `CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037, LONGTAIL_0011, LONGTAIL_0012, LONGTAIL_0013, LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024, PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054, PERF_0056, PERF_0062, PERF_0077, PERF_0082, PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025`.
- Cases with standalone taxonomy files: `CONS_0024, PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0054, PORT_0003, PORT_0004, PORT_0005`.
- Cases with both manifest tags and standalone taxonomy files: `CONS_0024, PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0054, PORT_0003, PORT_0004, PORT_0005`.
- Taxonomy status counts: `{'confirmed_both_manifest_tags_and_standalone_trial_taxonomy_files': 13, 'not_confirmed_manifest_tags_only': 27}`.
- Evidence paths: standalone files such as `cases/CONS/CONS_0024/taxonomy_trial_v0.3.yaml` explicitly identify themselves as draft/trial artifacts, while corresponding `manifest.yaml` files already contain `tags:` blocks.
- Recommended release-facing fix: keep manifest `tags:` as the release-facing location. Migrate any missing taxonomy content into manifest tags, then archive or remove standalone `taxonomy_trial*.yaml` files in a later cleanup pass after review. Do not delete them in this audit.
- Blocking issue for public artifact release: **blocking for clean artifact packaging if standalone trial files are shipped as first-class taxonomy**, but not blocking for tag availability when manifest tags already cover the case.

### 3. Multiple positive / negative rewrites in PORT cases

Status: **confirmed for specific PORT cases; not an error by default**. Multiple rewrite files are used as engine/dialect variants in some PORT packages.

| case_id | positives | negatives | evidence | interpretation |
| --- | ---: | ---: | --- | --- |
| PORT_0003 | 2 | 2 | `cases/PORT/PORT_0003/rewrite_pos_01.sql;cases/PORT/PORT_0003/rewrite_pos_02_spark.sql; cases/PORT/PORT_0003/rewrite_neg_01.sql;cases/PORT/PORT_0003/rewrite_neg_02_spark.sql` | engine/dialect variant naming present |
| PORT_0004 | 2 | 2 | `cases/PORT/PORT_0004/rewrite_pos_01.sql;cases/PORT/PORT_0004/rewrite_pos_02_spark.sql; cases/PORT/PORT_0004/rewrite_neg_01.sql;cases/PORT/PORT_0004/rewrite_neg_02_spark.sql` | engine/dialect variant naming present |
| PORT_0005 | 2 | 2 | `cases/PORT/PORT_0005/rewrite_pos_01.sql;cases/PORT/PORT_0005/rewrite_pos_02_spark.sql; cases/PORT/PORT_0005/rewrite_neg_01.sql;cases/PORT/PORT_0005/rewrite_neg_02_spark.sql` | engine/dialect variant naming present |
| PORT_0013 | 2 | 2 | `cases/PORT/PORT_0013/rewrite_pos_01.sql;cases/PORT/PORT_0013/rewrite_pos_02_spark.sql; cases/PORT/PORT_0013/rewrite_neg_01.sql;cases/PORT/PORT_0013/rewrite_neg_02_spark.sql` | engine/dialect variant naming present |

- Recommended release-facing fix: represent rewrites as `positive_rewrites[]` and `hard_negatives[]` arrays with `path`, `role`, `target_engine`, and `dialect_variant` metadata. Multiple rewrites should not be treated as a defect without inspecting role metadata.
- Blocking issue for public artifact release: **not blocking as evidence**, but blocking for an unambiguous machine-readable release schema if role/engine metadata is absent.

### 4. Spark witness / validation files for PERF_0006, PERF_0007, PERF_0008, PERF_0013

Status: **partially confirmed as manifest contract gaps and missing plan-collection scripts, not missing Spark witness/validation evidence**. Spark witness and validation artifacts exist for the checked files. Spark plan artifacts also exist. However, manifests do not consistently declare the Spark witness, validation script, or Spark plan artifacts, and `run_spark_plan_collection.sh` / `collect_spark_plans.sh` is absent in these four packages.

| case_id | spark_witness_data | run_spark_validation | spark_validation_artifacts | spark_plan_artifacts | spark_plan_collection_script | issue status |
| --- | --- | --- | --- | --- | --- | --- |
| PERF_0006 | `cases/PERF/PERF_0006/validation/spark_witness_data.sql` | `cases/PERF/PERF_0006/validation/run_spark_validation.sh` | `4 files under runs/spark` | `cases/PERF/PERF_0006/runs/spark/plans/rewrite_neg_01.txt; cases/PERF/PERF_0006/runs/spark/plans/rewrite_pos_01.txt` | `missing` | partially_confirmed_missing_files_and_manifest_contract_gaps:spark_plan_collection_script,manifest_does_not_declare_spark_witness_data,manifest_does_not_declare_run_spark_validation,manifest_does_not_declare_spark_plan_artifacts |
| PERF_0007 | `cases/PERF/PERF_0007/validation/spark_witness_data.sql` | `cases/PERF/PERF_0007/validation/run_spark_validation.sh` | `4 files under runs/spark` | `cases/PERF/PERF_0007/runs/spark/plans/rewrite_neg_01.txt; cases/PERF/PERF_0007/runs/spark/plans/rewrite_pos_01.txt` | `missing` | partially_confirmed_missing_files_and_manifest_contract_gaps:spark_plan_collection_script,manifest_does_not_declare_spark_witness_data,manifest_does_not_declare_run_spark_validation,manifest_does_not_declare_spark_plan_artifacts |
| PERF_0008 | `cases/PERF/PERF_0008/validation/spark_witness_data.sql` | `cases/PERF/PERF_0008/validation/run_spark_validation.sh` | `4 files under runs/spark` | `cases/PERF/PERF_0008/runs/spark/plans/rewrite_neg_01.txt; cases/PERF/PERF_0008/runs/spark/plans/rewrite_pos_01.txt` | `missing` | partially_confirmed_missing_files_and_manifest_contract_gaps:spark_plan_collection_script,manifest_does_not_declare_spark_witness_data,manifest_does_not_declare_run_spark_validation,manifest_does_not_declare_spark_plan_artifacts |
| PERF_0013 | `cases/PERF/PERF_0013/validation/spark_witness_data.sql` | `cases/PERF/PERF_0013/validation/run_spark_validation.sh` | `4 files under runs/spark` | `cases/PERF/PERF_0013/runs/spark/plans/rewrite_neg_01.txt; cases/PERF/PERF_0013/runs/spark/plans/rewrite_pos_01.txt` | `missing` | partially_confirmed_missing_files_and_manifest_contract_gaps:spark_plan_collection_script,manifest_does_not_declare_spark_witness_data,manifest_does_not_declare_run_spark_validation,manifest_does_not_declare_spark_plan_artifacts |

- Recommended release-facing fix: for these PERF cases, update `manifest.yaml` later to declare existing Spark witness, validation, and plan artifacts. Add Spark plan collection scripts or explicitly state that retained plan artifacts are accepted without collection scripts for release.
- Blocking issue for public artifact release: **partially blocking for manifest contract completeness and reproducible plan collection**, not blocking as missing Spark witness/validation evidence for the checked files.

## Per-case audit table

Full machine-readable details are in `reports/artifact_release/case_package_contract_audit_v1.csv`. Compact view:

| case_id | pool | provenance_style | taxonomy | rewrites | key contract gaps |
| --- | --- | --- | --- | --- | --- |
| CONS_0005 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0007 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0009 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0010 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0011 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0012 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0024 | consistency | implicit_source_fields_only | manifest+standalone | +1/-1 | no_top_level_provenance_block;standalone_taxonomy_trial_file_needs_release_disposition |
| CONS_0036 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| CONS_0037 | consistency | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| LONGTAIL_0011 | longtail | implicit_source_fields_only | manifest | +1/-1 | missing_checker;no_top_level_provenance_block |
| LONGTAIL_0012 | longtail | implicit_source_fields_only | manifest | +1/-1 | missing_checker;no_top_level_provenance_block |
| LONGTAIL_0013 | longtail | implicit_source_fields_only | manifest | +1/-1 | missing_checker;no_top_level_provenance_block |
| LONGTAIL_0022 | longtail | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| LONGTAIL_0023 | longtail | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| LONGTAIL_0024 | longtail | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| PERF_0006 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition;manifest_does_not_declare_spark_witness_data;manifest_does_not_declare_run_spark_validation;manifest_does_not_declare_spark_plan_artifacts |
| PERF_0007 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition;manifest_does_not_declare_spark_witness_data;manifest_does_not_declare_run_spark_validation;manifest_does_not_declare_spark_plan_artifacts |
| PERF_0008 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition;manifest_does_not_declare_spark_witness_data;manifest_does_not_declare_run_spark_validation;manifest_does_not_declare_spark_plan_artifacts |
| PERF_0013 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition;manifest_does_not_declare_spark_witness_data;manifest_does_not_declare_run_spark_validation;manifest_does_not_declare_spark_plan_artifacts |
| PERF_0017 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition |
| PERF_0019 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition |
| PERF_0024 | performance | source_fields_plus_case_local_files_no_manifest_block | manifest+standalone | +1/-1 | no_top_level_provenance_block;standalone_taxonomy_trial_file_needs_release_disposition |
| PERF_0033 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition |
| PERF_0034 | performance | explicit_manifest_block_and_case_local_files | manifest | +1/-1 | none_detected |
| PERF_0035 | performance | explicit_manifest_block_and_case_local_files | manifest | +1/-1 | none_detected |
| PERF_0052 | performance | explicit_manifest_block_and_case_local_files | manifest | +1/-1 | none_detected |
| PERF_0054 | performance | explicit_manifest_block_and_case_local_files | manifest+standalone | +1/-1 | standalone_taxonomy_trial_file_needs_release_disposition |
| PERF_0056 | performance | explicit_manifest_block_and_case_local_files | manifest | +1/-1 | none_detected |
| PERF_0062 | performance | explicit_manifest_block_and_case_local_files | manifest | +1/-1 | none_detected |
| PERF_0077 | performance | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| PERF_0082 | performance | implicit_source_fields_only | manifest | +1/-1 | no_top_level_provenance_block |
| PORT_0003 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest+standalone | +2/-2 | no_top_level_provenance_block;standalone_taxonomy_trial_file_needs_release_disposition;multiple_rewrite_files_need_array_role_metadata |
| PORT_0004 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest+standalone | +2/-2 | no_top_level_provenance_block;standalone_taxonomy_trial_file_needs_release_disposition;multiple_rewrite_files_need_array_role_metadata |
| PORT_0005 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest+standalone | +2/-2 | no_top_level_provenance_block;standalone_taxonomy_trial_file_needs_release_disposition;multiple_rewrite_files_need_array_role_metadata |
| PORT_0008 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | missing_checker;no_top_level_provenance_block |
| PORT_0012 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| PORT_0013 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +2/-2 | no_top_level_provenance_block;multiple_rewrite_files_need_array_role_metadata |
| PORT_0022 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| PORT_0024 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |
| PORT_0025 | portability | source_fields_plus_case_local_files_no_manifest_block | manifest | +1/-1 | no_top_level_provenance_block |

## Recommended release-facing actions

1. Normalize provenance into manifest-level `provenance:` blocks across all 40 Common-core v0 packages, linking existing case-local provenance files where available.
2. Make manifest `tags:` the release-facing taxonomy source. Treat standalone `taxonomy_trial*.yaml` files as draft/intermediate and archive or remove them only after migration review.
3. Update the release schema for rewrites to use arrays: `positive_rewrites[]` and `hard_negatives[]`, each with `path`, `role`, `target_engine`, and `dialect_variant`.
4. For `PERF_0006`, `PERF_0007`, `PERF_0008`, and `PERF_0013`, distinguish evidence presence from manifest declaration: add manifest declarations for existing Spark witness/validation/plan artifacts, and decide whether missing Spark plan collection scripts are required for release.
5. Do not change admission/common-core/extended status as part of this cleanup; treat this as artifact contract alignment only.
