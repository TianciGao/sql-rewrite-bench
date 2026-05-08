# Formal `stackoverflow-rewrite-embed.zip` Audit

## Scope

This package audits the last remaining formal contamination blocker carried in `formal_gate_status_v7`:

- `stackoverflow-rewrite-embed.zip / binary_or_unavailable_text_corpus`

It does not copy the ZIP into the repo.
It does not extract large contents into the repo.
It does not run databases, SQL, `R-Bot`, or any API.

## Direct Outcome

The archive container is binary as a ZIP file, but its primary members are text-readable `.jsonl` files.

So the v7 blocker label:

- `binary_or_unavailable_text_corpus`

is too coarse as a final technical classification.

The more precise classification is:

- text-bearing archive container
- tmp-only
- checksum-visible
- retained external provenance still missing
- checker-consumable deterministic text extraction contract not yet materialized

Therefore the formal gate still remains closed, but no longer because the archive is wholly non-text.

## Located ZIP

- ZIP path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- visible SHA-256:
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`
- visible size:
  - `71,610,403` bytes

This matches the existing substrate inventory and prior freeze artifacts.

## ZIP Inventory Headline

Visible entries: `8`

Breakdown:

- text-readable JSONL members: `4`
- metadata entries under `__MACOSX/`: `4`
- binary/index-only members: `0`

Uncompressed total across all entries:

- `198,311,091` bytes

## Member Classification

### Text-readable members

1. `stackoverflow-rewrite-query-optimization.jsonl`
2. `stackoverflow-rewrite-rules-query-optimization.jsonl`
3. `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
4. `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

These are UTF-8 JSONL members and are text-readable by streamed archive access.

### Metadata members

1. `__MACOSX/._stackoverflow-rewrite-query-optimization.jsonl`
2. `__MACOSX/._stackoverflow-rewrite-rules-query-optimization.jsonl`
3. `__MACOSX/._stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
4. `__MACOSX/._stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

These are macOS metadata artifacts and should not be treated as retrieval corpus content.

## What Text Is Inside The JSONL Members

### `stackoverflow-rewrite-query-optimization.jsonl`

Observed text-bearing fields:

- `question_body`
- `question_body_sqls[]`
- `answer_body`
- `summary`

Also contains:

- `embedding` with length `1536`

Interpretation:

- usable text corpus exists
- member is not text-only because it mixes human text and embedding payload

### `stackoverflow-rewrite-rules-query-optimization.jsonl`

Observed text-bearing fields:

- `sql`
- `schema`
- `rules[]`
- `nl_rules[]`

Interpretation:

- directly relevant contamination-check text exists

### `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`

Observed text-bearing fields:

- `question_body_sqls[]`
- `sql_templates[].template`

Interpretation:

- directly relevant contamination-check text exists

### `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

Observed text-bearing fields:

- `sql_template`

Also contains:

- `embedding` with length `1536`

Interpretation:

- usable SQL-template text exists
- member also includes dense embedding payload

## Whether The ZIP Contains Usable Text For Contamination Checks

Answer: `yes`

Why:

1. multiple JSONL members contain direct SQL text, SQL templates, rules, schemas, question bodies, and answer bodies
2. these text fields are readable in streamed form from the ZIP without extracting the whole archive into the repo
3. the archive therefore contains contamination-relevant text

Important caveat:

- contamination checking should not operate on the raw ZIP bytes
- it also should not treat each whole JSONL member as one undifferentiated document
- a deterministic field-level extraction recipe is required

## Deterministic Text Extraction Recipe

Yes, a deterministic text extraction recipe can be written.

Minimal recipe shape:

1. open the ZIP by exact path and outer SHA-256
2. ignore all `__MACOSX/` metadata entries
3. stream the four JSONL members without unpacking large contents into the repo
4. parse each JSON line as JSON
5. emit only the contamination-relevant text fields:
   - `question_body_sqls[]`
   - `sql`
   - `schema`
   - `rules[]`
   - `nl_rules[]`
   - `sql_templates[].template`
   - `sql_template`
   - optionally `question_body`, `answer_body`, `summary` if the formal policy wants non-SQL natural-language contamination coverage
6. explicitly ignore embedding vectors as candidate text corpus
7. normalize emitted text with the existing deterministic normalization rules before comparison

This recipe is deterministic and can be implemented without retaining large extracted copies inside the repo.

## Final Classification

### External retained artifact with checksum

Current status: `candidate_yes_but_not_closed`

Reason:

- checksum is visible
- archive path is visible
- retained external provenance handle is still missing

### Deterministic rebuild input

Current status: `yes`

Reason:

- the ZIP is a named retrieval corpus input in the benchmark-common retrieval corpus family
- the exact bytes are identified by SHA-256
- a deterministic member-level text extraction recipe can be written

### Binary-only non-text corpus

Current status: `no`

Reason:

- the container is binary
- the meaningful members are text-readable JSONL

### Blocker that keeps the formal gate closed

Current status: `yes`

Reason:

1. retained external provenance is still incomplete
2. current contamination-checker contract does not yet consume ZIP-member text through a deterministic extraction layer
3. the archive is still `/tmp`-only

## Bottom Line

The archive does contain usable text corpus.

But formal `R-Bot @120` generation still may not start, because the ZIP is only partly resolved:

- text-bearing members are now technically identified
- provenance is still not fully retained
- checker-consumable extraction has not yet been frozen and rerun
