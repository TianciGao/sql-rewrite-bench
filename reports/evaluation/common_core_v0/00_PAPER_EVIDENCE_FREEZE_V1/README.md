# Common-core v0 Paper Evidence Freeze v1

This folder is the fixed first-read location for Common-core v0 paper evidence
and `120`-row rerun planning.

Use it before continuing any paper-results, route-promotion, or rerun-campaign
work under `reports/evaluation/common_core_v0/`.

## Role

This folder:

- is the fixed first-read folder for Common-core v0 paper evidence and
  `120`-row rerun planning
- is not a final ranked leaderboard
- does not replace original run artifacts
- does not update `method_comparison_summary_v2`
- records current frozen evidence, rerun status, and human-readable decisions

Future ChatGPT and Codex sessions should read this folder first before proposing
new result work.

## Denominator and Track Boundaries

- main Track A denominator:
  `common_core_v0_40_same_engine_120`
- Track A same-engine rewrite, Track B plan observability, and Track C
  portability must stay separate
- support/verifier methods must not be mixed into rewrite leaderboard rows
- PG-only, `prior_method_pg10`, `port_bounded_6`, and other bounded slices must
  not be treated as `120`-row evidence

## Contents

- `METHOD_STATUS_LEDGER.csv`
  - current method/route status snapshot
- `ARTIFACT_INDEX.csv`
  - stable machine-readable artifact entrypoint
- `RERUN_CAMPAIGN_LEDGER.csv`
  - current `120`-rerun campaign stage ledger
- `DECISION_NOTES.md`
  - current human-readable governance decisions
- `NEXT_ACTIONS.md`
  - exactly one highest-priority next action plus explicit deferrals

## Usage Boundary

This folder is a governance and indexing freeze.

It does not:

- create new benchmark evidence
- authorize execution
- promote proposed rows into canonical rows
- create a leaderboard

Original run directories, result cards, summaries, and synthesis files remain
the source artifacts behind this freeze folder.
