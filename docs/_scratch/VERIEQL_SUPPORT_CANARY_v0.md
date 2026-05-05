# VeriEQL Support Canary v0

## Scope

- Case: `CONS_0035`
- Pair roles:
  - `source_positive`
  - `source_negative`
- Boundary:
  - verifier/support only
  - no speedup
  - no PostgreSQL
  - not a rewrite baseline
  - not final support-table result

## Command Used

Help probe:

```bash
cd datasets/raw/verieql/staged/VeriEQL
/tmp/verieql-probe-venv/bin/python -m parallel.cli_within_timeout --help
```

Canary execution:

```bash
cd datasets/raw/verieql/staged/VeriEQL
/tmp/verieql-probe-venv/bin/python -m parallel.cli_within_timeout \
  -f /home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/verieql_support/cons_0035_pairs.jsonl \
  -s 2 \
  -t 600 \
  -m train \
  -c 1 \
  -i 0 \
  -o /home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/verieql_support/cons_0035_verieql_output.jsonl
```

## Result

- Pair count: `2`
- Wrapper input exists: `yes`
- Wrapper input parseable: `yes`
- Help probe status: `success`
- VeriEQL canary run status: `completed`
- Return code: `0`
- Output artifact produced: `yes`
- Output artifact path: `reports/formal_expansion/verieql_support/cons_0035_verieql_output.jsonl`
- Exact blocker: `runtime_exception`

## Per-Pair Result

- `source_positive`: `error`
- `source_negative`: `error`

Parseable VeriEQL output was produced for both pairs. The terminal state on both records is `OTE`, and the reported error text is:

```text
Or() got an unexpected keyword argument 'ctx'
```

That means the canary reaches the verifier, consumes the wrapper input contract correctly, and produces parseable output artifacts, but both pair evaluations terminate inside VeriEQL with a runtime exception rather than a verdict.

## Final Status

- `source_positive`: `OTE` / runtime error
- `source_negative`: `OTE` / runtime error
- `prove_count=0`
- `refute_count=0`
- `unknown_count=0`
- `timeout_count=0`
- `error_count=2`
- `support_rate_if_defined=0.0`

## Interpretation

This is real support-canary evidence for `CONS_0035`. It improves on the `CONS_0007` path in one important way: the blocker is no longer unsupported `EXISTS`, and the wrapper/input contract is no longer the issue. The safe module-mode VeriEQL runner now accepts the `CONS_0035` records and produces a parseable output artifact.

The remaining blocker is internal VeriEQL runtime behavior:

```text
Or() got an unexpected keyword argument 'ctx'
```

So this line is now beyond wrapper-only and beyond input-contract debugging, but it is still not support-clean on `CONS_0035`.

## What Was Resolved

- `--case-id` generalization works for the wrapper and canary commands
- the runner-required record metadata contract is satisfied
- `input_format_mismatch` is resolved
- module-mode batch execution reaches pair processing and writes output

## Next Action

Next action: do not search for an even simpler SQL shape yet. The active blocker is now a VeriEQL runtime issue in the staged implementation, not the specific `CONS_0035` feature profile.

Concretely:

1. Treat `CONS_0035` as the current best executed support-canary evidence.
2. If the VeriEQL line is advanced further, investigate the staged `constants.py` / z3 wrapper incompatibility behind `Or(..., ctx=...)`.
3. Only after that runtime issue is addressed should another bounded support verdict attempt be considered meaningful.
