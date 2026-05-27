# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows make Ahmed Samir Farag average to 61.666..., while the hard negative changes the filtered player and yields 80 instead.
