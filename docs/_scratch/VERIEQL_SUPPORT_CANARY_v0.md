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

More concretely, the positive pair is not universally equivalent as currently modeled:

- source: `SELECT EMPNO, COUNT(MGR) FROM EMP GROUP BY EMPNO, DEPTNO`
- positive: `SELECT EMPNO, CASE WHEN MGR IS NOT NULL THEN 1 ELSE 0 END FROM EMP`

The source query aggregates over `(EMPNO, DEPTNO)` groups, while the positive comparator stays row-level. VeriEQL's counterexample uses two rows with the same `(EMPNO, DEPTNO)`, one with `MGR` non-null and one with `MGR` null. Under that data:

- the source collapses the group and returns one row with count `1`
- the positive comparator returns two rows, `1` and `0`

So the `source_positive` refutation is best interpreted as missing constraint bridge evidence, not as a wrapper bug or a fresh VeriEQL runtime limitation.

The `source_negative` refutation is much cleaner:

- source: `COUNT(MGR)`
- negative: `COUNT(*)`

Those differ whenever a grouped row has `MGR IS NULL`, so `source_negative` being `non_equivalent` is expected under universal semantics.

Current support-table reading:

- yes, this can enter a bounded support table as executed verifier evidence
- caveat: only the negative refutation is clean support evidence without extra assumptions
- the positive refutation is constraint-sensitive under empty constraints and should not be treated as a clean failure of the benchmark pair itself

Follow-up bounded constraint-bridge experiment:

- report-local constraint tested: `UNIQUE (EMPNO, DEPTNO)`
- encoding used: `{"primary":[{"value":"EMP__EMPNO"},{"value":"EMP__DEPTNO"}]}`
- constrained `source_positive` result: `timeout`
- constrained `source_negative` result: `non_equivalent`

That changes the reading in an important way:

- the positive pair no longer refutes once the uniqueness bridge is supplied
- however, it also does not finish with a proof inside the bounded 600-second run
- the negative pair remains a clean refutation even with the bridge present

So the current best interpretation is:

- empty-constraint `source_positive` refutation was genuinely constraint-sensitive
- the bridge is accepted by VeriEQL and materially changes the search outcome
- but the bridge experiment is not yet a final proof of positive equivalence

## What Was Resolved

- `--case-id` generalization works for the wrapper and canary commands
- the runner-required record metadata contract is satisfied
- `input_format_mismatch` is resolved
- module-mode batch execution reaches pair processing and writes output
- z3 `ctx` runtime incompatibility is resolved for the executed path

## Next Action

Next action after the bridge experiment: keep `CONS_0035` as the active support canary and decide whether another bounded follow-up is worth the solver cost.

The current evidence already shows:

- unconstrained positive: `non_equivalent`
- constrained positive: `timeout` after repeated `EQU` states through growing bounds
- constrained negative: `non_equivalent`

That is enough to support the narrow statement that the positive result is constraint-sensitive. It is not enough yet to claim a clean proved-positive support result.

If this line is pushed further, the next step should be a bounded decision about whether to keep this as caveated support evidence or invest in a more targeted proof-oriented experiment.

Boundary remains unchanged:

- verifier/support only
- no speedup
- no PostgreSQL
- not a rewrite baseline
- not final support-table result
