# FORMAL_PORT_CURRENT_RESULTS_SNAPSHOT_v0

## 1. Status

This is a tracked scratch summary of the current formal PORT results snapshot.

This snapshot is for the current PORT / RQ3 line only and is built from existing smoke and canary artifacts.

## 2. Input Reports / References

Primary snapshot command:

- `python -m scripts.cli formal-port-results-snapshot`

Reports and references used:

- `reports/baseline_smoke/sqlglot_transpile_preflight_v0.json`
- `reports/baseline_smoke/sqlglot_transpile_pg_canary_v0.json`
- `reports/baseline_smoke/sqlglot_transpile_pg_summary_v0.json`
- `reports/baseline_smoke/llm_direct_translate_prompt_packages_v0.json`
- `reports/baseline_smoke/llm_direct_translate_call_port_0004_v0.json`
- `reports/baseline_smoke/llm_direct_translate_pg_port_0004_v0.json`
- `reports/baseline_smoke/llm_direct_translate_summary_port_0004_v0.json`
- `reports/baseline_smoke/llm_direct_translate_call_port_0022_v0.json`
- `reports/baseline_smoke/llm_direct_translate_pg_port_0022_v0.json`
- `reports/baseline_smoke/llm_direct_translate_summary_port_0022_v0.json`
- `reports/baseline_smoke/llm_direct_translate_2case_rollup_v0.json`
- `docs/_scratch/PORT_0012_FAILURE_ANALYSIS_PACKET_v0.md`
- `docs/_scratch/PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0.md`
- `reports/formal_port/port_current_results_snapshot_v0.json`

## 3. Current Clean PORT Denominator

The current clean PORT denominator remains:

- `PORT_0004`
- `PORT_0022`

Held-out failure-analysis case:

- `PORT_0012`

Current denominator implication:

- the clean PORT denominator remains `PORT_0004 / PORT_0022`
- `PORT_0012` remains holdout failure-analysis / stress case
- the clean `2`-case subset should not be described as full PORT closure

## 4. SQLGlot Transpile Current Snapshot

Current SQLGlot same-target portability snapshot:

- preflight parse + transpile: `3 / 3`
- PostgreSQL execution: `2 / 3`
- failure case:
  - `PORT_0012`
- failure category:
  - `InvalidDatetimeFormat`
- failure note:
  - quoted identifier literal `'birthday'` was treated as timestamp input

Interpretation:

- SQLGlot transpile currently shows one concrete translation failure on the bounded PORT smoke set
- this is useful route evidence, but it is not translation correctness scoring

## 5. LLM Translate Current Snapshot

Current LLM translate bounded snapshot:

- prompt dry-run ready: `3 / 3`
- clean subset execution passed: `2 / 2`
- passed clean cases:
  - `PORT_0004`
  - `PORT_0022`
- total token usage:
  - `912`
- `PORT_0012`:
  - prompt-ready
  - held out of the clean canary subset

Interpretation:

- the current clean LLM translate line is the `2`-case subset only
- this is route evidence from existing smoke artifacts, not a new model run

## 6. PORT_0012 Holdout / Failure-Analysis Status

Current `PORT_0012` status:

- holdout role:
  - failure-analysis / stress case
- SQLGlot preflight:
  - success
- SQLGlot PG execution:
  - failed
- failure category:
  - `InvalidDatetimeFormat`
- failure bucket:
  - quoted identifier vs string literal confusion
  - datetime / timestamp formatting
  - dialect normalization failure
  - portability translation failure
- LLM prompt status:
  - ready
- clean subset inclusion:
  - false

## 7. Current Interpretation For RQ3

Current RQ3-facing interpretation:

- SQLGlot Transpile:
  - bounded portability smoke evidence exists
  - one concrete failure remains on `PORT_0012`
- LLM Translate:
  - clean `2`-case execution evidence exists on `PORT_0004` and `PORT_0022`
  - `PORT_0012` remains intentionally outside the clean denominator

This means:

- the current clean PORT denominator is still `PORT_0004 / PORT_0022`
- the current snapshot is useful for formal route-status reporting
- it is not enough to claim full PORT closure

## 8. Claim Boundaries

- not translation correctness
- not cross-engine consistency
- not speedup
- not final PORT leaderboard
- not registry writeback
- not formal review update

## 9. Recommended Next Action

- decide whether to run a targeted `PORT_0012` LLM translate canary later, or keep the formal PORT denominator at the clean `2`-case subset for the first formal packet

## 10. Verification / Non-Modification Note

- only this note was created
- no database workloads were run
- no SQL was executed
- no SQLGlot was run
- no checker was run
- no LLM calls were made
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
