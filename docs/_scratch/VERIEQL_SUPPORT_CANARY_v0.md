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
- VeriEQL canary run status: `failed`
- Return code: `1`
- Output artifact produced: `no`

## Per-Pair Result

- `source_positive`: `not_run`
- `source_negative`: `not_run`

No verifier verdicts were produced. There is no `EQU`, `NEQ`, `UNK`, or `TMO` pair result to report because the batch runner failed before processing the input records into runnable cases.

## Exact Blocker

- `input_format_mismatch`

Observed failure:

```text
UnboundLocalError: cannot access local variable 'file_path' where it is not associated with a value
```

The failure site is inside `parallel/cli_within_timeout.py` when it builds `parameters`. The runner accepts records with `index`, `schema`, `constraint`, and `pair`, but then also assumes one of:

- `file`
- `name`
- `benchmark`

Our wrapper scaffold intentionally emitted only the top-level keys documented in the earlier bootstrap pass, so the module-mode canary reaches the runner and then aborts on this hidden extra-field assumption.

## Interpretation

This is real support-canary evidence, but it is blocker evidence rather than solver-verdict evidence. VeriEQL cannot yet be promoted from wrapper-scaffold to usable support-canary verdict status for `CONS_0007` because the current wrapper transport does not satisfy the batch runner’s full record contract.

What is now established:

- dependency/runtime setup is good enough to launch the safe module-mode entrypoint
- the wrapper artifact is readable and parseable
- the next concrete gap is not environment setup, but input contract closure

## Next Action

Next action: patch the wrapper input contract, not the verifier route.

Concretely:

1. Extend the wrapper-emitted jsonlines records with one accepted runner metadata field such as `benchmark` or `name`.
2. Rerun the same bounded module-mode canary.
3. Only after a successful batch output artifact exists should verdict parsing and support-rate reporting be attempted.
