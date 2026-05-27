# Witness Design Notes

Total-score top-user ranking with post-type counts and total views; negative removes no-post users from the ranked set.
The witness dataset is intentionally small and case-local.
It is designed so `source.sql` and `rewrite_pos_01.sql` should agree, while `rewrite_neg_01.sql` should diverge.
No engine-closure or review claim is made by package construction.
