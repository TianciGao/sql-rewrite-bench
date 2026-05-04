# FORMAL_COMMON_CORE_RESULTS_CLOSEOUT_v0

## 1. Status

This is the formal common-core results closeout packet.

It consolidates the completed paper-facing common-core results only.

It is not a registry writeback.

It is not a common-core admission decision.

It is not a formal review update.

It is not a final leaderboard claim.

It is not a benchmark protocol freeze.

## 2. Executive Summary

The formal common-core packet now has four closed first-pass result lines:

- control-route correctness and guard behavior are complete from existing checker-backed artifacts
- generated-method checker-backed consistency is complete across the full 9-case common-core denominator for SQLGlot same-dialect and Direct LLM rewrite
- PERF-only correctness-gated speedup is complete for the positive control, SQLGlot same-dialect, and Direct LLM rewrite
- plan observability is complete at the plan-availability, plan-parse, pair-readiness, and lightweight operator-delta observation layers

The remaining out-of-scope items are:

- full benchmark leaderboard packaging
- CONS inclusion in `GM_Speedup`
- operator-delta attribution
- PORT closure
- RQ4 taxonomy / failure slicing aggregation

## 3. Denominator

### 9-Case Common-Core Consistency Denominator

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

### 7-Case PERF-Only Speedup Denominator

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

### CONS Speedup Exclusion

- `CONS_0007` and `CONS_0012` are included in checker-backed consistency
- `CONS_0007` and `CONS_0012` are excluded from first-pass `GM_Speedup`
- CONS remains semantic / correctness analysis only in the current runtime packet

## 4. Table A: Correctness / Validity

| route | execution scope | executable rate | result consistency rate | negative rejection / false accept | checker mode | claim boundary |
|---|---|---:|---:|---|---|---|
| `NATIVE_IDENTITY` | full control denominator | `1.0` | `1.0` as control reference | n/a | existing case-local control checker artifacts | control reference only |
| `HUMAN_REFERENCE_POSITIVE` | full control denominator | `1.0` | `1.0` within control scoring | n/a | existing case-local control checker artifacts | positive-control rewrite, not generated-method route |
| `HARD_NEGATIVE_GUARD` | full control denominator | `1.0` | n/a | negative rejection `1.0`, false accept `0.0` | existing case-local control checker artifacts | guard / rejection route only |
| `SQLGLOT_OPT_SAME_DIALECT` | full 9-case common-core | `1.0` | `1.0` | n/a | `exact_tsv_report_local` | generated-method checker-backed consistency only |
| `LLM_DIRECT_REWRITE_STRONG` | full 9-case common-core | `1.0` | `1.0` | n/a | `exact_tsv_report_local` | generated-method checker-backed consistency only |

## 5. Table B: PERF-Only Speedup

| route | denominator | GM_Speedup | Win / Tie / Loss | RegressionRate@20% | token usage | claim boundary |
|---|---|---:|---|---|---|---|
| `HUMAN_REFERENCE_POSITIVE` | PERF-only `7` cases | `0.96159127168004` | `1 / 2 / 4` | `0 / 7` | n/a | positive-control speedup only |
| `SQLGLOT_OPT_SAME_DIALECT` | PERF-only `7` cases | `0.9709643241218479` | `1 / 2 / 4` | `0 / 7` | n/a | correctness-gated PERF-only generated-method speedup, not full leaderboard |
| `LLM_DIRECT_REWRITE_STRONG` | PERF-only `7` cases | `1.0023345046000625` | `1 / 5 / 1` | `0 / 7` | `4487` total, `641.0` per executed case | correctness-gated PERF-only generated-method speedup, not full leaderboard |

## 6. Table C: Plan Observability

| area | result |
|---|---|
| source plans parseable | `9 / 9` |
| human positive plans parseable | `9 / 9` |
| hard negative plans parseable | `9 / 9` |
| SQLGlot method plans parseable | `9 / 9` |
| Direct LLM method plans parseable | `9 / 9` |
| source-positive pair ready | `9 / 9` |
| source-negative pair ready | `9 / 9` |
| source-SQLGlot pair ready | `9 / 9` |
| source-LLM pair ready | `9 / 9` |
| source-positive top-node changed | `2 / 9` |
| source-negative top-node changed | `2 / 9` |
| source-SQLGlot top-node changed | `0 / 9` |
| source-LLM top-node changed | `1 / 9` |
| attribution status | not computed |
| speedup attribution status | not computed |

Interpretation:

- plan parse readiness is closed for all common-core roles
- pair readiness is closed for all source-to-candidate comparisons used in the current packet
- operator delta is available as a lightweight structural observation layer only
- operator delta is not attribution

## 7. Boundary / Non-Claim Table

| boundary | status |
|---|---|
| full benchmark leaderboard | not claimed |
| registry writeback | not performed |
| common-core admission | not performed |
| formal review update | not performed |
| PERF-only speedup as full suite speedup | not claimed |
| CONS included in `GM_Speedup` | excluded |
| operator delta as attribution | not claimed |
| PORT mixed into this closeout | excluded; PORT remains separate |

## 8. Remaining Work

- PORT formal expansion and `PORT_0012` decision
- RQ4 taxonomy / failure slicing aggregation
- attribution design over plan-operator evidence
- final leaderboard packaging
- protocol-level review and admission decisions

## 9. Recommended Next Action

- move to RQ4 taxonomy / failure slicing aggregation, now that common-core correctness, PERF-only speedup, and plan-observable evidence are closed to a first paper-facing packet

## 10. Verification / Non-Modification Note

- only this closeout document was created
- no SQL execution was performed
- no database workload was run
- no model / LLM call was made
- no SQLGlot generation was run
- no checker execution was run
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
