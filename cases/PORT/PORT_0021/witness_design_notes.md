# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows give France Ligue 1 two draws and Spain LIGA BBVA one, so the hard negative flips the grouped top-1 league.
