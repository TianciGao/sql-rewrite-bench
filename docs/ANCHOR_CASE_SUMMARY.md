# Anchor Case Summary

## 1. Document Role

This document summarizes the current anchor cases used to stabilize the benchmark shape during the early pilot stage.

Its purpose is to provide a compact, human-readable overview of:

- which formal pool each anchor case primarily represents
- whether the case is currently treated as `common-core` or `extended`
- what benchmark question each anchor case is intended to answer
- whether tri-engine result closure has been completed
- whether tri-engine plan closure has been completed
- what taxonomy dimensions each case currently exercises
- what role each case plays in the benchmark story

This document is not the full benchmark specification.

For project-wide scope and roadmap, see `docs/PROJECT_PLAN.md`.  
For pool assignment rules, see `docs/POOL_MAPPING_RULES.md`.  
For common-core / extended rules, see `benchmark_spec/common_core_extended_rules_v0.md`.  
For current executable boundary, see `benchmark_spec/benchmark_spec_v0.md`.  
For primary metrics, see `benchmark_spec/primary_metrics_v0.md`.

---

## 2. Current Anchor Set

At the current repository stage, the benchmark has one anchor case for each formal pool:

- performance
- longtail
- consistency
- portability

These anchors are not intended to exhaust the benchmark.
They exist to establish the first stable benchmark shape and validate the end-to-end construction workflow.

At the current early pilot stage, all four anchors are treated as **common-core** because:

- tri-engine execution has been demonstrated
- result comparison has been demonstrated
- plan collection has been demonstrated
- the cases are simple enough to support fair cross-engine reporting

This classification may change later if the benchmark grows more complex.

---

## 3. Anchor Matrix

| case_id | primary_pool | dataset_line | anchor_role | key question answered | result closure | plan closure | taxonomy trial | current status |
|---|---|---|---|---|---|---|---|---|
| PERF_0001 | performance | common-core | smoke / pipeline anchor | Can the minimal benchmark pipeline run end-to-end across PostgreSQL, MySQL, and Spark? | closed | closed | complete | stable pilot anchor |
| LONGTAIL_0001 | longtail | common-core | structure-rich anchor | Can the benchmark carry richer SQL structure beyond simple template cases? | closed | closed | complete | stable pilot anchor |
| CONS_0001 | consistency | common-core | correctness anchor | Can the benchmark clearly distinguish semantically equivalent and non-equivalent rewrites? | closed | closed | complete | stable pilot anchor |
| PORT_0001 | portability | common-core | migration anchor | Can a source-style expression be rewritten into a more portable form without changing semantics? | closed | closed | complete | stable pilot anchor |

---

## 4. Anchor Case Table

| case_id | representative structure / trap | main taxonomy emphasis | notes |
|---|---|---|---|
| PERF_0001 | simple filter + order-by sanity case | basic plan operators only | lowest-complexity pipeline anchor |
| LONGTAIL_0001 | CTE + window + top-k-per-group | sql_feature + plan_operator + longtail realism | first structure-rich long-tail anchor |
| CONS_0001 | `COUNT(*)` vs `COUNT(column)` under NULL values | rewrite_opportunity + consistency semantics | first clean correctness anchor |
| PORT_0001 | function-style month selection vs half-open time range | portability + dialect adaptation | first clean portability anchor |

---

## 5. Per-Case Notes

### 5.1 PERF_0001
**Role**
- Minimal smoke / sanity anchor
- Verifies that the repository can execute a complete case-package loop

**Why it exists**
- Confirms tri-engine execution
- Confirms positive vs negative comparison path
- Confirms plan collection path
- Serves as a low-complexity benchmark sanity reference

**Representative characteristics**
- simple source / positive / negative structure
- low SQL feature density
- easy-to-explain outputs
- useful for tooling validation

**What it is not**
- Not a rich long-tail case
- Not a portability-rich case
- Not a representative consistency trap
- Not intended to demonstrate broad SQL feature coverage

**Current interpretation**
- Keep as the simplest stable pipeline anchor
- Use it to validate tooling and preflight behavior before more complex cases

---

### 5.2 LONGTAIL_0001
**Role**
- First structure-rich long-tail anchor

**Why it exists**
- Demonstrates that the benchmark can support richer SQL structure
- Exercises non-trivial SQL feature tags
- Exercises longtail-oriented trial labeling
- Provides a structure-oriented contrast against PERF_0001

**Representative characteristics**
- CTE
- window function
- top-k-per-group pattern
- richer execution plans across engines

**What it is not**
- Not primarily a portability case
- Not primarily a correctness-only case
- Not intended to be the canonical performance baseline

**Current interpretation**
- Use as the first serious long-tail coverage anchor
- Use it to validate taxonomy behavior on structure-rich SQL

---

### 5.3 CONS_0001
**Role**
- First consistency anchor

**Why it exists**
- Shows that rewrite correctness must be treated as a first-class benchmark dimension
- Demonstrates a simple but important semantic trap
- Validates positive / negative pair handling with witness-style data

**Representative characteristics**
- aggregation-sensitive rewrite
- NULL-sensitive semantic change
- easy-to-explain positive / negative contrast
- clear tri-engine reproducibility

**What it is not**
- Not primarily a longtail case
- Not primarily a portability case
- Not intended to maximize SQL structure complexity

**Current interpretation**
- Use as the baseline consistency teaching case
- Keep it simple and pedagogical
- Use it before moving to more complex semantic traps

---

### 5.4 PORT_0001
**Role**
- First portability anchor

**Why it exists**
- Shows that a more portable rewrite can preserve semantics
- Shows that a seemingly reasonable migration can still be wrong
- Establishes portability as a benchmark dimension distinct from performance and consistency

**Representative characteristics**
- date-time function based source expression
- common-core half-open range positive rewrite
- boundary-condition negative rewrite
- clear semantic portability trap

**What it is not**
- Not primarily a longtail structure case
- Not primarily a performance baseline
- Not primarily a NULL-based correctness case

**Current interpretation**
- Use as the first portability teaching case
- Use it to motivate later, harder cross-dialect portability cases

---

## 6. Coverage and Closure Summary

### 6.1 Formal pool coverage
At least one anchor exists for each formal pool:

- performance: yes
- longtail: yes
- consistency: yes
- portability: yes

### 6.2 Dataset-line coverage
At the current stage:

- common-core anchors: 4
- extended anchors: 0
- not-yet-admitted anchors: 0

### 6.3 Case-package closure
All current anchor cases support the following closure pattern:

source SQL  
→ positive rewrite / negative rewrite  
→ tri-engine execution  
→ result comparison  
→ plan collection  
→ taxonomy trial labeling

### 6.4 Taxonomy coverage (high-level)
- PERF_0001: minimal plan/operator anchor
- LONGTAIL_0001: SQL structure and long-tail anchor
- CONS_0001: consistency semantics anchor
- PORT_0001: portability semantics anchor

---

## 7. Why These Anchors Matter

These anchors provide the first stable benchmark shape.

They allow the project to move from:
- ad hoc examples

to:
- a structured benchmark story with explicit pool coverage
- explicit anchor roles
- explicit case-package closure
- explicit cross-engine comparability assumptions

They also make it possible to:
- evaluate whether the taxonomy is too weak or too noisy
- verify that each formal pool has at least one concrete case
- test the CLI / artifact-preflight pipeline against realistic benchmark objects
- prepare later benchmark characterization work
- separate benchmark design questions from benchmark expansion questions

---

## 8. Current Limitations

These anchors are not yet a full benchmark.
Current limitations include:

- each pool currently has only a small number of trial examples
- coverage density is still low
- the source inventory has not yet been transformed into a broad admitted case set
- pool-level characterization is still early-stage
- some taxonomy labels are still trial-level rather than final release-level
- common-core currently dominates because expansion has not yet introduced harder extended-only cases

---

## 9. Immediate Next Step

The next recommended step is not immediate large-scale benchmark expansion.

Instead, the project should first:

1. verify that the source inventory, pool rules, common-core / extended rules, and taxonomy remain aligned with the four anchor cases
2. produce a small anchor-based characterization summary
3. decide whether any taxonomy fields should be promoted into standard case metadata
4. decide which future cases should remain common-core and which should enter extended
5. only then begin controlled expansion beyond the four anchors

---

## 10. Update Rule

This file should be updated whenever:

- a new anchor case is added
- an anchor case changes primary role
- an anchor case changes dataset line (`common-core` / `extended`)
- an anchor case completes result closure or plan closure
- a trial anchor is promoted into a more stable benchmark reference
- the project changes the formal pool structure

Related protocol changes should also be reflected in:

- `benchmark_spec/decision_log.md`
- `benchmark_spec/benchmark_spec_v0.md`
- `docs/POOL_MAPPING_RULES.md`
- `benchmark_spec/common_core_extended_rules_v0.md`

when applicable.