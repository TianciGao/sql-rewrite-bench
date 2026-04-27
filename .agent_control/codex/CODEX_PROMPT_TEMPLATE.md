# CODEX_PROMPT_TEMPLATE.md
## 给 Codex 的可复用 Prompt 模板

本文件不是项目规则本身，而是**给人类/ChatGPT使用的任务Prompt模板库**。  
它的作用是：每次你要给 Codex 分配任务时，不要临时发挥，而是按固定结构发 prompt。

这样做的目的：

- 让 Codex 每次都先读对文件
- 让 Codex 每次都按同一套 source-of-truth 规则工作
- 让任务边界稳定，避免越界
- 让输出更可验收、更可复用

> 本文件是给**人类**看的，不是给 Codex 自动读取的项目规则文件。

---

## 0. 使用原则

每次给 Codex 发任务时，默认顺序是：

1. 先在 **WSL** 正确进入项目目录并准备环境
2. 启动 Codex
3. 先做一次**只读审计**
4. 再发正式任务
5. 优先让它先给计划，再决定是否允许它改文件
6. 做完后按 `git diff` / `git status` 验收

---

## 1. 启动前固定动作

在 WSL 中先执行：

```bash
cd ~/code/sql-rewrite-bench
source .venv/bin/activate
git status --short
```

如果本次任务会碰数据库 / Spark / Codex，再执行：

```bash
export PGPASSWORD='你的本地密码'
source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh
```

如果 `scripts/env_spark.sh` 临时不可用，可替代为：

```bash
export SPARK_LOCAL_IP="$(hostname -I | awk '{print $1}')"
export SPARK_DRIVER_MEMORY="8g"
```

然后再启动：

```bash
codex
```

---

## 2. 占位符说明

下面模板里会用到这些占位符。发送给 Codex 前，把它们替换掉：

- `[PHASE_BOUNDARY]`：这次任务的阶段边界
- `[CURRENT_STATUS]`：当前已确认事实
- `[TASK]`：这次任务本身
- `[OUTPUTS]`：这次任务要求的输出
- `[FILES_TO_READ]`：本次任务额外需要读的文件
- `[TARGET_FILE]`：本次要改的唯一或主要文件
- `[TARGET_COMMAND]`：本次要复跑验证的命令
- `[ONE_SPECIFIC_ISSUE]`：本次只修的那个问题

---

## 3. 当前仓库默认 source-of-truth 规则

除非本次任务有特殊说明，否则默认使用下面这套：

- source facts -> `inventory/source_registry.csv`
- case facts -> `inventory/case_registry.csv`
- current stage interpretation -> `docs/EXECUTION_STATUS.md`
- long-term direction -> `docs/PROJECT_PLAN.md`
- long-term rules -> `benchmark_spec/*rules*.md`
- review-history -> `benchmark_spec/reviews/*.md`

永远不要把这些层混起来：

- `PROJECT_PLAN.md` 不是状态表
- `EXECUTION_STATUS.md` 不是 live registry
- review 文件不是 live fact table
- registry 不是规则文件

---

## 4. 默认先读文件顺序

除非任务明确更窄，否则默认要求 Codex 先读：

1. `AGENTS.md`
2. `docs/DOC_MAP.md`
3. `docs/EXECUTION_STATUS.md`
4. `benchmark_spec/decision_log.md`

如果任务涉及 source，再额外读：

- `inventory/source_registry.csv`
- `docs/POOL_MAPPING_RULES.md`

如果任务涉及 case，再额外读：

- `inventory/case_registry.csv`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`

如果任务涉及 batch 审查结论，再额外读：

- `benchmark_spec/reviews/BATCH1_EXTERNAL_CASE_REVIEW_v1.md`

如果任务涉及长期方向 / spec，再额外读：

- `docs/PROJECT_PLAN.md`
- `benchmark_spec/benchmark_spec_v0.md`

---

## 5. 模板 A：进入项目后的第一次只读审计

这段用于确认：

- Codex 的 cwd 是否正确
- 环境变量是否可见
- 当前 shell 是否准备好

```text
Please do not modify any files yet.

First report only:
1. current working directory
2. whether PGHOST is visible (yes/no)
3. whether MYSQL_HOST is visible (yes/no)
4. whether SPARK_LOCAL_IP is visible (yes/no)

Then stop and wait.
```

### 通过标准

只有当它回答：

- cwd 正确
- PGHOST=yes
- MYSQL_HOST=yes
- SPARK_LOCAL_IP=yes

才进入下一步。

如果这里不对，先退出 Codex，回 shell 修环境，再重开。

---

## 6. 模板 B：仓库分层理解只读审计

这段用于确认：

- Codex 有没有读懂仓库结构
- 有没有把方向 / 事实 / 解释 / 规则 / review-history 分清

```text
Please do not modify any files yet.

Read these files in order:
1. AGENTS.md
2. docs/DOC_MAP.md
3. docs/EXECUTION_STATUS.md
4. benchmark_spec/decision_log.md

Then report only:
1. current repository stage
2. the live source-of-truth for source facts
3. the live source-of-truth for case facts
4. the file that explains current stage interpretation
5. the files that define long-term rules
6. the files that are review-history only
7. whether archetype completion is the same as admission (yes/no)
8. whether common-core / extended is the same as primary pool (yes/no)
9. what kinds of work are allowed right now
10. what kinds of work require stop-and-ask

Then stop and wait.
```

### 通过标准

至少应答对：

- current repository stage
- source facts / case facts / stage interpretation 分工
- `archetype completion != admission`
- `common-core / extended != primary pool`

---

## 7. 模板 C：标准工程任务模板（先读文件，再改）

这是最常用模板。适合：

- CLI scaffolding
- validator
- report generator
- preflight / registry-check / current-snapshot 工具
- 其他窄范围工程任务

```text
Stay strictly within [PHASE_BOUNDARY].

Before editing anything, read these files in order:
1. AGENTS.md
2. docs/DOC_MAP.md
3. docs/EXECUTION_STATUS.md
4. benchmark_spec/decision_log.md
[FILES_TO_READ]

Use the following source-of-truth rules:
- source facts -> inventory/source_registry.csv
- case facts -> inventory/case_registry.csv
- current stage interpretation -> docs/EXECUTION_STATUS.md
- long-term direction -> docs/PROJECT_PLAN.md
- long-term rules -> benchmark_spec/*rules*.md
- review-history -> benchmark_spec/reviews/*.md

Do not change protocol decisions.
Do not add benchmark workloads.
Do not generate new benchmark cases.
Do not start workload curation.
Do not modify docs/PROJECT_PLAN.md, docs/EXECUTION_STATUS.md, inventory/source_registry.csv, inventory/case_registry.csv, or benchmark_spec/*rules*.md unless I explicitly ask.

Current confirmed status:
[CURRENT_STATUS]

Task:
[TASK]

Requirements:
[OUTPUTS]

Before editing, tell me exactly:
1. which files you will modify
2. which files you will only read
3. which commands you plan to run
4. why this stays within scope

Then proceed.
```

---

## 8. 模板 D：只要计划，不许改文件

当你想先看 Codex 的思路，再决定要不要放行改文件时，用这段：

```text
Do not modify any files yet.

Read these files first:
1. AGENTS.md
2. docs/DOC_MAP.md
3. docs/EXECUTION_STATUS.md
4. benchmark_spec/decision_log.md
[FILES_TO_READ]

Task:
[TASK]

Requirements:
[OUTPUTS]

Before editing, report only:
1. which existing files/scripts you would reuse
2. which new files you would create
3. which commands you would run
4. what you must not touch

Do not edit files.
Stop after the plan.
```

---

## 9. 模板 E：窄范围修 bug / 修一处逻辑

当 Codex 已经做了一半，只允许修一个点时，用这段：

```text
Do not widen scope.

Read only:
- [FILE_A]
- [FILE_B]
- [FILE_C]

Task:
Fix only [ONE_SPECIFIC_ISSUE].

Requirements:
- change only the failing logic
- do not modify any other command behavior
- do not touch protocol/spec/taxonomy/case/inventory/docs/review files

Before editing, report only:
1. which exact check or logic is failing
2. which exact lines you would change
3. why this fix does not widen scope

Then proceed.
```

---

## 10. 模板 F：只做诊断，不许动代码

当你不确定错误是在环境、路径、数据还是代码时，用这段：

```text
Do not modify any files yet.

Read only:
- [FILE_A]
- [FILE_B]
- [FILE_C]

Task:
Diagnose only.

Report only:
1. the exact failure
2. the most likely cause
3. whether this is a code bug, environment issue, path issue, or data issue
4. what single next action you recommend

Do not edit files.
Do not run unrelated commands.
Stop after the diagnosis.
```

---

## 11. 模板 H：允许执行命令，但不允许越界改文件

当你允许它跑检查命令，但不允许顺手扩任务时，用这段：

```text
You may run only the minimum commands required for this task.

Do not widen scope.
Do not modify protocol/spec/taxonomy/case/inventory/docs/review files.
Do not add new workloads or benchmark cases.

Allowed commands:
- [COMMAND_1]
- [COMMAND_2]
- [COMMAND_3]

Before running them, tell me:
1. why each command is necessary
2. which file(s) it may affect
3. what output artifact it should produce

Then proceed.
```

---

## 12. 模板 I：收口提交前的人类验收请求

当 Codex 任务做完后，你想让它自己做一次收口检查，但不继续加任务时，用这段：

```text
Do not modify any files further.

Report only:
1. which files were modified
2. which commands were run
3. which outputs were generated
4. whether any protocol/spec/taxonomy/case/inventory/docs/review files were modified
5. whether the task is complete
6. what the exact next human verification step should be

Then stop and wait.
```

---

## 13. 模板 J：任务完成后的状态回写判断

当 Codex 完成一次任务后，如果该任务可能改变了 case/source 的实时事实、代表性状态快照或审查结论，不应直接结束。

先让 Codex 报告是否需要状态回写，再由人决定是否允许它修改状态文件。

```text
Do not modify any files further yet.

Based on the completed task, report only:
1. whether any live source facts changed (yes/no)
2. whether any live case facts changed (yes/no)
3. whether `inventory/source_registry.csv` needs an update (yes/no)
4. whether `inventory/case_registry.csv` needs an update (yes/no)
5. whether `docs/EXECUTION_STATUS.md` needs an update (yes/no)
6. whether any `benchmark_spec/reviews/*.md` file needs an update (yes/no)
7. which exact fields or sections would need to change
8. why those changes are or are not required under the repository’s source-of-truth rules

Do not edit files.
Stop after the report.
```

---

## 14. 附录 A：当前项目最常用的 `[CURRENT_STATUS]` 模板

你可以直接复用这段，按需删减：

```text
- Week 1 closeout completed
- tri-engine smoke passed
- PERF_0001 tri-engine consistency closure passed
- first plan artifacts collected
- minimal CLI scaffolding exists
- artifact-preflight passes
- registry-check exists
- current-snapshot exists
```

---

## 15. 附录 B：当前项目最常用的 `[PHASE_BOUNDARY]` 模板

### Week 1 closeout
```text
Week-1 bootstrap closeout and minimal CLI scaffolding
```

### Week 2 最小硬化
```text
Week-2 minimal hardening and reporting preparation
```

### 最强 case 深化
```text
Week-2 selective deepening of strongest admitted external cases only
```

---

## 16. 附录 C：当前项目最常用的禁止项块

你可以直接复用：

```text
Do not change protocol decisions.
Do not add benchmark workloads.
Do not generate new benchmark cases.
Do not start workload curation.
Do not modify docs/PROJECT_PLAN.md, docs/EXECUTION_STATUS.md, inventory/source_registry.csv, inventory/case_registry.csv, or benchmark_spec/*rules*.md unless I explicitly ask.
```

---

## 17. 附录 D：当前项目最常用的输出要求块

你可以直接复用：

```text
Requirements:
- output machine-readable JSON under reports/cli/
- keep implementation read-only with respect to source facts / case facts
- do not modify protocol/spec/taxonomy/case/inventory/docs/review files
- keep changes as small and local as possible
```

---

## 18. 什么时候必须要求它读 `docs/EXECUTION_STATUS.md`

答案是：几乎每次都要，只要任务和下面任一项有关：

- 当前阶段
- 当前 focus
- 当前允许做什么
- 当前不该做什么
- 当前 strongest cases 是谁
- 当前 blockers / risks 是什么

原因：

- `AGENTS.md` 负责稳定规则
- `EXECUTION_STATUS.md` 负责当前解释

不要只依赖 `AGENTS.md`。

---

## 19. 什么时候必须先停下来做人类判断

遇到这些情况，不要直接让 Codex干：

- benchmark 协议要变
- taxonomy 原则要变
- primary metrics 要变
- 要新增 benchmark case
- 要下载 / 纳入新 workload
- 要做 candidate / admitted 判断
- 要改 registry 的事实字段含义
- 要修改 rules / review-history 文件
- 要进入 workload curation / benchmark expansion

这类都应该先由人做判断，再决定是否让 Codex 执行工程部分。

---

## 20. 验收 Codex 的固定 4 项

每次任务结束后，只看这四件事：

### 1）有没有越界
有没有偷偷：

- 改 protocol
- 改 rules
- 加 workload
- 加 case
- 做 admission judgment

### 2）有没有读对 source-of-truth
比如：

- source facts → `source_registry.csv`
- case facts → `case_registry.csv`
- 当前阶段 → `EXECUTION_STATUS.md`
- review-history → `benchmark_spec/reviews/*.md`

### 3）有没有把东西程序化
它应该把手工工作收敛成：

- CLI
- validator
- preflight
- JSON report

### 4）有没有输出 machine-readable artifact
如果只是终端打印，没有 JSON / report / output 文件，就还不够好。

---

## 21. 如果 Codex 做偏了，立刻用这段

```text
Stop. This is outside the allowed scope.
Do not modify any more files.
Report only:
1. which files you changed
2. what commands you ran
3. whether any protocol or case-state files were modified
Then stop and wait.
```

然后回 shell 检查：

```bash
git status --short
git diff
```

---

## 22. 最后一条规则

每次给 Codex 发任务前，先问自己三件事：

1. 这次任务属于哪一层？
   - 方向
   - 事实
   - 解释
   - 规则
   - 审查历史

2. 这次任务是工程实现，还是科学判断？
   - 如果是科学判断，不要默认交给 Codex

3. 这次任务有没有现成 source-of-truth？
   - 如果有，就先让它读那个，不要让它自己猜