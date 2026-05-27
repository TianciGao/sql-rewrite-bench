# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows make one of four cards count as `Chinese Simplified`, while two of four count as `Japanese`, so the positive query yields `25` and the hard negative yields `50`.
