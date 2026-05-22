# Common-core v0 Paper Results README v4

这是一次 **package hard-negative closure + Table 4 refresh**。

## What This Package Is

- 一个基于保留 case package 工件的新 hard-negative closure packet
- 一个把 Table 4 从 aggregate-only hard-negative control，推进到 package-level hard-negative closure 的版本
- 一个明确区分 `hard_negative_rejection` 与 `method_candidate_rejection_accounting` 的 paper-facing refresh

## What It Is Not

- 不是 final ranked leaderboard
- 不是新的方法生成 run
- 不是新的 timing run
- 不是 accepted generated candidate false-accept audit

## Hard-negative Closure Highlights

- expected negative rows: `120`
- runnable negative rows: `111`
- tested negative rows: `111`
- rejected negative rows: `111`
- false accept rows: `0`
- blocked rows: `9`
- NegativeRejectionRate: `111/111 = 1.0000`
- FalseAcceptRate: `0/111 = 0.0000`

## Reading Order

1. `package_hard_negative_denominator_v1.csv`
2. `package_hard_negative_closure_event_long_v1.csv`
3. `package_hard_negative_closure_summary_v1.csv`
4. `package_hard_negative_false_accept_audit_v1.csv`
5. `table4_correctness_guardrail_evidence_v3.csv`
6. `table4_correctness_guardrail_gap_summary_v3.csv`
7. `paper_claim_matrix_v4.csv`
8. `paper_remaining_experiment_gaps_v4.csv`

## Claim Boundaries

- package-level hard-negative closure 不等于 method-generated hard-negative rejection
- method accepted-candidate false-accept audit 仍然没有完成
- 不声明 final ranked leaderboard
- 不声明 global winner
