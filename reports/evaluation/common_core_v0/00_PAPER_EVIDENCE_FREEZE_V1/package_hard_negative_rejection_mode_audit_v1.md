# Package Hard-Negative Rejection Mode Audit V1

This is a diagnostic audit over retained hard-negative closure artifacts only. No DB, checker, timing, generation, verifier, or EXPLAIN run was performed in this step.

核心结论很直接：`111/111` 的测试通过并不是“多数负例自己跑挂了”，而是 `111/111` 都属于 **negative SQL 可执行、checker 运行成功、结果不匹配，因此被语义性拒绝**。未覆盖的 9 行是 `PORT` 的 source-reference-engine `not_applicable` 单元，不是测试失败。

| group_type | group_name | planned_negative_rows | applicable_or_runnable_rows | tested_negative_rows | rejected_negative_rows | negative_execution_failed_rejected | mismatch_rejected | checker_failed | source_execution_failed | unsupported_or_not_applicable | false_accept | blocked_rows | negative_rejection_rate | false_accept_rate | executable_mismatch_negative_rate | conditional_mismatch_rate_among_executable_negatives | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | overall | 120 | 111 | 111 | 111 | 0 | 111 | 0 | 0 | 9 | 0 | 9 | 111/111 = 1.0000 | 0/111 = 0.0000 | 111/111 = 1.0000 | 111/111 = 1.0000 | All tested rows were executable semantic negatives rejected as mismatches; the only uncovered rows are explicit not_applicable portability source-reference-engine cells. |
| pool | PERF | 48 | 48 | 48 | 48 | 0 | 48 | 0 | 0 | 0 | 0 | 0 | 48/48 = 1.0000 | 0/48 = 0.0000 | 48/48 = 1.0000 | 48/48 = 1.0000 | Cleanest pool-level semantic negative packet with no blocked rows. |
| pool | CONS | 27 | 27 | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 | 27/27 = 1.0000 | 0/27 = 0.0000 | 27/27 = 1.0000 | 27/27 = 1.0000 | All retained consistency negatives execute and reject semantically. |
| pool | PORT | 27 | 18 | 18 | 18 | 0 | 18 | 0 | 0 | 9 | 0 | 9 | 18/18 = 1.0000 | 0/18 = 0.0000 | 18/18 = 1.0000 | 18/18 = 1.0000 | Semantic negative value is still strong on tested rows but nine source-reference-engine cells remain explicitly not applicable rather than tested. |
| pool | LONGTAIL | 18 | 18 | 18 | 18 | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 18/18 = 1.0000 | 0/18 = 0.0000 | 18/18 = 1.0000 | 18/18 = 1.0000 | All tested longtail negatives reject as executable mismatches. |
| engine | pg | 40 | 36 | 36 | 36 | 0 | 36 | 0 | 0 | 4 | 0 | 4 | 36/36 = 1.0000 | 0/36 = 0.0000 | 36/36 = 1.0000 | 36/36 = 1.0000 | No PostgreSQL execution-failure negatives; blocked cells are portability reference-engine not-applicable rows. |
| engine | mysql | 40 | 35 | 35 | 35 | 0 | 35 | 0 | 0 | 5 | 0 | 5 | 35/35 = 1.0000 | 0/35 = 0.0000 | 35/35 = 1.0000 | 35/35 = 1.0000 | No MySQL execution-failure negatives; this engine carries the largest blocked not-applicable slice. |
| engine | spark | 40 | 40 | 40 | 40 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 40/40 = 1.0000 | 0/40 = 0.0000 | 40/40 = 1.0000 | 40/40 = 1.0000 | Spark provides the cleanest full-engine demonstration because every planned row is runnable and every tested row rejects semantically. |

解读边界：

- 这份审计支持“package hard negatives 在可测范围内具有强语义区分能力”。
- 这份审计**不**支持“method-generated candidates 的 false accept 已经审完”。
- 这份审计**不**支持“所有计划中的 portability 负例都在每个 source-reference-engine 上可测”。
