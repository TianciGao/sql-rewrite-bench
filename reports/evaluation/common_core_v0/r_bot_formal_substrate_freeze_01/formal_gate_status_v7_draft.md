# Formal Gate Status v7 Draft

## Scope

This is a draft gate-status update after the corpus retention and text-manifest completion package.

It incorporates:

- [formal_gate_status_v6.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v6.md)
- [formal_corpus_retention_plan.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_retention_plan.md)
- [formal_corpus_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_v1.csv)
- [formal_corpus_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_summary.md)
- [formal_corpus_text_availability_matrix.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_availability_matrix.csv)
- [formal_generated_output_source_path_audit.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_source_path_audit.md)

It remains a draft only.
It does not authorize generation.

## Draft Direct Answers

- corpus text availability status: `partial`
- near-duplicate checking currently stands as of executed evidence: `blocked`
- generated-output exclusion currently stands as of executed evidence: `blocked`
- near-duplicate checker can be rerun meaningfully against the visible text corpus subset: `yes`
- generated-output exclusion checker can be rerun meaningfully against the visible text corpus subset: `yes`
- missing Calcite path root cause: `stale checker/template path`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## What Improved In This Draft

1. the visible retrieval corpus is no longer a single opaque `manifest_text_unavailable` bucket
2. `31` text-readable included corpus rows are now explicitly manifested
3. the remaining included non-text corpus blocker is reduced to one precise item:
   - `stackoverflow-rewrite-embed.zip`
4. the single Calcite blocker is now traced to a stale path/template assumption rather than a blanket “no Calcite outputs exist” interpretation

## What Is Still Not Closed

### Contamination gate

Still blocked because:

1. the included retrieval archive `stackoverflow-rewrite-embed.zip` remains binary-only to this package
2. that archive is still `/tmp`-only and still lacks retained external provenance
3. the newly manifested text corpus is still not formally retained as a current retained corpus line

### Generated-output exclusion gate

Still blocked at draft level because:

1. the archive blocker above still prevents full include-side contamination closure
2. the Calcite family input path in the old human-run checker package is stale and must be corrected before the next rerun

## Draft Replacement For The Old Blanket Blocker

The old blocker text:

- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`
- `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

should no longer be interpreted as one undifferentiated visibility failure.

The more precise draft interpretation is:

1. knowledge-base text rows are visible and text-readable
2. the remaining include-side text blocker is the binary-only archive
3. the remaining Calcite family blocker is a stale generated-output source path

## Recommended Next Package

The next package should be a human-run rerun package that:

1. consumes `formal_corpus_text_manifest_v1.csv` for include-side text availability
2. carries forward an explicit blocker for `stackoverflow-rewrite-embed.zip` unless a retained text-readable expansion or retained external provenance closure is added
3. retargets the Calcite generated-output family to the actual retained root:
   - `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`

## Gate Outcome

The overall formal gate remains closed in this draft.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

This package improves the substrate evidence enough to support a more meaningful next rerun of the human-run contamination checks.

It does **not** make the benchmark gate-ready, and it does **not** permit formal `R-Bot @120` generation to start.
