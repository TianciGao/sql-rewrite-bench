# PERF_0078

- case_id: `PERF_0078`
- draft_origin: `JOB_DRAFT_0017`
- official package path: `cases/PERF/PERF_0078`
- original JOB query file: `17a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: clean keyword/company/cast realism case with low semantic ambiguity
- expected benchmark value: clean keyword/company/cast realism case with low semantic ambiguity
- expected risk level: `medium`
- hardening status: rewrite cleanup applied; witness includes explicit country-code and name near-miss paths; validation status must be established only by engine runs under `runs/`
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should be fully minimal or preserve extra duplicate rows for aggregate stability
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
