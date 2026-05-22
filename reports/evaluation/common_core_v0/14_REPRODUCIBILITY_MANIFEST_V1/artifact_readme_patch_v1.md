# Artifact README Patch v1

## Reproducibility Environment And Route Metadata

The reproducibility manifest for the Common-core v0 paper artifact is retained under `reports/evaluation/common_core_v0/14_REPRODUCIBILITY_MANIFEST_V1/`.

Included files:
- `reproducibility_environment_manifest_v1.csv` and `.md`: route-local and repo-level environment fields, separated into retained exact, retained partial, missing-before-submission, and human-review-needed values.
- `route_metadata_manifest_v1.csv`: paper-facing route metadata for main Track A routes, bounded appendix routes, and retained Track C portability routes.
- `table_regeneration_commands_v1.md`: exact retained runner commands where they exist, plus explicit gaps where no final render command is frozen.
- `reproducibility_missing_items_v1.csv`: submission blockers and human-review items only.

Current retained state:
- Direct LLM original and repair packets preserve model/provider/prompt/decode metadata, candidate-count assumptions, and call-date proxies.
- Timing policy is retained at the packet level (`warmup=1`, `repeat=3`, timeout retained where present) rather than as one repo-wide lock.
- Selected plan observability remains a selected PG frontier (`6` retained frontier rows in the Round 4 table), not full-denominator NodeAlignmentCoverage.
- Repo-wide hardware, exact PostgreSQL/Spark versions, and one final Section 8 render command are still missing or need human review before submission.

Boundary:
- This manifest does not change protocol, denominators, taxonomy, or claims.
- It records what is already frozen versus what still must be captured before camera-ready packaging.
