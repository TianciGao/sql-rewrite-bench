# Case Package Manifest Release Schema v1

## Scope

This schema is a release-facing manifest shape for aligning the 40 Common-core v0 case packages with the paper Table 2 case-package contract. It is a migration target for case-local `manifest.yaml` files only. It does not change registry status, common-core membership, admission status, benchmark rules, metrics, or paper evidence.

The manifest should act as the release-facing index for a case package. It should point to source SQL, positive rewrites, hard negatives, schemas/data, witness/checker assets, validation scripts, plan/failure artifacts, provenance, taxonomy tags, and reporting metadata that already live in the case package.

## Design Rules

- Keep case facts explicit in `manifest.yaml`; do not rely on implicit file naming when a release reader needs to understand the package.
- Represent positive rewrites and hard negatives as arrays so dialect variants and engine-specific rewrites are first-class rather than conflicting duplicates.
- Store taxonomy in the manifest `tags` block for release consumption; standalone `taxonomy*.yaml` files can remain as archived/trial artifacts until a later cleanup pass.
- Store provenance in a top-level `provenance` block for every release case. Link existing `provenance/` files where present.
- Declare existing Spark evidence when it exists. If a plan collection script is intentionally absent, document that as an explicit gap or waiver rather than implying the evidence is missing.
- Do not encode method performance, timing, or rewrite utility claims in the case manifest.

## Required Blocks

### Case Identity And Reporting Metadata

The identity block records stable identifiers and release/reporting facts.

Required fields:

- `manifest_schema_version`: release schema version, for example `case_package_manifest_release_schema_v1`.
- `case_id`: stable case identifier such as `PORT_0003`.
- `primary_pool`: one of the existing case pools, for example `CONS`, `PERF`, `PORT`, or `LONGTAIL`.
- `reporting`: release-facing metadata such as benchmark line, admission/common-core status, caveats, and notes.
- `status`: current case-local status fields carried forward without reclassification.

### Source

The `source` block identifies the source query and its lineage.

Recommended fields:

- `path`: source SQL path, normally `source.sql`.
- `dialect`: declared source dialect when known.
- `source_family`, `source_id`, `source_subset`, `source_entry_pointer`: existing source lineage fields when present.
- `source_query_identity`: existing identity label when present.
- `workload`: workload/source name when present.
- `notes`: caveats needed to interpret source SQL.

### Positive Rewrites

Use `positive_rewrites` as an array. Each entry is one validated positive candidate or dialect/engine variant.

Recommended entry fields:

- `id`: stable local identifier such as `rewrite_pos_01`.
- `path`: SQL file path.
- `role`: `positive_rewrite`.
- `target_engine`: target engine or `multi_engine` when shared.
- `dialect_variant`: dialect family such as `postgresql`, `mysql`, `spark`, `ansi_like`, or `source_like`.
- `expected_relation_to_source`: why this is a positive rewrite.
- `validated_engines`: engines with validation evidence for this entry.
- `notes`: any engine-specific constraints.

### Hard Negatives

Use `hard_negatives` as an array. Each entry is one negative candidate or dialect/engine variant.

Recommended entry fields:

- `id`: stable local identifier such as `rewrite_neg_01`.
- `path`: SQL file path.
- `role`: `hard_negative`.
- `target_engine`: target engine or `multi_engine` when shared.
- `dialect_variant`: dialect family.
- `expected_failure_mode`: semantic, cardinality, null, ordering, dialect, or plan-sensitive failure mode.
- `validated_engines`: engines with validation evidence for this entry.
- `notes`: any engine-specific constraints.

### Schema Data

The `schema_data` block declares schema, data profile, and witness data assets.

Recommended fields:

- `schemas`: map of engine name to schema DDL path.
- `witness_data`: map of engine name to witness data path.
- `data_profile`: compact data profile or pointer to profile artifact.
- `required_tables`: tables required by the source and rewrites.
- `notes`: known data-shape caveats.

### Checkers

The `checkers` block declares benchmark-local checking policy and checker artifacts.

Recommended fields:

- `result_checker`: checker script or policy used to compare source, positive rewrites, and hard negatives.
- `plan_checker`: plan checker script or policy, when plan observability is part of the package.
- `comparison_policy`: conservative equality semantics, ordering assumptions, tolerance policy, or engine-specific notes.
- `failure_expectations`: expected negative/failure assertions where applicable.

### Validation

The `validation` block declares validation scripts and result artifacts by engine.

Recommended engine entry fields:

- `script`: validation runner path.
- `witness_data`: witness data path used by that engine.
- `source_result`: retained source result artifact, when present.
- `positive_rewrite_results`: retained positive result artifacts.
- `hard_negative_results`: retained negative result artifacts.
- `status`: current validation status carried forward from existing evidence.
- `notes`: caveats and intentionally unsupported paths.

### Plans

The `plans` block declares plan collection scripts and plan artifacts by engine.

Recommended engine entry fields:

- `collection_script`: plan collection script path, or an explicit null/waiver with explanation if absent.
- `source_plan`: retained source plan artifact, when present.
- `positive_rewrite_plans`: retained positive plan artifacts.
- `hard_negative_plans`: retained negative plan artifacts.
- `status`: current plan evidence status.
- `notes`: plan observability caveats.

### Provenance

Every release manifest should have a top-level `provenance` block.

Recommended fields:

- `source_record`: source registry record, source paper/system, or workload identifier.
- `source_fields`: preserved source-lineage fields from the current manifest.
- `case_construction`: how the case was derived from the source query.
- `provenance_files`: case-local provenance files or directories when present.
- `license_or_terms`: source terms if known.
- `freeze_basis`: evidence basis for the release version.
- `notes`: unresolved provenance caveats.

### Tags

The `tags` block is the release-facing taxonomy location.

Recommended fields:

- `sql_features`: SQL constructs relevant to the case.
- `rewrite_opportunities`: intended rewrite opportunity classes.
- `plan_operators`: plan operators or observability dimensions.
- `workload_realism`: source/workload realism annotations.
- `portability`: engine or dialect portability annotations.
- `negative_modes`: hard-negative failure categories.
- `reporting_tags`: labels used by release reports.

## YAML Skeleton

```yaml
manifest_schema_version: case_package_manifest_release_schema_v1
case_id: PORT_0003
primary_pool: PORT
status:
  admission_status: common_core_v0
  official_case_status: unchanged_from_registry
reporting:
  benchmark_line: common_core_v0
  release_notes: []

source:
  path: source.sql
  dialect: mysql
  source_family: null
  source_id: null
  source_subset: null
  source_entry_pointer: null
  source_query_identity: null
  workload: null
  notes: []

positive_rewrites:
  - id: rewrite_pos_01
    path: rewrite_pos_01.sql
    role: positive_rewrite
    target_engine: multi_engine
    dialect_variant: ansi_or_engine_specific
    expected_relation_to_source: null
    validated_engines: []
    notes: []

hard_negatives:
  - id: rewrite_neg_01
    path: rewrite_neg_01.sql
    role: hard_negative
    target_engine: multi_engine
    dialect_variant: ansi_or_engine_specific
    expected_failure_mode: null
    validated_engines: []
    notes: []

schema_data:
  schemas:
    pg: schema/ddl_pg.sql
    mysql: schema/ddl_mysql.sql
    spark: schema/ddl_spark.sql
  witness_data:
    pg: validation/pg_witness_data.sql
    mysql: validation/mysql_witness_data.sql
    spark: validation/spark_witness_data.sql
  data_profile: null
  required_tables: []
  notes: []

checkers:
  result_checker: null
  plan_checker: null
  comparison_policy: conservative_result_equality
  failure_expectations: []

validation:
  pg:
    script: validation/run_pg_validation.sh
    witness_data: validation/pg_witness_data.sql
    status: null
  mysql:
    script: validation/run_mysql_validation.sh
    witness_data: validation/mysql_witness_data.sql
    status: null
  spark:
    script: validation/run_spark_validation.sh
    witness_data: validation/spark_witness_data.sql
    status: null

plans:
  pg:
    collection_script: validation/run_pg_plan_collection.sh
    status: null
  mysql:
    collection_script: validation/run_mysql_plan_collection.sh
    status: null
  spark:
    collection_script: validation/run_spark_plan_collection.sh
    status: null
    notes: []

provenance:
  source_record: null
  source_fields: {}
  case_construction: null
  provenance_files: []
  license_or_terms: null
  freeze_basis: null
  notes: []

tags:
  sql_features: []
  rewrite_opportunities: []
  plan_operators: []
  workload_realism: []
  portability: []
  negative_modes: []
  reporting_tags: []
```

## Migration Rules From Current Common-core v0 Manifests

- Move existing `source_*`, `source_path`, `source_files`, and source pointer fields into the `source` block and mirror lineage-critical fields in `provenance.source_fields`.
- Convert current positive and negative rewrite file references into `positive_rewrites[]` and `hard_negatives[]` entries.
- For PORT cases with both base and Spark rewrite files, represent each file as a separate array entry with `target_engine` and `dialect_variant` metadata.
- Keep existing manifest `tags` as the release taxonomy source. For standalone `taxonomy*.yaml` and `taxonomy_trial*.yaml`, migrate or confirm the represented tags in `manifest.yaml`, then archive later; do not delete during schema migration.
- For cases with existing `provenance/` directories or standalone provenance files, add a top-level `provenance` block linking those files.
- For cases with only source fields and no provenance block, add a top-level `provenance` block derived from source fields and mark any missing release source-record detail explicitly.
- For PERF_0006, PERF_0007, PERF_0008, and PERF_0013, declare existing Spark witness, Spark validation runner, and Spark plan artifacts; separately add or explicitly waive the missing Spark plan collection script.
- For cases without checker declaration, add a release-facing checker policy or checker artifact reference rather than changing benchmark equality rules.

## Non-goals

This schema does not require rewriting SQL, regenerating evidence, rerunning databases, changing admission status, deleting trial taxonomy files, or changing benchmark metrics. It is a documentation and manifest alignment target only.
