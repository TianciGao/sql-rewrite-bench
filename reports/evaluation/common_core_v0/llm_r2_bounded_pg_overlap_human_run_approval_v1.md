# LLM-R2 Bounded PG Overlap Human-Run Approval v1

This record grants human approval only for a future local **human-run**
LLM-R2 bounded PostgreSQL overlap generation dry-run.

This record does not authorize Codex execution.
This record does not authorize PostgreSQL execution, checker execution, timing,
or speedup collection.
This record does not authorize MySQL, Spark, full `120`-row generation, result
card creation, proposed-row creation, or any
`method_comparison_summary_v2` update.

## Approved Slice

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0013:pg`

## Approved Goals

- runner invocation boundary
- logical-plan substrate check
- output SQL extraction
- generated SQL retention
- failure-bucket assignment
- post-run static artifact validation

## Not Approved

- no Codex execution
- no PostgreSQL execution
- no checker execution
- no timing or speedup collection
- no MySQL or Spark work
- no full `120`-row generation
- no result card or proposed row
- no `method_comparison_summary_v2` update

## Boundary

Generated outputs, if later created by the approved future local human-run, are
not paper evidence until they are reviewed and explicitly packaged in a later
governance step.
