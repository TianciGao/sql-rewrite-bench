# R-Bot Demo Policy v0

This document defines the bounded demo and retrieval policy for the `R-Bot` `PERF_0006 / pg` recovery canary.

It is a policy freeze artifact only.
It does not authorize execution by itself.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- current use: policy definition for any future PG1 canary actual generation attempt

## Current Policy State

Before this file, demo policy was `not_frozen`.

After this file:

- the intended policy shape is frozen
- but execution is still blocked by contamination and substrate gates

## Core Policy

### Retrieved examples are allowed only under bounded canary rules

Any future PG1 actual generation may use retrieved examples only if the retrieval corpus and index snapshot are the ones named in the freeze manifest and remain within the contamination guard defined separately.

This means:

- no ad hoc change of corpus after looking at `PERF_0006`
- no case-specific manual demo injection after inspecting outcomes
- no mixing of unnamed scratch corpora into the actual run

## Retrieval Selection Policy

### Selection mechanism

The future actual run must use the upstream retrieval/index path that is pinned for this canary.

Known current substrate facts:

- retrieval substrate is Chroma-backed
- corpus comes from `LLM4Rewrite` knowledge/rule assets and `stackoverflow-rewrite-embed.zip`

### Top-k / similarity settings

Current exact `top_k` and similarity hyperparameters are not recoverable with high confidence from the allowed read set.

Therefore the frozen policy is:

- do not claim exact `top_k` or exact similarity threshold unless surfaced by the actual runner command or pinned config at run time
- the actual run must record:
  - retrieval mode
  - top-k
  - any fusion or reranking mode
  - any threshold if applied

Until that record exists, the canary remains exploratory only.

### Determinism rule

The future actual run must preserve:

- one fixed retrieval corpus snapshot
- one fixed index snapshot
- one fixed runner/config snapshot
- no manual override of retrieved examples after target inspection

If the upstream stack contains nondeterministic ordering, the run must still log the selected-rules and retrieval-trace artifacts so the exact observed retrieval can be audited.

## Use Of Retrieved Examples In PG1 Actual Generation

Current decision:

- retrieved examples may be used only under exploratory-canary conditions
- they may not yet support current benchmark metric evidence

Reason:

- the contamination guard is still a separate blocking gate
- the exact retrieval hyperparameters are not yet surfaced as frozen benchmark-side parameters

## Common-core Contamination Avoidance

To avoid training/test contamination against `common_core_v0_40`:

1. `PERF_0006` itself must be excluded from retrieval if it or its exact source SQL appears in the retrieval corpus.
2. Any exact or near-duplicate SQL for frozen denominator rows must be excluded from retrieval.
3. Any benchmark-produced candidate SQL outputs must be excluded from retrieval.
4. Any post-hoc manual demo tuning after seeing `PERF_0006` outcomes is forbidden.

## PERF_0006 And Near-Duplicate Exclusion

Policy:

- exact `PERF_0006` source SQL must not be used as a retrieved example
- normalized near-duplicates of `PERF_0006` must also be excluded if detected

Minimum normalized matching basis:

- trim whitespace
- lowercase SQL keywords and identifiers where normalization is safe
- collapse repeated whitespace
- strip trailing semicolons

If a stronger AST-level or canonicalized-SQL match is available later, it should be preferred, but this policy does not require implementing that matcher now.

## Required Logging At Actual Run Time

If a later run is attempted, it must log:

- retrieval corpus identity
- index snapshot identity
- retrieval mode
- top-k as actually used
- selected rules
- retrieval trace
- prompt text
- provider/model/base_url metadata without secrets

Without those logs, the run may not be treated as current benchmark evidence.

## Current Decision Boundary

This policy file is enough to forbid the most obvious contamination and post-hoc tuning paths.

It is not enough by itself to authorize current-evidence PG1 actual generation.

Current status:

`exploratory_only_if_run_before_all_other_gates_close`
