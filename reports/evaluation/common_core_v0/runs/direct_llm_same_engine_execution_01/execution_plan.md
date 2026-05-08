# Direct LLM @40 Same-Engine Execution Plan

## Scope

- denominator_id: `common_core_v0_40`
- method_id: `direct_llm`
- route_id: `direct_llm_same_engine_rewrite`
- planned rows: `120`
- cases: all `40` Common-core v0 cases
- engines: `pg`, `mysql`, `spark`
- one generated SQL candidate per `case_id x engine` row

## Purpose

This package prepares a **human-run only** same-engine execution package for the completed Direct LLM generation run.

It does not:

- call any LLM or API
- modify generated SQL outputs
- modify case files or registry files
- compute timing
- compute speedup
- create a leaderboard

## Execution Boundary

This package is designed to produce execution evidence only after a human runs the shell entrypoint.

Before execution:

- `execution_command_matrix.csv` keeps all `120` rows explicit
- blocked rows remain visible rather than silently disappearing
- `PORT` caveats remain explicit
- no `run_event_long.csv` or `method_case_summary.csv` is materialized by this package

## Preflight Summary

- total planned rows: `120`
- ready_to_execute rows: `115`
- rows with preflight caveats: `22`
- blocked rows due to missing artifacts: `5`

Ready rows by pool:

- performance: `48`
- consistency: `27`
- longtail: `18`
- portability: `22`

Ready rows by engine:

- pg: `39`
- mysql: `38`
- spark: `38`

Blocked rows:

- `PORT_0003 / mysql`
- `PORT_0003 / spark`
- `PORT_0004 / pg`
- `PORT_0005 / mysql`
- `PORT_0005 / spark`

Current blocker reason:

- missing `validation/*_witness_data.sql` for the target engine

## Portability Caveats

All `PORT` rows remain explicit in the matrix.

Current portability handling:

- `22` `PORT` rows are marked `ready_to_execute` but carry `preflight_caveat`
- `5` `PORT` rows are blocked by missing witness-data artifacts
- rows whose native-source controls row is `skipped` are kept explicit with that caveat
- `PORT_0013 / spark` carries the generation-triage watchlist note for backtick-quoted identifiers

## Runner Pattern

The shell entrypoint reuses the corrected same-engine execution runner pattern established by:

- `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_execution_canary_01/run_manual_sqlglot_execution_canary.sh`

Adapted behavior for Direct LLM:

- `pg`
  - isolated schema per row
  - load schema and witness data
  - run source SQL and generated SQL
  - write `source.tsv` and `generated.tsv`
  - compare TSV outputs
- `mysql`
  - use `MYSQL_DATABASE`
  - do not `CREATE DATABASE`
  - parse and drop case tables before and after each row
  - load schema and witness data
  - run source SQL and generated SQL
  - compare TSV outputs
- `spark`
  - use a workspace-local warehouse/session per row
  - load schema and witness data
  - run source SQL and generated SQL
  - compare TSV outputs

## Human-Run Outputs

After a human run, the script should write:

- `logs/*.stdout.log`
- `logs/*.stderr.log`
- `workspaces/<case_id>/<engine>/<route_id>/source.tsv`
- `workspaces/<case_id>/<engine>/<route_id>/generated.tsv`
- `workspaces/<case_id>/<engine>/<route_id>/result_check.json`
- `records.tmp.jsonl`
- `run_results.json`

## Reporting Guardrails

This package must not claim:

- validity beyond row-local TSV comparison
- timing
- speedup
- leaderboard placement
- case admission or benchmark-policy changes
