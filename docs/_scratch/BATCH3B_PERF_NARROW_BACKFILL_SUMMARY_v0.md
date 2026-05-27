# Status

This note records the narrow Batch 3B PERF backfill applied to four ready-lane candidates:

- `PERF_0027`
- `PERF_0028`
- `PERF_0030`
- `PERF_0031`

Scope of this backfill:

- add root-level `runs/result_check.json`
- add bounded `taxonomy_trial_v0.3.yaml`

No SQL execution was performed.

# Files Added

For each of the four cases:

- `runs/result_check.json`
- `taxonomy_trial_v0.3.yaml`

# Backfill Policy

Root `runs/result_check.json` files were derived from the existing `runs/pg/result_check.json` files and were kept explicitly PostgreSQL-only:

- source vs positive result signal preserved as equal
- source vs negative result signal preserved as different
- PG witness scope stated directly
- no tri-engine closure claim
- no admission claim

`taxonomy_trial_v0.3.yaml` files were drafted conservatively from:

- `manifest.yaml`
- `source.sql`
- `validation/checker.yaml`
- existing PostgreSQL plan artifacts

The taxonomy drafts intentionally avoid over-tagging and keep explicit claim boundaries.

# Validation Commands

- JSON validation:
  - `python -m json.tool cases/PERF/PERF_0027/runs/result_check.json >/dev/null`
  - `python -m json.tool cases/PERF/PERF_0028/runs/result_check.json >/dev/null`
  - `python -m json.tool cases/PERF/PERF_0030/runs/result_check.json >/dev/null`
  - `python -m json.tool cases/PERF/PERF_0031/runs/result_check.json >/dev/null`
- YAML validation:
  - `python - <<'PY' ... yaml.safe_load(...)` over all four `taxonomy_trial_v0.3.yaml`
- preflight rerun:
  - `python -m scripts.cli formal-batch3b-perf-backfill-preflight`
  - `python -m json.tool reports/formal_expansion/batch3b_perf_backfill_preflight_v0.json >/dev/null`

# Preflight Result After Backfill

After this narrow backfill, the four cases still do **not** move to `ready_for_batch3b_execution` under the current preflight rule.

Current result for all four:

- `PERF_0027`: `minor_backfill_needed`
- `PERF_0028`: `minor_backfill_needed`
- `PERF_0030`: `minor_backfill_needed`
- `PERF_0031`: `minor_backfill_needed`

Reason:

- the new root-level `runs/result_check.json` and bounded taxonomy drafts close the file-level backfill requested here
- but the current preflight command still treats these cases as not fully ready because registry staging fields remain:
  - `benchmark_line=not_assessed`
  - `admission_status=not_assessed`
  - `promotion_status=not_assessed`

This note does not change registry state.

# Remaining Diagnostic-Only Cases

The following remain `diagnostic_only` and were not part of this narrow backfill:

- `PERF_0029`
- `PERF_0032`
- `PERF_0037`
- `PERF_0039`
- `PERF_0040`
- `PERF_0041`
- `PERF_0042`

Their current blockers are still governance/closure-side:

- `tri_engine_closure=not_assessed`
- `admission_blockers=missing_mysql_and_spark_closure_and_release_hardening`

# Boundary

- no SQL execution
- no checker execution
- no `scripts/cli.py` change
- no registry change
- no `docs/EXECUTION_STATUS.md` change
- no formal review change
