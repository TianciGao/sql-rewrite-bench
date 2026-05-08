# Formal ZIP Text Extraction Contract

## Scope

This contract defines the human-run-only extraction layer for
`stackoverflow-rewrite-embed.zip`.

It exists so the formal near-duplicate and generated-output exclusion checkers
can consume contamination-relevant text without:

- copying the ZIP into the repo
- extracting full JSONL members into the repo
- treating the outer ZIP bytes as a text corpus file

## Archive Identity

- ZIP path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`
- expected outer SHA-256:
  - `e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a`

The archive remains `/tmp`-only unless a retained external provenance handle is
recorded separately. That retention gap stays a formal gate blocker even if the
text extraction succeeds.

## Allowed Member Set

The extraction script reads only these four JSONL members:

1. `stackoverflow-rewrite-query-optimization.jsonl`
2. `stackoverflow-rewrite-rules-query-optimization.jsonl`
3. `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
4. `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

The script must ignore:

- all `__MACOSX/` sidecars
- embedding vectors as comparison text
- any unlisted archive members

## Field-Level Extraction

The script emits only these contamination-relevant fields:

- `sql`
- `schema`
- `rules[]`
- `question_body_sqls[]`
- `sql_templates[].template`
- `sql_template`

The script does not emit:

- embedding payloads
- macOS metadata sidecars
- the raw ZIP bytes
- full extracted JSONL members

## Streaming Requirement

The script must:

1. open the ZIP in-place
2. stream listed members directly from the archive
3. parse JSONL one record at a time
4. write only the extracted row-level manifest outputs

It must not unpack the full archive or full JSONL members into the repo.

## Output Files

The script writes:

1. `formal_zip_text_manifest_v1.csv`
2. `formal_zip_text_hashes_v1.json`
3. `formal_zip_text_manifest_summary.md`

## Manifest Row Contract

Each CSV row represents one extracted text item, not one archive member.

Required row identity/provenance fields:

- `zip_text_item_id`
- `source_family`
- `zip_path`
- `zip_sha256`
- `zip_entry_name`
- `entry_sha256`
- `source_record_locator`
- `json_field_selector`

Required status fields:

- `path_status`
- `text_readable`
- `included_for_formal_retrieval`
- `included_for_contamination_check`
- `formal_retention_blocker`
- `retention_blocker_reason`

Required text/hash fields:

- `text_length`
- `normalized_hash`
- `extracted_text`

## Retention / Gate Semantics

Successful extraction does not open the formal gate by itself.

If the ZIP text is available and the comparison succeeds, the checkers should
still preserve:

- `formal_retention_blocked`

when the archive remains `/tmp`-only and retained external provenance is still
missing.

So the checker outcomes must distinguish:

- `contamination_check_passed_against_visible_text`
- `formal_retention_blocked`
- `corpus_text_unavailable`
- `generated_output_match_found`
- `near_duplicate_found`

## Bottom Line

This contract enables provisional contamination checking against visible ZIP
text, but it does not authorize formal `R-Bot @120` generation while archive
retention/provenance remains unresolved.
