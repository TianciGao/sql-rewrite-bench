# Formal `stackoverflow-rewrite-embed.zip` Text Availability

## Direct Answer

The ZIP contains usable text corpus.

It is not accurate to treat the archive as wholly non-text.

## Availability Breakdown

- outer ZIP container:
  - binary container
  - not directly text-readable
- non-metadata members:
  - `4`
  - all are JSONL
  - all are text-readable by streamed archive access
- metadata members:
  - `4`
  - all under `__MACOSX/`
  - not corpus content

## Text-Relevant Members

### `stackoverflow-rewrite-query-optimization.jsonl`

- line count: `2091`
- contains contamination-relevant text: `yes`
- relevant fields:
  - `question_body`
  - `question_body_sqls[]`
  - `answer_body`
  - `summary`

### `stackoverflow-rewrite-rules-query-optimization.jsonl`

- line count: `2428`
- contains contamination-relevant text: `yes`
- relevant fields:
  - `sql`
  - `schema`
  - `rules[]`
  - `nl_rules[]`

### `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`

- line count: `1139`
- contains contamination-relevant text: `yes`
- relevant fields:
  - `question_body_sqls[]`
  - `sql_templates[].template`

### `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

- line count: `3798`
- contains contamination-relevant text: `yes`
- relevant fields:
  - `sql_template`
- also contains embedding vectors:
  - `embedding` length `1536`

## What Is Still Missing

Text availability is no longer the core uncertainty.

What is still missing is a frozen contract for how the checkers should consume the text:

1. stream archive members instead of treating the ZIP bytes as one opaque path
2. parse JSONL deterministically
3. select contamination-relevant text fields only
4. ignore embedding vectors and metadata sidecars

## Can The Current Checkers Rerun As-Is?

Current answer: `no`

Reason:

- the current checkers are filesystem-path-oriented
- they expect direct text files, not ZIP-member streaming with field extraction
- simply marking the ZIP itself text-readable would still be semantically wrong

## Can The Checkers Be Rerun Meaningfully After A Small Follow-Up Package?

Answer: `yes`

Needed follow-up:

1. add deterministic ZIP-member streaming support or a temporary non-repo extraction workspace
2. map member fields to checker-consumable text rows
3. rerun near-duplicate and generated-output exclusion checks against that extracted text view

## Bottom Line

The archive contains usable text corpus, but current formal contamination tooling does not yet consume it in a benchmark-frozen way.

So text exists, but text-consumption closure is still pending.
