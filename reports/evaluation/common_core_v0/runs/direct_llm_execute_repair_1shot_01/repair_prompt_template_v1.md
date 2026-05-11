You are repairing a SQL rewrite.

Goal:
Return one complete SQL statement that is semantically equivalent to the source SQL and executable on the target engine.

Target engine:
{engine}

Schema:
{schema_or_ddl}

Source SQL:
{source_sql}

Previous candidate SQL:
{first_candidate_sql}

Observed failure:
{observed_failure}

Checker or execution context:
{checker_or_execution_context}

Rules:
- Return exactly one complete SQL statement.
- Do not include markdown.
- Do not include explanation.
- Do not include comments unless required by SQL syntax.
- Preserve source semantics.
- Use only tables and columns from the schema.
- Use syntax supported by the target engine.
