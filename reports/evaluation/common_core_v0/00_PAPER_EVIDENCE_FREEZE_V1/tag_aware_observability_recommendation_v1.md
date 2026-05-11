# Tag-aware Observability Recommendation V1

This is a retained-artifact taxonomy audit only. No DB, EXPLAIN, checker, timing, generation, verifier, or LLM work was run.

## Key counts

- all registry cases: 190
- common-core cases: 40
- selected PG attribution packet: 24 rows across 20 unique cases
- PG attribution-ready frontier: 113 rows
- Table 10 selected cases: 7 rows including the separate failure diagnostic exemplar

## Recommendation

- The current 24-row PG attribution packet is sufficient for a selected-case Table 10 and for a route-level Table 5 note that selected PG attribution exists.
- The current 24-row packet is not strong enough if the next goal is a tag-aware observability coverage argument across common-core.
- The 24-row packet misses 7 common-core tags: portability:confirmed:boolean_semantics_gap, portability:confirmed:datetime_semantics_gap, portability:confirmed:type_semantics_gap, rewrite_opportunity:secondary:expression_simplification, rewrite_opportunity:secondary:function_normalization, sql_feature:primary:expression_complexity, sql_feature:primary:subquery_in_from.
- Expanding to the 113-row PG-ready frontier would recover 6 of those missing tags: portability:confirmed:datetime_semantics_gap, portability:confirmed:type_semantics_gap, rewrite_opportunity:secondary:expression_simplification, rewrite_opportunity:secondary:function_normalization, sql_feature:primary:expression_complexity, sql_feature:primary:subquery_in_from.
- Even after 113 rows, these common-core tags remain absent: portability:confirmed:boolean_semantics_gap.

## Smaller-than-113 follow-up if needed

- If a smaller follow-up is preferred, prioritize portability rows on PORT_0008 and PORT_0012 and subquery rows on CONS_0007 and LONGTAIL_0012.
- The most useful route/tag combinations are Direct LLM original and SQLGlot optimize for portability gaps, plus SQLGlot no-op and Calcite HEP for subquery_in_from coverage.

## Cleanest option

- If the goal is to redesign Table 5 around route x attribution frontier x tag coverage, the full 113-row PG-ready expansion is the cleanest retained frontier to target next.
- If the goal is only a stronger paper-facing Table 10, the current selected 24 plus one portability diagnostic supplement may already be enough.

## What Table 5 should say next

- Table 5 should be redesigned around route-level observability assets plus PG attribution frontier size plus tag coverage breadth.
- It should remain explicit that this is PG-only attribution readiness, not denominator-wide or cross-engine attribution.

## What Table 10 should say next

- Table 10 should present tag-aware representative diagnostics instead of only delta-class diversity.
- Keep the failure diagnostic separate from the exact-timed PG attribution panel.

## What must not be overclaimed

- Do not claim denominator-wide plan attribution.
- Do not claim global causal attribution.
- Do not claim the PG-ready 113 frontier is equivalent to full 120 or cross-engine attribution coverage.

中文说明：当前 24 行 packet 适合做 selected-case evidence，但如果想把 Table 5 变成真正 tag-aware 的 observability coverage matrix，那么扩展到 113 行 PG-ready frontier 是更干净的下一步。它能补回 24 行当前缺失的大部分 common-core tags，但依然不能支持 full-denominator 或 global causal attribution。
