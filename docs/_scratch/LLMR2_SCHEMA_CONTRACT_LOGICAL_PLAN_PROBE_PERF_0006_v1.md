# LLMR2_SCHEMA_CONTRACT_LOGICAL_PLAN_PROBE_PERF_0006_v1

## 0. Purpose And Boundary
This is a schema-contract patch + logical-plan probe only.

## 1. Prior Failure
- schema list shape fixed
- logical-plan probe still failed
- Java stderr had NumberFormatException on "unknown" and defaultSchema null

## 2. Native Schema Contract
- native schema example inspected: `/tmp/rewritebench_llmr2_audit/LLM-R2/data/data_llmr2/schemas/tpch.json`, `/tmp/rewritebench_llmr2_audit/LLM-R2/data/data_llmr2/schemas/dsb.json`
- native shape: `list_of_table_dicts`
- table fields: `['columns', 'rows', 'table']`
- column fields: `['name', 'type']`
- rows/cardinality field type: `int`
- differences from prior staged schema: prior staged stub used non-native type strings and non-numeric `rows`

## 3. Patch Applied
- staged schema path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- backup path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.before_schema_native_contract_v1.json`
- rows/cardinality value chosen: `4`
- table count: `1`
- column count: `7`
- schema_native_contract=true
- only temp runtime root modified

## 4. Probe Result
- staged query CSV path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- staged schema path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- db_id: `rewritebench_perf_0006`
- raw query has leading comments: `yes`
- comment-stripped query prepared: `yes`

## 5. Raw Query Probe
- command used: `java -cp rewriter_java.jar src/get_logical_plan.java`
- exit status: `0`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stdout_schema_contract_v1.txt`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stderr_schema_contract_v1.txt`
- explain text produced: `yes`
- output appears parseable by create_nested_tree: `yes`
- parser failure reason: `none`

## 6. Comment-stripped Query Probe
- attempted: `no`
- command used: `java -cp rewriter_java.jar src/get_logical_plan.java`
- exit status: `None`
- stdout path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stdout_schema_contract_v1.txt`
- stderr path: `/tmp/rewritebench_llmr2_fast_path/PERF_0006/logical_plan_probe_stderr_schema_contract_v1.txt`
- explain text produced: `no`
- output appears parseable by create_nested_tree: `no`
- parser failure reason: `none`

## 7. Diagnosis
- primary diagnosis: `schema_contract_fixed_logical_plan_ready`
- prior smoke generation_status: `method_execution_failed`
- generated SQL exists: `no`
- result CSV exists: `no`

## 8. Recommended Next Step
- `retry CPU fast-path LLM-R2 smoke`

## 9. Non-Modification Note
No full LLM-R2 run occurred. No model/API call occurred. No DB, checker, or speedup step ran. No registry or case files were modified.
