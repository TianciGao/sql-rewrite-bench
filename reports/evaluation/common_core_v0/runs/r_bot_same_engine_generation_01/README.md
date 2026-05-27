# R-Bot Same-Engine Generation Package

This directory is the human-run formal generation package for the denominator:

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `denominator_id = common_core_v0_40_same_engine_120`
- `planned_rows = 120`

It is a package directory only.
It does not mean generation has already occurred.

## Contents

- `generation_plan.md`
- `generation_command_matrix.csv`
- `run_manual_r_bot_generation.sh`
- `expected_artifacts.md`

## Human-Run Entry Point

```bash
bash reports/evaluation/common_core_v0/runs/r_bot_same_engine_generation_01/run_manual_r_bot_generation.sh
```

## Important Boundary

The package directory is not the retained output root.

Human-run generated outputs must be written under:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/`

That output root is already frozen by the retained artifact contract.

## Current Recovered Runner Shape

The visible committed recovered R-Bot path is still the `LLM4Rewrite`
PG-oriented single-case smoke runner in `scripts/cli.py`.

Therefore:

- all `120` denominator rows remain in the command matrix
- unsupported or blocked rows remain explicit
- only the recovered PG-supported subset is marked `human_run_generation_ready`

## Not Included Here

This package does not compute:

- database execution
- validity
- timing
- speedup
- leaderboard metrics

Those remain downstream phases after generation.
