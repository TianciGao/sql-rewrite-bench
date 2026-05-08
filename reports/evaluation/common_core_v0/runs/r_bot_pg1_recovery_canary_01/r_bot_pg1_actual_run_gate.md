# R-Bot PG1 Actual Run Gate

This document defines the exact gate for whether `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` may produce current Common-core v0 benchmark evidence for the `PERF_0006 / pg` canary.

Current decision:

`actual_pg1_generation_not_allowed_for_current_evidence`

## Why The Gate Exists

The canary is not blocked only by runtime. It is blocked by a mixed set of:

- dependency substrate requirements
- retrieval/index reproducibility requirements
- policy freeze requirements
- artifact contract requirements

Without all four classes closed, an actual run would still be exploratory smoke rather than current benchmark evidence.

## Gate Conditions

All items below must be true before `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` may produce current evidence.

### 1. Dependencies installed in a smoke-scoped environment

Must be true:

- the runnable dependency set exists in a smoke-scoped environment
- the smoke-scoped environment is identified and documented
- package versions are snapshotted
- the repo default environment is not implicitly redefined as an `R-Bot` startup requirement

Current status:

- `partially satisfied`

Reason:

- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke` exists
- package snapshot exists
- but the retained benchmark-side freeze of that environment is not complete

### 2. Upstream repo identity pinned

Must be true:

- upstream repo URL recorded
- upstream commit recorded
- local substrate root recorded

Current status:

- `satisfied for identification`
- `not sufficient alone for current evidence`

Observed values:

- repo: `https://github.com/curtis-sun/LLM4Rewrite`
- commit: `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375`

### 3. Retrieval corpus pinned

Must be true:

- the retrieval corpus inputs are named
- key files are hashed
- the current run declares whether `/tmp` retention is temporary or promoted into a frozen substrate record

Current status:

- `not satisfied`

Reason:

- some files are hashed
- but the corpus is still `/tmp`-only and not frozen as a retained benchmark substrate

### 4. Index snapshot pinned

Must be true:

- index path recorded
- anchor files hashed
- build provenance recorded
- current benchmark package explicitly recognizes the retained index snapshot

Current status:

- `not satisfied`

Reason:

- `chroma_db` exists and some files are hashed
- but it still belongs to a scratch build line and is not yet frozen as retained current-evidence substrate

### 5. Demo policy frozen

Must be true:

- retrieval corpus scope frozen
- retrieval mode frozen
- top-k frozen
- tie-break policy frozen
- manual override policy frozen
- selected-rules/retrieval-trace capture requirement frozen

Current status:

- `not satisfied`

Reason:

- prompt/config source files are identifiable
- experiment policy is still not frozen

### 6. Contamination guard frozen

Must be true:

- no frozen-denominator answer leakage attested
- no prior RewriteBench outputs re-indexed attested
- no post-outcome demo tuning attested
- provenance attestation recorded

Current status:

- `not satisfied`

### 7. Output artifact contract frozen

Must be true:

- generated SQL retained at the declared package path
- selected rules retained
- retrieval trace retained
- token/cost log retained
- failure category retained
- artifact names frozen before run

Current status:

- `not satisfied`

Reason:

- the package declares the generated SQL destination
- the full retained artifact naming contract for trace files is not yet frozen in the package

### 8. OpenAI/API endpoint logged without exposing secret

Must be true if actual generation later occurs:

- do not log API key
- do log provider/model/backend choice
- do log base URL or endpoint family if non-default or OpenAI-like path is used
- do log whether token/cost accounting is available

Current status:

- `not satisfied`

Reason:

- current canary only observed `OPENAI_API_KEY` visibility as false
- no actual run occurred
- no endpoint/provider record exists yet

### 9. PG1 canary remains exploratory until all gates pass

Must be true:

- any run before all gates pass is labeled exploratory smoke only
- no current metric claims
- no leaderboard claim
- no denominator-wide inference

Current status:

- `satisfied`

Reason:

- the current package already preserves that boundary

## Exact Remaining Blockers

The exact blockers still preventing current-evidence actual generation are:

1. retrieval corpus not frozen as retained substrate
2. index snapshot not frozen as retained substrate
3. demo policy not frozen
4. contamination guard not frozen
5. output artifact contract not fully frozen
6. endpoint/provider logging contract not frozen
7. observed canary shell did not expose `OPENAI_API_KEY`

## Final Decision

`RBOT_CANARY_ALLOW_ACTUAL_RUN=1` must not yet produce current benchmark evidence.

If a human chooses to run it before all gates pass, that run must be labeled:

`exploratory_smoke_only_not_current_common_core_evidence`
