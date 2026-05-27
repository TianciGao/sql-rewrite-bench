# Formal Artifact Contract Validation Plan

## Scope

This plan defines how the future formal `R-Bot` run package must be validated against the benchmark artifact contract before any row can count as current evidence.

Target scope:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Required Run Artifacts

The future formal run package must retain, for each planned row or for benchmark-wide shared context where appropriate:

1. generated SQL
2. selected rules
3. retrieval trace
4. prompt
5. raw response
6. token/cost/provider metadata
7. environment snapshot
8. run results

## Validation Rules

Generated SQL:

- must exist at the contract path for every planned row that was actually attempted
- must not be manually edited after generation
- must remain denominator-aware, meaning unsupported or failed rows still remain represented in `run_results`

Selected rules:

- must exist in machine-readable form
- must identify which rules/examples were selected for each row

Retrieval trace:

- must show retrieval mode, `top_k`, threshold if any, and reranking mode if any
- must link back to the frozen corpus/index identifiers

Prompt and raw response:

- must exist separately
- must permit audit of SQL extraction policy without exposing secrets

Token/cost/provider metadata:

- must record provider name, base URL family, and model name
- must not expose API keys or equivalent secrets

Environment snapshot:

- must record Python/runtime metadata and dependency lock identity
- must tie back to the pinned upstream commit

Run results:

- must preserve the full `120`-row denominator accounting
- must not silently drop unsupported or failed rows

## Current Blockers Against Validation

The validation plan itself is now defined, but actual validation remains blocked because:

1. no formal run package exists yet
2. no rebuilt formal index identifier exists yet
3. retrieval settings are still not fully frozen
4. contamination attestation rows are all still blocked
5. runtime lock is still candidate-only

## Gate Rule

The artifact contract is not satisfied by policy documents alone.

Formal `R-Bot @120` generation remains blocked until a future retained run package can satisfy every required artifact class above.

