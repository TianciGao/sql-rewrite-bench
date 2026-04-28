# Validation Draft Notes

`PORT_0003` has not been validated yet.

This directory only contains draft checker scaffolding. A later validation task should:

1. load the draft witness rows into PostgreSQL, MySQL, and Spark-compatible schemas,
2. execute `source.sql`,
3. execute `rewrite_pos_01.sql` and `rewrite_neg_01.sql`,
4. execute the Spark draft rewrites after human review of the null-order expression,
5. compare source vs positive for equality and source vs negative for divergence,
6. record engine-specific evidence only after those checks succeed.

No engine commands have been run for this draft package in the current task.
