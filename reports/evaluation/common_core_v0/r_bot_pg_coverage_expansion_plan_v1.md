# R-Bot PG Coverage Expansion Plan v1

## Recommendation

Recommended next patch sequence:

1. `B. expand blocked PG31`
2. `A. recover failed PG2`
3. `C. keep MySQL/Spark unsupported`

Do not choose `D. stop and retain current boundary`.

## Why This Order

### 1. Expand blocked PG31 first
This is the highest-yield patch.

Observed blocker pattern:

- all `31` blocked PG rows share the same harness reason
- the blocker is a hard-coded supported-case subset in the recovered formal runner surface
- no retained evidence points to missing case SQL, missing schema, or missing witness data as the primary cause

Expected gain:

- immediate denominator expansion on PostgreSQL
- closer alignment with visible upstream `LLM4Rewrite` workload behavior
- cleaner separation between real method/runtime failures and artificial harness gating

### 2. Recover failed PG2 second
This is a localized bug fix.

Observed failure pattern:

- `PERF_0019:pg`
- `PERF_0033:pg`
- same crash in retrieval query synthesis
- same traceback endpoint in `gen_sql_templates.py`

Expected gain:

- convert two current method-execution failures into either successful generations or cleaner method-level negatives
- reduce ambiguity caused by harness/runtime crashes

### 3. Keep MySQL/Spark unsupported for now
This is the conservative boundary.

Observed status:

- all `80` unsupported rows are `mysql` or `spark`
- current retained committed route is explicitly PG-only

Why not expand these next:

- there is no retained committed same-engine mysql/spark runner path in the recovered formal harness
- upstream capability for those engines is not cleanly classified from the current evidence package
- PG expansion offers lower-risk denominator gain first

## Patch Scope For PG Expansion

### Patch family 1: remove the hard-coded PG support boundary
Targets:

- the recovered formal generation wrapper
- the `scripts/cli.py` support subset used by the `formal-rbot-llm4rewrite-single-case-smoke-run` path

Goal:

- replace a fixed supported-case subset with general PG case intake from the formal command matrix

Required guardrails:

- keep denominator awareness explicit
- continue after row failures
- preserve blocked vs failed distinctions if a row still cannot run

### Patch family 2: align inputs to visible upstream expectations
Targets:

- query text shaping
- schema text shaping
- run-name / log-path plumbing
- per-row artifact extraction

Goal:

- make the formal harness resemble upstream `test.py` and `test_utils.py` semantics more closely
- reduce wrapper-specific divergence

### Patch family 3: harden retrieval template synthesis
Targets:

- patched runtime copy of the upstream retrieval/template path
- especially the `gen_sql_templates.py` `NoneType.find_all` failure surface

Goal:

- avoid crash-only outcomes on valid PG benchmark cases
- degrade into controlled non-generation only when truly necessary

## Success Criteria

A successful PG coverage expansion patch should produce:

- fewer or no PG rows blocked solely by whitelist gating
- the same denominator-aware explicit status tracking
- clean distinction among:
  - generated
  - failed by runtime/method execution
  - blocked by true unrecovered route limitations
- no regression on the already-generated `7` PG rows

## What Not To Conclude

Do not conclude:

- original R-Bot only supports `7/120`
- original R-Bot only supports `7/40` on PostgreSQL
- MySQL/Spark are method-inherently impossible

Current evidence only supports:

- the recovered formal harness is narrower than the visible upstream runner shape
- PostgreSQL coverage expansion appears technically feasible with bounded patching
- MySQL/Spark remain implementation-missing or not yet classified in the formal harness

## Bottom Line

The next patch should target the harness boundary, not freeze it in place.

Primary action:

- `B. expand blocked PG31`

Secondary action:

- `A. recover failed PG2`

Current retained boundary for other engines:

- `C. keep MySQL/Spark unsupported`
