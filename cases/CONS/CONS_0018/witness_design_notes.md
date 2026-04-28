# Witness Design Notes

- One department has an employee and two do not. The source and positive rewrite still retain all departments because the aggregate subquery always emits one row, while the hard negative does not.
