# Witness Design Notes

Total-post-score user ranking with wiki/question/answer breakdown; negative drops zero-post users from the candidate set.
The witness dataset is intentionally small and case-local.
It is designed so `source.sql` and `rewrite_pos_01.sql` should agree, while `rewrite_neg_01.sql` should diverge.
No engine-closure or review claim is made by package construction.
