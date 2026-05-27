# R-Bot Upstream Runner Alignment And PG Coverage Audit v1

## Scope
This is a read-only audit of the completed formal `R-Bot @120` generation run and the currently recovered `LLM4Rewrite`-based formal harness. The goal is to separate:

- original method capability
- recovered formal harness coverage
- bounded expansion opportunities for PostgreSQL coverage

This document does **not** claim that original R-Bot only supports `7/120`. The evidence here is about the current recovered formal runner surface.

## Current Formal Run Outcome

- Planned rows: `120`
- Generated: `7`
- Failed: `2`
- Blocked: `31`
- Unsupported: `80`
- Engines in denominator: `pg=40`, `mysql=40`, `spark=40`

### Exact 7 generated PG rows

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

### Exact 2 failed PG rows

- `PERF_0019:pg`
- `PERF_0033:pg`

Observed failure class for both:

- `subprocess_nonzero_exit`
- `smoke subprocess exited with code 1`

Observed deeper failure reason from recovered runner logs for both:

- crash inside retrieval query synthesis before SQL extraction
- traceback terminates in `runtime_patch_v3/rag/gen_sql_templates.py`
- exact error:
  `AttributeError: 'NoneType' object has no attribute 'find_all'`

This is a runner/runtime failure inside the patched upstream retrieval flow, not a whitelist block and not a deliberate unsupported classification.

### Exact 31 blocked PG rows

- `PERF_0007:pg`
- `PERF_0034:pg`
- `PERF_0035:pg`
- `PERF_0056:pg`
- `PERF_0062:pg`
- `PERF_0077:pg`
- `PERF_0082:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `CONS_0009:pg`
- `CONS_0010:pg`
- `CONS_0011:pg`
- `CONS_0012:pg`
- `CONS_0024:pg`
- `CONS_0036:pg`
- `CONS_0037:pg`
- `PORT_0003:pg`
- `PORT_0004:pg`
- `PORT_0005:pg`
- `PORT_0008:pg`
- `PORT_0012:pg`
- `PORT_0013:pg`
- `PORT_0022:pg`
- `PORT_0024:pg`
- `PORT_0025:pg`
- `LONGTAIL_0011:pg`
- `LONGTAIL_0012:pg`
- `LONGTAIL_0013:pg`
- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`

Exact blocker reason for all `31` blocked PG rows:

`Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.`

Blocked PG rows are therefore blocked by:

- `whitelist`: yes
- `policy`: no direct evidence
- `missing adapter`: yes, in the sense that the formal harness has not generalized the route past the subset
- `missing artifacts`: no evidence
- `missing schema/data`: no evidence
- `unimplemented runner route`: yes

The dominant cause is a recovered-harness support whitelist, not case package incompleteness.

### Exact 80 unsupported rows

All `80` unsupported rows are `MySQL` or `Spark`. None are PostgreSQL.

Exact unsupported rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `PERF_0008:mysql`
- `PERF_0008:spark`
- `PERF_0013:mysql`
- `PERF_0013:spark`
- `PERF_0017:mysql`
- `PERF_0017:spark`
- `PERF_0019:mysql`
- `PERF_0019:spark`
- `PERF_0024:mysql`
- `PERF_0024:spark`
- `PERF_0033:mysql`
- `PERF_0033:spark`
- `PERF_0034:mysql`
- `PERF_0034:spark`
- `PERF_0035:mysql`
- `PERF_0035:spark`
- `PERF_0052:mysql`
- `PERF_0052:spark`
- `PERF_0054:mysql`
- `PERF_0054:spark`
- `PERF_0056:mysql`
- `PERF_0056:spark`
- `PERF_0062:mysql`
- `PERF_0062:spark`
- `PERF_0077:mysql`
- `PERF_0077:spark`
- `PERF_0082:mysql`
- `PERF_0082:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`
- `CONS_0007:mysql`
- `CONS_0007:spark`
- `CONS_0009:mysql`
- `CONS_0009:spark`
- `CONS_0010:mysql`
- `CONS_0010:spark`
- `CONS_0011:mysql`
- `CONS_0011:spark`
- `CONS_0012:mysql`
- `CONS_0012:spark`
- `CONS_0024:mysql`
- `CONS_0024:spark`
- `CONS_0036:mysql`
- `CONS_0036:spark`
- `CONS_0037:mysql`
- `CONS_0037:spark`
- `PORT_0003:mysql`
- `PORT_0003:spark`
- `PORT_0004:mysql`
- `PORT_0004:spark`
- `PORT_0005:mysql`
- `PORT_0005:spark`
- `PORT_0008:mysql`
- `PORT_0008:spark`
- `PORT_0012:mysql`
- `PORT_0012:spark`
- `PORT_0013:mysql`
- `PORT_0013:spark`
- `PORT_0022:mysql`
- `PORT_0022:spark`
- `PORT_0024:mysql`
- `PORT_0024:spark`
- `PORT_0025:mysql`
- `PORT_0025:spark`
- `LONGTAIL_0011:mysql`
- `LONGTAIL_0011:spark`
- `LONGTAIL_0012:mysql`
- `LONGTAIL_0012:spark`
- `LONGTAIL_0013:mysql`
- `LONGTAIL_0013:spark`
- `LONGTAIL_0022:mysql`
- `LONGTAIL_0022:spark`
- `LONGTAIL_0023:mysql`
- `LONGTAIL_0023:spark`
- `LONGTAIL_0024:mysql`
- `LONGTAIL_0024:spark`

Exact unsupported reason for all `80` rows:

`Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.`

This supports:

- all unsupported rows are MySQL or Spark: yes
- MySQL/Spark unsupported in current formal harness: yes
- method-inherent impossibility proven: no
- implementation missing / route not recovered: yes

## Where The Current Formal Harness Is Narrow

The formal generation wrapper uses a hard-coded PostgreSQL support subset in `run_manual_r_bot_generation.sh`, matching a narrow recovered runner surface under `scripts/cli.py`.

Observed supported PG subset in the wrapper:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

This is already evidence that the formal harness is narrower than the full Common Core PG40 denominator:

- it is hard-coded
- it covers only a small subset
- it even contains `PERF_0063`, which is outside the formal `40`-case denominator used for the run

That pattern is consistent with a recovered smoke adapter, not with a general PG runner boundary intrinsic to the original method.

## How Upstream LLM4Rewrite Differs

Visible upstream flow under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite` is workload-driven rather than case-whitelist-driven:

- `my_rewriter/test.sh` calls:
  - `test_tpch.sh`
  - `test_dsb.sh`
  - `test_calcite.sh`
- `my_rewriter/test.py`:
  - accepts `--database`
  - loads a dataset schema
  - iterates over workload query files
  - runs `test(...)` over each query
- `my_rewriter/test_utils.py`:
  - runs `rag_retrieve(...)`
  - then `rag_rewrite(...)`
- `my_rewriter/rewrite.py` exposes general rule matching and rewrite entry points
- `my_rewriter/rag_rewrite.py` shows the upstream `retrieval -> rule selection -> arrange -> execute_rewrite` flow

The visible upstream code therefore differs from our formal harness in two important ways:

1. It is organized around general dataset/query iteration rather than a hard-coded benchmark-case whitelist.
2. It expects adapted workload inputs and environment plumbing, but not a fixed ten-case support set.

## Can Upstream Code Accept More PG Cases After Adaptation?

Best evidence-based answer: **yes, probably**, with bounded adaptation caveats.

Why this is plausible:

- upstream `test.py` iterates arbitrary query files within a dataset directory
- upstream `test_utils.py` accepts `query` and `schema` as direct inputs
- the formal harness already proved that the adapter can feed benchmark case SQL and schema into the upstream-style flow for more than one PG case

What is still not proven:

- that every Common Core PG case is accepted unchanged by the upstream retrieval/template synthesis logic
- that every case avoids the `gen_sql_templates.py` crash seen on `PERF_0019` and `PERF_0033`

So the correct statement is:

- arbitrary PG case SQL/schema after adaptation appears **feasible**
- full PG40 success is **not yet demonstrated**
- the current `7/40` PG generation coverage is **too narrow to treat as the original method boundary**

## PG40 Coverage Expansion Feasibility

### Feasibility judgment
PG40 coverage expansion appears feasible with bounded patching.

### Why

- `31` PG rows are blocked by harness gating, not by observed missing case artifacts
- the upstream visible runner pattern is broader than the local whitelist
- only `2` PG rows currently fail inside the adapted retrieval/template path, which is a concrete bug surface rather than a denominator-wide impossibility proof

### Main risks

- adapter assumptions in the recovered single-case runner
- retrieval template synthesis fragility on some queries
- possible PG case-specific parsing edge cases in the patched upstream flow

## Capability Classification

### PostgreSQL
- current formal harness coverage: narrow
- evidence of broader upstream capability: yes
- bounded expansion path: yes

### MySQL and Spark
- current formal harness classification: unsupported
- reason: recovered committed route is PG-only
- method-inherent limitation proven: no
- best classification: implementation-missing / not yet classified

## Recommended Next Patch

Primary recommendation:

- `B. expand blocked PG31`

Reason:

- this is the largest denominator gain
- the blocker is clearly the local whitelist / unrecovered general route
- it aligns the formal harness more closely with visible upstream workload behavior

Secondary recommendation:

- `A. recover failed PG2`

Reason:

- both failures share a concrete retrieval-template crash
- the fix surface looks localized

Current recommendation for non-PG engines:

- `C. keep MySQL/Spark unsupported`

Reason:

- there is no retained recovered committed same-engine mysql/spark runner path yet
- those rows should remain explicit but not be misread as original-method impossibility

Do **not** recommend:

- `D. stop and retain current boundary`

Reason:

- the evidence points to a harness recovery boundary, not a method boundary
- PG expansion looks technically bounded and worthwhile

## Bottom Line

The current formal R-Bot result should be read as:

- `7 generated + 2 failed + 31 blocked` on `PG40`
- where `31` PG rows are blocked by the recovered formal harness support surface
- and `2` PG rows fail inside the adapted upstream retrieval/template path

It should **not** be read as proof that original R-Bot only supports `7/120` or only `7/40` on PostgreSQL.
