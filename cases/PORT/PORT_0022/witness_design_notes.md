# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows create three qualifying 2010 postlinks and one qualifying 2011 postlink, so the year boundary cleanly separates positive and negative results.
