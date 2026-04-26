# TPC-H Tri-Engine Performance Review v0

## 1. Document role and scope

This document is a **review-prep packet** for the already tri-engine-closed TPC-H performance batch.

Current scope:

- Group A: `PERF_0017`, `PERF_0018`, `PERF_0019`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0024`, `PERF_0025`, `PERF_0026`
- Group B: `PERF_0006`, `PERF_0007`, `PERF_0008`, `PERF_0009`, `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0013`, `PERF_0014`, `PERF_0015`, `PERF_0016`
- Group C: `PERF_0027`, `PERF_0028`, `PERF_0030`, `PERF_0031`

Explicitly excluded:

- `PERF_0029`

Reason for exclusion:

- `PERF_0029` remains deferred because of source execution shape / view lifecycle design questions and is therefore outside this review-prep packet.

Live case facts remain in:

- `inventory/case_registry.csv`

This document is **review-prep only**.

It does **not** make:

- admission judgments
- promotion judgments
- `common-core` movement judgments
- `extended` movement judgments
- formal review completion claims
- benchmark-line change claims
- any other status-movement claim

---

## 2. Methodological boundary

This packet summarizes **existing** package and artifact evidence only.

It is bounded by the following constraints:

- no engine reruns
- no validation reruns
- no plan recollection
- no registry updates
- no taxonomy rule changes
- no status movement

The packet therefore answers a narrower question:

> How should the current evidence-complete TPC-H tri-engine performance batch be organized for a later human review pass?

---

## 3. Batch summary

| case_id | TPC-H query identity / variant | group | packet role | validated engines | result evidence summary | plan evidence summary | package/taxonomy note | review-prep caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0017` | Query 10 / Returned Item Reporting | A | anchor | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | none |
| `PERF_0018` | Query 11 / Important Stock Identification | A | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | none |
| `PERF_0019` | Query 13 / Customer Distribution | A | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | none |
| `PERF_0020` | Query 16 / Parts/Supplier Relationship | A | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | none |
| `PERF_0021` | Query 17 / Small-Quantity-Order Revenue | A | coverage extender | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | none |
| `PERF_0022` | Query 18 / Large Volume Customer | A | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | registry status layer is `not_assessed`, not `staged_not_yet_admitted` |
| `PERF_0023` | Query 19 / Discounted Revenue | A | variant / edge case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | registry status layer is `not_assessed`, not `staged_not_yet_admitted` |
| `PERF_0024` | Query 20 / Potential Part Promotion | A | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | registry status layer is `not_assessed`, not `staged_not_yet_admitted` |
| `PERF_0025` | Query 21 / Suppliers Who Kept Orders Waiting | A | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | registry status layer is `not_assessed`, not `staged_not_yet_admitted` |
| `PERF_0026` | Query 22 / Global Sales Opportunity | A | coverage extender | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | full current-generation package and validation bundle present | registry status layer is `not_assessed`, not `staged_not_yet_admitted` |
| `PERF_0006` | Query 1 / Pricing Summary Report | B | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0007` | Query 6 / Forecasting Revenue Change | B | coverage extender | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0008` | Query 3 / Shipping Priority | B | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0009` | Query 4 / Order Priority Checking | B | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0010` | Query 12 / Shipping Modes and Order Priority | B | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0011` | Query 14 / Promotion Effect | B | coverage extender | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0012` | Query 2 / Minimum Cost Supplier | B | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0013` | Query 5 / Local Supplier Volume | B | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0014` | Query 7 / Volume Shipping | B | subquery-heavy case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0015` | Query 8 / National Market Share | B | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0016` | Query 9 / Product Type Profit Measure | B | representative join/aggregate case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; current case-local Spark validation bundle remains partial | package-layout hardening remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0027` | Query 8 Variant A | C | variant / edge case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; case-local taxonomy/trial file remains absent | taxonomy/trial backfill remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0028` | Query 12 Variant A | C | variant / edge case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; case-local taxonomy/trial file remains absent | taxonomy/trial backfill remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0030` | Query 14 Variant A | C | variant / edge case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; case-local taxonomy/trial file remains absent | taxonomy/trial backfill remains before any later formal review packet, but this is not an engine-closure failure |
| `PERF_0031` | Query 15 Variant A | C | variant / edge case | PostgreSQL / MySQL / Spark | PG/MySQL/Spark result checks all `ok=true` | PG/MySQL/Spark plan checks all `ok=true` | tri-engine evidence complete; case-local taxonomy/trial file remains absent | taxonomy/trial backfill remains before any later formal review packet, but this is not an engine-closure failure |

---

## 4. Recommended review order

Recommended Group A order:

1. `PERF_0017`
2. `PERF_0019`
3. `PERF_0022`
4. `PERF_0018`
5. `PERF_0020`
6. `PERF_0024`
7. `PERF_0025`
8. `PERF_0026`
9. `PERF_0021`
10. `PERF_0023`

Recommended Group B order:

11. `PERF_0006`
12. `PERF_0007`
13. `PERF_0008`
14. `PERF_0009`
15. `PERF_0010`
16. `PERF_0011`
17. `PERF_0012`
18. `PERF_0013`
19. `PERF_0014`
20. `PERF_0015`
21. `PERF_0016`

Recommended Group C order:

22. `PERF_0027`
23. `PERF_0028`
24. `PERF_0030`
25. `PERF_0031`

Short rationale:

- Group A should be reviewed first because it is the cleanest evidence-complete subset with current-generation package, validation-bundle, and taxonomy/trial coverage
- Group B should follow because its tri-engine execution and plan evidence is already sufficient for review-prep ordering, while package-layout hardening remains a bounded follow-up item
- Group C should come last because its tri-engine execution and plan evidence is already sufficient for review-prep ordering, while taxonomy/trial backfill remains a bounded follow-up item

---

## 5. Per-case evidence notes

### 5.1 Group A: fully review-ready artifact-complete cases

#### `PERF_0017`
- Query identity / variant: TPC-H Query 10 / Returned Item Reporting Query
- Role: anchor
- Source/rewrite interpretation: grouped reporting query with ordering and bounded result set; positive rewrite normalizes structure into a cleaner benchmark-shaped form
- Positive rewrite value: strong anchor example for cross-engine grouped reporting closure
- Negative rewrite value: controlled perturbation of limiting/selection behavior for a clear divergence check
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: source, positive, negative, all three DDLs, MySQL/Spark witness SQL, MySQL/Spark validation scripts, and plan-collection scripts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: none beyond general status-layer differences elsewhere in the batch
- Packet role: anchor

#### `PERF_0018`
- Query identity / variant: TPC-H Query 11 / Important Stock Identification Query
- Role: subquery-heavy case
- Source/rewrite interpretation: aggregate-and-threshold query with scalar-subquery and `HAVING` structure
- Positive rewrite value: useful cross-engine evidence for non-trivial aggregate + subquery behavior
- Negative rewrite value: threshold/condition perturbation provides a clean non-equivalence witness
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: none
- Packet role: subquery-heavy case

#### `PERF_0019`
- Query identity / variant: TPC-H Query 13 / Customer Distribution Query
- Role: representative join/aggregate case
- Source/rewrite interpretation: grouped customer-distribution query with join structure and ordered reporting output
- Positive rewrite value: representative grouped join/reporting case with good review readability
- Negative rewrite value: condition perturbation gives a compact divergence witness
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: none
- Packet role: representative join/aggregate case

#### `PERF_0020`
- Query identity / variant: TPC-H Query 16 / Parts/Supplier Relationship Query
- Role: subquery-heavy case
- Source/rewrite interpretation: subquery/filter-heavy analytical query with membership logic
- Positive rewrite value: good cross-engine example of subquery normalization under grouped analysis
- Negative rewrite value: `EXISTS`/filter perturbation preserves a meaningful negative contrast
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: none
- Packet role: subquery-heavy case

#### `PERF_0021`
- Query identity / variant: TPC-H Query 17 / Small-Quantity-Order Revenue Query
- Role: coverage extender
- Source/rewrite interpretation: compact scalar-subquery revenue case
- Positive rewrite value: extends coverage beyond heavy grouped reporting toward smaller subquery-driven analytical form
- Negative rewrite value: controlled aggregation/filter perturbation
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: none
- Packet role: coverage extender

#### `PERF_0022`
- Query identity / variant: TPC-H Query 18 / Large Volume Customer Query
- Role: representative join/aggregate case
- Source/rewrite interpretation: grouped reporting query combining subquery, `HAVING`, ordering, and limit
- Positive rewrite value: strong representative case for complex reporting-oriented tri-engine closure
- Negative rewrite value: limit/cardinality perturbation gives a clear divergence channel
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: registry status layer is `not_assessed`, not `staged_not_yet_admitted`
- Packet role: representative join/aggregate case

#### `PERF_0023`
- Query identity / variant: TPC-H Query 19 / Discounted Revenue Query
- Role: variant / edge case
- Source/rewrite interpretation: predicate-heavy revenue query with broad OR-style filtering logic
- Positive rewrite value: broadens packet coverage toward filter-dense edge behavior
- Negative rewrite value: predicate perturbation provides a useful edge-case negative
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: registry status layer is `not_assessed`, not `staged_not_yet_admitted`
- Packet role: variant / edge case

#### `PERF_0024`
- Query identity / variant: TPC-H Query 20 / Potential Part Promotion Query
- Role: subquery-heavy case
- Source/rewrite interpretation: nested subquery and ordering case with anti-/existence-style logic
- Positive rewrite value: strong coverage of nested subquery performance shape
- Negative rewrite value: existence/filter perturbation supports a meaningful negative witness
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: registry status layer is `not_assessed`, not `staged_not_yet_admitted`
- Packet role: subquery-heavy case

#### `PERF_0025`
- Query identity / variant: TPC-H Query 21 / Suppliers Who Kept Orders Waiting Query
- Role: subquery-heavy case
- Source/rewrite interpretation: `EXISTS` / `NOT EXISTS`-heavy analytical query with ordered/limited reporting output
- Positive rewrite value: high-value coverage for nested existence logic across all three engines
- Negative rewrite value: existence/limit perturbation keeps the negative easy to explain
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: registry status layer is `not_assessed`, not `staged_not_yet_admitted`
- Packet role: subquery-heavy case

#### `PERF_0026`
- Query identity / variant: TPC-H Query 22 / Global Sales Opportunity Query
- Role: coverage extender
- Source/rewrite interpretation: global-filtering query with nested existence logic and membership filtering
- Positive rewrite value: extends coverage toward multi-condition existence-driven logic
- Negative rewrite value: existence/filter perturbation provides a readable negative contrast
- Result evidence summary: PG/MySQL/Spark result checks all present and `ok=true`
- Plan evidence summary: PG/MySQL/Spark plan checks all present and `ok=true`
- Package completeness summary: all expected scoped package and validation artifacts are present
- Taxonomy/trial presence: present
- Human reviewer caveat: registry status layer is `not_assessed`, not `staged_not_yet_admitted`
- Packet role: coverage extender

### 5.2 Group B: review-ready with minor package notes

Group B cases are included in this packet because registry state and machine-readable tri-engine evidence are already aligned. The remaining issue is narrower: some current-generation case-local Spark validation-bundle components are not present in the package layout. In this packet, that gap is treated as package hardening still to be done before any later formal review packet, not as an engine-closure failure and not as a status judgment.

#### `PERF_0006`
- Query identity / variant: TPC-H Query 1 / Pricing Summary Report Query
- Role: representative join/aggregate case
- Evidence status: registry tri-engine closure matches PG/MySQL/Spark result and plan checks, all `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial (`spark_witness_data.sql`, `run_spark_validation.sh`, `run_spark_plan_collection.sh` absent); this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0007`
- Query identity / variant: TPC-H Query 6 / Forecasting Revenue Change Query
- Role: coverage extender
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0008`
- Query identity / variant: TPC-H Query 3 / Shipping Priority Query
- Role: representative join/aggregate case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0009`
- Query identity / variant: TPC-H Query 4 / Order Priority Checking Query
- Role: subquery-heavy case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0010`
- Query identity / variant: TPC-H Query 12 / Shipping Modes and Order Priority Query
- Role: subquery-heavy case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0011`
- Query identity / variant: TPC-H Query 14 / Promotion Effect Query
- Role: coverage extender
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0012`
- Query identity / variant: TPC-H Query 2 / Minimum Cost Supplier Query
- Role: subquery-heavy case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0013`
- Query identity / variant: TPC-H Query 5 / Local Supplier Volume Query
- Role: representative join/aggregate case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0014`
- Query identity / variant: TPC-H Query 7 / Volume Shipping Query
- Role: subquery-heavy case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0015`
- Query identity / variant: TPC-H Query 8 / National Market Share Query
- Role: representative join/aggregate case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

#### `PERF_0016`
- Query identity / variant: TPC-H Query 9 / Product Type Profit Measure Query
- Role: representative join/aggregate case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: current case-local Spark validation-bundle coverage remains partial; this is carried here as a package-layout hardening note, not as an engine-closure failure

### 5.3 Group C: review-ready evidence but taxonomy/trial backfill note

Group C cases are included in this packet because registry state and machine-readable tri-engine evidence are already aligned. The remaining issue is narrower: a case-local taxonomy/trial file is not yet present in the package. In this packet, that gap is treated as review-prep backfill still to be done before any later formal review packet, not as an engine-closure failure and not as a status judgment.

#### `PERF_0027`
- Query identity / variant: TPC-H Query 8 Variant A
- Role: variant / edge case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: case-local taxonomy/trial coverage remains absent; this is carried here as a review-prep backfill note, not as an engine-closure failure

#### `PERF_0028`
- Query identity / variant: TPC-H Query 12 Variant A
- Role: variant / edge case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: case-local taxonomy/trial coverage remains absent; this is carried here as a review-prep backfill note, not as an engine-closure failure

#### `PERF_0030`
- Query identity / variant: TPC-H Query 14 Variant A
- Role: variant / edge case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: case-local taxonomy/trial coverage remains absent; this is carried here as a review-prep backfill note, not as an engine-closure failure

#### `PERF_0031`
- Query identity / variant: TPC-H Query 15 Variant A
- Role: variant / edge case
- Evidence status: tri-engine registry/artifact state is consistent and all result/plan checks are `ok=true`
- Caveat: case-local taxonomy/trial coverage remains absent; this is carried here as a review-prep backfill note, not as an engine-closure failure

---

## 6. Evidence matrix

| case_id | registry tri-engine | PG result/plan ok | MySQL result/plan ok | Spark result/plan ok | source/pos/neg present | DDL coverage | validation bundle coverage | taxonomy/trial coverage | review-prep group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0007` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0008` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0009` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0010` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0011` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0012` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0013` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0014` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0015` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0016` | yes | yes | yes | yes | yes | all three | MySQL yes / Spark partial | yes | B |
| `PERF_0017` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0018` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0019` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0020` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0021` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0022` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0023` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0024` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0025` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0026` | yes | yes | yes | yes | yes | all three | full | yes | A |
| `PERF_0027` | yes | yes | yes | yes | yes | all three | full | missing | C |
| `PERF_0028` | yes | yes | yes | yes | yes | all three | full | missing | C |
| `PERF_0030` | yes | yes | yes | yes | yes | all three | full | missing | C |
| `PERF_0031` | yes | yes | yes | yes | yes | all three | full | missing | C |

---

## 7. Cross-case coverage summary

### 7.1 Join/aggregate coverage
- `PERF_0006`, `PERF_0008`, `PERF_0013`, `PERF_0015`, `PERF_0016`, `PERF_0017`, `PERF_0019`, and `PERF_0022` provide the clearest grouped reporting backbone
- aggregate-heavy reporting with ordering and bounded output is well represented

### 7.2 Subquery coverage
- `PERF_0009`, `PERF_0010`, `PERF_0012`, `PERF_0014`, `PERF_0018`, `PERF_0020`, `PERF_0021`, `PERF_0024`, `PERF_0025`, and `PERF_0026` provide strong scalar-subquery, membership, and existence coverage
- the batch is therefore not limited to simple join normalization

### 7.3 Predicate/edge coverage
- `PERF_0023` is the clearest predicate-heavy edge case
- `PERF_0025` and `PERF_0026` extend that with nested existence logic
- Group C adds controlled variant coverage without changing the underlying tri-engine evidence basis

### 7.4 Reporting/limit/order coverage
- `PERF_0008`, `PERF_0013`, `PERF_0015`, `PERF_0017`, `PERF_0019`, `PERF_0022`, and `PERF_0025` carry the clearest order/limit reporting pattern
- both reporting-oriented and subquery-oriented performance shapes are therefore reviewable from current artifacts

### 7.5 Variant coverage
- `PERF_0027`, `PERF_0028`, `PERF_0030`, and `PERF_0031` extend the packet with TPC-H variant forms that remain tri-engine evidenced even though they still carry taxonomy/trial backfill notes

---

## 8. Open questions for human reviewer

- Should Group A become the first formal review target because it is the cleanest evidence-complete subset?
- Does Group B need package hardening before any formal review, or is the existing tri-engine machine-readable evidence sufficient despite the older-generation Spark validation layout?
- Does Group C need taxonomy/trial backfill before any formal review, or can that remain a bounded follow-up note?
- Should `PERF_0023` remain the predicate-heavy edge case at the end of the first formal packet?
- Should `PERF_0022` be highlighted as a second representative anchor alongside `PERF_0017`?
- How much taxonomy / mapping detail is required before any later formal review beyond the current case-local taxonomy trial coverage in Groups A/B and the missing trial files in Group C?

---

## 9. Bottom line

This packet is suitable as review-prep material.

Group A is the easiest first review target.

Groups B and C are evidence-consistent but carry package / taxonomy notes.

No status movement is claimed.
