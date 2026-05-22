# Spark Ready36 Resolved Controls Package

This package resolves the Spark ready36 manual controls run by folding in the targeted retry successes for `PORT_0003` and `PORT_0005`.

Scope:
- Spark only
- `36` fresh-executable cases from the Spark ready subset
- excludes the four `artifact_reuse_only` performance cases

Resolution rule:
- original ready36 successes are carried forward unchanged
- `PORT_0003` and `PORT_0005` use the targeted retry success records instead of the original failed records
- the original `LOCATION_ALREADY_EXISTS` failure provenance is preserved in row notes and package notes

This is a resolved manual controls package, not a full Spark `@40` package.
