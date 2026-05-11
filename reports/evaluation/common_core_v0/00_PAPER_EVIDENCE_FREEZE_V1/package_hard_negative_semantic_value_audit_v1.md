# Package Hard-Negative Semantic Value Audit V1

This is a paper-facing diagnostic summary built from retained hard-negative closure artifacts only. No new execution or checking happened here.

中文解释：这张表回答的不是“负例有没有被拒绝”这么粗的问题，而是“这些被拒绝的负例，到底是因为语义真的错了，还是只是自己跑挂了”。当前保留下来的证据非常明确：**111 个已测试负例全部是可执行的语义错例，并且全部被 checker 判成结果不等价**。

| metric | value | denominator | interpretation | paper_value | risk_if_low | recommended_action |
| --- | --- | --- | --- | --- | --- | --- |
| planned_negative_rows | 120 | 120 | Full Common-core v0 package hard-negative design space before applicability filtering. | Shows the intended closure scope. | Would make the package closure look too small if the denominator were narrow. | Keep as the headline denominator. |
| tested_negative_rows | 111 | 120 | Rows that were actually executed and checked. | Shows the tested semantic-negative frontier. | If low the paper would need stronger caveats about coverage. | Report tested rows alongside planned rows and blocked rows. |
| blocked_rows | 9 | 120 | Explicit source-reference-engine not_applicable cells concentrated in PORT. | Coverage caveat rather than semantic weakness. | If hidden readers may overread 111/111 as 120/120 closure. | Keep blocked not_applicable rows visible in the table notes. |
| rejected_negative_rows | 111 | 111 | All tested negatives were rejected. | Strong package-level rejection result. | If lower the package-level closure would look noisy. | Retain as the main rejection headline. |
| false_accept_rows | 0 | 111 | No tested negative rewrite was accepted as equivalent. | Strongest safety signal in the retained packet. | Any nonzero value would materially weaken the guardrail story. | Keep false_accept as an explicit column. |
| negative_execution_failed_rejected_rows | 0 | 111 | No tested rejection came from the negative query failing to execute. | Shows rejection is not being carried by crash-only negatives. | If high the semantic value of negatives would be weaker. | State explicitly that execution-failure negatives are absent in the retained tested frontier. |
| mismatch_rejected_rows | 111 | 111 | Every tested rejection is a semantic result mismatch under retained checker policy. | This is the strongest available substantive signal. | If low the table would mostly show infrastructural rather than semantic guardrail value. | Promote mismatch-based rejection to the main text. |
| checker_failed_rows | 0 | 111 | No checker failures occurred on the tested negative frontier. | Supports stability of the audit packet. | If nonzero the packet would need operational caveats. | Keep checker-failed count in appendix or notes. |
| executable_mismatch_negative_rate | 111/111 = 1.0000 | 111 | Share of tested negatives rejected as executable mismatches. | Strong main-paper semantic guardrail metric. | If low the hard-negative table would be weak evidence. | Use in the main text or Table 4A notes. |
| conditional_mismatch_rate_among_executable_negatives | 111/111 = 1.0000 | 111 | Among negatives that executed successfully every one mismatched the source result. | Best single summary of semantic negative value. | If low the negatives would mostly be syntactic or operational traps. | Prefer this rate when motivating package-level negative examples. |
| strongest_pool_by_executable_mismatch_negative_rate | PERF, CONS, PORT, LONGTAIL (tie at 1.0000 on tested rows) | tested rows by pool | All tested pools tie on semantic rejection rate; PERF or CONS are cleaner exemplars because they have no blocked rows. | Supports pool-robustness without overclaiming PORT completeness. | If one pool were much weaker the argument would become pool-specific. | Use PERF or CONS as the illustrative pool if one exemplar is needed. |
| weakest_pool_by_executable_mismatch_negative_rate | PERF, CONS, PORT, LONGTAIL (tie at 1.0000 on tested rows) | tested rows by pool | No tested pool is weaker on semantic rejection rate; PORT only differs by having nine blocked not_applicable rows. | Keeps the limitation on coverage separate from semantic value. | If PORT were conflated with failure the story would become misleading. | Describe PORT as coverage-limited rather than semantically weak. |
| strongest_engine_by_executable_mismatch_negative_rate | pg, mysql, spark (tie at 1.0000 on tested rows) | tested rows by engine | All tested engines tie on semantic rejection rate; Spark is the cleanest full-engine exemplar because it has no blocked rows. | Supports cross-engine semantic value where tested. | If one engine were weak the story would narrow to engine-specific evidence. | Use Spark as the cleanest engine-level exemplar if space is tight. |
| weakest_engine_by_executable_mismatch_negative_rate | pg, mysql, spark (tie at 1.0000 on tested rows) | tested rows by engine | No engine is weaker on tested semantic rejection rate; MySQL only has the largest blocked not_applicable slice. | Separates coverage gaps from tested semantic quality. | If readers confuse blocked rows with failed negatives the table could be underread. | Call out MySQL blocked rows as applicability gaps rather than rejection failures. |

结论边界：

- 可以说：package-level hard negatives 在可测范围内展示了强语义区分能力。
- 不可以说：所有 planned negatives 在所有 engine 上都完成了同等强度的闭环。
- 也不可以把这份结果外推成 method-generated candidates 的 false accept 审计结果。
