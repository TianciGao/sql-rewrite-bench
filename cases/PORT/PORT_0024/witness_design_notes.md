# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows yield a 50 percent positive result and a 25 percent negative result by flipping the spotlight predicate only.
