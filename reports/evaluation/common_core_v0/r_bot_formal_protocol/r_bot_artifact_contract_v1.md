# R-Bot Artifact Contract v1

## Role

This document freezes the required retained artifact contract for any future formal `R-Bot` Common-core v0 same-engine run on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It does not authorize execution by itself.

## Required Retained Outputs

For every row that reaches generation, the run must retain the following.

### 1. Generated SQL

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/generated/<CASE>/<engine>/r_bot_same_engine_rewrite.sql`

### 2. Selected rules trace

Required retained artifact:

- machine-readable selected-rules trace

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/traces/<CASE>/<engine>/selected_rules.json`

### 3. Retrieval trace

Required retained artifact:

- machine-readable retrieval trace

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/traces/<CASE>/<engine>/retrieval_trace.json`

### 4. Prompt text or structured prompt payload

Required retained artifact:

- the actual prompt text or structured payload used for that row

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/prompts/<CASE>/<engine>/prompt.txt`

### 5. Raw model response

Required retained artifact:

- raw model response text returned by the method-side call path

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/raw_responses/<CASE>/<engine>/response.txt`

Boundary:

- never retain secrets
- never retain API keys

### 6. Token / cost / provider metadata

Required retained artifact:

- machine-readable metadata containing:
  - provider name
  - model name
  - base URL or endpoint family if non-default
  - token usage if available
  - cost fields if available
  - retry count if any

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/metadata/<CASE>/<engine>/token_cost_provider.json`

### 7. Environment snapshot without secrets

Required retained artifact:

- environment snapshot that may include:
  - Python executable path
  - dependency snapshot or requirements checksum
  - upstream clone identity
  - retrieval corpus identity
  - index snapshot identity
  - `OPENAI_API_KEY visible: true/false`

Required retained path pattern:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/metadata/<CASE>/<engine>/environment_snapshot.json`

Forbidden:

- do not write API keys
- do not write passwords
- do not write raw connection secrets

## Package-Level Required Outputs

The package must also retain:

### 8. `run_results.json`

Required retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/run_results.json`

It must preserve:

- `run_id`
- `method_id`
- `route_id`
- `engine` or row-level engine fields
- `denominator_id`
- `git_commit`
- success / failure / blocked status
- explicit claim boundary

### 9. Raw row table

Required retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/run_event_long.csv`

It must preserve:

- case identity
- engine identity
- route identity
- success / failure / blocked / unsupported status
- denominator identity

### 10. Package summary

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/generation_summary.csv`

## Output Hygiene Rules

The future formal run must:

- preserve blocked rows explicitly
- preserve unsupported rows explicitly
- preserve failed rows explicitly
- not silently drop denominator rows
- not treat exploratory-only packets as current benchmark evidence
- not expose secrets

## Current Decision Boundary

The contract is now frozen for the `120`-row formal route.

It is not yet satisfied by a current denominator-aware `R-Bot` run.
