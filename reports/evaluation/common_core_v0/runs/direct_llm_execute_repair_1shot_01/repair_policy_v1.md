# Repair Policy v1

- Baseline: `Direct LLM + Execute-and-Repair-1`
- Route id: `direct_llm_execute_repair_1shot`
- Denominator: `common_core_v0_40_same_engine_120`
- Repair scope: only the retained `21` `repair_ready` rows
- Blocked rows: retained visible, unrepaired `5` rows
- Model: `gpt-4o-mini`
- Provider/runtime family: `api.gptsapi.net` / OpenAI-compatible API
- Temperature: `0`
- Top-p: `1`
- Max tokens: `2048`
- Candidate count: `1`
- Repair attempts: `1`
- Output acceptance: non-empty, no markdown fences, no prose prefix, SQL-like first line
- Evaluation: execute repaired SQL, run retained exactness check, time only exact rows actually in timing scope
- Boundary: extends Direct LLM; does not replace it; not a final ranked leaderboard
