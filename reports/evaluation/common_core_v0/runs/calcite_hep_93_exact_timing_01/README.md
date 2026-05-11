# Calcite HEP 93 Exact Timing Packet

This run packet times exactly the 93 retained exact-match Calcite HEP rows listed in the preflight denominator.
It does not regenerate Calcite rewrites, does not change the 93/120 correctness ledger, and does not create a final ranked leaderboard.

## Inputs

- preflight denominator: `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/calcite_hep_93_exact_timing_denominator_preflight_v1.csv`
- timing runner: `reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/run_manual_calcite_hep_93_exact_timing.sh`
- warmup_count = 1
- repeat_count = 3

## Outputs

- `timing_event_long.csv`
- `timing_summary.csv`
- `timing_summary.md`
- `run_results.json`
- `validation_report.json`
- `timing_command_matrix.csv`
- `timing_failures.csv`

## Boundary

Existing Calcite HEP PG-only timing evidence was not reused as the 93-row timing result.
