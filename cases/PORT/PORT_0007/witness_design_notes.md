# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `comments`
- `posts`

## Minimal Draft Witness

- 3 to 4 `posts` rows and 4 to 5 `comments` rows should be enough.
- Include one qualifying post in the `viewcount BETWEEN 100 AND 150` band, one non-qualifying post, a tied score situation, and one `NULL` score row.

## Boundary Goal

- The source and positive rewrites should agree on the selected comment text after viewcount filtering and descending score ordering.
- The hard negative should fail by reversing the ordering pressure on the same witness rows.
