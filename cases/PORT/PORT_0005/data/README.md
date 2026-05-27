# Draft Witness Rows

This directory contains draft-only witness rows for `PORT_0005`.

- These rows have not been loaded into any engine.
- They are engine-neutral planning artifacts only.
- The main purpose is to expose the difference between earliest non-null `dob` selection and the intentionally wrong descending hard negative.

Before later validation, a human or Codex task should:

1. review the row set against the SQL files,
2. translate the rows into engine-specific load statements if needed,
3. confirm that the selected nationality is stable for source vs positive and divergent for source vs negative.
