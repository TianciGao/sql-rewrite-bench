## R-Bot Formal Rule-Vector Catalog Reconciliation

Date: 2026-05-08

### Scope

This packet reconciles the frozen formal contract `rule_vector_width = 100` with the current formal build failure:

`Rule catalog width mismatch: NL=30, NORMAL=37, TOTAL=67`

This is a read-only reconciliation. It does not change build behavior, does not rebuild the index, and does not close the formal index blocker.

### Findings

#### 1. Where the current 30 NL rules are parsed from

The current formal build helper parses NL rules from visible upstream `LLM4Rewrite/rag/gen_rewrites_from_rules.py`.

- `RULE_FUNCTIONS = [...]` contains 30 Python rule functions.
- `NL_RULES = [r.__name__ for r in RULE_FUNCTIONS]`.
- The visible upstream runtime also contains 30 corresponding files under `knowledge-base/rule_cluster_funcs/0.py` through `29.py`.

Conclusion: the current `NL = 30` parse is well-explained and stable.

#### 2. Where the current 37 NORMAL rules are parsed from

The current formal build helper parses Calcite-normal rules from visible upstream `LLM4Rewrite/CalciteRewrite/src/rewriter/MyRules.java`.

- `NORMAL_RULES = Map.ofEntries(...)` contains 37 entries.
- `my_rewriter/rewrite.py` exposes these via `get_normal_rules()`.
- `rag/gen_rewrites_from_rules.py` imports those names into `NORMAL_RULES`.

Conclusion: the current `NORMAL = 37` parse is also well-explained, but it is not broad enough to satisfy the frozen `100`-slot formal contract.

#### 3. Additional visible upstream rule files and catalogs

Visible upstream artifacts contain more rule catalog material than the current `37`-wide Calcite parse:

- `MyRules.EXPLORE_RULES` contains 31 entries.
- `MyRules.SEMI_JOIN_RULES` contains 4 entries, but they do not add new names beyond the visible normal/explore union.
- In the visible PG1/runtime-root recovery artifacts:
  - `explain_rule/calcite_rewrite_rules_structured.jsonl` contains 70 rows.
  - `my_rewriter/calcite_rules_selected_simple.jsonl` contains 70 rows.

The 70-row structured Calcite catalog is the strongest retained clue for the frozen formal `100`-slot rule contract.

#### 4. What the 70-row Calcite structured catalog implies

Comparing the visible catalogs:

- `NORMAL_RULES`: 37
- `EXPLORE_RULES`: 31
- `NORMAL + EXPLORE`: 68 unique names
- `calcite_rewrite_rules_structured.jsonl`: 70 names

The 70-row structured catalog contains two names that are not present in the currently visible `MyRules.NORMAL_RULES + MyRules.EXPLORE_RULES` parse:

- `AGGREGATE_EXPAND_DISTINCT_AGGREGATES_TO_JOIN`
- `JOIN_PROJECT_RIGHT_TRANSPOSE_INCLUDE_OUTER`

Therefore the current failure is not just "37 normal rules vs expected 70 Calcite rules". It is:

- current build helper uses a 37-name Calcite catalog source
- prior retained recovery artifacts point to a 70-name Calcite catalog
- 2 of those 70 names are not recovered from the currently visible Java rule maps

#### 5. Whether the ZIP contains metadata implying 100 slots

No retained ZIP row metadata directly formalizes a `100`-slot rule vector.

Visible rule-row evidence from `stackoverflow-rewrite-rules-query-optimization.jsonl` shows:

- 2428 rows in the rule file copy inspected in runtime-root
- 29 distinct NL labels observed in row data
- 23 distinct Calcite labels observed in row data
- 52 distinct total observed labels

Important distinction:

- per-row observed labels are not the same thing as the full rule catalog
- the ZIP rows do not expose slot indices
- the ZIP rows do not expose a rule-vector width field
- the ZIP rows do not expose a canonical 100-slot ordering

Conclusion: the ZIP alone does not justify silent padding to 100, and it does not by itself identify all 100 slots.

#### 6. Whether old PG1 recovery artifacts reveal selected rule indices or rule-vector width

The visible PG1 recovery artifacts do not reveal a canonical 100-slot index map, but they do reveal the expected width and a temporary alignment strategy.

Evidence:

- `docs/_scratch/RBOT_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v3.md` records:
  - expected rule-vector dimension `100`
  - temporary runtime alignment by padding a live rule vector with trailing zeroes to width `100`
- `docs/_scratch/RBOT_LLM4REWRITE_EMBEDDING_DIM_MISMATCH_AUDIT_v1.md` records:
  - Chroma collection dimension `3172`
  - runtime mismatch `3172` vs `3139`
- visible `selected_rules.json`, `selected_rules_v2.json`, and `selected_rules_v3.json` do not reveal a canonical slot index mapping

Conclusion: the recovery line proves that `100` was an operational expectation, but it does not freeze a formal slot-order contract by itself.

#### 7. Whether the original Chroma collection dimension 3172 proves a 100-slot rule vector

It proves the build-time vector width expectation, not the semantic identity of every slot.

`3172 = 1536 + 100 + 1536`

Therefore the prior collection strongly supports:

- two semantic embedding segments of width `1536`
- one intermediate rule vector of width `100`

But `3172` alone does not answer:

- whether all 100 slots correspond to named rule definitions
- whether some slots were reserved zeros
- what the canonical slot ordering was

#### 8. Best current interpretation of what "100" means

The best-supported reconstruction hypothesis is:

- `30` NL slots
- `70` Calcite slots
- total `100`

Why this is the strongest current hypothesis:

- the runtime/root recovery artifacts retain a 70-row Calcite structured catalog
- `30 + 70 = 100`
- the current `37`-wide parse is visibly incomplete against that retained 70-row Calcite evidence

However, this is still not fully formalized because:

- 2 of the 70 Calcite names are not recovered from the current visible Java rule maps
- the ZIP does not retain a canonical slot index/order artifact

### Decision Against A/B/C

Current read-only judgment:

- `A. 100 actual rule definitions`:
  - best-supported reconstruction hypothesis
  - not yet formally proven end-to-end from currently retained canonical artifacts
- `B. 67 actual rules + 33 reserved zero-fill slots`:
  - not supported by the strongest visible evidence
  - the best retained catalog evidence points to 70 Calcite names, not 37 plus 33 anonymous placeholders
  - scratch padding evidence exists, but that was a temporary runtime compatibility patch, not a formal corpus-build contract
- `C. unknown / cannot formalize yet`:
  - this remains the correct formal gate decision today

Therefore:

- working hypothesis: closest to `A`
- formal benchmark decision: still `C` until the 70-slot Calcite catalog and slot ordering are frozen in retained artifacts

### Root Cause Hypothesis

The current formal build failure is most likely caused by using the wrong Calcite catalog basis.

The current builder derives the rule vector from:

- 30 NL names from `RULE_FUNCTIONS`
- 37 Calcite names from `MyRules.NORMAL_RULES`

But the frozen formal `100`-slot contract is more consistent with:

- 30 NL names
- 70 retained Calcite catalog names from the structured recovery artifacts

That mismatch produces the current `67` total instead of the expected `100`.

### Recommended Next Patch

Do not change the formal dimension contract.

Instead:

1. Freeze a canonical retained 70-name Calcite catalog artifact and slot order.
2. Reconcile the two missing structured names against visible upstream source lineage.
3. Patch the formal build helper to derive the Calcite side from the retained 70-name formal catalog, not from `MyRules.NORMAL_RULES` alone.
4. Keep formal build and formal `@120` generation blocked until that catalog artifact is retained and validated.

### Gate Effect

- formal Chroma index blocker: still open
- current benchmark gate ready: `false`
- formal `@120` generation may start: `no`
