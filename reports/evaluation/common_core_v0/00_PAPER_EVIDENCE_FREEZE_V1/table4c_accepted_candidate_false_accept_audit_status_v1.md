# Table 4C: Accepted-Candidate False-Accept Audit Status

这是一次 **Table 4 展示重构**，只重组保留证据，不运行任何新实验。

- 该子表只回答：如果论文想报告 method false_accept rate，还需要做什么。
- 这不是 hard-negative closure，也不是现有 candidate rejection accounting 的重复。
- 对 main methods，这一步应视为 must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods。

| method_or_route | accepted_rows_to_audit | audit_status | required_next_experiment | priority | notes |
| --- | --- | --- | --- | --- | --- |
| Direct LLM | 94 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Run an independent accepted-candidate false-accept audit with an external oracle on the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| Direct LLM + Execute-and-Repair-1 | 96 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Run an independent accepted-candidate false-accept audit with an external oracle on the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| SQLGlot no-op / same-dialect | 72 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Run an independent accepted-candidate false-accept audit with an external oracle on the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| SQLGlot optimize | 63 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Run an independent accepted-candidate false-accept audit with an external oracle on the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| Calcite HEP | 93 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Run an independent accepted-candidate false-accept audit with an external oracle on the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| LLM-R2 original | 3 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Freeze a bounded accepted-candidate oracle audit for the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| LLM-R2 recovered | 6 | must_do_before_final_claim_if_false_accept_rate_is_reported_for_methods | Freeze a bounded accepted-candidate oracle audit for the retained accepted rows. | high | This table is status-only. It does not claim any method false_accept rate yet. |
| R-Bot summary-only | NA_not_split | summary_only_not_auditable_yet | Recover a denominator-aligned accepted-row frontier before any method false_accept rate is reported. | medium | This table is status-only. It does not claim any method false_accept rate yet. |
| LearnedRewrite summary-only | 10 | summary_only_not_auditable_yet | Recover a denominator-aligned accepted-row frontier before any method false_accept rate is reported. | medium | This table is status-only. It does not claim any method false_accept rate yet. |
