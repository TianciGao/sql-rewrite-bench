# Status

This note records the bounded Batch 2C PORT PostgreSQL route-matrix and reference-consistency run for:

- `PORT_0013`
- `PORT_0024`
- `PORT_0025`

Routes:

- `SQLGLOT_TRANSPILE`
- `LLM_DIRECT_TRANSLATE`

This packet is PostgreSQL only.

# Policy Basis

Checker policy applied from `docs/_scratch/BATCH2C_PORT_REFERENCE_CHECKER_POLICY_v0.md`:

- `PORT_0013`: `exact_tsv_report_local`
- `PORT_0024`: `normalized_tsv_report_local`
- `PORT_0025`: `exact_tsv_report_local`

Reference SQL source for all three cases:

- `rewrite_pos_01.sql`

# Run Sequence

- dry-run completed successfully
- one-case canary executed for `PORT_0013`
- full three-case run executed

# SQLGlot Result

PostgreSQL execution:

- success: `2 / 3`
- failed: `1 / 3`

Per case:

- `PORT_0013`
  - PostgreSQL execution: failed
  - failure category: `UndefinedFunction`
  - observed issue: generated SQL used `SUM(boolean)` in PostgreSQL
  - checker status: not checked
- `PORT_0024`
  - PostgreSQL execution: success
  - row count: `1`
  - raw exact status: inconsistent
  - normalized equal: `true`
  - checker policy result: consistent
- `PORT_0025`
  - PostgreSQL execution: success
  - row count: `1`
  - raw exact status: consistent
  - checker policy result: consistent

Consistency result:

- consistent under Batch 2C checker policy: `2`
- inconsistent under Batch 2C checker policy: `0`
- not checked because execution failed: `1`

# LLM Result

Current environment result:

- model call success: `0 / 3`
- extraction success: `0 / 3`
- PostgreSQL execution success: `0 / 3`
- PostgreSQL execution failed / blocked: `3 / 3`
- total token usage: `0`

Per case:

- `PORT_0013`
  - model call status: `env_blocked`
  - extraction status: `not_available`
  - PostgreSQL status: failed
  - failure category: `missing_api_key`
- `PORT_0024`
  - model call status: `env_blocked`
  - extraction status: `not_available`
  - PostgreSQL status: failed
  - failure category: `missing_api_key`
- `PORT_0025`
  - model call status: `env_blocked`
  - extraction status: `not_available`
  - PostgreSQL status: failed
  - failure category: `missing_api_key`

Interpretation:

- the LLM route did not fail on case-specific SQL behavior in this run
- it was blocked uniformly by missing API credentials in the current environment

# Failed / Inconsistent Cases

- `PORT_0013`
  - route: `SQLGLOT_TRANSPILE`
  - PostgreSQL failure: `UndefinedFunction`
  - summary: SQLGlot same-dialect transpile produced PostgreSQL SQL that still relies on boolean aggregation behavior not accepted by PostgreSQL
- `PORT_0024`
  - route: `SQLGLOT_TRANSPILE`
  - raw exact TSV mismatch
  - normalized checker policy: consistent
  - summary: difference collapsed under the allowed normalized TSV policy for numeric-formatting-sensitive output
- all three `LLM_DIRECT_TRANSLATE` records
  - blocked by `missing_api_key`

# Boundaries

- PostgreSQL only
- bounded Batch 2C portability slice only
- not translation correctness
- not cross-engine closure
- not speedup
- not denominator expansion by itself
- no case-local artifact writes
- `SQLGLOT_TRANSPILE` and `LLM_DIRECT_TRANSLATE` remain route evidence only under this packet
