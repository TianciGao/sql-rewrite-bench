# Expected Artifacts

## Always expected

- `generation_plan.md`
- `generation_command_matrix.csv`
- `run_direct_llm_generation.py`
- `run_results.json`
- `README.md`
- `expected_artifacts.md`

## Per planned row

- `prompts/<case_id>/<engine>/prompt.txt`
- `raw_responses/<case_id>/<engine>/response.txt`

## Success-only artifacts

- `generated/<case_id>/<engine>/direct_llm_same_engine_rewrite.sql`

Rows with `format_violation` or `generation_failed` still remain explicit in `run_results.json` and still retain prompt and raw response audit files.
