# R-Bot Actual Run Gate v1

This is the current execution gate for whether `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` may produce benchmark evidence for the `R-Bot` PG1 recovery canary.

## Decision

`actual_pg1_generation_not_allowed_as_current_benchmark_evidence`

## What Changed Relative To The Earlier Gate

This package now adds:

- a retention decision
- a demo policy
- a contamination guard
- an artifact contract

That improves governance, but it still does not fully close the current-evidence gate.

## Gate Outcome

### Allowed now

- a future human-run actual generation may be allowed only as:
  `exploratory_smoke_only_not_current_common_core_metric_evidence`

### Not allowed now

- current Common-core metric evidence
- any leaderboard claim
- any denominator-wide inference

## Remaining Blockers

Exact remaining blockers:

1. retrieval corpus is still `/tmp`-only and not retained as a frozen benchmark substrate
2. `chroma_db` index is still `/tmp`-only and not retained as a frozen benchmark substrate
3. the demo policy is now defined, but the exact retrieval hyperparameters are still not surfaced from a frozen run contract
4. contamination guard is defined, but not yet operationally attested by a run artifact
5. artifact contract is defined, but no actual run has yet produced the required retained artifacts
6. endpoint/provider/base_url logging contract is defined, but no actual run has yet emitted it
7. the observed canary shell still had `OPENAI_API_KEY` visibility set to false

## Conditional Exploratory Allowance

If a human still wants to run the canary before all blockers are closed, the run may proceed only under these boundaries:

- one case only: `PERF_0006`
- PostgreSQL only
- explicit label:
  `exploratory_smoke_only_not_current_common_core_evidence`
- no validity-summary writeback
- no speedup summary writeback
- no leaderboard use

## Conditions Required For Future Current-Evidence Allowance

All of the following must be true:

1. smoke-scoped dependency environment documented and visible at run time
2. upstream clone identity pinned
3. retrieval corpus retained or explicitly frozen through an approved external artifact reference
4. index snapshot retained or explicitly frozen through an approved external artifact reference or deterministic rebuild contract
5. demo policy used by the actual run logged in artifacts
6. contamination exclusion policy attested in artifacts
7. full artifact contract satisfied
8. provider/model/base_url metadata logged without secrets
9. run results preserve the claim boundary and denominator identity

## Final Status

After this package:

- governance readiness improved
- reproducibility documentation improved
- current benchmark execution readiness is still blocked

So the correct current label is:

`exploratory_only_if_human_runs_not_current_metric_evidence`
