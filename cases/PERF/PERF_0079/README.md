# PERF_0079

- case_id: `PERF_0079`
- draft_origin: `JOB_DRAFT_0010`
- official package path: `cases/PERF/PERF_0079`
- original JOB query file: `10a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: mid-complexity cast/company/info realism case with multiple correlated filters
- expected benchmark value: mid-complexity cast/company/info realism case with multiple correlated filters
- expected risk level: `medium`
- hardening status: explicit `company_type` join cleanup applied and witness repaired so source/positive should no longer collapse to empty solely because `(voice)` was missing; validation status must be established only by engine runs under `runs/`
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should be fully minimal or preserve extra duplicate rows for aggregate stability
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
