# VeriEQL Support Constraint Bridge v0

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

## Constraint Policy

- Baseline already recorded: empty constraint
- Report-local bridge tested here:
  - `UNIQUE (EMPNO, DEPTNO)`
- VeriEQL encoding used:

```json
{"primary":[{"value":"EMP__EMPNO"},{"value":"EMP__DEPTNO"}]}
```

- Input artifact:
  - `reports/formal_expansion/verieql_support/cons_0035_pairs_with_constraints.jsonl`

The original unconstrained wrapper artifact was preserved unchanged.

## Result

- `constraint_encoding_status=structured_primary_constraint_emitted`
- `source_positive_empty_constraint_status=non_equivalent`
- `source_positive_constrained_status=timeout`
- `source_negative_empty_constraint_status=non_equivalent`
- `source_negative_constrained_status=non_equivalent`
- `prove_count=0`
- `refute_count=1`
- `unknown_count=0`
- `timeout_count=1`
- `error_count=0`
- `support_rate_if_defined=0.5`
- `exact_blocker_if_any=` empty

## What Changed

The constraint bridge was accepted and materially changed the positive-pair outcome.

Unconstrained positive:

- VeriEQL found a concrete counterexample with two rows in the same `(EMPNO, DEPTNO)` group
- final status: `non_equivalent`

Constrained positive:

- VeriEQL stayed in `EQU` across many increasing bounds
- no counterexample was produced
- final status at the bounded limit: `timeout`

This means the earlier positive refutation was genuinely constraint-sensitive.

The constraint did not produce a final proof inside the bounded run, so the result is:

- stronger than the empty-constraint refutation alone
- weaker than a finished equivalence proof

## Negative Pair

The negative pair remained `non_equivalent` even with the uniqueness bridge present.

That strengthens the negative support evidence, because the clean `COUNT(MGR)` versus `COUNT(*)` mismatch survives the added bridge.

## Solver Cost Signal

The constrained positive path became much more expensive:

- it progressed through repeated `EQU` states
- solving time grew sharply with larger bounds
- it hit the 600-second timeout limit without producing either a counterexample or a proof

So the bridge appears meaningful, but also costly for VeriEQL on this case.

## Interpretation

Current best reading:

- `source_negative` is clean support evidence
- `source_positive` is constraint-sensitive
- the tested uniqueness bridge removes the immediate refutation behavior
- but bounded verification still stops at timeout, not proof

So this can be recorded as:

- support-canary verdict evidence with a stronger caveat than before

The caveat is now:

- empty constraints refute the positive pair
- uniqueness bridge suppresses that refutation but does not finish proof within the bounded run

## Next Step

Recommended next step: keep `CONS_0035` as bounded support evidence with caveat, rather than claiming final positive support closure.

If more work is justified later, it should be a narrowly scoped proof-oriented follow-up on this same constrained pair, not a restart from wrapper or runtime debugging.
