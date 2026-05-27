# Package Hard-Negative Closure Summary v1

这是一次基于保留工件的综合，不包含新的方法生成或计时。

- 该汇总展示 runnable / tested / rejected / false_accept / blocked 的分布。
- package-level hard-negative rejection 与 method_candidate_rejection_accounting 是两个不同概念。

| denominator_id | expected_negative_rows | runnable_negative_rows | tested_negative_rows | rejected_negative_rows | false_accept_rows | blocked_rows | needs_human_review_rows | negative_rejection_rate | false_accept_rate | rejection_category_breakdown | support_level | source_artifacts | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| common_core_v0_40_same_engine_120 | 120 | 111 | 111 | 111 | 0 | 9 | 0 | 111/111 = 1.0000 | 0/111 = 0.0000 | {"mismatch_rejected": 111, "missing_artifact": 9} | strong | /home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/hard_negative_denominator_manifest.csv\|/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/hard_negative_event_long.csv | Package-level hard-negative closure only. This does not audit accepted generated candidates. |

