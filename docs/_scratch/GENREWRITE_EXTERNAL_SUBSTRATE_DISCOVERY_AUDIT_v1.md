# GENREWRITE_EXTERNAL_SUBSTRATE_DISCOVERY_AUDIT_v1

## 0. Purpose And Boundary
This is a discovery and substrate audit only. It does not execute GenRewrite, does not call any model/API, does not run any database, and does not attempt checker or speedup evaluation.

## 1. Local Evidence Recap
Current repo-local GenRewrite state remains readiness-only:
- readiness scaffold exists
- no repo-local GenRewrite runner exists
- no correction loop exists
- no verifier/checker feedback loop exists
- no executor-feedback loop exists
- no rerank or n-best path exists
- no prompt/rule library exists
- no output SQL contract is implemented as runnable code

Key local evidence:
- [docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md)
- [docs/_scratch/GENREWRITE_MANUAL_ACQUISITION_CHECKLIST_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/GENREWRITE_MANUAL_ACQUISITION_CHECKLIST_v1.md)
- [docs/_scratch/PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1.md)
- [reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json)

## 2. Public / External Discovery
Search terms used:
- `GenRewrite SQL rewrite LLM counterexample correction`
- `GenRewrite database query rewrite`
- `GenRewrite natural language rewrite rules SQL`
- `"GenRewrite" SQL`
- `"GenRewrite" "rewrite" "SQL"`
- `2403.09060 GenRewrite GitHub`
- `site:github.com "GenRewrite" SQL rewrite`

Observed external results:
- paper page: `https://huggingface.co/papers/2403.09060`
- paper summary: `https://www.emergentmind.com/articles/2403.09060`
- survey/list references that mention the paper but do not expose an upstream runnable repo

GitHub repository discovery result from this audit:
- no plausible public GenRewrite source repository was returned by GitHub repository search
- no candidate source URL was strong enough to justify clone inspection

Clone status:
- clone attempted: no
- clone success: no
- candidate repo path: none

Why the external hits do not yet count as substrate:
- they identify the paper and method concept
- they do not expose a runnable repository, artifact bundle, prompt/rule package, or correction-loop implementation
- they do not surface a reproducible input/output contract or output SQL artifact path

## 3. Candidate Repository Inventory
No public runnable GenRewrite substrate was found from this audit.

Therefore the following remain not recoverable from public code in this pass:
- README for an upstream runnable repo
- LICENSE for runnable code
- requirements/runtime file
- scripts or entrypoints
- prompts/rules
- correction loop
- checker/executor feedback contract
- output SQL path
- model/API dependency contract
- runnable examples or demos

## 4. RewriteBench Mapping Feasibility
For `PERF_0006`, only the high-level conceptual mapping is visible:

Source SQL mapping:
- likely possible in principle because RewriteBench already has `source.sql`

Schema mapping:
- likely possible in principle because RewriteBench already has `schema/ddl_pg.sql`

Prompt/rule mapping:
- blocked because no external prompt/rule library was recovered

Feedback-loop mapping:
- blocked because no public correction loop, verifier/checker feedback loop, or executor-feedback loop was recovered

Output SQL capture:
- blocked because no public runnable substrate shows where final candidate SQL is emitted

Checker handoff:
- blocked until a real final SQL output contract exists

Current blockers before any bounded smoke:
- no public runnable entrypoint
- no correction loop implementation
- no verifier/checker feedback loop
- no executor feedback loop
- no prompt/rule library
- no rerank or n-best path
- no output SQL artifact contract
- no dependency/runtime package for a runnable substrate
- no visible license/redistribution status for runnable code artifacts

## 5. Classification
`no_public_substrate_found`

Justification:
- repo-local evidence still shows readiness scaffolding only
- external discovery surfaced paper pages and survey references, but not a runnable upstream repository or artifact package
- without a public substrate, adapter preflight would be speculative and would invent missing method behavior

## 6. Recommended Next Step
`perform deeper manual acquisition search`

Reason:
- the paper and method identity are visible, so the line is not purely fictional
- however this audit did not recover a runnable public substrate
- the next step should be targeted manual acquisition of an upstream repo, artifact bundle, prompt/rule package, or author-released reproducibility material before any adapter or execution discussion

## 7. Non-Modification Note
This audit was read-only except for the scratch note and `/tmp` audit JSON.

Confirmed:
- no execution
- no model/API calls
- no DB activity
- no package install
- no checker
- no speedup
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
