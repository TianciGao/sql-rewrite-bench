# LLM-R2 Extraction / Wrapper Recovery Audit v1

## Executive Summary

This is a read-only extraction and wrapper recovery audit.

No LLM-R2 inference, PostgreSQL, MySQL, Spark, checker, timing, or speedup
work was run. No generated SQL was modified. No run artifact was replaced.

Main finding:

- The frozen PG9 bounded evidence remains valid as original recovered-route
  evidence.
- For all 6 PG6 failure rows, the retained
  `generated_sql_schema_native_v1.sql` file exactly matches the raw
  `rewritten_sql_gpt` field copied from the retained result CSV.
- The local retention wrapper in `scripts/cli.py` does not perform a
  last-`SELECT` or last-`WITH` extraction on these PG6 artifacts. It copies the
  raw field verbatim.
- The malformed shape already exists in the upstream runtime result CSV.
- The strongest retained root-cause signal is upstream wrapper/substrate
  assembly failure:
  - `src/rewriter.py` reconstructs SQL by finding the first line that starts
    with `SELECT` or `WITH`, then dropping that line via `queries = output[ind+1:-3]`.
  - This likely removes the leading `SELECT`/`WITH` line from the candidate.
  - The retained raw field also shows source-comment contamination for all 6
    PG6 rows, meaning source-layer comment text is being concatenated into the
    raw candidate string before the local wrapper copies it.

## Evidence Inspected

- PG9 bounded packet:
  - [llm_r2_pg9_bounded_evidence_reconciliation_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.md)
  - [llm_r2_pg9_bounded_evidence_reconciliation_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv)
- PG6 generation run:
  - [llm_r2_common_core_pg6_generation_dry_run_02](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_generation_dry_run_02)
  - [llm_r2_common_core_pg6_generation_attempt_ledger.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_generation_dry_run_02/llm_r2_common_core_pg6_generation_attempt_ledger.csv)
- PG6 execution/checker failure run:
  - [llm_r2_common_core_pg6_pg_execution_checker_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_pg_execution_checker_01)
  - [llm_r2_common_core_pg6_pg_execution_checker_ledger.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_pg_execution_checker_01/llm_r2_common_core_pg6_pg_execution_checker_ledger.csv)
  - [pg6_generated_execution_failure_diagnosis.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_pg_execution_checker_01/validation/pg6_generated_execution_failure_diagnosis.csv)
  - [pg6_generated_sql_malformed_pattern_diagnosis.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_common_core_pg6_pg_execution_checker_01/validation/pg6_generated_sql_malformed_pattern_diagnosis.csv)
- Local wrapper code:
  - [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:34897)
- Retained upstream substrate references:
  - `/tmp/rewritebench_llmr2_fast_path/*/runtime_root_v1/src/LLM_R2.py`
  - `/tmp/rewritebench_llmr2_fast_path/*/runtime_root_v1/src/rewriter.py`
  - `/tmp/rewritebench_llmr2_fast_path/*/runtime_root_v1/results/gpt_rewritebench_*_one_promo_queryCL_updated.csv`

## Per-Case Diagnosis

| case_id | raw CSV field malformed | generated SQL file status | comment contamination | leading `SELECT/WITH` in raw | leading `SELECT/WITH` in retained file | likely root cause | safe extraction patch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0008` | yes | exact verbatim copy of malformed CSV field | yes | no | no | first SQL line likely dropped before CSV write; source comments concatenated later in field | yes, but only as a separate recovered route |
| `PERF_0017` | yes | exact verbatim copy of malformed CSV field | yes | no | no | first SQL line likely dropped before CSV write; source comments concatenated later in field | yes, but only as a separate recovered route |
| `PERF_0019` | yes | exact verbatim copy of malformed CSV field | yes | no | no | first SQL line likely dropped before CSV write; source comments concatenated later in field | yes, but only as a separate recovered route |
| `PERF_0033` | yes | exact verbatim copy of malformed CSV field | yes | no | no | first SQL line likely dropped before CSV write; source comments concatenated later in field | yes, but only as a separate recovered route |
| `PERF_0052` | yes | exact verbatim copy of malformed CSV field | yes | yes, but malformed | yes, but malformed | likely same first-line drop on leading `WITH` plus source-comment contamination; retained CTE header appears truncated | yes, but only as a separate recovered route |
| `PERF_0054` | yes | exact verbatim copy of malformed CSV field | yes | no | no | first SQL line likely dropped before CSV write; source comments concatenated later in field | yes, but only as a separate recovered route |

Detailed retained observations:

- `PERF_0008`, `PERF_0017`, `PERF_0019`, `PERF_0033`, `PERF_0054`
  - `rewritten_sql_gpt` begins with a valid-looking query body fragment but
    not `SELECT` or `WITH`.
  - The same field later contains source comment text such as
    `-- PERF_0008 source layer` or dsqgen provenance comments.
  - After the comment block, a later full `select ...` statement is present,
    but that span is contaminated by source-material leakage and must not be
    retroactively treated as original-route success.
- `PERF_0052`
  - `rewritten_sql_gpt` begins with `select`, but the retained execution
    failure is consistent with a missing or truncated earlier `WITH` / CTE
    header.
  - A later contaminated `with ...` span also appears in the field, again
    mixed with leaked source comment content.

## Root-Cause Hypothesis

The retained evidence supports this hierarchy:

1. The local `scripts/cli.py` PG6 retention path is not the primary cause.
   - It reads the result CSV.
   - It assigns `output_sql = row.get("rewritten_sql_gpt")`.
   - It writes that value directly to
     `generated_sql_schema_native_v1.sql`.
   - No last-`SELECT/WITH` search is applied here.
2. The malformed shape is already present in the upstream runtime result CSV.
   - Retained copies under `reports/.../retained_tmp_artifacts/.../*.csv`
     exactly match the runtime copies under
     `/tmp/rewritebench_llmr2_fast_path/.../runtime_root_v1/results/...`.
3. The strongest concrete wrapper/substrate defect is in
   `/tmp/.../src/rewriter.py`.
   - It scans Java output for the first line starting with `SELECT` or `WITH`.
   - It then drops that line via `queries = output[ind+1:-3]`.
   - This directly explains the 5 rows that lost the leading `SELECT/WITH`.
   - It plausibly explains `PERF_0052` as a dropped leading `WITH` line,
     leaving a malformed inner `select` and broken CTE structure.
4. Source comment contamination is also retained in the raw field.
   - All 6 rows contain source-package comment text in `rewritten_sql_gpt`.
   - That implies the upstream route is mixing source-layer commented SQL into
     the candidate path.

## Method Failure, Wrapper Failure, or Unresolved

Current paper-safe diagnosis:

- primary classification: `wrapper_or_upstream_substrate_failure_likely`
- secondary classification: `not_resolved_without_new_recovery_route`

Why this is not a clean method-only failure:

- the retained malformed output is strongly consistent with a deterministic
  assembly bug in `rewriter.py`
- the retained malformed output is also contaminated by source comments

Why this is not fully resolved:

- the retained artifacts do not prove what the clean method candidate would
  have been after fixing the upstream assembly path
- the later full `SELECT/WITH` spans inside the raw field are contaminated by
  leaked source content and must not be backfilled into the original route

## Is an Extraction-Recovery Route Justified

Yes, but only as a separate route.

A later task could justify a narrowly scoped:

- wrapper recovery patch
- or extraction recovery patch

only if it:

- preserves the current PG9 bounded evidence packet unchanged
- creates a new recovered-extraction or recovered-wrapper route
- reruns generation and downstream validation separately
- does not reinterpret the existing original-route PG9 evidence as fixed

## Exact Safe Boundaries for Any Future Patch

Safe future patch boundary:

1. Do not patch or overwrite existing retained PG9 artifacts.
2. Do not count patched SQL as original-route method success.
3. If approved later, patch only the wrapper/substrate assembly path:
   - upstream `src/rewriter.py`
   - and, if needed, bounded local wrapper guards in `scripts/cli.py`
4. Any patched output must be emitted under a new recovered route, such as:
   - `llm_r2_pg_recovered_extraction_*`
   - or `llm_r2_pg_recovered_wrapper_*`
5. Any later local wrapper guard should only:
   - preserve the first matched `SELECT/WITH` line rather than dropping it
   - strip or reject embedded source-comment contamination
   - write recovered output to a new file name
   - never replace the original retained generated SQL files

Narrow future patch proposal:

- upstream substrate patch:
  - in `/tmp/.../src/rewriter.py`, change SQL reconstruction from
    `queries = output[ind+1:-3]`
    to logic that preserves the first matched SQL line
  - keep only the contiguous SQL block beginning at the first valid
    `SELECT/WITH` line
- bounded local wrapper guard:
  - in `scripts/cli.py`, validate `rewritten_sql_gpt` before writing
    retained candidate SQL
  - if the raw field contains embedded source-comment markers or lacks leading
    `SELECT/WITH`, do not overwrite the original route; instead emit a separate
    recovered-route artifact or fail closed

## Recommended Next Action

Human review this extraction/wrapper recovery audit and decide whether to
approve a separate LLM-R2 recovered-wrapper patch plan that preserves original
PG9 evidence and creates a new recovered route.

## Non-Claims

- This does not say LLM-R2 is fixed.
- This does not invalidate the frozen PG9 bounded evidence packet.
- This does not authorize patching `scripts/cli.py` in this task.
- This does not authorize rerunning LLM-R2.
- This does not claim PG40 or full `120` evidence.
- This does not update `method_comparison_summary_v2`.
