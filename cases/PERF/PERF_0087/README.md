# PERF_0087

- case_id: `PERF_0087`
- draft_origin: `JOB_DRAFT_0011`
- official package path: `cases/PERF/PERF_0087`
- original JOB query file: `11a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: join-heavy aggregate with multiple role and info filters
- expected benchmark value: join-heavy aggregate with multiple role and info filters
- expected risk level: `medium`
- hardening status: official case-local package constructed from the promotion-ready draft; witness is designed to keep source and positive equal while the negative rewrite narrows one `company_name.name` prefix branch
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should stay minimal or preserve additional aggregate-stability rows
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
