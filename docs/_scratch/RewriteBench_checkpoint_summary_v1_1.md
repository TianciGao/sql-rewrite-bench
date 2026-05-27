# RewriteBench_checkpoint_summary_v1_1

## Status

This is a paper-facing checkpoint summary for evidence-packet synchronization only.

It does not record a new experiment, does not perform registry writeback, and does not imply admission, promotion, or common-core movement.

## Current Evidence Packet

`paper-draft-v1` remains the base evidence packet.

`v1.1` adds bounded PORT cross-engine evidence on top of that base packet.

The evidence packet should now be described as:

- `46` common-core evidence cases
- `6` PostgreSQL-side PORT cases
- bounded `3`-case x `2`-engine MySQL/Spark execution sub-slice

Interpretation:

- the `46`-case common-core packet remains the main same-engine paper basis
- the `6`-case PORT packet remains a PostgreSQL-side portability packet
- the new MySQL/Spark evidence is bounded follow-up evidence inside the approved `3`-case PORT subset, not a replacement for the base packet

## Same-engine Findings

The base paper packet remains centered on the already consolidated same-engine evidence.

- common-core evidence remains the main paper-draft-v1 basis at `46` cases
- same-engine PORT route evidence remains PostgreSQL-side only at `6` cases
- the bounded MySQL/Spark update does not change the same-engine denominator
- `SpeedupTransferRate` is not computed in this checkpoint

Interpretation:

- `v1.1` is an additive checkpoint, not a reset of the base paper packet
- the correct paper framing remains: strong same-engine evidence first, bounded cross-engine portability evidence second

## PORT / Cross-engine Findings

The PORT evidence now has three explicit layers:

1. PG-side PORT route evidence:
   - `6` cases
   - SQLGlot Transpile remains PG-side only and partial
   - LLM Translate remains PG-side only on the bounded slice
2. Cross-engine feasibility preflight:
   - `3 / 6` ready
   - recommended bounded subset:
     - `PORT_0022`
     - `PORT_0024`
     - `PORT_0025`
3. Bounded MySQL+Spark execution:
   - `3` approved cases x `2` engines
   - no PostgreSQL execution in this bounded run
   - no SQLGlot invocation in this bounded run
   - no LLM generation in this bounded run

Actual bounded result:

- only `PORT_0024` closed on both MySQL and Spark
- `PORT_0022` and `PORT_0025` remain execution-blocked before checker comparison
- `PORT_0024` closed under the existing normalized numeric policy
- the failed pairs are execution blockers, not checker mismatches

Claim boundary:

- this is not full PORT closure
- this is not a final cross-engine matrix
- the bounded execution layer remains:
  - `bounded_3_case_mysql_spark_execution_not_full_port_closure`

Accepted paper wording:

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

## Updated Paper-writeable Conclusions

- `paper-draft-v1` remains the base evidence packet and should not be rewritten as if the entire benchmark denominator changed.
- `v1.1` adds bounded cross-engine portability evidence without changing the main common-core same-engine packet.
- The paper can now describe the evidence packet as `46` common-core evidence cases, `6` PostgreSQL-side PORT cases, and a bounded `3`-case x `2`-engine MySQL/Spark execution sub-slice.
- The paper can now say that PORT evidence has three layers: PG-side route evidence, cross-engine feasibility preflight, and a bounded MySQL+Spark execution attempt.
- The paper can now say that only `PORT_0024` closed on both MySQL and Spark, while `PORT_0022` and `PORT_0025` remained execution-blocked before checker comparison.
- The paper must keep the bounded claim explicit and must not describe this as full PORT closure or a final cross-engine matrix.

## Remaining Gaps

- full PORT closure is still not established
- final cross-engine matrix coverage is still not established
- the blocked PORT cases outside the approved bounded subset remain unresolved for this paper cycle
- `PORT_0022` and `PORT_0025` remain blocked by engine-specific SQL compatibility before checker comparison
- `SpeedupTransferRate` is not computed
- broader cross-engine runtime or transfer claims should not be added from this checkpoint

## Recommended Updates To Paper-draft-v1

- update the evidence-packet description to:
  - `46` common-core evidence cases
  - `6` PostgreSQL-side PORT cases
  - bounded `3`-case x `2`-engine MySQL/Spark execution sub-slice
- update the RQ3 / portability wording so that the PORT evidence is described in three layers rather than as a single closure claim
- add the accepted bounded wording for the MySQL+Spark execution attempt
- state explicitly that only `PORT_0024` closed on both engines
- state explicitly that `PORT_0022` and `PORT_0025` remained execution-blocked before checker comparison
- state explicitly that the bounded MySQL/Spark run did not invoke SQLGlot or LLM generation
- keep explicit non-claims:
  - not full PORT closure
  - not a final cross-engine matrix
  - no `SpeedupTransferRate`

## Recommended Stop Decision

- do not expand PORT further for this paper draft
- use the new bounded evidence to update RQ3 / portability wording
- keep the `46`-case common-core packet as the main paper-draft-v1 base
- keep the bounded MySQL/Spark slice as an additive checkpoint rather than a new primary denominator

## Source Basis

- `docs/_scratch/PAPER_EXPERIMENT_RESULTS_ROLLUP_v0.md`
- `docs/_scratch/BASELINE_COVERAGE_AUDIT_v0.md`
- `docs/_scratch/EXPANDED_PORT_RESULTS_CLOSEOUT_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_CLOSEOUT_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_BOUNDED_EXECUTION_v0.md`
- `docs/_scratch/PORT_CROSS_ENGINE_FEASIBILITY_PREFLIGHT_v0.md`
- `reports/formal_expansion/port_cross_engine_bounded_execution_v0.json`

## Non-Modification Note

- no DB execution was performed while producing this checkpoint
- no model calls were performed while producing this checkpoint
- no SQLGlot execution was performed while producing this checkpoint
- no case files were modified
- no registry files were modified
- no review files were modified
- no benchmark rules, taxonomy rules, admission rules, common-core rules, or `docs/EXECUTION_STATUS.md` were modified
- the three long-standing untracked taxonomy notes were left untouched
