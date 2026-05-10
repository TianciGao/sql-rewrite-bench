# LLM-R2 Bounded PG Overlap Approval Gate v1

Status: **approved for local human-run generation dry-run only**

## Human approval required before execution

The bounded PG overlap dry-run is now approved only for a future local
human-run generation dry-run on the fixed 8-row PostgreSQL slice.

The following approvals remain frozen:

- `approved_for_local_human_run_generation_dry_run = yes`
- `approved_for_codex_execution = no`
- `approved_for_database_execution = no`
- `approved_for_checker = no`
- `approved_for_timing = no`
- `approved_for_full_120 = no`
- `approved_for_result_card = no`

Before any local human-run dry-run proceeds, a human must still confirm all of
the following:

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

- approved for local human-run generation dry-run only
- not approved for Codex execution
- not approved for database execution
- not approved for checker
- not approved for timing
- not approved for full `120`
- not approved for result card or proposed row
