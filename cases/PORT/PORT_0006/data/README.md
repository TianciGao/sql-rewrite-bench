# Draft Witness Rows

This directory contains draft-only witness rows for `PORT_0006`.

- These rows have not been loaded into any engine.
- They are planning artifacts for later portability validation.
- The main purpose is to expose the difference between `< 100000` and `<= 100000` while preserving the intended boolean-count adaptation story.

Before later validation, a human or Codex task should:

1. confirm the row set against the source and rewrite SQL,
2. translate the rows into engine-specific load statements if needed,
3. verify that the source and positive rewrites agree below the threshold,
4. verify that the hard negative diverges because of the `amount = 100000` boundary row.
