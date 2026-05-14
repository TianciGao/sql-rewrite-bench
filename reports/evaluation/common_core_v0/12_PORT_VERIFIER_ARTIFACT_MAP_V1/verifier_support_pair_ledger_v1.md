# Verifier Support Pair Ledger v1

## Purpose

这个文件回答什么问题：把 Section 8.9 的 verifier/support evidence 做成 pair-denominator-aware ledger，并明确它不是 rewrite-generation baseline。

## Verifier support table

| verifier | pair_id | case_id | pair_type | result | prove | refute | unknown | timeout | support_status | denominator_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SQLSolver | summary_support_pairs_4_smoke | NA_not_retained | summary_smoke_support_pairs | bounded_3_over_4_support_smoke | NA_not_found | NA_not_found | NA_not_found | NA_not_found | smoke_only | support_pairs_4_smoke |
| VeriEQL | summary_cons_0035_pairs_2 | CONS_0035 | bounded_canary_pair_set | bounded_1.0_on_2_pairs_caveated | 0 | 2 | 0 | 0 | canary_only | bounded_canary_cons_0035_pairs_2 |

## SQLSolver status

- Retained evidence supports only `support_pairs_4_smoke`.
- The freeze layer retains `3/4` bounded support but does not retain a clean prove/refute/unknown/timeout split.

## VeriEQL status

- Retained evidence supports only a bounded `CONS_0035` two-pair canary.
- The negative refutation evidence is clear, while the positive side remains caveated and must not be generalized to a broader denominator.

## What this supports

- Verifier-support evidence as bounded support-layer context.
- Explicit support-pair denominator labels.

## What this does not support

- Rewrite generation claims.
- Same-engine speedup comparison.
- Common-core 120-row denominator comparison.
- Broad CONS9 verifier completion claims.

## Safe prose snippet for the paper

Verifier tools provide support evidence only. They do not generate rewrite candidates. They should not be compared to rewrite methods on speedup or same-engine correctness.
