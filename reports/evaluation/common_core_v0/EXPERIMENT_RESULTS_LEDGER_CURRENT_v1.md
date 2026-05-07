**EXPERIMENT_RESULTS_LEDGER_CURRENT_v1**

This ledger organizes current Common-core v0 and related historical evidence without merging incompatible denominators into one leaderboard.

**1. Denominator Dictionary**
- `seed_common_core_9`: bounded seed common-core packet.
- `expanded_pg_evidence_46`: historic expanded PostgreSQL evidence line.
- `prior_method_pg10`: bounded PG-only prior-method speedup slice.
- `port_bounded_6`: bounded six-case portability closure packet.
- `common_core_v0_40`: frozen current Common-core v0 denominator.
- Different denominators must not be merged into one leaderboard.

**2. Controls / Benchmark Support Results**
- `common_core_v0_40` controls are denominator-complete benchmark support evidence: `360` planned rows, `324` success, `36` explicit `skipped_unsupported`, `0` missing.
- Controls are support evidence, not a method leaderboard.
- The historic `expanded_pg_evidence_46` control line remains a separate older support packet.

**3. SQLGlot Generation Results**
- `common_core_v0_40` generation-only packet: `240` rows, `203` generated, `37` generation failures, `37` no-op outputs.
- This is generation coverage only. It is not execution, consistency, timing, or speedup evidence.

**4. SQLGlot Same-Engine Execution Results**
- Combined `common_core_v0_40` SQLGlot same-engine execution evidence: `240` planned rows, `137` executed successes, `16` executed failures, `87` explicit skipped rows.
- Source package validators are both clean: non-PORT `ok=true issue_count=0`, PORT resolved `ok=true issue_count=0`.
- PORT witness gaps for `PORT_0003` and `PORT_0005` were resolved by retry and are not counted as SQLGlot method failures.

**5. SQLGlot Validity-Only Summary**
- `common_core_v0_40` validity summary: executable rate over full planned denominator `0.5708`, executable rate over attempted denominator `0.8954`.
- Explicit preserved buckets remain visible: `generation_failed=27`, `noop_generated=24`, `skipped_unsupported=36`.
- This is validity/execution-only evidence, not timing or speedup.

**6. Existing Speedup / Performance Evidence**
- `prior_method_pg10` bounded PG-only speedup slice remains reportable as historic bounded evidence: Calcite HEP `GM=0.9443`, R-Bot `GM=0.8804`, LearnedRewrite `GM=0.6296`, LLM-R2 `GM=0.9592`.
- `seed_common_core_9` and `expanded_pg_evidence_46` packets also contain older bounded validity/performance rows in the paper draft and baseline evidence matrix.
- These are separate historical packets and must not be merged with `common_core_v0_40`.

**7. PORT / Generalization Evidence**
- `port_bounded_6` cross-engine closure snapshot is reportable now as bounded closure evidence: `6/6` closed for `PORT_0004`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`.
- `SQLGlot Transpile` PG-side bounded packet: `4/6` success, `2/6` failure.
- `LLM Translate` PG-side bounded packet: `6/6` success.
- None of these support `SpeedupTransferRate` yet.

**8. Plan Observability Evidence**
- Current formal plan-observability evidence is preflight-only on `seed_common_core_9`: controls `9/9` ready, SQLGlot method plans `0/9`, Direct LLM method plans `0/9`.
- No operator alignment or attribution has been computed.

**9. Verifier / Support Evidence**
- `SQLSolver`: bounded support smoke, `verifier_support_rate=3/4` across `4` pairs.
- `VeriEQL`: bounded support canary / availability evidence; negative refutation usable, positive proof not closed.
- These are verifier/support rows, not rewrite speed leaderboard rows.

**10. Taxonomy / RQ4 Coverage Evidence**
- Current RQ4 draft slice covers `12` cases: `9` common-core plus `3` PORT snapshot cases.
- Useful for paper drafting, but metadata caveats remain and taxonomy closure is not final.

**11. What Can Be Reported Now**
- denominator dictionary and denominator separation rules
- Common-core v0 controls / benchmark support coverage
- SQLGlot generation coverage
- SQLGlot same-engine execution evidence on `common_core_v0_40`
- SQLGlot validity-only executable-rate style summaries
- bounded historic PG-only performance evidence on separate older denominators
- bounded PORT closure/generalization evidence on the six-case packet
- plan-observability preflight readiness status
- verifier/support evidence as separate support-track results

**12. What Must Not Be Claimed Yet**
- no merged leaderboard across `seed_common_core_9`, `expanded_pg_evidence_46`, `prior_method_pg10`, `port_bounded_6`, and `common_core_v0_40`
- no `GM_Speedup` for `common_core_v0_40` SQLGlot, because timing-bearing method rows do not exist
- no `RegressionRate@20%` for `common_core_v0_40` SQLGlot, for the same reason
- no `SpeedupTransferRate`, because bounded PORT closure does not include aligned target-engine benefit evidence
- no use of SQLSolver or VeriEQL as rewrite speed leaderboard methods
- no plan parse / node alignment / attribution metric claims for Common-core v0 method runs yet

**13. Next Recommended Experiment Gaps**
1. Build timing-bearing same-engine method packages on `common_core_v0_40` before any speedup or regression claims.
2. Materialize explicit `port_translation_summary` style packages before any cross-engine method ranking.
3. Collect method-generated plan artifacts before claiming Common-core v0 plan observability metrics.
4. Expand verifier/support only if a broader support table is needed.
5. Harden taxonomy metadata before stronger RQ4 claims.
