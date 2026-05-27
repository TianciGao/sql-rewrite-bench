# Common-core v0 Paper Results README v5

这是一次 **Table 4 presentation redesign only**。

## What Changed

- Table 4 不再用一个矩阵同时承载三种不同问题。
- 现在分成：
  1. `Table 4A` package hard-negative closure
  2. `Table 4B` method candidate rejection accounting
  3. `Table 4C` accepted-candidate false-accept audit status
- `Table 4 v4` 变成 compact index-style 导航表。

## What This Does Better

- 让 package-level negative evidence 更强、更直观
- 让 method rows 不再被大量 `NA` 的 hard-negative 列稀释
- 让 future false-accept audit 的缺口单独可见

## What This Does Not Change

- 不新增任何实验
- 不改变 package hard-negative closure 的数值
- 不改变 method_candidate_rejection_accounting 的数值
- 不把 method false_accept rate 从 `NA` 变成数字
- 不形成 final ranked leaderboard

## Reading Order

1. `table4_correctness_guardrail_evidence_v4.csv`
2. `table4a_package_hard_negative_closure_v1.csv`
3. `table4b_method_candidate_rejection_accounting_v1.csv`
4. `table4c_accepted_candidate_false_accept_audit_status_v1.csv`
5. `table4_display_guidance_v1.md`
6. `paper_claim_matrix_v5.csv`
7. `paper_remaining_experiment_gaps_v5.csv`

## Core Boundary

- `hard_negative_rejection` 只用于 case-provided known-negative rewrites
- `method_candidate_rejection_accounting` 只用于 generated method candidates
- `accepted_candidate_false_accept_audit` 仍然是未来实验，不应提前写成现有结果
