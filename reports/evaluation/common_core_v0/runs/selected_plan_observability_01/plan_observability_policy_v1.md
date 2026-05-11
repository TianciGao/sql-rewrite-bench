# Plan Observability Policy V1

- Selection base: retained exact-timed rows from Direct LLM repair timing, SQLGlot per-case timing, and Calcite 93-row timing, plus the retained Table 10 failure exemplar.
- Speedup selection: highest retained speedup across the selected exact-timed packets.
- Regression selection: lowest retained speedup across the selected exact-timed packets.
- Tie selection: speedup closest to 1.0; rows within 0.001 of the best closeness are tie-candidates, and PostgreSQL is preferred inside that band.
- Extra coverage: add one SQLGlot row if SQLGlot is absent from the base four; add one Calcite row if Calcite is absent from the base four.
- Plan extraction: PostgreSQL uses EXPLAIN (FORMAT JSON); Spark uses EXPLAIN FORMATTED.
- Attribution: selected-case only, low/medium confidence only, no node alignment claim.
