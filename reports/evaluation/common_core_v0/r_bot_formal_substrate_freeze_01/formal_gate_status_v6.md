# Formal Gate Status v6

## Scope

This document updates the formal gate status after the human-run near-duplicate and generated-output exclusion checks.

It incorporates:

- [formal_gate_status_v5.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v5.md)
- [formal_near_duplicate_check_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_v1.csv)
- [formal_near_duplicate_check_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_near_duplicate_check_summary.md)
- [formal_generated_output_exclusion_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_v1.csv)
- [formal_generated_output_exclusion_summary.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_exclusion_summary.md)
- [formal_generated_output_hashes_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_generated_output_hashes_v1.json)
- [formal_retrieval_config_v4.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_retrieval_config_v4.json)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a gate-status document only.
It does not authorize generation.

## Direct Answers

- near-duplicate checking: `blocked`
- generated-output exclusion: `blocked`
- rows still blocked because corpus text is unavailable: `yes`
- contamination attestation complete for all 40 cases: `no`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## What Changed In v6

Closed as process/evidence improvements:

1. human-run near-duplicate checking now exists as a machine-readable package
2. human-run generated-output exclusion checking now exists as a machine-readable package
3. the previous v5 blocker "`machine-readable near-duplicate exclusion checking is not implemented`" is no longer accurate

Not closed substantively:

1. near-duplicate checking did not pass any denominator rows
2. generated-output exclusion did not pass any generated-output rows
3. contamination attestation did not become complete

## Human-Run Check Results

### Near-Duplicate Check

- rows covered: `40`
- rows passed: `0`
- rows failed near-duplicate detection: `0`
- rows blocked: `40`
- gate interpretation: `blocked`, not `pass`, not `fail`

Why blocked:

- all `40` rows have `corpus_text_available = no`
- all `40` rows have `attestation_status = blocked_corpus_text_unavailable`
- all `40` rows share the same blocker family:
  - `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
  - `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
  - `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`
  - `manifest_text_unavailable:/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

Affected denominator cases:

`PERF_0006`, `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`, `CONS_0005`, `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`, `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`, `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`

### Generated-Output Exclusion

- rows covered: `325`
- rows passed: `0`
- rows failed generated-output exclusion: `0`
- rows blocked: `325`
- gate interpretation: `blocked`, not `pass`, not `fail`

Blocker breakdown:

- `324` rows: `blocked_corpus_text_unavailable`
- `1` row: `blocked_missing_generated_output_source`

Coverage breakdown:

- `203` rows from `sqlglot`
- `120` rows from `direct_llm`
- `1` row from `r_bot_pg1_recovery`
- `1` row from `calcite`

Additional generated-output blocker from the hash package:

- `generated_source_missing:calcite:/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`

## Contamination Status After v6

The contamination gate remains blocked.

Reasoning:

1. near-duplicate attestation is blocked on all `40` denominator rows
2. generated-output exclusion is blocked on all `325` generated-output rows
3. visible text-readable included manifest items remain `4`, with `4` manifest blockers
4. generated-output family coverage still has `1` blocker, the missing `calcite` generated-output source

Therefore:

- there are still rows blocked because corpus text is unavailable
- contamination attestation is not complete for all `40` cases
- no formal pass/fail contamination conclusion can be issued yet for the denominator

## Remaining Blockers

1. near-duplicate attestation remains blocked for all `40` denominator rows because included corpus text is unavailable
2. generated-output exclusion remains blocked for `324` generated-output rows because included corpus text is unavailable
3. generated-output exclusion remains additionally blocked by one missing generated-output source for the `calcite` family
4. corpus manifest completeness remains insufficient for deterministic text-readable and hashable contamination attestation
5. retained external archive provenance for `stackoverflow-rewrite-embed.zip` remains incomplete
6. exact retained rebuild-time embedding provider/model/base_url identity still requires final attestation
7. the formal rebuilt retained index identifier/package does not yet exist
8. dependency lock remains candidate-only rather than a retained final lock
9. retained runtime package snapshot and environment metadata path do not yet exist
10. the future retained run package has not yet been validated against the full artifact contract

## Recommended Next Package

The next package should be a corpus-manifest and generated-output coverage closure package.

It should do all of the following before any new gate reopening attempt:

1. materialize text-readable retained corpus coverage for every included manifest entry used by the contamination checks
2. close retained provenance for `stackoverflow-rewrite-embed.zip`
3. materialize or formally account for the missing `calcite` generated-output source path
4. rerun the same human-run near-duplicate and generated-output exclusion checks against that closed retained corpus line

## Gate Outcome

The overall formal gate remains closed.

Therefore:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

v6 improves the contamination evidence package by replacing missing-process blockers with executed human-run check artifacts.

However, those checks remain blocked at the corpus-text-availability layer, so the benchmark is still not gate-ready and formal `R-Bot @120` generation must not start.
