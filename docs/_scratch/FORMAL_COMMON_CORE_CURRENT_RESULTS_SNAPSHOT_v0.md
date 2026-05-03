# FORMAL_COMMON_CORE_CURRENT_RESULTS_SNAPSHOT_v0

## 1. Status

This is a tracked scratch snapshot of the current formal common-core results state.

It summarizes the current formal route status across:

- control routes
- SQLGlot same-dialect
- Direct LLM rewrite

## 2. Inputs / Report References

- `reports/formal_common_core/control_scoring_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_v0.json`

## 3. Current Route Snapshot

| route | execution status | executable rate | row-count observation | checker-backed consistency status | token usage | speedup status | claim boundary |
|---|---|---:|---|---|---|---|---|
| `NATIVE_IDENTITY / HUMAN_REFERENCE_POSITIVE / HARD_NEGATIVE_GUARD` | complete from existing formal execution reports | `1.0 / 1.0 / 1.0` | positive match `9/9`; hard negative differs `4/9`, same `5/9` | control scoring complete from existing checker artifacts: result consistency `1.0`, negative rejection `1.0`, false accept `0.0` | n/a | `false` | control-route scoring only, not leaderboard |
| `SQLGLOT_OPT_SAME_DIALECT` | formal execution complete | `1.0` | match `9/9` | `not_computed_checker_required` | n/a | `false` | row-count observation only, not correctness |
| `LLM_DIRECT_REWRITE_STRONG` | formalized from existing smoke execution reports | `1.0` | match `9/9` | `not_computed_checker_required` | `5089 total tokens` | `false` | existing-report formalization only, not correctness |

## 4. Interpretation

Current formal common-core state:

- control scoring is complete
- SQLGlot execution and row-count observation are complete, but checker-backed consistency is not computed
- Direct LLM scoring is based on existing reports only
- speedup is not computed for any route
- no leaderboard claim is available from the current state

## 5. Route Notes

### 5.1 Control Routes

- executable-rate layer is complete
- checker-backed control scoring is complete
- this is the strongest current formal route family

### 5.2 SQLGlot Same-Dialect

- parse, generation, and execution are complete on the 9-case denominator
- row-count matched native on `9 / 9`
- checker-backed route correctness is still not available

### 5.3 Direct LLM Rewrite

- execution formalization reused existing smoke call and PG artifacts
- execution succeeded on `9 / 9`
- total token usage is `5089`
- checker-backed route correctness is still not available

## 6. Boundary

- no leaderboard claim
- no speedup scoring
- row-count observations are not semantic correctness by themselves
- SQLGlot and Direct LLM checker-backed route consistency are still incomplete

## 7. Recommended Next Action

- begin route-specific checker-backed formal scoring for the learned / generated baselines starting from Direct LLM rewrite or define an explicit deferred correctness boundary if route-specific checker evidence remains unavailable

## 8. Verification / Non-Modification Note

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
