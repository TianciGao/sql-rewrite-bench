# R-Bot PG40 Generation Expansion 02

This package prepares a human-run PostgreSQL-only R-Bot generation expansion run.

It exists because the earlier formal same-engine run kept `31` PG rows blocked by a recovered-harness whitelist. This package attempts all `40` PG rows through a generalized PG route while preserving denominator-aware reporting and without changing the prior PG7 retained evidence.

Boundary:

- PG only
- generation only
- no execution
- no timing
- no speedup
- no leaderboard claim

MySQL and Spark remain unsupported in this package.

The runner now includes a package-level preflight, uses an unsigned temp runtime copy of `LearnedRewrite.jar` only inside `/tmp`, and provisions the required upstream RAG JSONL corpus files into the temp runtime `rag/` directory. The retained upstream artifact and retained ZIP are not modified in place.
