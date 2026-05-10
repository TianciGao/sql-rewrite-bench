# LLM-R2 Bounded PG Overlap Execution Runbook v1

This is a future human-run runbook only.

This task does not authorize execution.

- no commands in this runbook were run in this task
- no SQL was generated in this task
- no database was executed in this task
- no timing was collected in this task
- this does not create `120`-row LLM-R2 evidence

## Candidate slice summary

The bounded PostgreSQL overlap candidate slice currently contains `8` rows:

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0013:pg`

All rows remain:

- `planned_for_future_dry_run = true`
- `current_generation_status = not_run`
- `current_execution_status = not_run`

## Future human-run phases

### 1. Pre-run static validation

- purpose:
  - confirm static coherence of manifest, candidate matrix, run plan, and
    recovery inventory before any runner-facing work
- required inputs:
  - rerun manifest
  - candidate matrix
  - run plan JSON
  - runner recovery inventory JSON
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
python reports/evaluation/common_core_v0/llm_r2_120_runner_dry_run_validator_v1.py \
  --manifest reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv \
  --candidate-matrix reports/evaluation/common_core_v0/llm_r2_120_candidate_matrix_v1.csv \
  --run-plan reports/evaluation/common_core_v0/llm_r2_120_run_plan_v1.json \
  --recovery-inventory reports/evaluation/common_core_v0/llm_r2_120_runner_recovery_inventory_v1.json
```

- expected outputs:
  - static validation JSON report
- stop conditions:
  - validator reports missing keys or wrong row counts
- failure bucket if failed:
  - `unknown_not_recovered`
- explicit non-claims:
  - no LLM-R2 invocation
  - no generation

### 2. Runner availability check

- purpose:
  - verify whether the recovered runner boundary can be entered safely
- required inputs:
  - runner recovery scaffold
  - runner recovery inventory
  - candidate slice
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run llm-r2 runner availability probe wrapper>
Requires separate human approval before any use.
Must not execute PostgreSQL, MySQL, Spark, timing, or benchmark commands.
```

- expected outputs:
  - runner readiness report
  - per-row runner availability notes
- stop conditions:
  - runner cannot load or wrapper cannot initialize
- failure bucket if failed:
  - `generation_failed`
- explicit non-claims:
  - no correctness evidence
  - no timing evidence

### 3. Logical-plan substrate check

- purpose:
  - observe whether the logical-plan substrate can progress far enough to
    support later SQL extraction
- required inputs:
  - runner availability output
  - retained logical-plan substrate notes
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run llm-r2 logical-plan substrate probe on bounded pg slice>
Requires separate human approval before any use.
```

- expected outputs:
  - per-row logical-plan substrate notes
  - substrate failure ledger
- stop conditions:
  - logical-plan substrate fails before SQL extraction can be attempted
- failure bucket if failed:
  - `parse_failed`
- explicit non-claims:
  - no SQL execution
  - no timing

### 4. Bounded PG generation dry-run

- purpose:
  - attempt bounded PG-only route generation once earlier gates pass
- required inputs:
  - approved candidate slice
  - runner boundary accepted
  - logical-plan substrate accepted
  - output retention path accepted
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run llm-r2 bounded pg generation dry-run wrapper>
Requires separate human approval before any use.
No PostgreSQL execution is included in this phase.
```

- expected outputs:
  - per-row generation attempt log
  - retained raw LLM-R2 outputs
  - generated SQL files only if actually produced
- stop conditions:
  - route cannot produce bounded dry-run outputs safely
- failure bucket if failed:
  - `generation_failed`
- explicit non-claims:
  - no execution
  - no timing

### 5. Output SQL extraction check

- purpose:
  - verify whether generated raw outputs can yield explicit `output_sql` files
- required inputs:
  - retained raw outputs from the future bounded dry-run
  - extraction contract expectations
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run extraction review step on bounded pg dry-run outputs>
Requires separate human approval before any use.
```

- expected outputs:
  - extracted output SQL files
  - extraction status ledger
- stop conditions:
  - `output_sql` cannot be extracted
- failure bucket if failed:
  - `generation_failed`
- explicit non-claims:
  - no checker execution
  - no timing

### 6. Generated SQL retention check

- purpose:
  - verify generated SQL retention path and artifact completeness
- required inputs:
  - extracted SQL files if present
  - retention-path contract
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run artifact retention verification on bounded pg dry-run outputs>
Requires separate human approval before any use.
```

- expected outputs:
  - retention-path verification note
  - artifact completeness ledger
- stop conditions:
  - generated SQL path cannot be retained consistently
- failure bucket if failed:
  - `unknown_not_recovered`
- explicit non-claims:
  - no execution validity claim

### 7. Failure-bucket assignment

- purpose:
  - assign fail-closed buckets for every attempted row in the bounded slice
- required inputs:
  - bounded dry-run attempt logs
  - failure bucket policy
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run failure-bucket assignment step using Stage-0 policy>
Requires separate human approval before any use.
```

- expected outputs:
  - failure bucket ledger
- stop conditions:
  - failure bucket cannot be assigned deterministically
- failure bucket if failed:
  - `unknown_not_recovered`
- explicit non-claims:
  - no exact-match evidence
  - no timing evidence

### 8. Post-run static artifact validation

- purpose:
  - confirm expected dry-run artifacts exist and are internally coherent
- required inputs:
  - failure bucket ledger
  - generation attempt logs
  - extracted SQL files if present
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human-run static artifact validation over bounded pg dry-run outputs>
Must remain local-only and must not invoke databases.
```

- expected outputs:
  - static validation report
- stop conditions:
  - expected artifacts are missing or inconsistent
- failure bucket if failed:
  - `unknown_not_recovered`
- explicit non-claims:
  - no execution
  - no timing

### 9. Human review before any execution/checker/timing

- purpose:
  - ensure that any later move toward execution, checker, or timing remains a
    separate approval decision
- required inputs:
  - all bounded dry-run artifacts
  - approval gate
- future human-run command placeholder:

```text
FUTURE HUMAN-RUN TEMPLATE ONLY — NOT EXECUTED IN THIS TASK
<future human review checkpoint>
No database execution, checker run, or timing run may proceed without separate
explicit approval.
```

- expected outputs:
  - human review note
- stop conditions:
  - approval is absent
- failure bucket if failed:
  - `methodology_boundary`
- explicit non-claims:
  - no automatic promotion to execution
  - no result card or proposed row
