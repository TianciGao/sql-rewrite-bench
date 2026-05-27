# Failure Bucket Policy For Rerun v1

This is a reviewable Stage-0 failure-accounting draft for future
`common_core_v0_40_same_engine_120` reruns.

It does not change checker policy.
It does not change denominator policy.
It does not create a leaderboard.

## Core Principles

- No failed row is dropped from the `120`-row denominator.
- No unsupported row is dropped from the `120`-row denominator.
- No no-op row is silently counted as success without explicit policy.
- Timing denominator is a subset unless it is explicitly proven to be
  full-denominator.
- `leaderboard_comparable` remains `no` unless later policy and
  full-denominator evidence explicitly support `yes`.

## Required Buckets

| bucket | meaning | remains in denominator | counts as exact | can enter timing denominator | notes |
|---|---|---|---|---|---|
| `planned` | row exists in the frozen rerun manifest and is part of the intended denominator | `yes` | `no` | `no` | every manifest row starts here before route outcomes are assigned |
| `generated` | route produced a candidate SQL artifact or route output intended for execution | `yes` | `no` | `no` | generation alone is not correctness |
| `unsupported` | row is explicitly unsupported by route, engine, or scope contract | `yes` | `no` | `no` | unsupported rows remain visible and are not silently removed |
| `parse_failed` | route or wrapper failed before candidate execution because parsing or ingestion failed | `yes` | `no` | `no` | parser failures remain explicit in denominator accounting |
| `generation_failed` | route attempted generation but did not produce executable candidate SQL | `yes` | `no` | `no` | includes route failures distinct from parse failures |
| `noop_generated` | candidate output is effectively source-like or policy-defined no-op | `yes` | `no` | `no` unless later explicitly timing-eligible by policy | no-op behavior must remain explicit and not be silently scored as useful rewrite success |
| `execution_failed` | source and candidate did not both complete successful execution under the retained checker contract | `yes` | `no` | `no` | execution failure is distinct from mismatch |
| `mismatch` | source and candidate executed, but exact or checker-consistent result validation failed | `yes` | `no` | `no` | mismatch rows are correctness-validity failures, not executability failures |
| `exact_match` | source and candidate executed and matched exactly under the retained checker contract | `yes` | `yes` | `yes` if timing policy allows | this is the only correctness-success bucket in the current fail-closed policy |
| `timing_missing` | row is correctness-valid but has no retained timing artifact under the declared timing contract | `yes` | `depends_on_correctness_bucket` | `no` | timing absence must remain explicit and blocks full timing comparability |
| `timing_success` | row has retained timing artifact under the declared timing contract | `yes` | `depends_on_correctness_bucket` | `yes` | timing denominator is a subset unless later explicitly closed on all intended rows |
| `methodology_boundary` | row crosses a route or evaluation boundary that must remain explicit rather than normalized away | `yes` | `no` | `no` | examples include out-of-scope portability semantics inside a same-engine campaign |
| `unknown_not_recovered` | required outcome field or retained evidence is missing and cannot be safely recovered | `yes` | `no` | `no` | use only when retained artifacts are insufficient; do not guess |

## Interpretation Boundary

This bucket policy is for future rerun planning and artifact design only.

It does not itself:

- authorize any rerun
- redefine success semantics
- redefine exact-match checking
- turn subset timing into full-denominator timing
- create a leaderboard
