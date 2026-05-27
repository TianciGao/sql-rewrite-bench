# PERF_0102

- case_id: `PERF_0102`
- draft_origin: `local_job_corpus_direct_wave_06`
- official package path: `cases/PERF/PERF_0102`
- original JOB query file: `17a.sql`
- local source path: `datasets/raw/job/staged/job/17a.sql`
- case intent: JOB/IMDB-derived case-local performance draft package for controlled engine validation
- why selected: compact character-name keyword family with a stable person-name prefix hard negative
- expected benchmark value: compact character-name keyword family with a stable person-name prefix hard negative
- expected risk level: `low`
- hardening status: official case-local package constructed directly from the local JOB corpus; witness is designed to keep source and positive equal while the negative rewrite narrows one stable predicate or literal family
- disclaimer: This case-local package does not imply admission, promotion, common-core movement, extended-line movement, or formal review completion.
- exact remaining human decisions after construction:
  - confirm whether the positive rewrite is semantically safe enough for long-term retention
  - confirm whether the negative rewrite is the right divergence mechanism for witness validation
  - confirm minimal cross-engine DDL types and whether any text columns need tighter typing
  - confirm whether the witness data should stay minimal or preserve additional aggregate-stability rows
  - decide whether this JOB-derived case should remain staged or proceed to later formal review
