# RBOT_LLMR2_MANUAL_ACQUISITION_CHECKLIST_v1

## 0. Status

This is documentation-only.

It is not implementation.
It is not execution.
It is not a runnable-substrate claim.
It is not a registry writeback.
It is not a closeout.

Current repo-local state remains blocked: there is no runnable repo-local substrate for either `R-Bot` or `LLM-R2`.

## 1. Shared Retrieval / Demonstration Substrate Requirements

Before any RewriteBench adapter can be discussed, both `R-Bot` and `LLM-R2` require the following upstream substrate to be manually acquired and pinned:

- source repo / artifact location
- exact commit hash or release
- retrieval corpus
- retrieval index or embedding store
- demonstration pool
- rule pool
- selector / retriever implementation
- rerank path
- rule-application path
- contamination policy
- dependency/runtime contract
- license / redistribution constraints
- model/API requirements if any
- hardware/runtime assumptions

Current repo-local evidence says these are missing at the substrate level, not merely missing at the adapter level:

- `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- `reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json`
- `docs/_scratch/PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1.md`

The practical boundary is strict:

- no retrieval corpus
- no retrieval index
- no demo pool
- no rule pool
- no selector
- no rerank path
- no reproducibility or contamination contract

Without those, no repo-local runnable prior-method coverage exists.

## 2. R-Bot Acquisition Checklist

### 2.1 External artifacts needed

Manual acquisition must recover:

- source repo
- retrieval corpus
- retrieval index
- selector / retriever
- rule pool
- reranker
- prompt templates if any
- model/API dependencies if any
- dependency/runtime contract
- license / redistribution constraints

Additional recovery questions:

- whether the retrieval corpus is static, generated, or benchmark-derived
- whether the retrieval index is stored or rebuilt
- whether rule-pool artifacts are bundled or constructed from an external source
- whether reranking depends on additional model calls or learned weights

### 2.2 Input contract to recover

Must be recovered from upstream source:

- whether `R-Bot` accepts SQL text
- whether it needs schema
- whether it needs query plans
- whether it retrieves examples, rules, or demonstrations
- whether retrieval depends on workload history
- whether it needs DB feedback or cost feedback
- whether it is dialect-specific or PG-only

Current best repo-local approximation:

- likely accepts SQL text plus schema
- likely retrieves examples/rules/evidence
- likely depends on retrieval corpus and rule pool together
- likely uses LLM-assisted stepwise rule selection
- exact DB feedback or cost-feedback dependence is still not recovered

### 2.3 Output contract to recover

Must be recovered from upstream source:

- final rewritten SQL
- ranked candidates
- selected rule sequence
- retrieval trace
- rerank trace
- confidence/cost metadata
- failure modes

Hard requirement for RewriteBench later:

- the method must eventually yield candidate SQL that can be passed into the existing PostgreSQL checker and speedup pipeline

### 2.4 RewriteBench adapter boundary

No adapter should be created now.

Later adapter boundary must define:

- case package -> `R-Bot` input
- `R-Bot` retrieval/rerank -> candidate SQL
- candidate SQL -> existing PG checker/speedup pipeline
- artifact paths for reproducibility
- contamination prevention boundaries

Specific adapter questions that acquisition must answer first:

- how the retrieval corpus is referenced at runtime
- how schema/context is serialized for retrieval
- whether retrieved items are examples, rules, or both
- whether final SQL is directly emitted or reconstructed from a rule sequence

### 2.5 Minimum bounded smoke after acquisition

Only after full acquisition and contract recovery:

- `1-3` cases only
- PostgreSQL-only first
- suggested first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- no registry writeback
- no leaderboard claim
- no full prior-method coverage claim

Claim boundary for any later smoke:

- bounded PostgreSQL-only retrieval-guided rewrite smoke only
- not final baseline coverage
- not full runnable coverage

### 2.6 Stop conditions

Stop and classify acquisition as blocked if any of the following remains unresolved:

- no source repo
- no retrieval corpus
- no retrieval index
- no rule pool
- no selector
- no rerank path
- no output SQL
- no reproducibility / contamination policy
- requires inaccessible private corpus, private service, private prompts, or private workload data

Additional practical stop conditions:

- retrieval corpus exists but cannot be legally redistributed or pinned
- selector exists only as a hosted or unshareable service
- the method cannot be separated from a benchmark-specific hidden history

### 2.7 Current provisional decision

Based only on current repo-local evidence:

- current classification: `unavailable_blocked`

Reason:

- no source snapshot is pinned locally
- no retrieval corpus is present
- no retrieval index is present
- no rule pool is present
- no selector or rerank path is present
- no output-SQL contract is recovered
- no contamination or reproducibility contract exists

## 3. LLM-R2 Acquisition Checklist

### 3.1 External artifacts needed

Manual acquisition must recover:

- source repo
- demonstration pool
- rule library
- rule applier
- demonstration selector
- embedding / contrastive retrieval path if required
- prompt templates
- model/API dependencies if any
- dependency/runtime contract
- license / redistribution constraints

Additional recovery questions:

- whether demonstrations are fixed or dynamically retrieved
- whether embeddings are pretrained or generated locally
- whether rule application is symbolic, template-based, or model-mediated

### 3.2 Input contract to recover

Must be recovered from upstream source:

- whether `LLM-R2` accepts SQL text
- whether it needs schema
- whether it needs query plans
- whether it needs demonstrations
- whether it needs rule selection or rule application
- whether it needs embedding vectors
- whether it needs DB feedback, checker feedback, or cost feedback
- whether it is PG-specific or dialect-agnostic

Current best repo-local approximation:

- likely accepts SQL text plus schema
- likely uses demonstrations and rule candidates together
- likely requires some demonstration-selection or embedding path
- exact DB/checker/cost-feedback dependence is still not recovered

### 3.3 Output contract to recover

Must be recovered from upstream source:

- final rewritten SQL
- selected demonstrations
- selected rules
- rule-application trace
- candidate list
- model call trace / token usage
- failure modes

Hard requirement for RewriteBench later:

- the method must eventually yield candidate SQL that can be passed into the existing PostgreSQL checker and speedup pipeline

### 3.4 RewriteBench adapter boundary

No adapter should be created now.

Later adapter boundary must define:

- case package -> `LLM-R2` input
- demo/rule selection -> candidate SQL
- candidate SQL -> existing PG checker/speedup pipeline
- artifact paths for reproducibility
- token/cost accounting
- contamination prevention boundaries

Specific adapter questions that acquisition must answer first:

- how demonstrations are selected and represented
- how rules are represented and applied
- whether final SQL is directly emitted or reconstructed through a rule-applier path
- how token/cost accounting is preserved if LLM calls are part of the original method

### 3.5 Minimum bounded smoke after acquisition

Only after full acquisition and contract recovery:

- `1-3` cases only
- PostgreSQL-only first
- suggested first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- no registry writeback
- no leaderboard claim
- no full prior-method coverage claim

Claim boundary for any later smoke:

- bounded PostgreSQL-only demonstration/rule-selection rewrite smoke only
- not final baseline coverage
- not full runnable coverage

### 3.6 Stop conditions

Stop and classify acquisition as blocked if any of the following remains unresolved:

- no source repo
- no demonstration pool
- no rule library
- no rule applier
- no demo selector
- no embedding/retrieval path if required
- no output SQL
- no reproducibility / contamination policy
- requires inaccessible private demonstrations, private prompts, private service, or private workload data

Additional practical stop conditions:

- demonstrations exist but cannot be legally redistributed or pinned
- rule application depends on unshared proprietary logic
- the method cannot be separated from hidden prompt assets or private examples

### 3.7 Current provisional decision

Based only on current repo-local evidence:

- current classification: `unavailable_blocked`

Reason:

- no source snapshot is pinned locally
- no demonstration pool is present
- no rule library is present
- no rule applier is present
- no demo selector is present
- no embedding/retrieval path is present
- no output-SQL contract is recovered
- no contamination or reproducibility contract exists

## 4. Shared Decision Tree

Use the following classification for retrieval/demo/rule-selection baselines:

### `acquired_and_runnable`

Use only if all are true:

- upstream source is pinned to a reproducible commit/release
- retrieval/demo/rule substrate exists locally
- runnable entrypoint exists
- output SQL is recoverable
- contamination and reproducibility policy are explicit
- no inaccessible private service or private corpus is required

### `acquired_but_adapter_needed`

Use if:

- upstream substrate is real and reproducible
- retrieval/demo/rule assets are acquired
- runnable entrypoint exists
- output contract is understood
- but RewriteBench still lacks the case-package adapter and artifact plumbing

### `acquired_but_not_reproducible`

Use if:

- some upstream artifacts are found
- but exact commit/release, corpus/demo/rule assets, runtime contract, or licensing is not stable enough for reproducible repo-local use

### `unavailable_blocked`

Use if:

- no source repo
- no retrieval/demo/rule substrate
- no runnable entrypoint
- no output SQL
- or the method depends on inaccessible private service, private corpus, private prompts, or private workload data

## 5. Shared Do-Not-Implement Rule

Codex should not implement `R-Bot` or `LLM-R2` until a real upstream substrate is acquired and pinned.

Creating a synthetic retrieval corpus, synthetic rule pool, or synthetic demo selector would not count as prior-method coverage.

## 6. Recommended Next Step

Move to the `SQLSolver` support-only acquisition checklist.

Reason:

- current evidence already shows both `R-Bot` and `LLM-R2` are blocked on a large shared retrieval/demo/rule-selection substrate family
- the missing pieces are deeper and broader than a single acquisition checklist can unblock
- `SQLSolver` has a narrower support-only role and a smaller future acquisition surface than these retrieval-dependent lines

## 7. Non-Modification Note

- no execution was performed
- no download was performed
- no model call was performed
- no DB run was performed
- no SQLGlot run was performed
- no adapter was created
- no scripts were modified
- no registry files were modified
- no review files were modified
- no rules, taxonomy, admission, or common-core files were modified
- `docs/EXECUTION_STATUS.md` was not modified
- the three long-standing untracked taxonomy notes were left untouched
