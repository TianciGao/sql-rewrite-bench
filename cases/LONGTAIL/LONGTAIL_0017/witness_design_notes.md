# Witness Design Notes

Multi-rank user profile rollup with net votes and post/view ranks; negative removes users without posts from the rollup base.
The witness dataset is intentionally small and case-local.
It is designed so `source.sql` and `rewrite_pos_01.sql` should agree, while `rewrite_neg_01.sql` should diverge.
No engine-closure or review claim is made by package construction.
