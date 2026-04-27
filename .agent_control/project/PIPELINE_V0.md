# PIPELINE_V0.md
## SQL Rewrite Benchmark 自动化推进流水线 v0.1

本文件定义无人值守 / 半自动模式下允许的推进顺序。

本 pipeline 不替代项目计划、benchmark spec、case registry、source registry 或 taxonomy yaml。  
它只回答：

> 当前任务完成后，下一步最多可以做什么？

---

## 0. 总原则

本项目采用：

> pool → source → seed → case package → PG closure → taxonomy draft → human review → MySQL/Spark closure → registry writeback

的受控流水线。

自动化系统只能在本文件允许的 transition 内移动。  
任何 admission、promotion、common-core / extended 判断都必须停下来等人类确认。

---

## 1. 四个 pool 的长期角色

### performance pool
目标：稳定、经典、可复现的性能 rewrite 基线。  
优先来源：TPC-H、TPC-DS。

### longtail pool
目标：补经典 benchmark 覆盖不到的长尾 SQL 结构。  
优先来源：SQLStorm、Stack queries、人工复杂 SQL seeds。

### consistency pool
目标：把 correctness / equivalence 作为一等任务。  
优先来源：Calcite seeds、VeriEQL / SQLEquiQuest 受控子集、人工 positive / negative pairs。

### portability pool
目标：验证 Spark / PostgreSQL / MySQL 跨方言可执行性、一致性和收益迁移。  
优先来源：PARROT、人工三方言 triplets、受限 SQLGlot 候选。

---

## 2. Source-level pipeline

### S0_SOURCE_BACKLOG
source 只在计划或候选清单中，还没有进入当前工作批。

允许下一步：
- S1_SOURCE_SELECTION

禁止：
- 直接生成 case
- 直接下载大规模 workload
- 直接修改 source_registry

---

### S1_SOURCE_SELECTION
选择某个 pool 下的一小批 source，说明为什么它们值得进入 staging。

输入：
- PROJECT_PLAN
- source_registry
- coverage / gap rationale
- 当前 active phase

输出：
- source selection note
- 不直接修改正式 source_registry，除非任务明确授权

允许下一步：
- S2_SOURCE_STAGING

人类 gate：
- 是否接受这批 source

---

### S2_SOURCE_STAGING
对已批准 source 做受控获取、路径整理、许可/provenance 记录和最小 inspection。

输出：
- raw/staged source files
- provenance notes
- source inspection report

允许下一步：
- S3_SEED_EXTRACTION

禁止：
- 批量生成 case package
- 批量写 registry 状态，除非明确授权

---

### S3_SEED_EXTRACTION
从 source 中抽取候选 SQL seed。

输出：
- candidate seed list
- seed metadata
- parse / dedupe / initial feature hints

允许下一步：
- S4_SEED_REVIEW

---

### S4_SEED_REVIEW
对 candidate seed 做人工或 reviewer-assisted 审查。

输出：
- accepted seeds
- rejected seeds
- rationale

允许下一步：
- C1_CASE_SKELETON

人类 gate：
- 哪些 seed 进入 case package 构造

---

## 3. Case-level pipeline

### C1_CASE_SKELETON
为单个 accepted seed 建 case package skeleton。

最小内容：
- manifest.yaml
- source.sql
- provenance notes
- engine metadata placeholder
- expected files layout

允许下一步：
- C2_POS_NEG_CONSTRUCTION

禁止：
- 标记 admitted
- 标记 common-core
- 修改 registry，除非明确授权

---

### C2_POS_NEG_CONSTRUCTION
为 case 构造 positive rewrite 与 hard negative。

最小内容：
- rewrite_pos_01.sql
- rewrite_neg_01.sql
- notes explaining intended equivalence / non-equivalence

允许下一步：
- C3_PG_WITNESS_VALIDATION

人类 gate：
- 正例/反例是否语义上值得尝试

---

### C3_PG_WITNESS_VALIDATION
先在 PostgreSQL 上跑 witness validation。

输出：
- runs/pg/result_check.json
- source result artifact
- positive result artifact
- negative result artifact
- reproducible command log

允许下一步：
- C4_PG_PLAN_COLLECTION

失败时：
- 回到 C2_POS_NEG_CONSTRUCTION 或 STOP

---

### C4_PG_PLAN_COLLECTION
收集 PostgreSQL source / positive / negative plans。

输出：
- runs/pg/plans/source.json
- runs/pg/plans/rewrite_pos_01.json
- runs/pg/plans/rewrite_neg_01.json
- runs/pg/plans/plan_check.json

允许下一步：
- C5_TAXONOMY_DRAFT_BACKFILL

---

### C5_TAXONOMY_DRAFT_BACKFILL
基于 case package 和 PG artifacts 做 taxonomy 初版回填。

可正式草拟：
- sql_feature.primary / secondary
- rewrite_opportunity.primary / secondary
- plan_operator.present / delta_relevant based on PG plans
- workload_realism.source_inherited / case_specific
- portability.suspected

暂不自动确认：
- portability.confirmed
- tri-engine plan conclusions
- admission status
- common-core / extended line

允许下一步：
- C6_TAXONOMY_HUMAN_REVIEW

---

### C6_TAXONOMY_HUMAN_REVIEW
人工或 ChatGPT-assisted 审阅 taxonomy draft。

输出：
- accepted taxonomy tags
- ambiguous points
- whether this case may proceed to MySQL/Spark closure

允许下一步：
- C7_MYSQL_CLOSURE
- C8_SPARK_CLOSURE

人类 gate：
- taxonomy tags 是否接受
- 是否允许进入 MySQL/Spark closure

---

### C7_MYSQL_CLOSURE
在 MySQL 上做 result validation 和必要 plan artifact。

输出：
- runs/mysql/result_check.json
- runs/mysql/plans/* if supported
- MySQL-specific failure notes

允许下一步：
- C9_TRI_ENGINE_REVIEW

失败时：
- STOP 或标记需要人工处理

---

### C8_SPARK_CLOSURE
在 Spark 上做 result validation 和必要 plan artifact。

输出：
- runs/spark/result_check.json
- runs/spark/plans/* if supported
- Spark-specific failure notes

允许下一步：
- C9_TRI_ENGINE_REVIEW

失败时：
- STOP 或标记需要人工处理

---

### C9_TRI_ENGINE_REVIEW
综合 PG / MySQL / Spark 结果，判断 case 当前 closure 状态。

输出：
- closure summary
- portability.confirmed candidates
- remaining gaps
- whether case is only PG-draft, two-engine draft, or tri-engine closed

允许下一步：
- C10_CASE_REGISTRY_WRITEBACK_DRAFT

人类 gate：
- 是否允许写回 registry
- 是否触发 batch review

---

### C10_CASE_REGISTRY_WRITEBACK_DRAFT
仅在人工授权后，准备最小 case_registry 写回。

输出：
- proposed exact CSV row change
- rationale
- source artifacts supporting the change

允许下一步：
- C11_FINAL_REVIEW

禁止：
- 自主 admission / promotion
- 自主 common-core / extended 判断

---

### C11_FINAL_REVIEW
最终人工审阅。

输出：
- accepted / revise / rejected
- next gap
- whether to commit

---

## 4. 推荐默认顺序

对于新 case，默认顺序是：

```text
C1 skeleton
→ C2 positive/negative
→ C3 PG witness validation
→ C4 PG plan collection
→ C5 taxonomy draft
→ C6 human taxonomy review
→ C7 MySQL closure
→ C8 Spark closure
→ C9 tri-engine review
→ C10 registry writeback draft
→ C11 final review