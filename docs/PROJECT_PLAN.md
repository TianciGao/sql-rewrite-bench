# Project Plan
## A Consistency-Aware, Plan-Observable, Cross-Engine Benchmark for SQL Rewriting

## 1. Research claim

This project is based on three claims:

1. Existing SQL rewrite benchmarks focus primarily on final performance and insufficiently model rewrite correctness.
2. Existing SQL rewrite benchmarks usually report final latency only, but fail to reveal which SQL fragments changed, which plan nodes changed, and why a rewrite speeds up or regresses.
3. Existing SQL rewrite evaluations are often single-engine, single-dialect, and single-scenario, making it difficult to assess real-world generalization.

The benchmark is therefore designed to elevate consistency, plan observability, and cross-engine portability into first-class benchmark dimensions.

---

## 2. Scope

### 2.1 In scope for v1
- Engines / dialects: Spark SQL, PostgreSQL, MySQL
- Benchmark tasks:
  - Track A: same-engine rewrite
  - Track B: plan-observable rewrite
  - Track C: cross-dialect / cross-engine rewrite
- Minimum benchmark unit: case package
- Pilot-scale benchmark construction and evaluation

### 2.2 Out of scope for v1
- UDF / stored procedure / trigger benchmarks
- Procedural SQL pipelines
- New engine families beyond Spark / PostgreSQL / MySQL
- Full workload curation and large-scale benchmark expansion
- compositional OOD split
- engine / dialect hold-out split

Note:  
Earlier design discussions considered the two split settings above, but the current project freeze excludes them for v1. They may be revisited in a later version.

---

## 3. Benchmark task tracks

### Track A: Same-engine rewrite
Given a source SQL query, produce a semantically consistent rewrite that is more efficient under the same engine.

### Track B: Plan-observable rewrite
Evaluate whether SQL fragment edits can be mapped to logical and physical plan changes, and whether the performance impact can be attributed to those changes.

### Track C: Cross-dialect / cross-engine rewrite
Given a source-dialect SQL query, produce a target-dialect rewrite that remains executable and result-consistent, and evaluate whether performance benefit transfers.

---

## 4. Taxonomy design

Taxonomy is defined before large-scale workload expansion.

### 4.1 SQL feature taxonomy
Examples:
- CTE
- correlated subquery
- outer join
- non-equi join
- window
- set operations
- deep nesting
- grouping sets
- date / string function variation

### 4.2 Logical-plan taxonomy
Examples:
- scan
- filter
- project
- join
- aggregate
- sort
- limit
- window
- subquery decorrelation
- materialization
- exchange

### 4.3 Workload-realism taxonomy
Examples:
- query length
- join count
- nesting depth
- operator ratio
- repetition
- temporal dynamics
- read/write mix
- skew / correlation
- result cardinality

### 4.4 Portability taxonomy
Examples:
- dialect-specific functions
- type semantics
- null semantics
- date-time semantics
- string function differences
- limit/fetch differences

---

## 5. Case package definition

A benchmark case is not a single SQL string.  
Each case package should include at least:

- schema + data profile
- source SQL
- positive rewrites
- hard negatives
- feature tags
- canonical AST / logical IR
- source plan
- rewritten plan
- SQL span → logical operator → physical node mapping
- result checker
- engine / dialect metadata

---

## 6. Data source strategy

The benchmark will not be built by simple union of existing workloads.

### Pool 1: Performance pool
Traditional analytical benchmark queries used as stable and reproducible base cases.

### Pool 2: Long-tail coverage pool
High-expression or long-tail SQL used to fill feature coverage holes.

### Pool 3: Consistency pool
Rule tests, equivalence-style pairs, and manually constructed negatives used for correctness-oriented tasks.

### Pool 4: Portability pool
Cross-system translation cases and manually curated triplets used for Spark / PostgreSQL / MySQL portability.

Each case must preserve:
- provenance
- coverage tags
- task role

---

## 7. LLM usage policy

LLM is not the benchmark designer.  
LLM may only be used for:

1. filling coverage holes
2. generating dialect variants
3. generating hard negatives

All LLM-generated candidates must pass:
- parser / formatter checks
- multi-engine execution checks
- differential testing
- multi-dataset consistency checks
- random human review

---

## 8. Plan observability

The benchmark must record three plan-level annotation layers:

### A. Logical Plan Delta
Which logical subtree changed:
- join reorder
- predicate pushdown
- subquery decorrelation
- aggregation placement

### B. Physical Plan Delta
Which physical node changed:
- join operator replacement
- spool / materialization creation or removal
- sort creation or removal
- scan range narrowing

### C. Benefit Attribution
Which node-level metrics explain the observed gain or regression:
- runtime
- rows
- cost
- buffer
- spill
- scan bytes

---

## 9. Metrics

### 9.1 Correctness
- executable rate
- result consistency
- negative rejection rate
- verifier support rate

### 9.2 Performance
- GM speedup
- p95 / regression tail
- win / tie / loss
- workload-level net gain

### 9.3 Plan observability
- node alignment coverage
- operator delta diversity
- bottleneck removal rate
- attribution agreement

### 9.4 Generalization
- cross-engine executable rate
- cross-engine consistency rate
- speedup transfer rate
- dialect portability coverage

---

## 10. Experimental structure

Planned experiment groups:

- E1 Benchmark characterization
- E2 Ranking shift study
- E3 Plan observability study
- E4 Generalization study

---

## 11. Project execution roadmap

### Step 1 — Machine bring-up and tri-engine smoke
Bring up the machine and complete PostgreSQL / MySQL / Spark smoke.

**Status:** completed

### Step 2 — Taxonomy and case schema
Define taxonomy and initial case schema / metadata structure.

**Status:** completed at current pilot level

### Step 3A — Controlled Batch-1 source acquisition and staging
Acquire and stage the first-wave sources needed to stabilize the benchmark source layer.

Batch-1 target sources:
- TPC-H
- TPC-DS
- SQLStorm
- Calcite Seeds
- PARROT

**Status:** completed

### Step 3B — Batch-1 source inspection and seed extraction
Inspect staged sources, identify first-wave seeds, and map them into pool-specific draft-case directions.

**Status:** completed

### Step 4 — Data loading and preprocessing
Generate or construct minimal datasets, preprocess imported subsets, and validate source execution paths.

**Status:** completed for the current `002` archetype cases at the level needed by the pilot

### Step 5 — First anchor cases
Construct and stabilize the first anchor cases.

Anchor cases:
- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`

**Status:** completed

### Step 6 — First external draft cases
Construct the first external draft cases from Batch-1 sources.

External draft cases:
- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

**Status:** completed

### Step 7 — Archetype completion
Use the four `002` cases as pool-specific archetypes and push them to archetype-complete status.

Target archetypes:
- performance archetype → `PERF_0002`
- longtail archetype → `LONGTAIL_0002`
- consistency archetype → `CONS_0002`
- portability archetype → `PORT_0002`

**Status:** completed

### Step 8 — Promotion review and first admission
Review the external draft cases for promotion toward `common-core_candidate` and, when justified, formal admission.

Current outcomes:
- `PERF_0002` admitted as the first external common-core case
- `PORT_0002` promoted to `common-core_candidate`
- `LONGTAIL_0002` remains staged
- `CONS_0002` remains staged

**Status:** completed for the first review cycle

### Step 9 — Selective deepening, not broad expansion
Do not expand broadly yet.

Instead:
- keep `PERF_0002` as the admitted external common-core reference
- keep `PORT_0002` under candidate review
- keep `LONGTAIL_0002` and `CONS_0002` staged
- improve documentation, decision rules, and reusable case-construction workflows

**Status:** current active phase

### Step 10 — Reusable case construction workflow
Turn the current `002` archetypes into reusable production patterns for future large-scale construction.

Expected outputs:
- archetype completion rules
- promotion / admission rules
- case construction templates
- cleaner document hierarchy
- later, semi-structured or semi-automated batch case construction

**Status:** in progress

### Step 11 — Pilot benchmark characterization
Use the anchor cases plus the external archetype cases to build the first more stable benchmark characterization story.

### Step 12 — Draft the first benchmark paper story
Use the pilot benchmark, its construction methodology, and its promotion/admission logic to support the first benchmark paper narrative.

---

## 12. Current status

Current repository status:

### 12.1 Infrastructure and benchmark base
- tri-engine smoke completed
- minimal CLI scaffolding completed
- artifact-preflight completed
- source inventory v0 established
- pool mapping rules established
- common-core / extended rules established
- primary metrics v0 established
- taxonomy v0.2 established

### 12.2 Anchor layer
Four anchor cases established:
- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`

All four anchor cases have:
- tri-engine result closure
- tri-engine plan closure

### 12.3 External case layer
Four Batch-1 external draft cases established:
- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

Their current status is:

- `PERF_0002`: admitted external common-core case
- `PORT_0002`: common-core candidate
- `LONGTAIL_0002`: staged draft case
- `CONS_0002`: staged draft case

### 12.4 Methodology layer
The repository now also includes:
- external draft case status tracking
- external case promotion review
- common-core admission check
- case archetype completion rules
- case-local promotion/admission metadata
- project-level decision log support for promotion and admission

### 12.5 Current active focus
The project is **not** currently in:
- broad source expansion
- large-scale workload curation
- mass case generation

The project **is currently in**:
- selective deepening
- external case promotion/admission governance
- documentation and workflow consolidation
- preparation for later scalable case construction

---

## 13. Practical interpretation of the current stage

The current repository is no longer in early bootstrap.

It has moved into a new stage:

> **pilot benchmark consolidation with selective promotion of external archetype cases**

That means the immediate goal is no longer “build more examples first,” but rather:

- stabilize the strongest existing cases
- keep weaker-but-useful cases staged
- make promotion and admission explicit and reviewable
- prepare the construction workflow that later scales beyond the current small pilot set