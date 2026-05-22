# Common-core v0 Reviewer Reproduction V1

## Purpose
This is a reviewer-facing artifact-mode reproduction wrapper for Common-core v0 retained evidence validation.

## Mode Boundary
Artifact-mode does not run database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection. It reads retained CSV/JSON/MD artifacts and runs the static Table 12 renderer only.

## Results
- Table 12 regenerated successfully via `python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check`.
- Static recomputation had 0 conflicts / missing inputs.
- Table 12 diff summary: cells_compared=90; exact_match=55; rounded_match=0; expected_NA_match=8; artifact_boundary_match=27; conflicts=0; missing_input=0.
- Artifact-only rows remain artifact-only.
- Expected NA fields remain NA.

## Expected-NA And Scope Boundaries
- SpeedupTransferRate is not computed because paired target-engine timing is not retained.
- Full NodeAlignmentCoverage is not computed; retained plan evidence is a selected PG frontier, not full-denominator node alignment.
- Verifier support is not a same-engine rewrite baseline and does not use the common-core 120 denominator.
- Bounded PORT6 closure is retained separately and is not a full PORT9 experiment.

## Optional Future Modes
Deterministic reruns are available through `--mode deterministic` and require explicit `--execute` before any DB/timing command is run. LLM reruns remain a separate future mode, not default review mode.

## Outputs
- `reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_status_v1.csv`
- `reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt`
- `reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_summary_v1.md`
