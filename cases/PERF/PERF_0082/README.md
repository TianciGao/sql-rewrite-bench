# PERF_0082

- case_id: `PERF_0082`
- draft_origin: `JOB_DRAFT_0005`
- official package path: `cases/PERF/PERF_0082`
- original JOB query file: `5a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: movie company and genre-style filter interplay with theatrical-note realism
- expected benchmark value: movie company and genre-style filter interplay with theatrical-note realism
- expected risk level: `low`
- hardening status: official case-local package constructed from the promotion-ready draft; witness isolates the company-type divergence while keeping the theatrical/France note filters intact
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should stay minimal or preserve additional aggregate-stability rows
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
