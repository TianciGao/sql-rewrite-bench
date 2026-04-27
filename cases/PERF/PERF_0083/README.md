# PERF_0083

- case_id: `PERF_0083`
- draft_origin: `JOB_DRAFT_0006`
- official package path: `cases/PERF/PERF_0083`
- original JOB query file: `6a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: actor-keyword-title pattern with compact join-heavy realism
- expected benchmark value: actor-keyword-title pattern with compact join-heavy realism
- expected risk level: `low`
- hardening status: official case-local package constructed from the promotion-ready draft; witness keeps one shared Marvel path and one source-only name-pattern path so the anchored negative narrows rather than empties the result
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should stay minimal or preserve additional aggregate-stability rows
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
