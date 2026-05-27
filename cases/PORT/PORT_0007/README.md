# PORT_0007

`PORT_0007` is a draft portability case package derived from PARROT / BIRD `pg_res.json[1]`.

This case is portability-oriented because the source query combines PostgreSQL quoting, a subquery filter, and explicit `NULLS LAST` ordering, while the target forms adapt that logic for MySQL-like and Spark-like execution.

This package is not yet registered, not admitted, and not validated. It is only a case-local draft package.

Next steps are human review, witness implementation, checker implementation, tri-engine validation, and registry writeback only if the later validation evidence succeeds.
