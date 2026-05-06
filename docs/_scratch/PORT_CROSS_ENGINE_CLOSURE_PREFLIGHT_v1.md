# PORT_CROSS_ENGINE_CLOSURE_PREFLIGHT_v1

## 0. Purpose And Boundary
- read-only PORT cross-engine closure preflight
- no execution
- no checker/speedup
- no SpeedupTransferRate computation
- separates route readiness from actual transfer evidence

## 1. Current PORT Evidence Recap
- current formal route packet is bounded rather than full-pool closure
- SQLGlot Transpile has bounded PG-side evidence, mixed PG execution, and only partial MySQL/Spark closure
- LLM Translate has stronger PG-side execution coverage but still lacks aligned full MySQL/Spark closure
- bounded cross-engine execution exists for `PORT_0022`, `PORT_0024`, and `PORT_0025`, with only `PORT_0024` both-engine closed and consistent
- claim boundary remains bounded route evidence only, not full transfer closure and not SpeedupTransferRate

## 2. Denominator Discovery
| denominator_name | case_count | case_ids | source_doc_or_report | intended_use | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| registry_port_pool | 27 | PORT_0001, PORT_0002, PORT_0006, PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0009, PORT_0010, PORT_0011, PORT_0012, PORT_0013, PORT_0014, PORT_0015, PORT_0016, PORT_0017, PORT_0018, PORT_0019, PORT_0020, PORT_0021, PORT_0022, PORT_0023, PORT_0024, PORT_0025, PORT_0026, PORT_0027, PORT_0028 | inventory/case_registry.csv | full registry-visible PORT pool; not a closed formal transfer denominator | registry_inventory_only_not_cross_engine_closure |
| bounded_pg_side_route_subset | 6 | PORT_0004, PORT_0012, PORT_0022, PORT_0013, PORT_0024, PORT_0025 | reports/formal_expansion/port_cross_engine_feasibility_preflight_v0.json | smallest current formal PORT route packet spanning PG-side route evidence and closure preflight | bounded_pg_side_route_subset_not_cross_engine_closure |
| clean_pg_side_route_subset | 2 | PORT_0004, PORT_0022 | reports/formal_port/port_current_results_snapshot_v0.json | clean denominator for bounded PG-side route evidence only | pg_side_only_clean_subset_not_cross_engine_closure |
| bounded_mysql_spark_execution_subset | 3 | PORT_0022, PORT_0024, PORT_0025 | reports/formal_expansion/port_cross_engine_bounded_execution_v0.json | smallest bounded MySQL+Spark closure packet attempted so far | bounded_mysql_spark_execution_not_full_port_closure |
| already_cross_engine_closed_subset | 1 | PORT_0024 | reports/formal_expansion/port_cross_engine_bounded_execution_v0.json | cases with explicit both-engine executable and consistency evidence from existing bounded execution | existing_bounded_cross_engine_closed_subset_not_full_port_closure |

## 3. Per-case Cross-engine Readiness Table
| case_id | source_family_or_dataset | route_type | source_sql_exists | pg_evidence | mysql_evidence | spark_evidence | sqlglot_transpile_evidence | llm_translate_evidence | result_consistency_evidence | speedup_evidence | transfer_metric_ready | readiness_status | blockers | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT_0004 | PARROT | sqlglot_transpile + llm_translate | yes | pg_side_route_evidence_present | none | none | pg_side_execution_present | pg_side_execution_present | pg_reference_exact_consistent_llm_only | none | no | pg_side_only_existing | missing_standardized_mysql_spark_witness_contract_for_formal_closure_packet | fix missing PORT artifacts |
| PORT_0012 | PARROT | sqlglot_transpile + llm_translate | yes | pg_side_route_evidence_present | none | none | pg_side_failure_present | pg_side_execution_present | pg_route_execution_present_reference_checker_holdout | none | no | blocked_dialect_failure | datetime_formatting, dialect_functions | create route-specific dry-run for SQLGlot Transpile |
| PORT_0022 | PARROT | sqlglot_transpile + llm_translate | yes | pg_side_route_evidence_present | failed | failed | pg_side_execution_present | pg_side_execution_present | pg_reference_inconsistent_llm | none | no | ready_for_mysql_spark_execution | none | bounded MySQL+Spark execution rerun only after explicit approval |
| PORT_0013 | PARROT | sqlglot_transpile + llm_translate (batch2c pg-side subset) | yes | pg_side_route_evidence_present | none | none | pg_side_failure_present | pg_side_execution_present | pg_side_route_only_existing | none | no | blocked_dialect_failure | boolean_aggregation | create route-specific dry-run for SQLGlot Transpile |
| PORT_0024 | PARROT | sqlglot_transpile + llm_translate (batch2c pg-side subset) | yes | pg_side_route_evidence_present | execution_success_existing | execution_success_existing | pg_side_execution_present | pg_side_execution_present | cross_engine_consistent_existing | none | no | cross_engine_closed_existing | none | retain as bounded cross-engine anchor; do not overclaim beyond current packet |
| PORT_0025 | PARROT | sqlglot_transpile + llm_translate (batch2c pg-side subset) | yes | pg_side_route_evidence_present | failed | failed | pg_side_execution_present | pg_side_execution_present | pg_side_route_only_existing | none | no | ready_for_mysql_spark_execution | none | bounded MySQL+Spark execution rerun only after explicit approval |

## 4. Route-level Summary
### SQLGlot Transpile
- denominator: `PORT_0004, PORT_0012, PORT_0022, PORT_0013, PORT_0024, PORT_0025`
- current evidence: `{'pg_side_success_cases': ['PORT_0004', 'PORT_0022', 'PORT_0024', 'PORT_0025'], 'pg_side_failure_cases': ['PORT_0012', 'PORT_0013'], 'both_engine_closed_cases': ['PORT_0024']}`
- engine coverage: `{'postgresql': 'bounded_pg_side_present', 'mysql': 'bounded_partial_existing', 'spark': 'bounded_partial_existing'}`
- blockers: `['PORT_0012 datetime formatting / dialect function mismatch', 'PORT_0013 boolean aggregation mismatch', 'PORT_0004 missing standardized witness contract for formal closure packet', 'PORT_0022 and PORT_0025 still blocked in bounded cross-engine execution']`
- next action: `create PORT route-specific dry-run for SQLGlot Transpile`

### LLM Translate
- denominator: `PORT_0004, PORT_0012, PORT_0022, PORT_0013, PORT_0024, PORT_0025`
- current evidence: `{'pg_side_success_cases': ['PORT_0004', 'PORT_0012', 'PORT_0013', 'PORT_0022', 'PORT_0024', 'PORT_0025'], 'pg_reference_exact_consistent_cases': ['PORT_0004'], 'pg_reference_inconsistent_cases': ['PORT_0022'], 'both_engine_closed_cases': ['PORT_0024']}`
- engine coverage: `{'postgresql': 'bounded_pg_side_present', 'mysql': 'bounded_partial_existing', 'spark': 'bounded_partial_existing'}`
- blockers: `['no full MySQL/Spark closure on aligned denominator', 'PORT_0022 and PORT_0025 blocked by target-engine execution surfaces', 'PORT_0004 lacks standardized closure-packet witness contract']`
- next action: `execute PORT MySQL/Spark closure for bounded PG-side subset`

### Human / Reference / Controls
- support route interpretation, reference comparison, and failure bucketing only
- not a rewrite-generation leaderboard line and not a substitute for cross-engine closure

## 5. SpeedupTransferRate Readiness
- can SpeedupTransferRate be computed now? `no`
- why not: `['cross_engine executable evidence is incomplete on the bounded route denominator', 'cross_engine consistency evidence is incomplete beyond PORT_0024', 'target_engine speedup / benefit evidence is not closed on an aligned denominator', 'PG-side evidence alone does not establish transfer metrics']`
- minimum prerequisites: `['same-engine speedup evidence on the candidate route denominator', 'target-engine executable evidence for the same denominator', 'target-engine consistency evidence for the same denominator', 'target-engine speedup or benefit evidence for the same denominator', 'common denominator alignment across routes and engines']`

## 6. Proposed Execution Plan
- cases: `['PORT_0004', 'PORT_0022', 'PORT_0024', 'PORT_0025']`
- route(s): `['SQLGlot Transpile', 'LLM Translate']`
- target engines: `['MySQL', 'Spark']`
- expected command family: `['python -m scripts.cli formal-port-cross-engine-bounded-execution', 'python -m scripts.cli formal-port-cross-engine-feasibility-preflight']`
- why this batch is minimal: `it starts from the already PG-side-proven and already-feasibility-audited bounded subset rather than expanding the formal denominator`
- risk: `medium: PORT_0022 and PORT_0025 already expose target-engine dialect failures; PORT_0004 still needs standardized closure-packet witness artifacts`

## 7. Recommended Next Step
- `fix missing PORT artifacts`

## 8. Non-Modification Note
- no execution
- no DB
- no checker/speedup
- no model/API
- no registry/review/rules/EXECUTION_STATUS/case changes
- taxonomy notes untouched
