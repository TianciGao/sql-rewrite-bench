# Table 4A: Package Hard-Negative Closure

这是一次 **Table 4 展示重构**，只重组保留证据，不运行任何新实验。

- 该子表只回答 case package 已知负例是否被拒绝。
- 这里的 NegativeRejectionRate / FalseAcceptRate 只针对 package-provided hard negatives。
- 这不等于 generated method candidate 的 rejection accounting。
- 没有运行新的 DB/checker/timing/generation/verifier/EXPLAIN。

| panel_scope | scope_id | expected_rows | runnable_rows | tested_rows | rejected_rows | false_accept_rows | blocked_rows | NegativeRejectionRate | FalseAcceptRate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | common_core_v0_package_hard_negative | 120 | 111 | 111 | 111 | 0 | 9 | 111/111 = 1.0000 | 0/111 = 0.0000 | All 111 runnable hard-negative rows were rejected; 9 rows remain explicit as not_applicable portability reference cells. |
| by_pool | performance | 48 | 48 | 48 | 48 | 0 | 0 | 48/48 = 1.0000 | 0/48 = 0.0000 | Pool split derived directly from package_hard_negative_closure_event_long_v1. |
| by_pool | consistency | 27 | 27 | 27 | 27 | 0 | 0 | 27/27 = 1.0000 | 0/27 = 0.0000 | Pool split derived directly from package_hard_negative_closure_event_long_v1. |
| by_pool | portability | 27 | 18 | 18 | 18 | 0 | 9 | 18/18 = 1.0000 | 0/18 = 0.0000 | Pool split derived directly from package_hard_negative_closure_event_long_v1. |
| by_pool | longtail | 18 | 18 | 18 | 18 | 0 | 0 | 18/18 = 1.0000 | 0/18 = 0.0000 | Pool split derived directly from package_hard_negative_closure_event_long_v1. |
| by_engine | pg | 40 | 36 | 36 | 36 | 0 | 4 | 36/36 = 1.0000 | 0/36 = 0.0000 | Engine split derived directly from package_hard_negative_closure_event_long_v1. One-third of blocked rows sit on the portability source-reference engine for this engine family. |
| by_engine | mysql | 40 | 35 | 35 | 35 | 0 | 5 | 35/35 = 1.0000 | 0/35 = 0.0000 | Engine split derived directly from package_hard_negative_closure_event_long_v1. One-third of blocked rows sit on the portability source-reference engine for this engine family. |
| by_engine | spark | 40 | 40 | 40 | 40 | 0 | 0 | 40/40 = 1.0000 | 0/40 = 0.0000 | Engine split derived directly from package_hard_negative_closure_event_long_v1. |
