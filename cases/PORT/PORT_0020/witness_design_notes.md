# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows make Spain LIGA BBVA the unique highest-goal league for the season, while the hard negative selects the lower-scoring league instead.
