# R-Bot Formal Contamination Attestation Plan

## Role

This document defines the exact attestation content required before future `R-Bot` same-engine generation may count as current benchmark evidence.

## Required Attestation Claims

The formal attestation must explicitly state:

1. frozen denominator ID:
   `common_core_v0_40_same_engine_120`
2. target-case exclusion policy
3. denominator near-duplicate exclusion policy
4. benchmark-generated output exclusion policy
5. normalized SQL hash policy
6. no manual post-outcome demo tuning policy

## Excluded Retrieval Classes

The attested exclusion set must include:

- all rows from the frozen Common-core v0 denominator
- benchmark-generated outputs from SQLGlot
- benchmark-generated outputs from Direct LLM
- benchmark-generated outputs from Calcite
- benchmark-generated outputs from `R-Bot` exploratory recovery canaries

Interpretation:

- evaluation outputs are not valid retrieval demos

## Normalized SQL Matching Rule

Minimum acceptable policy:

- exact text match after whitespace normalization and trailing-semicolon stripping
- normalized SQL matching for denominator rows and known generated outputs

Preferred stronger policy:

- canonical parse-tree or AST-based matching

## Manual Override Prohibition

The attestation must forbid:

- manual retrieved-example swapping after target inspection
- manual prompt tuning to rescue a specific failed case without declaring a new experiment version
- reusing benchmark-generated SQL as a retrieval demo source

## Required Attestation Outputs

Before generation may start, the formal package should contain either:

- one human-readable attestation file, and
- one machine-readable attestation summary

At minimum, those artifacts must record:

- denominator ID
- excluded source classes
- normalization basis
- manual-override prohibition
- attesting package identity

## Current Status

Current status remains:

- contamination guard concept exists
- formal benchmark-facing attestation artifact does not yet exist

Therefore:

- formal gate impact: `blocked`

## Bottom Line

No `R-Bot @120` formal generation should start until a contamination attestation package exists and is linked into the formal run gate.
