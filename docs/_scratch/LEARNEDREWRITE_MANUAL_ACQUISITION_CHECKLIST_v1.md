# LEARNEDREWRITE_MANUAL_ACQUISITION_CHECKLIST_v1

## 0. Status

This is a documentation-only manual acquisition checklist for `LearnedRewrite`.

It is not implementation.
It is not execution.
It is not a runnable-substrate claim.
It is not a registry writeback.
It is not a closeout.

Current repo-local state remains:

- readiness scaffold exists
- bounded first-subset candidates are known
- no repo-local runner exists
- no checkpoint/model artifact exists
- no inference entrypoint exists
- no adapter exists

## 1. What Exact External Artifacts Are Needed?

### 1.1 Required acquisition targets

The following external artifacts must be identified manually before any implementation or execution discussion:

1. source repo
   - exact upstream repository or archived source package for the LearnedRewrite system
   - exact repo URL
   - exact branch, commit hash, tag, or release
   - any companion demo repo if the paper code is split from the main implementation
2. model/checkpoint files
   - exact learned model artifact names
   - exact checkpoint paths expected by the original code
   - whether a pretrained checkpoint is mandatory or whether the method assumes retraining
3. dependency/runtime contract
   - exact Java / Calcite / build-tool version
   - whether Maven or Gradle is required
   - whether additional native dependencies or database drivers are required
   - whether workload statistics, catalog metadata, or cost-model snapshots are required at runtime
4. license / redistribution constraints
   - repository license
   - model/checkpoint redistribution license
   - whether pretrained artifacts can be stored in-repo, only referenced, or not redistributed
5. expected hardware/runtime assumptions
   - CPU-only or GPU-required
   - expected memory requirements
   - whether the method assumes long offline preprocessing or training
   - whether the runtime assumes a persistent DB-backed statistics store or other external service

### 1.2 Current evidence and current unknowns

Current repo-local evidence:

- `docs/_scratch/baseline_inventory_boss_requirements.csv`
  - describes LearnedRewrite as:
    - `LearnedRewrite / learned query rewrite`
    - `Learned rule-order search`
    - implemented in Calcite
    - input/output roughly: `Input: SQL + schema/statistics + rule set; Output: rewritten SQL or rule sequence/optimized plan`
    - environment roughly: `Java/Calcite, model/checkpoint or training artifacts, statistics/cost model`
- `reports/baseline_smoke/learnedrewrite_input_readiness_v0.json`
  - `learnedrewrite_checkpoint_available=false`
  - `learnedrewrite_inference_entrypoint_available=false`
  - `dependency_file_available=false`

Current unknowns that must be recovered manually:

- exact upstream code location
- exact runnable commit/release
- exact checkpoint artifact names
- whether inference without retraining is possible
- whether workload statistics are mandatory
- exact license boundaries for code and model artifacts
- whether the code emits SQL directly or only rule sequences / plans

## 2. What Input Contract Must Be Recovered?

The following input-contract questions must be answered from the original source before any adapter work:

### 2.1 Core input format

- does LearnedRewrite accept raw SQL text directly?
- does it require a Calcite relational representation instead of plain SQL text?
- does it require a schema file, catalog model, or statistics snapshot in a Calcite-specific format?
- does it require a rule set file or learned rule-order policy file?

### 2.2 Context inputs

- does it consume:
  - SQL text
  - query plans
  - schema metadata
  - table/column statistics
  - cost feedback
  - workload context
  - training traces
  - DB-specific metadata
- does it assume PostgreSQL specifically, or only a Calcite-supported intermediate representation?
- does it require database-specific cardinality or cost estimates at inference time?

### 2.3 Training-data dependency

Must be clarified explicitly:

- is the released method usable with a pretrained checkpoint only?
- is retraining mandatory to get any meaningful output?
- if retraining is mandatory, what training corpus, labels, or workload traces are required?
- are benchmark-specific statistics required to transfer the method to RewriteBench?

### 2.4 Current best repo-local approximation

The current repo-local readiness materials imply only a partial input understanding:

- likely needed:
  - `source.sql`
  - PostgreSQL schema context
  - some statistics/cost-model context
  - a learned rule-order policy or model artifact
- not yet recovered:
  - exact file formats
  - exact command-line flags
  - exact metadata encoding
  - exact minimum runtime inputs

## 3. What Output Contract Must Be Recovered?

The following output-contract questions must be answered from the original source:

### 3.1 Primary outputs

- does the method emit rewritten SQL directly?
- does it emit a ranked list of candidates rather than one final SQL string?
- does it emit a rule sequence only, requiring later SQL regeneration?
- does it emit an optimized plan only, without SQL regeneration?

### 3.2 Auxiliary outputs

- cost estimates
- confidence scores
- search traces
- rule-application logs
- candidate ranking metadata
- failure or fallback diagnostics

### 3.3 Failure modes to recover

The acquisition packet should identify exact failure modes such as:

- no candidate generated
- parse failure
- schema/model mismatch
- unsupported SQL subset
- missing statistics
- checkpoint load failure
- search timeout
- output not convertible back to SQL

### 3.4 RewriteBench-critical output requirement

A hard requirement for later use is:

- the method must eventually yield candidate SQL that can be passed into the existing PostgreSQL checker and speedup pipeline

If the recovered implementation cannot produce SQL text or a deterministic SQL-regeneration path, acquisition should not be treated as sufficient for RewriteBench baseline use.

## 4. What RewriteBench Adapter Would Be Required Later?

No adapter should be implemented now.

This section defines only the later adapter boundary that manual acquisition must support.

### 4.1 Case package -> LearnedRewrite input

Later adapter must map:

- `cases/PERF/<CASE>/source.sql`
- `cases/PERF/<CASE>/schema/ddl_pg.sql`
- any required schema/statistics context
- any required rule-set configuration

into the original LearnedRewrite input format.

### 4.2 LearnedRewrite output -> candidate SQL

Later adapter must clarify one of the following paths:

- direct rewritten SQL output
- rule sequence -> deterministic SQL regeneration
- optimized plan -> deterministic SQL regeneration

If only plans or internal rule traces are emitted, the SQL regeneration contract must be recovered before any runnable-baseline claim.

### 4.3 Candidate SQL -> existing PG checker/speedup pipeline

Later adapter must support:

- writing generated candidate SQL to a reproducible artifact path
- passing that candidate into the existing PostgreSQL checker path
- passing the same candidate into the existing PostgreSQL speedup path
- recording method-specific logs without modifying case packages or registries

### 4.4 Artifact paths needed for reproducibility

Later reproducibility packet should reserve paths for:

- acquired upstream source snapshot reference
- acquired commit hash or release identifier
- model/checkpoint reference or local external path
- adapter config used for the run
- generated candidate SQL
- method logs
- runtime metadata
- failure diagnostics

Recommended future artifact categories only:

- `source_snapshot_ref`
- `checkpoint_ref`
- `input_contract_note`
- `generated_sql`
- `method_trace`
- `runtime_metadata`
- `failure_log`

## 5. What Minimum Bounded Smoke Would Be Allowed After Acquisition?

Only after all required artifacts are acquired and the input/output contracts are recovered:

- denominator: `1-3` cases only
- suggested first subset:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- PostgreSQL-only first
- no registry writeback
- no leaderboard claim

### 5.1 Why this subset

This subset is already supported by the current readiness scaffold:

- `reports/baseline_smoke/learnedrewrite_input_readiness_v0.json`
- `docs/_scratch/BASELINE_ROUTE_STATUS_AND_BACKLOG_v0.md`

These cases are currently the cleanest first-subset candidates because they are simpler analytical PERF cases and avoid the interval-heavy or more semantically loaded later cases.

### 5.2 Required preflight before any future run

Before any future bounded smoke is even proposed:

- source repo and commit must be pinned
- entrypoint command must be recovered
- checkpoint path must be verified
- dependency/runtime contract must be documented
- input contract must be proven against one case package on paper
- output contract must show recoverable candidate SQL
- license status must be clear

### 5.3 Claim boundary for any future smoke

If acquisition succeeds later, the first bounded smoke could support only:

- a bounded PostgreSQL-only LearnedRewrite substrate smoke
- no registry writeback
- no final baseline coverage claim
- no full prior-method coverage claim
- no leaderboard claim

## 6. Stop Conditions

Stop and classify the acquisition as blocked if any of the following remains unresolved:

- no checkpoint
- no entrypoint
- no license clarity
- no dependency contract
- no output SQL
- requires inaccessible service or private data

Additional practical stop conditions:

- retraining is mandatory but training data or procedure is unavailable
- output is only an internal plan form with no deterministic SQL regeneration path
- required statistics or metadata contract cannot be reconstructed
- upstream code exists but is not legally reusable or reproducible

## 7. Final Decision Tree

Use the following classification after manual acquisition work is completed:

### `acquired_and_runnable`

Use only if all are true:

- source repo identified and pinned
- runnable entrypoint recovered
- dependency/runtime contract recovered
- required checkpoint/model artifact acquired or clearly reproducible
- license clarity is acceptable
- output SQL is recoverable
- no inaccessible external service or private data is required

### `acquired_but_adapter_needed`

Use if:

- the upstream substrate is real and reproducible
- entrypoint and checkpoint exist
- output contract is understood
- but RewriteBench still lacks the case-package adapter and artifact plumbing

### `acquired_but_not_reproducible`

Use if:

- some upstream artifacts are found
- but exact commit/release, dependency contract, checkpoint source, or licensing is not stable enough for a reproducible repo-local baseline

### `unavailable_blocked`

Use if any stop condition remains:

- no checkpoint
- no entrypoint
- no license clarity
- no dependency contract
- no output SQL
- requires inaccessible service or private data

## 8. Current Provisional Decision

Based on current repo-local evidence only:

- current classification: `unavailable_blocked`

Reason:

- no source snapshot is pinned locally
- no repo-local LearnedRewrite runner exists
- no checkpoint is present
- no inference entrypoint is present
- no dependency contract is present
- no output-SQL contract is recovered

## 9. Non-Modification Note

- no LearnedRewrite execution was performed
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
