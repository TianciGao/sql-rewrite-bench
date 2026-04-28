# Validation Draft Notes

`PORT_0006` has not been validated yet.

This directory only contains draft checker scaffolding. A later validation task should:

1. load the draft witness rows into PostgreSQL, MySQL, and Spark-compatible schemas,
2. execute `source.sql`,
3. execute `rewrite_pos_01.sql` and `rewrite_neg_01.sql`,
4. execute the Spark draft rewrites after human review of boolean-count behavior,
5. compare scalar source vs positive results numerically,
6. confirm that the hard negative diverges because the boundary row enters the denominator and numerator set incorrectly.

No engine commands have been run for this draft package in the current task.
