# Project Plan
## A Consistency-Aware, Plan-Observable, Cross-Engine Benchmark for SQL Rewriting

## 1. Research claim
This project is based on three claims:

1. Existing SQL rewrite benchmarks focus primarily on final performance and insufficiently model rewrite correctness.
2. Existing SQL rewrite benchmarks usually report final latency only, but fail to reveal which SQL fragments changed, which plan nodes changed, and why a rewrite speeds up or regresses.
3. Existing SQL rewrite evaluations are often single-engine, single-dialect, and single-scenario, making it difficult to assess real-world generalization.

The benchmark is therefore designed to elevate consistency, plan observability, and cross-engine portability into first-class benchmark dimensions.

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

## 3. Benchmark task tracks
### Track A: Same-engine rewrite
Given a source SQL query, produce a semantically consistent rewrite that is more efficient under the same engine.

### Track B: Plan-observable rewrite
Evaluate whether SQL fragment edits can be mapped to logical and physical plan changes, and whether the performance impact can be attributed to those changes.

### Track C: Cross-dialect / cross-engine rewrite
Given a source-dialect SQL query, produce a target-dialect rewrite that remains executable and result-consistent, and evaluate whether performance benefit transfers.

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

## 10. Experimental structure
Planned experiment groups:

- E1 Benchmark characterization
- E2 Ranking shift study
- E3 Plan observability study
- E4 Generalization study

## 11. Project execution roadmap
### Step 1
Bring up the machine and three-engine smoke

### Step 2
Taxonomy and case schema

### Step 3
Download and stage the first benchmark sources

### Step 4
Data loading and preprocessing

### Step 5
Manually construct the first batch of case packages

### Step 6
Plan collection and node alignment

### Step 7
Constrained LLM entry into the pipeline

### Step 8
Four-pool pilot formation

### Step 9
Baseline runs

### Step 10
Draft the first benchmark paper story

## 12. Current status
Current repository status:
- Week 1 closeout completed
- tri-engine smoke completed
- first case package closure completed
- first plan artifacts collected
- minimal CLI scaffolding completed
- artifact-preflight completed
- ready for Week 2 inventory design and taxonomy refinement
- not yet entered workload curation