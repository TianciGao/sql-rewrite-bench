# Formal Gate Status v11 Draft

## Scope

This is a draft gate-status update after the formal Chroma index rebuild and
identifier package.

It remains a draft only.
It does not authorize generation.

## Draft Direct Answers

- Chroma index blocker closed: `no`
- current visible `/tmp` index acceptable as formal evidence: `no`
- formal `R-Bot @120` generation may start: `no`

## What This Draft Changes

This package does not close the index blocker.

What it does close is the specification gap around what the future retained
formal index identifier must contain:

1. index metadata field list is now explicit
2. DOI-backed corpus input is now tied directly into the index contract
3. retrieval settings are frozen in the index template:
   - embedding model `text-embedding-3-small`
   - rule-vector width `100`
   - total dimension `3172`
   - `top_k = 10`
   - reranking `rrf`
   - `rrf_k = 60`
   - similarity threshold `explicit none`

## Why The Gate Still Stays Closed

The expected answer remains `no` because no retained formal index metadata
exists yet.

The visible `/tmp` index is not enough because it lacks:

- retained `index_id`
- retained build timestamp
- retained build command identity
- retained collection name and file-hash package

## Remaining Blockers

1. formal Chroma index identifier / rebuild
2. runtime/dependency lock
3. retained run-path artifact-contract validation

## Bottom Line

This package converts the Chroma index blocker into an explicit retained
metadata contract, but the blocker remains open.

Formal `R-Bot @120` generation may not start.
