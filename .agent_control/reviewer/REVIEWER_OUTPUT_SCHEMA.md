# REVIEWER_OUTPUT_SCHEMA.md
## API Reviewer 输出格式契约 v0.1

本文件规定 API Reviewer 每轮审阅 Codex 输出后，必须返回的固定结构。

Reviewer 不是自由讨论助手。Reviewer 的任务是：
1. 判断 Codex 是否越界
2. 判断本轮产物是否可接受
3. 判断是否需要状态回写
4. 给出唯一下一步动作
5. 在允许时生成下一轮 Codex task

Reviewer 必须严格按照本 schema 输出，不要输出散文式长篇评论。

---

## 1. 输出总格式

Reviewer 每次必须输出一个 YAML block，格式如下：

```yaml
schema_version: reviewer_output_v0.1

status: PASS | NEEDS_FIX | STOP
acceptance: accepted | revise_and_retry | rejected

scope_class:
  value: read_only_audit | engineering_tooling | source_selection | seed_selection | case_construction | pg_witness_closure | pg_plan_collection | taxonomy_backfill | mysql_closure | spark_closure | tri_engine_review | registry_writeback | documentation_update | unknown
  confidence: high | medium | low

summary:
  one_line: ""
  checkpoint: ""

boundary_check:
  stayed_within_scope: true | false
  forbidden_protocol_change: true | false
  forbidden_taxonomy_change: true | false
  forbidden_registry_change: true | false
  forbidden_review_change: true | false
  forbidden_new_workload: true | false
  forbidden_new_case: true | false
  notes: ""

files:
  changed_files: []
  allowed_files_changed: []
  suspicious_or_forbidden_files_changed: []
  generated_artifacts: []

commands:
  reported_commands: []
  tests_or_checks_run: []
  missing_required_checks: []

source_of_truth_check:
  read_required_context: true | false
  respected_doc_map: true | false
  respected_case_registry_boundary: true | false
  respected_source_registry_boundary: true | false
  notes: ""

result_check:
  task_completed: true | false
  evidence_sufficient: true | false
  machine_readable_artifacts_present: true | false
  issues: []

state_writeback_judgment:
  live_source_facts_changed: true | false
  live_case_facts_changed: true | false
  source_registry_update_needed: true | false
  case_registry_update_needed: true | false
  execution_status_update_needed: true | false
  review_history_update_needed: true | false
  decision_log_update_needed: true | false
  exact_fields_or_sections_to_update: []
  rationale: ""

pipeline_position:
  current_stage: ""
  completed_stage: ""
  recommended_next_stage: ""
  allowed_to_continue_automatically: true | false
  requires_human_gate: true | false

next_action:
  type: stop_for_human | rerun_codex_fix | run_next_codex_task | update_task_queue | no_action
  title: ""
  rationale: ""

next_codex_task:
  allowed: true | false
  prompt: |
    ""
  stop_conditions: []

human_check_required:
  required: true | false
  questions: []

final_verdict: ""

