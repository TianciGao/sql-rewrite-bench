# LLMR2_BATCH_B_SYNTAX_FAILURE_AUDIT_v1

## 0. Purpose And Boundary
This is a read-only syntax failure audit only. It does not rerun LLM-R2, call any model/API, run Java rule application, run PostgreSQL, run checker, or run speedup.

## 1. Batch B Result Recap
- `PERF_0019` failed candidate execution with `SyntaxError`.
- `PERF_0024` failed candidate execution with `SyntaxError`.
- `PERF_0033` produced a clean extracted candidate that executed and was checker consistent.
- `speedup_status = not_run`.

## 2. Artifact Inventory
### PERF_0019
- result CSV path exists: yes
- raw generated SQL path exists: yes
- clean candidate path exists: yes
- checker result path exists: yes
- stdout path exists: yes
- stderr path exists: yes

### PERF_0024
- result CSV path exists: yes
- raw generated SQL path exists: yes
- clean candidate path exists: yes
- checker result path exists: yes
- stdout path exists: yes
- stderr path exists: yes

## 3. Candidate SQL Inspection
### PERF_0019
Candidate:

```sql
select             c_custkey,             count(o_orderkey)         from             customer left outer join orders on                 c_custkey = o_custkey                 and o_comment not like '%express%deposits%'         group by             c_custkey     ) as c_orders (c_custkey, c_count) group by     c_count order by     custdist desc,     c_count desc;
```

- statement count: `1`
- starts with `SELECT`/`WITH`: yes
- obvious syntax defects:
  - starts inside the inner subquery rather than at the outer `select c_count, count(*) as custdist`
  - contains a closing derived-table alias `) as c_orders ...` without the matching opening outer query context

### PERF_0024
Candidate:

```sql
SELECT l_partkey, l_suppkey, SUM(l_quantity) AS f2 FROM lineitem WHERE l_shipdate >= DATE '1997-01-01' AND l_shipdate < (DATE '1997-01-01' + INTERVAL '1' YEAR) GROUP BY l_partkey, l_suppkey) AS t4 ON partsupp.ps_partkey = t4.l_partkey AND partsupp.ps_suppkey = t4.l_suppkey AND partsupp.ps_availqty > 0.5 * t4.f2) AS t6 ON supplier.s_suppkey = t6.ps_suppkey ORDER BY supplier.s_name;
```

- statement count: `1`
- starts with `SELECT`/`WITH`: yes
- obvious syntax defects:
  - starts inside the innermost aggregation subquery rather than at the outer supplier query
  - contains `) AS t4 ON ...` and `) AS t6 ON ...` join fragments without the matching outer `SELECT ... FROM ... INNER JOIN (` prefixes

## 4. Checker Failure Inspection
### PERF_0019
- source execution status: `success`
- candidate execution status: `failed`
- exact `SyntaxError` text:

```text
语法错误 在 ")" 或附近的
LINE 1: ...sits%'         group by             c_custkey     ) as c_ord...
                                                             ^
```

- failure category: `SyntaxError`
- checker reached output comparison: no

### PERF_0024
- source execution status: `success`
- candidate execution status: `failed`
- exact `SyntaxError` text:

```text
语法错误 在 ")" 或附近的
LINE 1: ...+ INTERVAL '1' YEAR) GROUP BY l_partkey, l_suppkey) AS t4 ON...
                                                             ^
```

- failure category: `SyntaxError`
- checker reached output comparison: no

## 5. Control Case Comparison
- `PERF_0033` used the same output extraction pipeline: raw generated SQL artifact, deterministic cleanup, then checker handoff.
- `PERF_0033` clean candidate passed PostgreSQL execution and checker consistency.
- The visible difference is SQL shape:
  - `PERF_0033` is a single top-level `SELECT` without nested subqueries, so the “take the last `SELECT`” cleanup heuristic still yields the full query.
  - `PERF_0019` and `PERF_0024` contain nested subqueries, so the same heuristic wrongly cuts to an inner `SELECT`, producing truncated SQL.

## 6. Diagnosis
### PER-case
- `PERF_0019`: `extraction_artifact`
- `PERF_0024`: `extraction_artifact`

### Batch-level
- `extraction_artifact`

Reasoning:
- Both failed candidates are syntactically incomplete in a way that directly matches the cleanup heuristic, not a checker wrapper defect.
- The raw generated SQL artifacts contain multiple `SELECT` tokens and the recovered “clean” candidate for each failed case begins at an inner subquery.
- `PERF_0033` succeeds under the same checker wrapper and the same cleanup path because its query shape does not trigger this truncation.

## 7. Recommended Next Step
- fix extraction and rerun checker only

Reasoning:
- The evidence points to deterministic extraction damage after generation, not to a need to rerun LLM-R2.
- The next bounded step is to recover the outermost valid query statement from the existing Batch B artifacts for `PERF_0019` and `PERF_0024`, then rerun checker handoff only.

## 8. Non-Modification Note
- no LLM-R2 rerun occurred
- no model/API call occurred
- no Java rule applier ran
- no PostgreSQL, checker, or speedup step ran in this audit
- no repo, case, registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
