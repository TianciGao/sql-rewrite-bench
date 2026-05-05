# VeriEQL Runtime Compatibility Diagnostic v0

## Scope

- Runtime line: staged VeriEQL under `datasets/raw/verieql/staged/VeriEQL/`
- Bounded canary case: `CONS_0035`
- Boundary:
  - verifier/support only
  - no speedup
  - no PostgreSQL
  - not a rewrite baseline
  - not final support-table result

## Runtime Cause

The active blocker was a z3 API compatibility mismatch between staged VeriEQL and the installed `z3-solver` in `/tmp/verieql-probe-venv`.

Observed runtime:

- Python version: `3.12.3`
- z3 package version attribute: `unknown`
- z3 core version: `4.16.0`

Direct probe result:

- `z3.Or(..., ctx=z3.Context())` -> `TypeError`
- `z3.And(..., ctx=z3.Context())` -> `TypeError`
- `z3.Sum(..., ctx=z3.Context())` -> `TypeError`

At the same time, scalar constructors still accepted `ctx=...`, including:

- `BoolVal`
- `IntVal`
- `RealVal`
- `Int`
- `Not`
- `If`
- `Implies`

So the exact compatibility cause was:

```text
z3 4.16 rejects ctx= on variadic combinators such as And, Or, and Sum,
while staged VeriEQL wrapped those constructors as if ctx= were still accepted.
```

## Code Search Result

The directly relevant wrapper definitions were in:

- [constants.py](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/constants.py)

Pre-patch behavior:

- `Sum = lambda *args: Z3_Sum(*args, ctx=Z3_CONTEXT)`
- `And = lambda *args: Z3_And(*args, ctx=Z3_CONTEXT)`
- `Or = lambda *args: Z3_Or(*args, ctx=Z3_CONTEXT)`

This matched the observed failures:

- `Or() got an unexpected keyword argument 'ctx'`
- earlier sample path: `And() got an unexpected keyword argument 'ctx'`

## Patch

Patched file:

- [constants.py](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/constants.py)

Minimal compatibility patch:

- keep `ctx=Z3_CONTEXT` on constructors that still support it
- remove `ctx=` only from `Sum`, `And`, and `Or`

Post-patch wrapper behavior:

- `Sum = lambda *args: Z3_Sum(*args)`
- `And = lambda *args: Z3_And(*args)`
- `Or = lambda *args: Z3_Or(*args)`

Why this is the smallest safe patch:

- the operands passed into these combinators are already created in `Z3_CONTEXT`
- no global dependency pinning was required
- no wrapper contract or case SQL changes were required

## Post-Patch Canary Result

Reran bounded canary:

```bash
python -m scripts.cli formal-verieql-support-canary --case-id CONS_0035 --execute
```

Result:

- canary reached verdict stage: `yes`
- `source_positive_status=non_equivalent`
- `source_negative_status=non_equivalent`
- `prove_count=0`
- `refute_count=2`
- `unknown_count=0`
- `timeout_count=0`
- `error_count=0`

VeriEQL output was parseable and counterexample-backed for both pairs.

## Remaining Blocker

No runtime compatibility blocker remains on the executed `CONS_0035` path.

The remaining limitation is interpretive rather than operational:

- the current first-pass policy leaves constraints empty
- under that policy, VeriEQL refuted both the positive and negative pairs

So the next question is not runtime compatibility. It is whether stronger constraint modeling is needed before using positive-pair outcomes as stronger support evidence.

## Conclusion

The exact runtime compatibility cause was confirmed and fixed locally. `CONS_0035` now provides real module-mode VeriEQL verdict evidence rather than runtime-error evidence.
