# Witness Design Notes

- Every department row self-witnesses the source and positive rewrite through its own `deptno` and `dname`. Two rows share the same `loc`, so the hard negative retains only that pair and drops the isolated location row.
