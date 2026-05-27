## Formal Rule Catalog Reconciliation Report

Date: 2026-05-08

### Outcome

This package freezes a canonical 100-slot R-Bot rule-vector catalog:

- NL slots `0-29`
- Calcite slots `30-99`

Counts:

- NL rules: `30`
- Calcite rules: `70`
- total rule-vector width: `100`
- unresolved slots: `0`

### What Changed Relative To The Prior Reconciliation

The prior read-only reconciliation packet concluded that two Calcite names were not recovered from visible Java rule maps:

- `AGGREGATE_EXPAND_DISTINCT_AGGREGATES_TO_JOIN`
- `JOIN_PROJECT_RIGHT_TRANSPOSE_INCLUDE_OUTER`

That conclusion was caused by the earlier parser path, not by the underlying source.

Direct source audit of [MyRules.java](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/rewriter/MyRules.java:100>) shows both names are present under `EXPLORE_RULES`:

- `AGGREGATE_EXPAND_DISTINCT_AGGREGATES_TO_JOIN` at lines `103-104`
- `JOIN_PROJECT_RIGHT_TRANSPOSE_INCLUDE_OUTER` at lines `123-124`

Therefore the earlier "two missing Java names" finding is corrected here as a parser-artifact diagnosis, not a catalog-evidence gap.

### NL Freeze

The 30 NL slots are frozen from [gen_rewrites_from_rules.py](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/gen_rewrites_from_rules.py:38>), which defines `RULE_FUNCTIONS` in fixed order.

The runtime-root knowledge base also exposes corresponding files `rule_cluster_funcs/0.py` through `29.py`, which serve as secondary retained lineage hints for the slot numbering.

### Calcite Freeze

The 70 Calcite names are now frozen with:

- primary slot-order basis:
  - [calcite_rules_selected_simple.jsonl](</tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/calcite_rules_selected_simple.jsonl:1>)
- cross-check basis:
  - [calcite_rewrite_rules_structured.jsonl](</tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/explain_rule/calcite_rewrite_rules_structured.jsonl:1>)
  - [MyRules.java](</tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/rewriter/MyRules.java:60>)

Reason for choosing `calcite_rules_selected_simple.jsonl` line order as canonical:

- it is a concise 70-row retained catalog
- its name set matches `calcite_rewrite_rules_structured.jsonl` exactly
- every one of its 70 names is directly recoverable from visible `MyRules.java`
- the line order is compact and deterministic for formal slot assignment

This freeze does **not** claim that the retained selected-simple order is provably the exact hidden historical build order of the original upstream index. Instead, it formally defines the benchmark-side canonical slot order now, using the strongest visible retained evidence.

### Two Previously Flagged Calcite Names

#### `AGGREGATE_EXPAND_DISTINCT_AGGREGATES_TO_JOIN`

- present in `calcite_rewrite_rules_structured.jsonl`: yes, line `28`
- present in `calcite_rules_selected_simple.jsonl`: yes, line `4`
- present in visible Java maps: yes, `EXPLORE_RULES`, lines `103-104`
- alias of a Java rule name: no
- status: `recovered_from_java`

#### `JOIN_PROJECT_RIGHT_TRANSPOSE_INCLUDE_OUTER`

- present in `calcite_rewrite_rules_structured.jsonl`: yes, line `68`
- present in `calcite_rules_selected_simple.jsonl`: yes, line `36`
- present in visible Java maps: yes, `EXPLORE_RULES`, lines `123-124`
- alias of a Java rule name: no
- status: `recovered_from_java`

### Canonical Catalog Decision

The canonical 100-slot catalog is now frozen as:

1. NL slots `0-29`:
   - exact `RULE_FUNCTIONS` order from `gen_rewrites_from_rules.py`
2. Calcite slots `30-99`:
   - exact line order from `calcite_rules_selected_simple.jsonl`

### What This Freeze Does Not Do

- it does not patch `run_manual_r_bot_formal_index_build.py`
- it does not rebuild the formal Chroma index
- it does not open the formal `@120` generation gate

### Recommended Next Patch

Patch the formal build helper to consume:

- `formal_nl_rule_catalog_v1.csv`
- `formal_calcite_rule_catalog_v1.csv`
- `formal_rule_vector_catalog_v1.json`

instead of re-deriving a narrower catalog from the current parser path.
