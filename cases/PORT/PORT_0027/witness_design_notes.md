# Witness Design Notes

The witness rows are intentionally small and are designed so the source query and `rewrite_pos_01.sql` agree while `rewrite_neg_01.sql` drifts semantically but remains executable.

The witness rows give user `24` two owned posts across four distinct votes, so the positive query yields `0.5`. The hard negative switches to user `25`, which has two posts across two distinct votes and yields `1.0`.
