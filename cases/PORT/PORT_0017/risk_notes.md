# Risk Notes

- Portability focus: type_coercion, identifier_case_or_quoting.
- Witness exposure now relies on a draft-only row that falls strictly between `0.18` and `0.50` on the percentage scale so the hard negative is observable without changing SQL semantics.
- Spark execution is split onto Spark-specific rewrite files because PostgreSQL-target `DOUBLE PRECISION` casts are not parser-compatible with the Spark path.
- This package is draft-only and still needs later human review of plan semantics and execution behavior.
