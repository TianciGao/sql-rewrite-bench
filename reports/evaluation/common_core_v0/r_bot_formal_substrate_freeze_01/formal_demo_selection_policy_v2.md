# Formal Demo Selection Policy v2

## Scope

This document freezes the benchmark-facing demo and retrieval-selection policy shape for formal `R-Bot` same-engine generation on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

It does not authorize generation.

## Current Status

- policy shape: `frozen`
- exact retrieval settings: `still_blocked`
- formal gate impact: `blocked`

## Selection Unit

The retrieval subsystem may select:

- rewrite rules
- retrieval examples
- both, if the frozen runner contract uses both

Every selected item must come from the frozen retained corpus line only.

## Allowed Retrieval Example Source

Retrieval examples from the StackOverflow-derived corpus are allowed:

- `yes`, in principle
- only from the retained frozen corpus line
- only after denominator exclusions and generated-output exclusions are attested
- only if exact and near-duplicate normalized SQL exclusions are applied

## Prohibited Retrieval Source Classes

The retrieval/demo pool must exclude:

1. all `common_core_v0_40` denominator source SQL
2. any exact denominator duplicate
3. any normalized near-duplicate denominator SQL found by the chosen normalization policy
4. benchmark-generated SQL from:
   - SQLGlot
   - Direct LLM
   - Calcite
   - `R-Bot` exploratory recovery canaries

## Normalized SQL Exclusion Policy

Minimum normalization basis:

1. trim leading and trailing whitespace
2. collapse repeated whitespace
3. strip trailing semicolons
4. normalize case where safe

Required exclusion checks:

- exact normalized match exclusion: `required`
- near-duplicate normalized SQL exclusion: `required`

Current attestation state:

- exact match checked: `not yet machine-attested`
- near duplicate checked: `not yet machine-attested`

If actual normalized hash checking cannot be completed from retained artifacts, the row status must remain:

- `blocked_pending_hash_check`

## Manual Override Policy

Forbidden:

- manual retrieved-example swapping after target inspection
- manual prompt tuning to rescue a specific row without creating a new formal experiment version
- case-specific rule injection
- reuse of benchmark-generated SQL as retrieval demos

Allowed:

- deterministic retrieval from the frozen corpus under one benchmark-wide policy

## Retrieval Settings Freeze Boundary

Already frozen:

- rule-vector width `100`
- total dimension `3172 = 1536 + 100 + 1536`
- current `/tmp` scratch index is not formal evidence and must be rebuilt

Still blocked:

- exact `top_k`
- exact reranking mode
- exact similarity threshold or explicit none
- exact embedding model identity attestation for the rebuild line

## Gate Outcome

The demo-selection policy is now structurally frozen, but the retrieval/demo/contamination gate remains closed until:

1. retrieval settings are fully frozen
2. all 40 denominator rows have machine-readable contamination attestation status
3. generated-output exclusions are attested

## Bottom Line

StackOverflow retrieval examples are allowed only from the frozen retained corpus, and only after denominator, exact-match, near-duplicate, and generated-output exclusions are attested.

Formal `R-Bot @120` generation remains blocked.

