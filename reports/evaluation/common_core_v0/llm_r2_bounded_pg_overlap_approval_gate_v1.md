# LLM-R2 Bounded PG Overlap Approval Gate v1

Status: **superseded for the original 8-row slice by runner compatibility addendum**

## Human approval required before execution

The original bounded PG overlap approval is now superseded for the original
8-row PostgreSQL slice by the runner compatibility addendum.

The following approvals remain frozen:

- `original_8row_approval_status = superseded_by_runner_compatibility_addendum`
- `approved_for_local_human_run_generation_dry_run = no_for_original_8row_slice`
- `approved_for_pg3_supported_subset = pending_human_reapproval`
- `approved_for_unsupported_pg5 = no`
- `approved_for_codex_execution = no`
- `approved_for_database_execution = no`
- `approved_for_checker = no`
- `approved_for_timing = no`
- `approved_for_full_120 = no`
- `approved_for_result_card = no`

Before any later local human-run dry-run proceeds, a human must still confirm
all of the following:

- runner scaffold accepted
- candidate slice accepted
- output retention path accepted
- failure bucket policy accepted
- no MySQL/Spark claim
- no timing claim
- no result card/proposed row until dry-run artifacts exist

## Approval checklist

- [x] runner scaffold accepted
- [x] candidate slice accepted
- [x] output retention path accepted
- [x] failure bucket policy accepted
- [x] no MySQL/Spark claim
- [x] no timing claim
- [x] no result card/proposed row until dry-run artifacts exist

## Boundary

- original 8-row approval superseded by compatibility addendum
- not approved for the original 8-row slice as-is
- PG3 supported subset requires separate human reapproval
- unsupported PG5 rows require wrapper extension before any run discussion
- not approved for Codex execution
- not approved for database execution
- not approved for checker
- not approved for timing
- not approved for full `120`
- not approved for result card or proposed row
