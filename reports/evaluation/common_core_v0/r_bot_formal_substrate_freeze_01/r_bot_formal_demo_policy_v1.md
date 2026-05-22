# R-Bot Formal Demo Policy v1

## Role

This document defines the benchmark-facing demo and retrieval-selection policy for future `R-Bot` same-engine generation on the `120`-row Common-core denominator.

It is a freeze plan, not an execution authorization.

## Current State

Current status remains blocked because exact retrieval settings are not yet surfaced from a frozen runner contract.

Specifically unresolved:

- exact `top_k`
- exact threshold if any
- exact reranking/fusion mode if any

## Formal Requirements

Before generation may start, the formal run must freeze and retain:

1. retrieval mode
2. `top_k`
3. threshold if any
4. reranking/fusion mode if any
5. corpus snapshot identity
6. index snapshot identity
7. no-manual-override rule

## Fixed Policy Constraints

The future formal run must obey all of the following:

- same denominator for all rows
- same route definition for all rows
- same frozen retrieval corpus line
- same frozen index line
- no post-target manual demo injection
- no ad hoc corpus edits after seeing target rows
- no case-specific retrieval tuning

## Per-Case Exclusion Policy

For every planned row, retrieval/demo selection must exclude:

- the target row itself
- any exact denominator duplicate
- any normalized near-duplicate denominator row
- benchmark-generated outputs from:
  - SQLGlot
  - Direct LLM
  - Calcite
  - `R-Bot` exploratory recovery packets

## Normalized SQL Hash Policy

Minimum normalized matching basis:

1. trim leading/trailing whitespace
2. collapse repeated whitespace
3. strip trailing semicolons
4. normalize case where safe

Preferred stronger basis later:

- canonical parse-tree or canonical AST normalization

Formal requirement:

- the run package must retain the normalization policy used for exclusion checks

## Current Gate Condition

The formal demo policy is not closed until exact retrieval settings are frozen.

Therefore:

- `top_k = unresolved`
- `threshold = unresolved`
- `reranking_mode = unresolved`
- formal generation start permission: `no`

## Bottom Line

The shape of the benchmark-facing demo policy is now fixed, but the exact retrieval settings are still missing. That missing configuration is a hard blocker for starting `R-Bot @120` generation.
