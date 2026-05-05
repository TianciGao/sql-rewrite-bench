# VeriEQL Support Candidate Scan v0

## Scope

- Pool: `CONS` only
- Boundary: scan only, no VeriEQL execution, no PostgreSQL, no speedup, no baseline claim

## Summary

- Top 1 recommended candidate: `CONS_0035`
- Backup candidates:
  - `CONS_0004`
  - `CONS_0006`
- Scaffold wrapper for selected case next: `yes`

## Recommendation

### `CONS_0035`

- `source_sql_exists`: `yes`
- `positive_sql_exists`: `yes`
- `negative_sql_exists`: `yes`
- `ddl_pg_exists`: `yes`
- `has_exists`: `no`
- `has_correlated_subquery`: `no`
- `has_limit_offset`: `no`
- `has_aggregate`: `yes`
- `has_join`: `no`
- `likely_verieql_support_risk`: `low`
- `recommended_status`: `first_verdict_candidate`

Reason:

`CONS_0035` is the only full `source.sql` / `rewrite_pos_01.sql` / `rewrite_neg_01.sql` / `schema/ddl_pg.sql` package in the current scan that stays in a very small fragment across the triad: single-table, no `EXISTS`, no correlated subquery, no `LIMIT/OFFSET`, no derived subquery, and no dialect-sensitive function signals. It still uses aggregation, but that is materially simpler than the `EXISTS`-blocked `CONS_0007` path.

Relevant SQL shape:

```sql
-- source
SELECT EMPNO, COUNT(MGR) FROM EMP GROUP BY EMPNO, DEPTNO

-- positive
SELECT EMPNO, CASE WHEN MGR IS NOT NULL THEN 1 ELSE 0 END FROM EMP

-- negative
SELECT EMPNO, COUNT(*) FROM EMP GROUP BY EMPNO, DEPTNO
```

## Backup Candidates

### `CONS_0004`

- `source_sql_exists`: `yes`
- `positive_sql_exists`: `yes`
- `negative_sql_exists`: `yes`
- `ddl_pg_exists`: `yes`
- `has_exists`: `no`
- `has_correlated_subquery`: `no`
- `has_limit_offset`: `no`
- `has_aggregate`: `yes`
- `has_join`: `no`
- `likely_verieql_support_risk`: `medium`
- `recommended_status`: `maybe_later`

Reason:

This is still fairly small and avoids `EXISTS`, but the positive rewrite uses a derived subquery wrapper. That makes it a weaker first canary than `CONS_0035`.

### `CONS_0006`

- `source_sql_exists`: `yes`
- `positive_sql_exists`: `yes`
- `negative_sql_exists`: `yes`
- `ddl_pg_exists`: `yes`
- `has_exists`: `no`
- `has_correlated_subquery`: `no`
- `has_limit_offset`: `no`
- `has_aggregate`: `yes`
- `has_join`: `no`
- `likely_verieql_support_risk`: `medium`
- `recommended_status`: `maybe_later`

Reason:

This case stays single-table, but it introduces derived-subquery and `COUNT(DISTINCT ...)` complexity, which is riskier than `CONS_0035` for a first VeriEQL verdict attempt.

## Broader Classification

Cases recommended as `exclude_unsupported_feature` in this pass were excluded primarily because they contain one or more of:

- `EXISTS`
- likely correlated subquery structure
- `LIMIT` / `OFFSET`

This is now a concrete boundary informed by the executed `CONS_0007` canary, not just a theoretical concern.

Cases recommended as `maybe_later` generally have the required files and avoid `EXISTS`, but still carry one or more of:

- derived subquery wrappers
- joins
- `COUNT(DISTINCT ...)` or similar aggregate complexity

## Next Step

Recommended next step: scaffold the VeriEQL support wrapper for `CONS_0035` and run the same bounded module-mode canary path used for `CONS_0007`.
