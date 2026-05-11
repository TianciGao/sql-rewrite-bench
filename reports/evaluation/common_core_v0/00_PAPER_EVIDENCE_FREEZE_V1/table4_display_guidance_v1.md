# Table 4 Display Guidance v1

这是一次 **展示层重构**，不新增实验。

## 为什么要拆成 4A / 4B / 4C

- `Table 4A` 只讲 **case-package known-negative rewrites**。
  这里可以安全报告 package-level `NegativeRejectionRate` 和 `FalseAcceptRate`。
- `Table 4B` 只讲 **generated method candidates** 的 `method_candidate_rejection_accounting`。
  这里不应再出现 `hard_negative_rejection` 列。
- `Table 4C` 只讲 **accepted generated candidates** 的 future false-accept audit 状态。
  这里是“还缺什么实验”，不是结果表。

## 论文写作建议

- 当论文想强调“case-package negatives 很重要”时，引用 `Table 4A`。
- 当论文想强调“方法没有把 non-exact frontier 藏起来”时，引用 `Table 4B`。
- 当论文想解释“为什么 method false_accept 还不能报数字”时，引用 `Table 4C`。

## 必须避免的误写

- 不要把 `candidate_rejection_accounting` 写成 `hard_negative_rejection`。
- 不要把 `Table 4A` 的 `FalseAcceptRate=0` 推广为方法 false accept 为 0。
- 不要把 `Table 4C` 当成已经完成的 method false-accept audit。
- 不要把这个展示重构写成新的实验结果。
