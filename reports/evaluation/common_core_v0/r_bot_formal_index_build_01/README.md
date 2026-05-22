# R-Bot Formal Index Build 01

This package contains human-run scripts and metadata templates for building or
inspecting the formal `R-Bot` Chroma index.

## Files

- [index_build_plan.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/index_build_plan.md)
- [run_manual_r_bot_formal_index_build.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_build.py)
- [run_manual_r_bot_formal_index_inspect.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/run_manual_r_bot_formal_index_inspect.py)
- [index_identifier_schema.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/index_identifier_schema.json)
- [expected_artifacts.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/expected_artifacts.md)

## Usage Model

Recommended order:

1. run the build helper with default dry-run mode
2. review the identifier/report outputs
3. verify the dry-run metadata is manifest-driven and that provider-family status is explicit
4. do not treat `--execute-build` as a real formal build path until embedding/index population is implemented
5. run the inspect helper only against a genuinely built retained index directory

## Important Constraints

- do not treat the visible `/tmp` scratch index as formal evidence
- do not copy large index files into the repo
- do not mark the formal gate open from this package alone
- do not treat an unimplemented `--execute-build` attempt as a completed formal index build
- formal `R-Bot @120` generation may not start until the remaining runtime lock
  and artifact-contract blockers are also closed
