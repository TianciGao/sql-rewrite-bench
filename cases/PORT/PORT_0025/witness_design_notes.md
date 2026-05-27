# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows make account 2 the highest-amount qualifying 1993 loan, while the hard negative reverses the amount ordering and selects account 1.
