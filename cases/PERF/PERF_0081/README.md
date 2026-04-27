# PERF_0081

- case_id: `PERF_0081`
- draft_origin: `JOB_DRAFT_0004`
- official package path: `cases/PERF/PERF_0081`
- original JOB query file: `4a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: rating-plus-keyword join pattern with compact aggregation
- expected benchmark value: rating-plus-keyword join pattern with compact aggregation
- expected risk level: `low`
- hardening status: official case-local package constructed from the promotion-ready draft; witness keeps `rating` and `votes` paths separate while preserving the same sequel keyword shape
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should stay minimal or preserve additional aggregate-stability rows
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
