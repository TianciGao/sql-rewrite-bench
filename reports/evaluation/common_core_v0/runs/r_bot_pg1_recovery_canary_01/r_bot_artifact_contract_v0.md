# R-Bot Artifact Contract v0

This document freezes the required output artifact contract for any future `R-Bot` PG1 actual generation canary.

It does not authorize execution.

## Required Artifacts

If a future actual run occurs, the package must retain all of the following.

### 1. Generated SQL

Required path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`

### 2. Selected rules trace

Required retained artifact:

- machine-readable selected-rules trace

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/traces/PERF_0006/pg/selected_rules.json`

### 3. Retrieval trace

Required retained artifact:

- machine-readable retrieval trace

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/traces/PERF_0006/pg/retrieval_trace.json`

### 4. Prompt text

Required retained artifact:

- the actual prompt text or structured prompt payload used for generation

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/prompts/PERF_0006/pg/prompt.txt`

### 5. Raw model response

Required retained artifact:

- raw model response text as returned by the method-side call path

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/raw_responses/PERF_0006/pg/response.txt`

Boundary:

- never retain secrets or API keys

### 6. Token / cost / provider metadata

Required retained artifact:

- machine-readable metadata containing:
  - provider name
  - model name
  - base URL or endpoint family if non-default
  - token usage if available
  - cost fields if available

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/metadata/PERF_0006/pg/token_cost_provider.json`

### 7. Environment snapshot without secrets

Required retained artifact:

- environment snapshot that may include:
  - Python executable path
  - smoke requirements checksum
  - package snapshot reference
  - upstream clone commit
  - index snapshot identity
  - `OPENAI_API_KEY visible: true/false`

Forbidden:

- do not write API keys
- do not write passwords
- do not write raw connection secrets

Recommended retained path:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/metadata/PERF_0006/pg/environment_snapshot.json`

### 8. `run_results.json`

Required retained artifact:

- package-level `run_results.json`

It must preserve:

- `run_id`
- `method_id`
- `route_id`
- `engine`
- `denominator_id`
- `git_commit`
- success/failure/blocked status
- explicit claim boundary

## Output Hygiene Rules

The future actual run must:

- not expose secrets
- not expose API keys
- not treat exploratory smoke as current metric evidence
- preserve blocked or failed status explicitly

## Current Decision Boundary

The artifact contract is now defined at the package level.

It is not yet satisfied by an actual run, because no current actual run has occurred.
