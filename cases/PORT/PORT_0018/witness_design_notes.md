# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows make the latest non-null birthdate uniquely select Lance Stroll, while the hard negative flips the order and selects Mark Older instead.
