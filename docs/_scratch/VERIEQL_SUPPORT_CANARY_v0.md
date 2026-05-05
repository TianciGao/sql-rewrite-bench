# VeriEQL Support Canary v0

## Scope

- Case: `CONS_0007`
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
  -f /home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/verieql_support/cons_0007_pairs.jsonl \
  -s 2 \
  -t 600 \
  -m train \
  -c 1 \
  -i 0 \
  -o /home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/verieql_support/cons_0007_verieql_output.jsonl
```

## Result

- Pair count: `2`
- Wrapper input exists: `yes`
- Wrapper input parseable: `yes`
- Help probe status: `success`
- Input-format mismatch resolved: `yes`
- VeriEQL canary run status: `completed`
- Return code: `0`
- Output artifact produced: `yes`
- Output artifact path: `reports/formal_expansion/verieql_support/cons_0007_verieql_output.jsonl`

## Per-Pair Result

- `source_positive`: `error`
- `source_negative`: `error`

Parseable VeriEQL output was produced for both pairs. The terminal state on both records is `NSE`, and the reported error text is:

```text
Not supported feature: EXISTS
```

That means the canary now reaches the verifier and returns per-pair support-table evidence, but the evidence is a bounded unsupported-feature outcome rather than an equivalence or non-equivalence verdict.

## Final Status

- `source_positive`: `NSE` / unsupported feature
- `source_negative`: `NSE` / unsupported feature
- `prove_count=0`
- `refute_count=0`
- `unknown_count=0`
- `timeout_count=0`
- `error_count=2`
- `support_rate_if_defined=0.0`

## Contract Fix

The previous `input_format_mismatch` is fixed.

The batch runner expects one of:

- `file`
- `name`
- `benchmark`

The wrapper scaffold now emits all three, along with `case_id` and `pair_role`, so the runner no longer aborts before verification.

## Exact Blocker After Contract Fix

There is no longer an input-contract blocker. The remaining limitation is verifier feature support:

```text
Not supported feature: EXISTS
```

This is support-table evidence, not a runner/bootstrap failure. VeriEQL executed the bounded canary and explicitly reported that both `CONS_0007` pairs use a feature it does not support in this path.

## Interpretation

This is real support-canary evidence, and it does promote the line beyond wrapper-only status. The line now has executed verifier evidence on `CONS_0007`. However, it is not support-clean evidence: both pairs terminate in `NSE`, so VeriEQL is still not usable on this canary as a practical support-table method for the current case.

What is now established:

- dependency/runtime setup is good enough to launch the safe module-mode entrypoint
- the wrapper artifact is readable, parseable, and contract-complete for the batch runner
- the verifier produces parseable output artifacts on this canary
- the remaining limitation is feature support for `EXISTS`

## Next Action

Next action: do not spend more effort on this exact `CONS_0007` pair unless `EXISTS` support is a deliberate target.

Concretely:

1. Keep the wrapper contract patch.
2. Record this canary as executed support evidence with `NSE` outcomes.
3. If the VeriEQL line is advanced further, choose a simpler consistency case without `EXISTS`, or treat `EXISTS` as a current unsupported-feature boundary for the support table.
