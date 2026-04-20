# reviews

这个目录包含**项目级的 review 历史文档**。

## 作用
review 文件用于说明：

- 审查了什么
- 记录了什么判断
- 由此带来了什么元数据层面的后果

它们不是实时事实表。

## 实时状态来源
如需查看当前状态，请使用：

- `inventory/case_registry.csv`
- `docs/EXECUTION_STATUS.md`
- `benchmark_spec/decision_log.md`

## 当前文件
- `BATCH1_EXTERNAL_CASE_REVIEW_v1.md`  
  Batch-1 外部 case 的整合版 review。  
  它取代了：
  - `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`
  - `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`

## 命名规范
推荐使用如下命名模式：

- `BATCH<N>_<SCOPE>_REVIEW_v<M>.md`

示例：

- `BATCH1_EXTERNAL_CASE_REVIEW_v1.md`
- `BATCH2_PROMOTION_REVIEW_v1.md`
- `BATCH2_ADMISSION_REVIEW_v1.md`

## 规则
不要通过静默覆盖旧 review 的方式来表示后续 review 状态。  
应创建一个新的 review 文件，或明确标注“已被后续版本取代（supersession）”。