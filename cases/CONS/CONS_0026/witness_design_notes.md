# Witness Design Notes

- `deptno=10` has two employees with the same job, so the source and positive rewrite count employee rows while the hard negative counts only distinct jobs. `deptno=20` has no employees, which also checks scalar-subquery NULL behavior.
