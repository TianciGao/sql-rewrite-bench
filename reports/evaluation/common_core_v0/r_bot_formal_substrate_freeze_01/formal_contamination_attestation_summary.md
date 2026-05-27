# Formal Contamination Attestation Summary

## Scope

This summary covers the machine-readable contamination attestation package for:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Current Status

- denominator rows covered in CSV: `40`
- rows passed: `0`
- rows blocked: `40`
- attestation package complete enough to open gate: `no`

## What Is Now Defined

The package now records, for each of the 40 denominator cases:

- case ID
- pool
- whether a normalized source hash is actually available
- whether exclusion from retrieval is attested or only policy-defined
- whether exact-match exclusion was actually checked
- whether near-duplicate exclusion was actually checked
- whether generated-output exclusions are attested
- row-level status
- exact blocker reason

## Why Every Row Remains Blocked

Every row remains:

- `blocked_pending_hash_check`

Because the current package still lacks:

1. retained normalized source hashes for the denominator cases
2. machine-readable exact-match exclusion results
3. machine-readable near-duplicate exclusion results
4. machine-readable generated-output exclusion attestation

## Policy Claims That Are Defined But Not Yet Attested

Policy-defined exclusions exist for:

- all 40 denominator source SQL rows
- exact normalized duplicates
- near-duplicate normalized SQL
- generated SQL from SQLGlot
- generated SQL from Direct LLM
- generated SQL from Calcite
- generated SQL from `R-Bot` PG1 recovery canaries

Those policy claims do not count as passed contamination evidence until the corresponding checks are actually retained in machine-readable form.

## Gate Outcome

- contamination gate open: `no`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The contamination package is now structurally complete at the row-definition level, but all 40 rows remain blocked pending actual normalized-hash and duplicate-check evidence.

