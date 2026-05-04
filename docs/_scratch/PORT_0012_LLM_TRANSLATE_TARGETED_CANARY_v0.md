# PORT_0012_LLM_TRANSLATE_TARGETED_CANARY_v0

## 1. Status

This is a tracked scratch note for the targeted `PORT_0012` Direct LLM translate canary.

The targeted canary command was implemented and run.

The current execute-path result is blocked by missing model/API environment.

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
- provider mode: `env_blocked`
- model call attempted: `false`
- model call status: `env_blocked`
- extraction status: `not_available`

Reason:

- no visible `OPENAI_API_KEY` or `LLM_API_KEY` was available in the execution shell

## 5. Token Usage

- `token_usage_total=null`

No token usage was recorded because no model call was made.

## 6. Execution Result

- PostgreSQL execution status: `not_attempted`
- row count: `null`
- runtime: `null`
- failure category: `missing_api_key`

Interpretation:

- this targeted canary did not generate or execute a candidate SQL translation
- the current result is a bounded blocked-state artifact, not a successful or failed translation execution result

## 7. Current Interpretation

Current interpretation is conservative:

- this run does not show whether Direct LLM translate can repair the SQLGlot identifier-literal failure on `PORT_0012`
- it only shows that the targeted canary path is now scaffolded and that the current shell lacked model/API environment
- `PORT_0012` therefore remains a failure-analysis / targeted stress case rather than a clean denominator case

## 8. Claim Boundaries

- not full PORT closure
- not translation correctness
- not cross-engine matrix
- PostgreSQL only
- one-case targeted stress canary
- blocked by missing model/API env in the current execution shell

## 9. Recommended Next Action

- rerun the targeted `PORT_0012` Direct LLM translate canary only after a bounded model/API environment is available in the same execution shell
