# Formal Gate Status v7

## Scope

This document updates the formal gate status after the near-duplicate and generated-output exclusion checkers were rerun against the updated corpus text manifest and corrected Calcite output path.

It incorporates:

- [formal_gate_status_v6.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v6.md)
- [formal_near_duplicate_check_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_v1.csv)
- [formal_near_duplicate_check_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_summary.md)
- [formal_generated_output_exclusion_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_v1.csv)
- [formal_generated_output_exclusion_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_summary.md)
- [formal_generated_output_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_hashes_v1.json)
- [formal_corpus_text_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_v1.csv)
- [formal_corpus_text_manifest_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_text_manifest_summary.md)
- [formal_generated_output_source_path_audit.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_source_path_audit.md)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- near-duplicate checking: `blocked`
- generated-output exclusion: `blocked`
- near-duplicate checker now sees visible text-readable included corpus items: `31`
- near-duplicate manifest blockers are reduced to: `1`
- generated-output checker now sees visible text-readable included corpus items: `31`
- generated-output family blockers are reduced to: `0`
- stale Calcite path blocker: `resolved`
- remaining contamination blocker: `stackoverflow-rewrite-embed.zip / binary_or_unavailable_text_corpus`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## What Changed In v7

Closed relative to v6:

1. the near-duplicate checker no longer treats the visible knowledge-base text corpus as generally unavailable
2. the near-duplicate checker now sees `31` visible text-readable included corpus items
3. near-duplicate manifest blockers are reduced from `4` to `1`
4. the generated-output checker now sees `31` visible text-readable included corpus items
5. generated-output family blockers are reduced from `1` to `0`
6. the stale Calcite generated-output source-path blocker is resolved

Not closed:

1. near-duplicate rows still do not pass because the included retrieval archive remains binary-only for text-side contamination checking
2. generated-output exclusion rows still do not pass for the same reason
3. contamination attestation is still not complete for all `40` denominator cases

## Checker Results After The Rerun

### Near-Duplicate Check

- rows covered: `40`
- rows passed: `0`
- rows failed near-duplicate detection: `0`
- rows blocked: `40`
- visible text-readable included manifest items: `31`
- manifest blockers: `1`
- gate interpretation: `blocked`, not `pass`, not `fail`

Current blocker shape:

- all `40` rows are `blocked_corpus_text_unavailable`
- all `40` rows share the same blocker reason:
  - `binary_or_unavailable_text_corpus:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

### Generated-Output Exclusion

- rows covered: `357`
- rows passed: `0`
- rows failed generated-output exclusion: `0`
- rows blocked: `357`
- visible text-readable included manifest items: `31`
- manifest blockers: `1`
- generated-output family blockers: `0`
- gate interpretation: `blocked`, not `pass`, not `fail`

Coverage breakdown after the corrected Calcite path:

- `203` rows from `sqlglot`
- `120` rows from `direct_llm`
- `33` rows from `calcite`
- `1` row from `r_bot_pg1_recovery`

Current blocker shape:

- all `357` rows are `blocked_corpus_text_unavailable`
- all `357` rows share the same blocker reason:
  - `binary_or_unavailable_text_corpus:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

## Calcite Status

The stale Calcite blocker from v6 is resolved.

Resolved issue:

- old stale path:
  - `reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`

Current visible retained Calcite path used by the rerun:

- `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`

Interpretation:

- Calcite generated outputs are now being seen by the generated-output exclusion checker
- there is no longer any generated-output family blocker
- Calcite is no longer a separate gate blocker in v7

## Remaining Blocker

The remaining contamination blocker is now singular and precise:

- `stackoverflow-rewrite-embed.zip / binary_or_unavailable_text_corpus`

Why it still blocks:

1. it remains included for the formal retrieval corpus line
2. it is binary-only to the current contamination-check package
3. it is still `/tmp`-only
4. retained external provenance is still missing

Because of that one remaining blocker:

- all near-duplicate rows remain blocked
- all generated-output exclusion rows remain blocked
- contamination attestation remains incomplete for all `40` denominator cases

## Remaining Gate Blockers

1. included retrieval archive `stackoverflow-rewrite-embed.zip` remains `binary_or_unavailable_text_corpus`
2. retained external archive provenance for `stackoverflow-rewrite-embed.zip` remains incomplete
3. exact retained rebuild-time embedding provider/model/base_url identity still requires final attestation
4. the formal rebuilt retained index identifier/package does not yet exist
5. dependency lock remains candidate-only rather than a retained final lock
6. retained runtime package snapshot and environment metadata path do not yet exist
7. the future retained run package has not yet been validated against the full artifact contract

## Gate Outcome

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

v7 closes the stale Calcite source-path blocker and reduces the contamination blocker set to one precise remaining item.

However, because `stackoverflow-rewrite-embed.zip` is still included, binary-only, tmp-only, and lacking retained external provenance, the benchmark is still not gate-ready and formal `R-Bot @120` generation must not start.
