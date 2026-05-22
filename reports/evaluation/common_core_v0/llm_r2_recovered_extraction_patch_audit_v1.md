# LLM-R2 Recovered-Extraction Patch Audit v1

This is a patch audit and scaffold review only.

No LLM-R2 inference, PostgreSQL, MySQL, Spark, checker, timing, or speedup
work was run.

## Executive Summary

The retained extraction audit isolated a likely upstream assembly defect and
source-comment contamination boundary. `scripts/cli.py` now contains a narrow
separate-route scaffold for a future recovered-extraction path.

This patch does not touch:

- frozen PG9 bounded evidence
- retained run artifacts
- existing generated SQL files
- the global upstream external repo under `/tmp/rewritebench_llmr2_audit/LLM-R2`

## Exact CLI Additions

Added in `scripts/cli.py`:

- `LLMR2_RECOVERED_EXTRACTION_ROUTE_ROOT`
- `LLMR2_RECOVERED_EXTRACTION_ROUTE_ID`
- `llmr2_patch_rewriter_text_for_recovered_extraction(...)`
- `llmr2_recovered_extraction_from_raw_field(...)`
- `cmd_formal_llmr2_recovered_extraction_route(...)`
- parser entry for `formal-llmr2-recovered-extraction-route`

## Exact Staged Patch Boundary

The staged-runtime patch helper targets only the copied `rewriter.py` inside a
future recovered-route runtime root.

Original retained behavior:

```python
queries = output[ind+1:-3]
output = ' '.join(queries).replace('"', '')
```

Recovered-route staged behavior:

- start at `output[ind:-3]` so the first matched `SELECT/WITH` line is retained
- stop collecting once source-comment contamination begins
- preserve only the deterministic SQL block

## Exact Extraction Guard Boundary

The local recovered extraction helper:

- searches the raw field for the first line beginning with `SELECT` or `WITH`
- starts the candidate at that boundary
- strips full-line or inline source comments after that boundary
- records whether source comments were detected and stripped
- records whether the recovered candidate still begins with `SELECT` or `WITH`
- permits future candidate writing only if the recovered candidate preserves
  that SQL start boundary

This helper is deterministic text-boundary recovery only. It does not perform
semantic SQL repair.

## Per-Case Recovery Intent

| case_id | original route diagnosis | recovered-route intent |
| --- | --- | --- |
| `PERF_0008` | raw field missing leading `SELECT` and contaminated by source comments | preserve the first SQL line in staged `rewriter.py`; reject or strip later source comments in recovered route only |
| `PERF_0017` | same as `PERF_0008` | same recovered-route boundary |
| `PERF_0019` | same as `PERF_0008` | same recovered-route boundary |
| `PERF_0033` | same as `PERF_0008` plus dsqgen provenance leakage | same recovered-route boundary |
| `PERF_0052` | malformed or truncated CTE-WITH structure | preserve leading `WITH` line if dropped by staged rewriter and stop at source-comment contamination boundary |
| `PERF_0054` | same as `PERF_0008` | same recovered-route boundary |

## Safety Boundary

This patch is intentionally incomplete as an execution route.

Current state:

- dry-run-only scaffold exists
- route id and artifact family are fixed
- staged runtime patch target is fixed
- recovered extraction rule is fixed
- no recovered-route execution is enabled yet

This is deliberate. It forces a separate approval decision before any new run
is attempted.

## Current Classification

Paper-safe classification after this scaffold:

- original PG9 packet: still canonical original-route bounded appendix evidence
- recovered extraction route: possible future engineering recovery path only
- no fixed LLM-R2 claim
- no new evidence claim

## Recommended Next Action

Human review the recovered-extraction scaffold and decide whether to approve a
separate recovered-route human-run plan, or stop and preserve PG9 as final.

## Non-Claims

- This does not say the method is fixed.
- This does not invalidate the frozen PG9 evidence packet.
- This does not authorize execution of the recovered route.
- This does not update `method_comparison_summary_v2`.
