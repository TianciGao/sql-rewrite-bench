# Prior-Method Common-core v0 @40 Preflight

## Scope

This is a read-only feasibility and denominator preflight for these prior methods:

- `calcite_hep`
- `r_bot`
- `learnedrewrite`
- `llm_r2`

It does not run any method, database, SQL execution, timing, or speedup.

## Headline Answer

`common_core_v0_40` full same-engine evaluation is **not currently feasible** for any of the four prior methods.

The strongest currently supportable path is a **bounded PostgreSQL-only performance overlap denominator**, not full `@40` tri-engine evaluation.

## Method-by-method Feasibility

### `calcite_hep`

- Can this method run on all 40 cases: `no`
- Can this method run only on PERF cases: `yes, bounded PG-only subset evidence exists`
- Can this method run only on PG: `yes`
- Does it support MySQL or Spark: `no evidence`
- Does it need adapter work: `yes` for any extension beyond the historic subset; existing overlap evidence is already strong
- Does it already have candidate SQL outputs: `not preserved as repo-local SQL files, but checker/timing-backed PG artifacts exist`
- Does it already have checker-consistent outputs: `yes` on `9` current-overlap PERF PG cases
- Does it already have timing outputs: `yes` on the same overlap slice
- Is @40 feasible: `no`
- Safest denominator: `common_core_v0_40_perf_pg9_overlap`

Interpretation:
- Calcite HEP is the only prior method with strong repo-local checker and timing evidence that overlaps the current frozen denominator.
- Its historic `prior_method_pg10` slice included `PERF_0063`, which is not in `common_core_v0_40`; the current overlap is therefore `9`, not `10`.

### `r_bot`

- Can this method run on all 40 cases: `no`
- Can this method run only on PERF cases: `historically yes on a bounded PG-only subset`
- Can this method run only on PG: `historically yes`
- Does it support MySQL or Spark: `no evidence`
- Does it need adapter work: `yes, plus retrieval corpus / demo policy / rule-pool recovery`
- Does it already have candidate SQL outputs: `historical smoke evidence exists, but repo-local candidate SQL artifacts are not preserved here`
- Does it already have checker-consistent outputs: `yes on 6/9 current-overlap PERF PG cases; 1 checker failure and 2 generation failures remain visible`
- Does it already have timing outputs: `yes for the correctness-gated nontrivial overlap-compatible subset`
- Is @40 feasible: `no`
- Safest denominator: `prior_method_pg10` remains the current historical denominator; next common-core-compatible target is `common_core_v0_40_perf_pg9_overlap_after_retrieval_stack_recovery`

### `learnedrewrite`

- Can this method run on all 40 cases: `no`
- Can this method run only on PERF cases: `historically yes on a bounded PG-only subset`
- Can this method run only on PG: `historically yes`
- Does it support MySQL or Spark: `no evidence`
- Does it need adapter work: `yes, and checkpoint/inference stack recovery is missing`
- Does it already have candidate SQL outputs: `historical smoke evidence exists, but repo-local candidate SQL artifacts are not preserved here`
- Does it already have checker-consistent outputs: `yes on 9/9 current-overlap PERF PG cases`
- Does it already have timing outputs: `only on the non-noop subset; most historical outputs were source-like/no-op`
- Is @40 feasible: `no`
- Safest denominator: `prior_method_pg10` remains the safest denominator until artifacts are recovered; next common-core-compatible target is `common_core_v0_40_perf_pg9_overlap_after_adapter_checkpoint_recovery`

### `llm_r2`

- Can this method run on all 40 cases: `no`
- Can this method run only on PERF cases: `historically yes on a bounded PG-only subset`
- Can this method run only on PG: `historically yes`
- Does it support MySQL or Spark: `no evidence`
- Does it need adapter work: `yes, runner/logical-plan/extraction path recovery`
- Does it already have candidate SQL outputs: `historical smoke evidence exists, but repo-local candidate SQL artifacts are not preserved here`
- Does it already have checker-consistent outputs: `yes on 9/9 current-overlap PERF PG cases`
- Does it already have timing outputs: `yes on the same bounded PG-only subset`
- Is @40 feasible: `no`
- Safest denominator: `prior_method_pg10` remains the current historical denominator; next common-core-compatible target is `common_core_v0_40_perf_pg9_overlap_after_runner_recovery`

## Common-core v0 @40 Interpretation

### Can any prior method run on all 40 cases now

No.

Reasons:
- all four methods are effectively `PERF`-only in the current evidence
- all four methods are PostgreSQL-only in the current evidence
- none has MySQL or Spark route evidence compatible with `common_core_v0_40`
- the non-Calcite methods currently lack a runnable repo-local substrate even for bounded rerun

### Can any prior method run only on PERF cases

Yes, but only as a bounded PG-only slice.

The safest common-core-aligned first-wave denominator is:
- `common_core_v0_40_perf_pg9_overlap`
- case IDs: `PERF_0006, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0052, PERF_0054`

This is smaller than the historic `prior_method_pg10` because `PERF_0063` is not part of the frozen `common_core_v0_40` denominator.

## Blockers

- `calcite_hep`: extension blocker, not substrate blocker; needs explicit PG PERF expansion beyond the current overlap slice
- `r_bot`: retrieval corpus, demo-selection policy, contamination/fair-comparison contract, and runnable repo-local control stack are missing
- `learnedrewrite`: adapter, checkpoint, and inference entrypoint are missing; historical behavior also carries a dominant noop/source-like profile
- `llm_r2`: runner recovery is needed, plus the historical logical-plan/extraction scaffolding must be made repeatable in-repo
- all four methods: no MySQL support, no Spark support, no same-engine tri-engine common-core path today
- all four methods: no evidence on `CONS`, `PORT`, or `LONGTAIL` cases under the current protocol

## Recommended Execution Order

1. `calcite_hep`
2. `llm_r2`
3. `r_bot`
4. `learnedrewrite`

Reasoning:
- `calcite_hep` has the strongest repo-local PG overlap evidence and the least substrate uncertainty
- `llm_r2` has the strongest non-Calcite bounded PG overlap evidence once runner recovery is solved
- `r_bot` has useful nontrivial rewrite behavior but larger retrieval/control-stack recovery risk
- `learnedrewrite` is the weakest near-term candidate because the current repo lacks artifacts and the historical subset is mostly noop-like

## Recommendation

Treat this as a **denominator-definition preflight**, not as readiness to launch all prior methods on `common_core_v0_40`.

The safest next experiment is:
- start with `calcite_hep` on `common_core_v0_40_perf_pg9_overlap`
- if that closes cleanly, decide whether to extend Calcite HEP to the remaining `PERF` PostgreSQL cases
- only then consider recovering `llm_r2`, `r_bot`, and `learnedrewrite` on the same overlap denominator
