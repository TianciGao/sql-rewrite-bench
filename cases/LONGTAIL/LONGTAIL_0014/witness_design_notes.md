# Witness Design Notes

User-level positive-question rollup with HAVING over post count or upvotes; negative drops high-upvote users lacking qualifying posts.
The witness dataset is intentionally small and case-local.
It is designed so `source.sql` and `rewrite_pos_01.sql` should agree, while `rewrite_neg_01.sql` should diverge.
No engine-closure or review claim is made by package construction.
