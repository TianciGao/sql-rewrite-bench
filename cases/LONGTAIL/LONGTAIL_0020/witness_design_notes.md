# Witness Design Notes

Reputation-ranked users with optional post aggregates.
The witness keeps one top-ranked user with no posts so the left-join source and non-identity positive rewrite agree, while the inner-join negative drops that user and changes the top-10 membership.
The witness dataset is intentionally small and case-local.
No engine-closure or review claim is made by package construction.
