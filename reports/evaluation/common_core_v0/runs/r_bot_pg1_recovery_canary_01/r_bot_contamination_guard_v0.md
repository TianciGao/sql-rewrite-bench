# R-Bot Contamination Guard v0

This document defines the minimum contamination guard for any future `R-Bot` PG1 actual generation canary on `PERF_0006 / pg`.

It is a guardrail artifact only.

## Core Rule

No future actual run may be treated as current Common-core evidence if retrieval can see:

- the target case itself
- frozen-denominator near-duplicates
- prior benchmark-generated SQL outputs
- post-hoc hand-tuned demos derived from benchmark outcomes

## Excluded Sources

The retrieval substrate must exclude:

1. `common_core_v0_40` case-local benchmark artifacts
2. prior RewriteBench-generated outputs from:
   - SQLGlot
   - Direct LLM
   - Calcite HEP
   - any future `R-Bot`, `LearnedRewrite`, or `LLM-R2` benchmark runs
3. manual per-case demo files created after observing target-case outcomes

Interpretation:

- verifier/support artifacts are not rewrite baselines and must not be repurposed as retrieval demos either

## Case-ID Exclusion Policy

At minimum, exclude retrieval items that correspond to:

- `PERF_0006`
- any row in the frozen `common_core_v0_40` denominator if a mapping into the retrieval corpus can be established

Policy stance:

- if exact case IDs are not available inside the external corpus, normalized SQL matching must be used

## Hash / Normalized SQL Matching Policy

The future run should apply the strongest practical exclusion available.

Minimum acceptable exclusion logic:

1. exact text match after:
   - trimming leading/trailing whitespace
   - collapsing repeated whitespace
   - stripping trailing semicolons
2. normalized SQL match using the same normalization basis for:
   - target source SQL
   - known benchmark-produced generated SQL

Preferred stronger logic if available later:

- canonical parse-tree or normalized AST match

This task does not implement that matcher. It only freezes the policy requirement.

## Old Benchmark Outputs

Old benchmark outputs must not be retrievable.

That includes generated SQL from:

- SQLGlot optimize/transpile same-engine lines
- Direct LLM same-engine rewrite
- Calcite HEP PG40 rewrite
- bounded historical `R-Bot` smoke outputs
- bounded historical `LLM-R2` or `LearnedRewrite` smoke outputs

Reason:

- these are evaluation outputs, not allowed retrieval substrate

## Near-Duplicate Policy

If the external corpus contains a SQL text that is not byte-identical to `PERF_0006` but is a formatting or minor alias variant of the same query intent, it must still be excluded from retrieval for current benchmark evidence.

If that exclusion cannot be guaranteed, the run remains exploratory only.

## Manual Override Policy

Forbidden:

- manually editing the retrieved example set after inspecting `PERF_0006`
- manually swapping in “better” examples for a rerun without declaring a new experiment version
- editing prompts or rules to target `PERF_0006` specifically after seeing failure output

## Minimum Attestation Required Before Current Evidence

Before a future run can be called current evidence, a human-readable or machine-readable attestation must exist stating:

- frozen denominator ID
- excluded benchmark output classes
- target-case exclusion policy
- duplicate/near-duplicate exclusion policy
- manual tuning prohibition

Without that attestation, any actual run remains exploratory.

## Current Decision

This contamination guard is now defined, but not yet proven operationally enforced by a future run.

So the current status remains:

`guard_defined_but_not_yet_executed_or_attested_in_run_artifacts`
