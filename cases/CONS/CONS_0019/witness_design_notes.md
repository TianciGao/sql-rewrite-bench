# Witness Design Notes

- The source and positive rewrite still keep every outer row because COUNT star emits a row even when the filter rejects everything. The hard negative produces no subquery rows at all.
