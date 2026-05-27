# GENREWRITE_MANUAL_ACQUISITION_CHECKLIST_v1

## 0. Status

This is a documentation-only manual acquisition checklist for `GenRewrite`.

It is not implementation.
It is not execution.
It is not a runnable-substrate claim.
It is not a registry writeback.
It is not a closeout.

Current repo-local state remains:

- readiness scaffold exists
- bounded first-subset candidates are known
- no repo-local GenRewrite runner exists
- no correction loop exists
- no verifier/checker feedback loop exists
- no executor-feedback loop exists
- no rerank or n-best path exists
- no prompt/rule library exists

## 1. What Exact External Artifacts Are Needed?

### 1.1 Required acquisition targets

The following external artifacts must be identified manually before any implementation or execution discussion:

1. source repo
   - exact upstream repository or archived source package for the GenRewrite system
   - exact repo URL
   - exact branch, commit hash, tag, or release
   - any companion demo or artifact repo if the method is split across multiple packages
2. model/checkpoint files, if any
   - whether the original method uses a hosted model only, a local model only, or an optional checkpoint
   - exact checkpoint names and paths if any model artifact is expected
   - whether the method is prompt-only or requires task-specific tuned artifacts
3. prompt/rule library
   - exact natural-language rewrite rules
   - exact prompt templates
   - exact correction prompts
   - any example pool or fixed system/user prompt contracts
4. correction-loop implementation
   - exact control loop for candidate generation and iterative repair
   - exact round limit
   - exact retry/sample policy
5. verifier/checker feedback loop
   - exact source of counterexamples or checker diagnostics used during correction
   - exact interface between candidate generation and equivalence or correctness feedback
6. executor-feedback loop
   - exact DB execution feedback or runtime feedback contract, if the original method uses it
   - exact boundary between external method behavior and benchmark-local execution/checking
7. rerank or n-best candidate path
   - whether GenRewrite emits one candidate at a time or an n-best list
   - whether ranking uses cost, checker feedback, execution feedback, or LLM self-judgment
8. dependency/runtime contract
   - exact Python or other runtime version
   - exact package list
   - whether local model serving, API access, or additional tools are required
   - whether a DB runtime is required during correction
9. license / redistribution constraints
   - code license
   - prompt/rule redistribution permission
   - model or API license restrictions
   - whether correction traces or prompts may be stored in-repo
10. expected hardware/runtime assumptions
   - CPU-only or GPU-required
   - expected memory/runtime assumptions
   - whether repeated model calls are assumed
   - whether the method assumes always-online API access

### 1.2 Current evidence and current unknowns

Current repo-local evidence:

- `docs/_scratch/baseline_inventory_boss_requirements.csv`
  - describes GenRewrite as:
    - `LLM + natural-language rewrite rules + counterexample correction`
    - representative LLM rewrite with correction loop
    - rough input/output: `Input: SQL + schema + NLR rules + checker/counterexamples; Output: rewritten SQL after correction loop`
    - rough environment: `LLM API/local LLM, prompt/rule library, checker feedback loop, token logging`
- `reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json`
  - `genrewrite_runner_available=false`
  - `correction_loop_available=false`
  - `executor_feedback_loop_available=false`
  - `prompt_rule_library_available=false`
  - `nbest_generation_available=false`
  - `pricing_snapshot_frozen=false`
- `docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md`
  - no correction loop, verifier loop, rerank path, or executor-feedback loop is present

Current unknowns that must be recovered manually:

- exact upstream code location
- exact runnable commit/release
- exact prompt/rule bundle
- exact correction-loop semantics
- exact source of checker/counterexample feedback
- whether executor feedback is mandatory or optional
- whether model artifacts are needed beyond prompts
- exact license boundaries for code, prompts, and models
- whether the original method requires private prompts, private services, or private workload data

## 2. What Input Contract Must Be Recovered?

The following input-contract questions must be answered from the original source before any adapter work:

### 2.1 Core input format

- does GenRewrite accept raw SQL text directly?
- does it require schema text or schema serialization in a fixed prompt format?
- does it require natural-language rewrite rules as a fixed library?
- does it require counterexamples or checker diagnostics as structured feedback?
- does it require execution traces, plans, or runtime statistics?

### 2.2 Context inputs

Must be clarified explicitly:

- whether GenRewrite consumes:
  - SQL text
  - schema
  - query plans
  - cost feedback
  - execution feedback
  - workload context
  - counterexamples
  - natural-language rule libraries
  - external prompt packages
- whether it requires PostgreSQL-specific execution feedback
- whether it requires a verifier or checker loop during generation
- whether it requires DB runtime access during candidate correction
- whether it assumes a particular DB dialect or can remain dialect-agnostic until execution time

### 2.3 Training/prompt/rule dependency

Must be clarified explicitly:

- whether GenRewrite depends on:
  - a released prompt set
  - a rule library
  - demonstrations
  - tuning artifacts
  - private prompts
  - external workload traces
- whether the released method is reproducible without private prompt assets
- whether checker or counterexample generation is part of the method itself or delegated to external tooling

### 2.4 Current best repo-local approximation

The current repo-local readiness materials imply only a partial input understanding:

- likely needed:
  - `source.sql`
  - schema context
  - prompt/rule library
  - checker or counterexample feedback
  - bounded correction policy
- not yet recovered:
  - exact prompt format
  - exact feedback format
  - exact round structure
  - exact requirements for execution feedback during repair

## 3. What Output Contract Must Be Recovered?

The following output-contract questions must be answered from the original source:

### 3.1 Primary outputs

- final rewritten SQL
- whether an n-best candidate SQL list is emitted before final selection
- whether partial candidates or intermediate repairs are emitted

### 3.2 Required trace outputs

- correction trace
- verifier/checker feedback trace
- executor feedback trace, if used
- cost or ranking metadata
- token usage or API-cost metadata if model calls are part of the original method

### 3.3 Failure modes to recover

The acquisition packet should identify exact failure modes such as:

- no candidate generated
- no valid correction produced
- prompt/rule lookup failure
- checker feedback unavailable
- executor feedback unavailable
- round-budget exhausted
- parse failure
- output not convertible to SQL
- cost budget exceeded

### 3.4 RewriteBench-critical output requirement

A hard requirement for later use is:

- the method must eventually yield candidate SQL that can be passed into the existing PostgreSQL checker and speedup pipeline

If the recovered implementation cannot produce SQL text or cannot separate method-side correction from benchmark-side checking, acquisition should not be treated as sufficient for RewriteBench baseline use.

## 4. What RewriteBench Adapter Would Be Required Later?

No adapter should be implemented now.

This section defines only the later adapter boundary that manual acquisition must support.

### 4.1 Case package -> GenRewrite input

Later adapter must map:

- `cases/PERF/<CASE>/source.sql`
- `cases/PERF/<CASE>/schema/ddl_pg.sql`
- any required prompt/rule assets
- any required checker or counterexample input
- any bounded correction policy settings

into the original GenRewrite input contract.

### 4.2 GenRewrite output -> candidate SQL

Later adapter must support one of the following paths:

- direct final rewritten SQL
- n-best list plus deterministic final-selection rule
- correction trace plus deterministic final candidate extraction

### 4.3 Candidate SQL -> existing PostgreSQL checker/speedup pipeline

Later adapter must support:

- writing generated candidate SQL to a reproducible artifact path
- passing that candidate into the existing PostgreSQL checker path
- passing the same candidate into the existing PostgreSQL speedup path
- preserving a clean separation between:
  - GenRewrite method behavior
  - RewriteBench checker behavior
  - RewriteBench execution/runtime behavior

### 4.4 Executor feedback loop boundaries

Later adapter must explicitly define:

- whether GenRewrite itself requests execution feedback
- whether RewriteBench execution logs are fed back into the correction loop
- which execution outcomes count as method input versus benchmark evaluation output
- how to prevent circular dependence where benchmark-local checker behavior becomes part of the method definition

### 4.5 Artifact paths needed for reproducibility

Later reproducibility packet should reserve paths for:

- acquired upstream source snapshot reference
- acquired commit hash or release identifier
- prompt/rule bundle reference
- model/checkpoint reference, if any
- correction-policy config
- generated candidate SQL
- correction trace
- checker/executor feedback trace
- runtime and token/cost metadata
- failure diagnostics

Recommended future artifact categories only:

- `source_snapshot_ref`
- `prompt_rule_bundle_ref`
- `checkpoint_ref`
- `correction_policy_ref`
- `generated_sql`
- `correction_trace`
- `feedback_trace`
- `runtime_and_cost_metadata`
- `failure_log`

### 4.6 Cost/token accounting

If model calls are part of original GenRewrite behavior, later adapter work must preserve:

- input token count
- output token count
- total token count
- correction-round count
- per-round token/cost breakdown if available
- frozen pricing reference used for any derived cost estimate

## 5. What Minimum Bounded Smoke Would Be Allowed After Acquisition?

Only after all required artifacts are acquired and the input/output contracts are recovered:

- denominator: `1-3` cases only
- PostgreSQL-only first
- suggested first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- no registry writeback
- no leaderboard claim
- no full prior-method coverage claim

### 5.1 Why this subset

This subset is already supported by the current readiness scaffold:

- `reports/baseline_smoke/genrewrite_input_cost_readiness_v0.json`
- `docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`

These cases are currently the cleanest first-subset candidates because they are simpler analytical PERF cases and avoid the interval-heavy or more semantically loaded later cases.

### 5.2 Required preflight before any future run

Before any future bounded smoke is even proposed:

- source repo and commit must be pinned
- runnable entrypoint must be recovered
- correction loop must be recovered
- verifier/checker feedback contract must be recovered
- executor-feedback contract must be recovered or explicitly ruled out
- prompt/rule library must be recovered
- dependency/runtime contract must be documented
- output contract must show recoverable candidate SQL
- license status must be clear

### 5.3 Claim boundary for any future smoke

If acquisition succeeds later, the first bounded smoke could support only:

- a bounded PostgreSQL-only GenRewrite substrate smoke
- no registry writeback
- no final baseline coverage claim
- no leaderboard claim
- no full prior-method coverage claim

## 6. Stop Conditions

Stop and classify the acquisition as blocked if any of the following remains unresolved:

- no source repo
- no runnable entrypoint
- no correction loop
- no verifier/checker feedback loop
- no executor-feedback loop
- no prompt/rule library
- no dependency contract
- no output SQL
- requires inaccessible private service, private model, private prompts, or private workload data
- cannot separate GenRewrite method behavior from RewriteBench checker behavior

Additional practical stop conditions:

- correction is described conceptually but no concrete runnable implementation exists
- prompt/rule bundle is only partially published
- executor feedback is mandatory but requires unshareable or non-reproducible infrastructure
- cost behavior cannot be made reproducible because pricing, prompt bundle, or round policy is missing

## 7. Final Decision Tree

Use the following classification after manual acquisition work is completed:

### `acquired_and_runnable`

Use only if all are true:

- source repo identified and pinned
- runnable entrypoint recovered
- correction loop recovered
- verifier/checker feedback loop recovered
- executor-feedback loop recovered or explicitly not required
- prompt/rule library recovered
- dependency/runtime contract recovered
- output SQL is recoverable
- no inaccessible private service, private model, private prompts, or private workload data is required

### `acquired_but_adapter_needed`

Use if:

- the upstream substrate is real and reproducible
- entrypoint and correction loop exist
- prompt/rule assets and feedback contracts exist
- output contract is understood
- but RewriteBench still lacks the case-package adapter and artifact plumbing

### `acquired_but_not_reproducible`

Use if:

- some upstream artifacts are found
- but exact commit/release, prompt/rule bundle, correction-loop policy, dependency contract, or licensing is not stable enough for a reproducible repo-local baseline

### `unavailable_blocked`

Use if any stop condition remains:

- no source repo
- no runnable entrypoint
- no correction loop
- no verifier/checker feedback loop
- no executor-feedback loop
- no prompt/rule library
- no dependency contract
- no output SQL
- requires inaccessible private service, private model, private prompts, or private workload data
- cannot separate GenRewrite method behavior from RewriteBench checker behavior

## 8. Current Provisional Decision

Based only on current repo-local evidence:

- current classification: `unavailable_blocked`

Reason:

- no source snapshot is pinned locally
- no repo-local GenRewrite runner exists
- no correction loop exists
- no verifier/checker feedback loop exists
- no executor-feedback loop exists
- no prompt/rule library exists
- no dependency contract is present
- no output-SQL contract is recovered

## 9. Non-Modification Note

- no GenRewrite execution was performed
- no DB execution was performed
- no model calls were performed
- no SQLGlot execution was performed
- no packages were installed
- no repositories were cloned
- no checkpoints were downloaded
- no adapters were created
- no scripts were modified
- no registry files were modified
- no review files were modified
- no rules, taxonomy, admission, or common-core files were modified
- `docs/EXECUTION_STATUS.md` was not modified
- the three long-standing untracked taxonomy notes were left untouched
