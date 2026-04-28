# PORT_0003

`PORT_0003` is a draft portability case package derived from PARROT / BIRD `pg_res.json[3]`.

This case is portability-oriented because the source query depends on PostgreSQL-style identifier quoting and explicit `NULLS LAST` ordering, while the draft target rewrites adapt that behavior for MySQL-like and Spark-like forms.

This package is not yet registered, not admitted, and not validated. It is only a case-local draft package.

Next steps are human review, witness implementation, checker implementation, tri-engine validation, and registry writeback only if the later validation evidence succeeds.
