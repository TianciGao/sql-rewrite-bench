# Common-core 120 Recovery Priority Decision v1

This is a human-approved rerun-campaign priority decision for the
`common_core_v0_40_same_engine_120` campaign.

It is:

- not a leaderboard
- not admission
- not a benchmark rule change
- not a checker-policy change
- not a denominator-policy change
- not an update to `method_comparison_summary_v2`

## Current method situation

### R-Bot

R-Bot has reconciled mixed-scope retained evidence and should not be pursued
for full `120` immediately.

The retained packet now fixes the status boundary:

- attempted `120` generation
- PG40 generation expansion
- PG15 execution/timing subset
- MySQL/Spark canary failures explicit
- not full `120` execution/timing
- not leaderboard comparable

### LearnedRewrite

LearnedRewrite is dependency-blocked due to missing:

- adapter
- checkpoint
- inference stack

It is therefore deferred unless those artifacts are provided.

### LLM-R2

LLM-R2 is also dependency-blocked, but it is the highest-priority recovery
candidate.

The current human-approved rationale is:

- historical PG10 evidence is stronger than LearnedRewrite
- the missing pieces are runner / logical-plan / output-extraction /
  reproducibility recovery
- this is narrower than full adapter / checkpoint / inference recovery

## Final recovery priority order

1. `llm_r2` recovery
2. `r_bot` no further full-`120` pursuit for now; retain as mixed-scope
   evidence
3. `learnedrewrite` deferred unless external artifacts are provided

## Next gate for LLM-R2

Create an LLM-R2 recovery plan for:

- runner
- logical-plan
- output-extraction
- reproducibility

Boundary:

- no generation until a human approves the recovery plan

## Explicit non-claims

- this decision does not authorize generation
- this decision does not authorize execution
- this decision does not create new benchmark evidence
- this decision does not create a leaderboard
- this decision does not promote any method into leaderboard-comparable status
- this decision does not update `method_comparison_summary_v2`
