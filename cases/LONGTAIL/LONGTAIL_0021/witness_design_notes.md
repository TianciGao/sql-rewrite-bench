# Witness Design Notes

Reputation-ranked users with optional post participation and a top-10 cut.
The witness keeps the highest-reputation user without posts so the left-join source and non-identity positive rewrite agree, while the inner-join negative removes that user and shifts the selected top-10 set.
The witness dataset is intentionally small and case-local.
No engine-closure or review claim is made by package construction.
