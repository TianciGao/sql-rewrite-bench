# LLM-R2 Unsupported PG5 Wrapper Extension Plan v1

This note is wrapper-extension planning only.

The following 5 rows from the original approved 8-row PostgreSQL slice are not
authorized for execution:

- `PERF_0007:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0013:pg`

They require wrapper extension or case adaptation before any later run
discussion.

No runner is modified in this task.
No case is executed in this task.
Any extension path must be separately approved before implementation or use.

## Likely Blocker Categories

- `PERF_0007:pg`
  - likely blocker category: current recovered runner support set does not
    declare this case
- `CONS_0005:pg`
  - likely blocker category: current recovered runner support set does not
    declare this consistency case
- `CONS_0007:pg`
  - likely blocker category: current recovered runner support set does not
    declare this consistency case
- `LONGTAIL_0011:pg`
  - likely blocker category: current recovered runner support set does not
    declare this long-tail case
- `LONGTAIL_0013:pg`
  - likely blocker category: current recovered runner support set does not
    declare this long-tail case

## Boundary

- unsupported PG5 rows are not approved for immediate future human-run use
- no MySQL or Spark support is implied
- no database execution, checker, timing, result card, or proposed row work is
  authorized
