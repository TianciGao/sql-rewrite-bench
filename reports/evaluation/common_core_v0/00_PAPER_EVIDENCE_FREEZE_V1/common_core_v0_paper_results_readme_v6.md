# Common-core v0 Paper Results README v6

这是一次 **selected-case plan observability packet** 刷新。

## What Changed

- 新增了机械选择的 5 个 representative rows。
- 对这些 selected rows 保留了 source/rewrite plan artifact。
- Table 5 现在能明确展示 selected-case plan coverage。
- Table 10 v3 现在不再只有 failure 身份信息，而是补上了 speedup / regression / tie / failure 的 bounded plan evidence。

## What This Supports

- selected-case observability evidence
- bounded plan-delta classes
- 比单纯 latency label 更可解释的 outcome narrative

## What This Does Not Support

- full-denominator PlanParseRate
- full NodeAlignmentCoverage
- full AttributionCoverage
- global causal attribution
- final ranked leaderboard
- SpeedupTransferRate

## Reading Order

1. `selected_plan_observability_manifest_v1.csv`
2. `table5_observability_plan_artifact_v2.csv`
3. `table10_plan_observability_case_study_v3.csv`
4. `selected_plan_delta_classification_v1.csv`
5. `plan_observability_case_study_gap_matrix_v3.csv`
6. `paper_remaining_experiment_gaps_v6.csv`

## Core Boundary

这套 packet 的价值在于：对代表性的 speedup / regression / tie / failure 行，paper 现在能保留 source/rewrite plan artifact 和保守的 delta class。
它**不是**一个 full plan-alignment benchmark，也不支持 full-denominator observability claim。
