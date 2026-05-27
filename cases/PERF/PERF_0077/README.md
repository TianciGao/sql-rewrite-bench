# PERF_0077

- case_id: `PERF_0077`
- source_family: `JOB/IMDB`
- source query identity: `JOB 3a.sql`
- draft_origin: `JOB_DRAFT_0003`
- package role: official case-local construction package only
- expected benchmark value: compact JOB/IMDB performance case with explicit positive rewrite, hard negative rewrite, and multi-path witness design around `%sequel%` vs `sequel%`
- expected engines: `PostgreSQL`, `MySQL`, `Spark`
- current status: case-local package constructed; not yet validated; not yet registry-updated
- disclaimer: this task does not make any admission, promotion, common-core, extended, or tri-engine-closure claim

## Remaining human decisions

- confirm that the positive rewrite is semantically safe enough for official validation
- confirm that the `%sequel%` vs `sequel%` negative is the preferred divergence mechanism for this JOB family
- confirm that text-column typing and collation expectations are acceptable for the first PG/MySQL/Spark pass
- confirm that the witness remains strong enough when converted from draft package to official case-local package
