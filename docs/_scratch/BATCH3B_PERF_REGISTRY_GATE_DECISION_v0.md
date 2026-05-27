# Status

This note records a paper-draft execution gate decision for the Batch 3B PERF ready-lane candidates.

It is not a registry freeze, admission decision, or common-core promotion decision.

# Artifact Evidence After Backfill

The following cases were reviewed:

- `PERF_0027`
- `PERF_0028`
- `PERF_0030`
- `PERF_0031`

After the narrow backfill, each of the four cases now has the bounded PostgreSQL-local artifacts needed for a Batch 3B PostgreSQL execution/scoring pass:

- `manifest.yaml`
- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- `validation/checker.yaml`
- `runs/pg/result_check.json`
- `runs/pg/source.tsv`
- `runs/pg/rewrite_pos_01.tsv`
- `runs/pg/rewrite_neg_01.tsv`
- `runs/pg/plans/source.json`
- `runs/pg/plans/rewrite_pos_01.json`
- `runs/pg/plans/rewrite_neg_01.json`
- `runs/pg/plans/plan_check.json`
- root `runs/result_check.json`
- `taxonomy_trial_v0.3.yaml`

The new root `runs/result_check.json` files explicitly preserve PostgreSQL witness evidence only:

- source vs positive result signal: equal
- source vs negative result signal: different
- claim scope: PostgreSQL witness only
- no tri-engine closure claim
- no admission claim

The new `taxonomy_trial_v0.3.yaml` files are conservative draft metadata only:

- `status=batch3b_taxonomy_draft`
- `candidate_primary_pool=performance`
- `dataset_line_candidate=common-core-candidate`
- explicit evidence notes and claim boundaries

# Registry Gate Issue

The current preflight still leaves these four cases at `minor_backfill_needed`, but the remaining gate is registry staging metadata rather than missing PostgreSQL-local evidence.

For all four cases, the registry still shows:

- `current_role=pg_witness_validated_perf_draft`
- `benchmark_line=not_assessed`
- `admission_status=not_assessed`
- `promotion_status=not_assessed`
- `tri_engine_closure=yes`
- `admission_blockers=missing_formal_review_only`

This means the unresolved issue is governance staging, not PostgreSQL execution/scoring readiness.

# Decision

For paper-draft evidence only, `PERF_0027`, `PERF_0028`, `PERF_0030`, and `PERF_0031` may proceed as `batch3b_execution_candidate` cases for bounded Batch 3B PostgreSQL execution/scoring.

This decision is based on the existing PostgreSQL-local artifact package and witness-backed source / positive / negative result evidence.

This decision does not change registry state and does not resolve the registry staging fields.

# Boundaries

- PostgreSQL execution/scoring gate only
- not registry promotion
- not admission
- not final common-core inclusion
- not final benchmark denominator
- not final leaderboard denominator
- not tri-engine closure
- not formal review completion
- no registry writeback

# Recommended Next Action

- run Batch 3B PostgreSQL execution/scoring with an explicit override flag or explicit candidate list for `PERF_0027`, `PERF_0028`, `PERF_0030`, and `PERF_0031`, while keeping registry state unchanged
