# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows create one Canadian Grand Prix driver with two retired results and another with one, so the positive top count is 2 while the hard negative drops to 1.
