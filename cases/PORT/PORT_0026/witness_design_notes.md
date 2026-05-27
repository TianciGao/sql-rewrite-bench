# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows place exactly one non-null result time and three null result times on `1983-07-16`, so the positive query yields `25` while the hard negative flips to the null-time percentage and yields `75`.
