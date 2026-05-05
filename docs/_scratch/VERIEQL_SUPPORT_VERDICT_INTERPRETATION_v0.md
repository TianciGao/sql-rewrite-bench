# VeriEQL Support Verdict Interpretation v0

## Scope

- Case: `CONS_0035`
- Boundary:
  - support/verifier only
  - no speedup
  - no rewrite baseline
  - not final support-table result

## SQL Under Review

Source SQL:

```sql
SELECT EMPNO, COUNT(MGR) FROM EMP GROUP BY EMPNO, DEPTNO
```

Positive SQL:

```sql
SELECT EMPNO, CASE WHEN MGR IS NOT NULL THEN 1 ELSE 0 END FROM EMP
```

Negative SQL:

```sql
SELECT EMPNO, COUNT(*) FROM EMP GROUP BY EMPNO, DEPTNO
```

DDL:

```sql
CREATE TABLE EMP (EMPNO BIGINT, MGR BIGINT, DEPTNO BIGINT);
```

## Verdicts

- `source_positive_status=non_equivalent`
- `source_negative_status=non_equivalent`
- `prove_count=0`
- `refute_count=2`
- `error_count=0`

## Source-Positive Interpretation

`source_positive` being `non_equivalent` is best explained by missing constraint bridge, not by wrapper/schema failure and not by a fresh VeriEQL runtime issue.

Why:

- the source query is aggregate and grouped by `(EMPNO, DEPTNO)`
- the positive query is row-level and emits one row per input row
- with empty constraints, VeriEQL is allowed to consider multiple rows in the same `(EMPNO, DEPTNO)` group

The counterexample it found is exactly that shape:

- row 1: `(EMPNO=0, MGR=0, DEPTNO=0)`
- row 2: `(EMPNO=0, MGR=NULL, DEPTNO=0)`

Under this data:

- source returns one grouped row with `COUNT(MGR)=1`
- positive returns two rows, one with `1` and one with `0`

So under universal semantics with no constraints, the refutation is expected.

Classification:

- expected non-equivalence under universal semantics: `yes`
- missing constraint bridge: `yes`
- wrapper/schema bug: `no`
- VeriEQL semantic/subset limitation: `no`
- unknown: `no`

## Source-Negative Interpretation

`source_negative` being `non_equivalent` is expected and cleaner.

The negative comparator replaces `COUNT(MGR)` with `COUNT(*)`. Those differ whenever a grouped row has `MGR IS NULL`. VeriEQL's counterexample uses exactly that condition, so this refutation is strong support evidence under the current empty-constraint policy.

Classification:

- expected non-equivalence under universal semantics: `yes`
- missing constraint bridge: `no`

## Candidate Constraints If Positive Equivalence Was Intended

Do not add these yet, but the smallest plausible bridge suggested by the counterexample is:

- `UNIQUE (EMPNO, DEPTNO)`
- equivalently: at most one row per `(EMPNO, DEPTNO)` group

That would block the specific duplicate-group counterexample and is the first bounded constraint to test.

## Support-Table Readiness

This result can enter a support table only with a narrow caveat.

Usable now:

- executed VeriEQL canary reached verdict stage
- negative pair refutation is meaningful support evidence

Required caveat:

- positive pair refutation is constraint-sensitive under the current empty-constraint first pass
- it should not be treated as a clean failure of the benchmark pair itself

So the correct status is:

- support-canary verdict evidence with caveat, not final support-table evidence

## Recommended Next Step

Recommended next step: add a bounded constraint-bridge experiment for `CONS_0035`.

That is better than scanning for an even simpler case first, because the current executed result already isolates a precise semantic reason for the positive refutation.
