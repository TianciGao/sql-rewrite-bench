# Runtime Root Not Retained

The staged external runtime copy `runtime_root_recovered_extraction_v1` was intentionally not retained in the repository run artifacts.

Reason:
- it is a staged external runtime copy under the recovered-extraction route
- retaining it would create an unnecessary bulky snapshot risk
- this run preserves patch audits, extraction audits, raw fields, generated SQL, and logs instead
