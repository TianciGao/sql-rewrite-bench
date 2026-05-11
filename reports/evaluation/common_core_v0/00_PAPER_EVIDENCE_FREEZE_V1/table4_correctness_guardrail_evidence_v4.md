# Table 4 v4: Correctness Guardrail Evidence Index

这是一次 **Table 4 展示重构**，只重组保留证据，不运行任何新实验。

- Table 4 v4 不再把 package negatives、method non-exact frontier、accepted-candidate false-accept audit 混在一个矩阵里。
- 它是一个 index-style 导航表，把读者引到 4A / 4B / 4C。

| panel_id | panel_title | question_answered | main_metric | scope | source_file | key_boundary | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Table 4A | Package hard-negative closure | Do case-package known-negative rewrites get rejected? | NegativeRejectionRate / FalseAcceptRate on package negatives | Common-core v0 package-level negatives | table4a_package_hard_negative_closure_v1.csv | Only package-provided known-negative rewrites. Not generated-method candidates. | Use this panel when discussing the value of case-package negative examples. |
| Table 4B | Method candidate rejection accounting | Are non-exact generated candidates kept visible and rejected rather than silently accepted? | candidate_rejection_accounting on the non-exact frontier | Method / route rows | table4b_method_candidate_rejection_accounting_v1.csv | Not a hard-negative rejection table. No method-level negative_rejection column here. | Use this panel when discussing full-denominator non-exact frontier accounting. |
| Table 4C | Accepted-candidate false-accept audit status | What still must be run before any method false_accept rate can be claimed? | audit_status | Accepted generated candidates only | table4c_accepted_candidate_false_accept_audit_status_v1.csv | Status table only; no numeric method false_accept rate is claimed. | Use this panel when stating what remains open before final method false_accept claims. |
