# Direct LLM + Execute-and-Repair-1 Protocol

This is preflight only. No LLM calls were made. No repaired SQL was generated. No DB or checker runs were performed.

## Baseline Identity

- Baseline name: `Direct LLM + Execute-and-Repair-1`
- Relationship to Direct LLM: extension, not replacement
- Denominator: `common_core_v0_40_same_engine_120`
- Repair scope: only rows that were not exact in the original `direct_llm_same_engine_rewrite` route
- Max repair attempts: `1`

## Frozen Policy Requirements Before Any Actual Repair Run

- Model and prompt policy must be frozen before the run.
- Temperature policy must be fixed before the run.
- The repair packet must not regenerate or overwrite the original Direct LLM first-pass artifacts.

## Allowed Input Fields

- engine
- source SQL
- schema / DDL
- first candidate SQL
- execution error or checker feedback
- result normalization / checker notes when retained

## Output Rule

- one complete SQL statement only
- no markdown
- no explanation

## Evaluation After Repair

- execute repaired SQL
- run checker
- classify `exact` / `mismatch` / `execution_failed` / `extraction_failed` / `unsupported`
- timing only for repaired exact rows

## Claim Boundary

- protocol baseline only
- not a prior-method reproduction
- not a final ranked leaderboard
- not a replacement for Direct LLM
