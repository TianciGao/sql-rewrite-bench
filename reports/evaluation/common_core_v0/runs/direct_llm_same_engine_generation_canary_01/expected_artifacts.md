# Expected Artifacts

## Always expected

- `generation_canary_plan.md`
- `generation_command_matrix.csv`
- `run_direct_llm_generation_canary.py`
- `run_results.json`
- `README.md`
- `expected_artifacts.md`

## Per planned row

- `prompts/<case_id>/<engine>/prompt.txt`
- `raw_responses/<case_id>/<engine>/response.txt`

## Success-only artifacts

- `generated/<case_id>/<engine>/direct_llm_same_engine_rewrite.sql`

Successful rows should write SQL-only output. Rows with `format_violation` or `generation_failed` remain explicit in `run_results.json` and still retain prompt and raw response audit files.
