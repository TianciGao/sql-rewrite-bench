# R-Bot MySQL/Spark 6-Row Generation Canary Triage

## Summary

This run produced **generation-only canary evidence**.

- planned rows = `6`
- generated rows = `0`
- failed rows = `6`
- preflight_blocked rows = `0`

Uniform result across all six rows:

- `failure_category = generation_failed`
- `blocker_reason = method finished without extractable output_sql`

## Row-level outcomes

- `PERF_0006:mysql` → `failed` → `generation_failed` → `method finished without extractable output_sql`
- `PERF_0006:spark` → `failed` → `generation_failed` → `method finished without extractable output_sql`
- `PERF_0007:mysql` → `failed` → `generation_failed` → `method finished without extractable output_sql`
- `PERF_0007:spark` → `failed` → `generation_failed` → `method finished without extractable output_sql`
- `CONS_0005:mysql` → `failed` → `generation_failed` → `method finished without extractable output_sql`
- `CONS_0005:spark` → `failed` → `generation_failed` → `method finished without extractable output_sql`

## Distribution

By engine:

- MySQL: `3 failed / 0 generated / 0 preflight_blocked`
- Spark: `3 failed / 0 generated / 0 preflight_blocked`

By case:

- `PERF_0006`: `2 failed`
- `PERF_0007`: `2 failed`
- `CONS_0005`: `2 failed`

This is a **uniform** failure pattern, not an engine-specific split.

## What is no longer the blocker

The retained `run_results.json` shows:

- MySQL preflight = `ok`
- Spark preflight = `ok`

So the current blocker is **not**:

- Java / JPype import
- CalciteRewrite jar layout
- RAG JSONL availability
- formal Chroma visibility
- provider auth visibility

The feasibility audit also already established that the broad MySQL/Spark schema and witness artifacts are not the blocker for these rows.

## Raw response behavior

The retained raw responses do **not** contain final executable rewritten SQL queries.

Observed pattern:

- responses contain strategy clustering lists such as python arrays
- responses contain rule-selection or rule-arrangement explanations
- responses contain narrative strategy summaries
- one response mentions a “final query” conceptually, but still does not emit a fenced or extractable SQL rewrite

There is no retained evidence here that SQL was present and merely missed by the extractor.

## Selected rules and retrieval artifacts

Artifacts exist for all six rows:

- prompts: present
- raw responses: present
- selected rules: present
- retrieval traces: present
- token-cost metadata: present
- provider metadata: present
- row metadata: present

But the selected-rule artifacts do not show usable final rewrite application:

- `selected_rules.available = false` for all six rows
- `used_rules = []` for all six rows

Retrieval traces are present, but they do not change the end result:

- `retrieval_trace.available = true` for all six rows

## Prompt context

Prompt artifacts confirm that target-engine context was injected correctly:

- MySQL rows explicitly say `Target SQL engine: MySQL`
- Spark rows explicitly say `Target SQL engine: Spark SQL`

So the current failure is not explained by missing engine labels in prompt context.

## Root-cause classification

Current best classification:

- **B. prompt/output-contract or recovered-route limitation**

Reason:

- the route reaches generation
- raw responses contain rule lists and strategy text
- raw responses do not contain final executable SQL rewrites
- selected-rule artifacts do not show successful final rewrite application
- there is no evidence that an SQL rewrite existed and was merely missed by the extractor

## Recommendation

Do **not** treat this as an extractor bug.

The next step should **not** be a silent harness patch that assumes SQL is already present. A further bounded patch is only justified if it is framed as an explicit recovered-route / method-design investigation into why the non-PG generation path stops at strategy/rule text instead of final rewritten SQL.

Conservative recommendation:

- stop here for benchmark-evidence purposes
- if work continues, do it as a separate bounded route-design discussion or recovery task

## Boundary

This is:

- generation-only canary evidence

This is **not**:

- execution evidence
- timing evidence
- speedup evidence
- leaderboard evidence
- MySQL/Spark correctness evidence
- MySQL/Spark performance evidence
