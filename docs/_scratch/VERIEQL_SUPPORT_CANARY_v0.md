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
- Exact blocker: ``

## Per-Pair Result

- `source_positive`: `non_equivalent`
- `source_negative`: `non_equivalent`

Parseable VeriEQL output was produced for both pairs. Both records now reach verdict stage and return counterexample-backed non-equivalence:

- `source_positive`: states `EQU -> NEQ`, final result `non_equivalent`
- `source_negative`: states `NEQ`, final result `non_equivalent`

## Final Status

- `source_positive`: `non_equivalent`
- `source_negative`: `non_equivalent`
- `prove_count=0`
- `refute_count=2`
- `unknown_count=0`
- `timeout_count=0`
- `error_count=0`
- `support_rate_if_defined=1.0`

## Interpretation

This is real support-canary evidence for `CONS_0035`. The safe module-mode VeriEQL runner accepts the wrapper records, executes both pairs, and produces parseable verdict output.

The earlier runtime blocker:

```text
Or() got an unexpected keyword argument 'ctx'
```

was resolved by a local compatibility patch in VeriEQL's z3 wrappers. This bounded canary is therefore beyond wrapper-only and beyond runtime-compatibility debugging.

Interpretation of the verdicts should remain narrow:

- `source_negative` refuting is expected support evidence.
- `source_positive` also refuted under the current first-pass empty-constraint policy.
- This does not mean the benchmark pair is wrong by itself; it means VeriEQL found a counterexample under the currently modeled schema and no extra constraints.

## What Was Resolved

- `--case-id` generalization works for the wrapper and canary commands
- the runner-required record metadata contract is satisfied
- `input_format_mismatch` is resolved
- module-mode batch execution reaches pair processing and writes output
- z3 `ctx` runtime incompatibility is resolved for the executed path

## Next Action

Next action: treat `CONS_0035` as the first real VeriEQL support-canary verdict case, then decide whether to:

- keep the current first-pass empty-constraint policy and record this as bounded refutation evidence, or
- add case-specific constraint modeling before interpreting positive-pair outcomes more strongly.

Boundary remains unchanged:

- verifier/support only
- no speedup
- no PostgreSQL
- not a rewrite baseline
- not final support-table result
