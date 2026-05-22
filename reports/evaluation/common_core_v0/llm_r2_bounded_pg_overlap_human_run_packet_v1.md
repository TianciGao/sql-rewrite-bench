# LLM-R2 Bounded PG Overlap Human-Run Packet v1

Do not run unless you are the human runner.

This packet is for a future local human-run only.
Codex did not execute any command in this task.
No SQL was generated in this task.
No database was executed in this task.
No timing was collected in this task.

## Approved Slice

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0013:pg`

## Pre-Run Checklist

- Confirm `git status -sb` is clean except for expected untracked local files.
- Confirm the static validator passes before any human-run action.
- Confirm the candidate slice still matches the approved 8 PostgreSQL rows.
- Prepare the output directory for bounded PG overlap dry-run artifacts.
- Prepare a failure-bucket ledger template with one row per approved slice row.

## Run-Time Capture Checklist

- Record the exact command manually used.
- Capture stdout and stderr.
- Retain the raw LLM-R2 output for each row.
- Retain extracted SQL if any output SQL is recoverable.
- Record exactly one failure bucket per row.

## Post-Run Checklist

- Do not execute generated SQL.
- Do not run checker.
- Do not run timing.
- Validate artifact completeness against the expected-artifacts file.
- Report the retained artifacts back for governance review.

## Command Template References

The future human runner may consult the existing command matrix for placeholder
templates and sequencing.

```text
FUTURE LOCAL HUMAN-RUN ONLY — NOT EXECUTED BY CODEX
See: reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_command_matrix_v1.csv
```

```text
FUTURE LOCAL HUMAN-RUN ONLY — NOT EXECUTED BY CODEX
Run the static validator locally before any human-run generation attempt.
See: reports/evaluation/common_core_v0/llm_r2_120_runner_dry_run_validator_v1.py
```

## Boundary

- No secrets or credentials are recorded in this packet.
- No result card or proposed row may be created from a future human-run until
  retained artifacts are reviewed.
- Future generated outputs are not paper evidence until governance review is
  complete.
