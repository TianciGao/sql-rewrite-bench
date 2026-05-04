# PORT_0012_LLM_TRANSLATE_TARGETED_CANARY_v0

## 1. Status

This is a tracked scratch note for the targeted `PORT_0012` Direct LLM translate canary.

The targeted canary command was implemented and run.

The latest targeted execute-path result is successful on PostgreSQL for this one-case canary.

## 2. Why `PORT_0012` Was Targeted

`PORT_0012` is the current formal PORT holdout failure-analysis / stress case.

It was selected because:

- SQLGlot transpile parse + generation succeeded
- SQLGlot PostgreSQL execution failed on a concrete translation failure
- the case is useful for checking whether a bounded Direct LLM translate route can avoid the same identifier / datetime failure pattern

This was a one-case targeted canary only.

## 3. SQLGlot Failure Recap

Current SQLGlot failure recap:

- case: `PORT_0012`
- route: `SQLGLOT_TRANSPILE`
- preflight parse + transpile: success
- PostgreSQL execution: failed
- failure category: `InvalidDatetimeFormat`

Observed failure mechanism:

- quoted identifiers such as `"birthday"` were converted into string literals such as `'birthday'`
- PostgreSQL then rejected `CAST('birthday' AS TIMESTAMPTZ)`

Tracked failure buckets remain:

- quoted identifier vs string literal confusion
- datetime / timestamp formatting
- dialect normalization failure
- portability translation failure

## 4. LLM Translate Targeted Result

Targeted canary output:

- route: `LLM_DIRECT_TRANSLATE`
- case: `PORT_0012`
- model label: `gpt-5.2`
- model call attempted: `true`
- model call status: `success`
- extraction status: `extracted`

## 5. Token Usage

- `token_usage_total=480`

## 6. Execution Result

- PostgreSQL execution status: `success`
- row count: `1`
- runtime: `63 ms`
- failure category: `none`

Interpretation:

- this targeted canary generated one extracted SQL candidate and executed it successfully on PostgreSQL
- this suggests the targeted LLM path avoided the SQLGlot identifier-literal / datetime failure in this one-case stress canary

## 7. Current Interpretation

Current interpretation is conservative:

- this run suggests Direct LLM translate can avoid the SQLGlot identifier-literal / datetime failure on `PORT_0012` in this targeted canary
- this is still not translation correctness
- this is still not full PORT closure
- this is still not a cross-engine matrix result
- `PORT_0012` therefore remains a failure-analysis / targeted stress case rather than a clean denominator case

## 8. Claim Boundaries

- not full PORT closure
- not translation correctness
- not cross-engine matrix
- PostgreSQL only
- one-case targeted stress canary
- not a denominator expansion decision

## 9. Recommended Next Action

- decide separately whether targeted `PORT_0012` LLM success evidence is strong enough to justify any later denominator-expansion review
