# LLMR2_LOGICAL_PLAN_PROBE_PERF_0006_v1

## 0. Purpose And Boundary
This is a bounded logical-plan extraction probe only.

## 1. Inputs
- staged query CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- staged schema path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- db_id: `rewritebench_perf_0006`
- raw query has leading comments: `yes`
- comment-stripped query prepared: `yes`

## 2. Raw Query Probe
- command used: `java -cp rewriter_java.jar src/get_logical_plan.java`
- exit status: `1`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stdout_v1.txt`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stderr_v1.txt`
- explain text produced: `no`
- output appears parseable by create_nested_tree: `no`
- parser failure reason: `no_direct_child_at_root_plus_one`

## 3. Comment-stripped Query Probe
- attempted: `yes`
- command used: `java -cp rewriter_java.jar src/get_logical_plan.java`
- exit status: `1`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stdout_v1.txt`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stderr_v1.txt`
- explain text produced: `no`
- output appears parseable by create_nested_tree: `no`
- parser failure reason: `no_direct_child_at_root_plus_one`

## 4. Diagnosis
- primary diagnosis: `schema_mapping_still_incomplete`
- prior smoke generation_status: `method_execution_failed`
- generated SQL exists: `no`
- result CSV exists: `no`

## 5. Recommended Next Step
- `patch db_id/schema mapping and retry`

## 6. Non-Modification Note
No full LLM-R2 run occurred. No model/API call occurred. No DB, checker, or speedup step ran. No registry or case files were modified.
