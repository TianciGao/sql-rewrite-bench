# LEARNEDREWRITE_LLM4REWRITE_EMBEDDED_PATH_PREFLIGHT_v1

## 0. Purpose And Boundary

This is a no-execution substrate and adapter preflight for the embedded `LearnedRewrite` path bundled inside upstream `LLM4Rewrite`.

It is read-only.
It is not implementation.
It is not execution.
It is not a runnable-baseline claim.
It is not registry writeback.

No LearnedRewrite run, R-Bot run, DB execution, model/API call, or SQLGlot route was executed during this preflight.

## 1. Executive Classification

Classification:
- `embedded_substrate_found_adapter_preflight_possible`

Why:
- the embedded `LearnedRewrite` jar exists
- the Python runner `my_rewriter/test_learned_rewrite.py` exists
- the JPype bridge and Java source path are visible
- the output contract includes `output_sql`
- the remaining gaps are adapter and bounded-runner engineering, not total substrate absence

## 2. Substrate Presence

### 2.1 Embedded jar

- embedded jar directory exists: yes
- embedded jar file exists: yes
- exact path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`

### 2.2 Runner

- `test_learned_rewrite.py` exists: yes
- exact path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_learned_rewrite.py`

### 2.3 Supporting bridge code

- JPype bridge exists:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/rewrite.py`
- Java implementation path exists:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/learned/LearnedRewriter.java`
- helper scripts exist:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_tpch.sh`
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_dsb.sh`
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_calcite.sh`

## 3. Later Command Shape

Visible later command pattern from upstream helper scripts:

```bash
python3 test_learned_rewrite.py --database tpch10 --logdir logs_learned_rewrite
python3 test_learned_rewrite.py --database dsb10 --logdir logs_learned_rewrite
python3 test_learned_rewrite.py --database calcite10 --logdir logs_learned_rewrite
```

For RewriteBench later, the likely bounded command shape would still be:

```bash
python3 test_learned_rewrite.py --database <pg_dbname> --logdir <bounded_logdir>
```

but only after a RewriteBench-specific one-case adapter is added, because the current upstream script scans whole upstream dataset folders and assumes upstream database naming and cache/log layout.

## 4. Input Contract

### 4.1 What the current runner expects

From `test_learned_rewrite.py`, the runner expects:

- `--database`
  - used both as PostgreSQL database name and dataset selector
- `--logdir`
  - default `logs_learned_rewrite`
- optional `--large`
- an existing JSONL log file at:
  - `os.path.join(logdir, database, 'res.jsonl')`
- schema file resolved from dataset family:
  - `../calcite/create_tables.sql`
  - `../tpch/create_tables.sql`
  - `../dsb/create_tables.sql`
- queries from upstream dataset layout:
  - `../calcite/calcite.jsonl`
  - or `../tpch/<template>/<template>_<idx>.sql`
  - or `../dsb/<template>/<template>_<idx>.sql`
- PostgreSQL connection parameters from `init_db_config(database)`
- JPype/JVM access to the embedded Calcite/LearnedRewrite jar
- cache file path via `cache/<dbname>.jsonl`

### 4.2 What the Java path expects

From `LearnedRewriter.learnedRewrite(...)`, the Java side takes:

- query SQL text
- list of `CREATE TABLE` statements
- search budget
- PostgreSQL host
- PostgreSQL port
- PostgreSQL user
- PostgreSQL password
- PostgreSQL database name

This means the embedded path is not just pure offline Calcite rewriting. It is Calcite/JVM plus PostgreSQL cost access.

## 5. Output Contract

### 5.1 Does it output SQL directly?

- yes

Visible output fields in `test_learned_rewrite.py`:

- `input_sql`
- `input_cost`
- `output_sql`
- `output_cost`
- `used_rules`
- `rewrite_time`

Visible Java emission in `CalciteRewrite/src/learned/LearnedRewriter.java`:

- `dataJson.put("output_sql", outputSql(sqlAfter));`

### 5.2 Where is `output_sql` captured?

- directly in `test_learned_rewrite.py` into `out_dict['output_sql']`
- appended to:
  - `LOG_FILENAME = os.path.join(args.logdir, DATABASE, 'res.jsonl')`
- also visible as a core field in later analysis scripts such as:
  - `my_rewriter/analyze_learned_rewrite.py`

So the output SQL path is visible and machine-capturable.

## 6. Runtime Dependency Interpretation

### 6.1 Does it require PostgreSQL?

- yes

Reasons:

- `test_learned_rewrite.py` calls `init_db_config(args.database)` and builds `DBArgs`
- `my_rewriter/database.py` uses `psycopg2.connect(...)`
- Java `LearnedRewriter.learnedRewrite(...)` opens a PostgreSQL-backed `DBConn`
- both input and output costs are computed against PostgreSQL

### 6.2 Does it require Calcite/JVM only?

- no

More accurate statement:

- it requires Calcite/JVM plus PostgreSQL

### 6.3 Does it require model/API?

- no, based on the visible embedded LearnedRewrite path

Notes:

- `test_learned_rewrite.py` imports `OpenAI` and `Settings`, but does not invoke `init_llms()` or any visible model-backed rewrite path
- the active rewrite call is `learned_rewrite(...)` from the JPype/Java bridge
- no visible OpenAI/API dependency is required for the embedded LearnedRewrite execution path itself

## 7. PERF_0006 Mapping Feasibility

### 7.1 Can `PERF_0006` be mapped into the current contract?

- yes, but only with a dedicated adapter

Why:

- RewriteBench already has:
  - `source.sql`
  - PostgreSQL DDL
  - PG witness/data files
- the Java bridge contract only fundamentally needs:
  - one SQL query
  - a list of `CREATE TABLE` statements
  - PostgreSQL connection info

### 7.2 Why is an adapter still needed?

The current upstream runner does not take a single arbitrary SQL file directly. It assumes:

- dataset-root scanning
- dataset-family naming from `--database`
- pre-existing log file layout
- upstream `create_tables.sql` placement
- upstream multi-query template traversal

So `PERF_0006` is adaptable, but not directly runnable through the current script without a bounded single-case adapter or wrapper.

## 8. First Smoke Shape

Would the first smoke be 1-case PG-only?

- yes, that is the appropriate RewriteBench first smoke shape

More precisely:

- one case only: `PERF_0006`
- PostgreSQL only
- no model/API
- no speedup initially
- candidate generation plus PG checker handoff only

That matches the visible runtime contract better than trying to adopt upstream whole-dataset loops.

## 9. Remaining Blockers Before Execution

Remaining blockers:

1. bounded single-case adapter does not exist yet
   - current upstream runner is dataset-loop oriented, not case-package oriented
2. current runner assumes existing log file path
   - `logs_learned_rewrite/<database>/res.jsonl` is opened for read before append
3. current runner binds `--database` to both dataset identity and PostgreSQL dbname
   - RewriteBench will need a controlled mapping strategy
4. current runner expects upstream schema/query folder layout
   - RewriteBench needs a direct mapping from `PERF_0006` files into `query` plus `create_tables`
5. bounded artifact capture path is not yet implemented
   - generated SQL, stdout/stderr, checker handoff JSON, and failure diagnostics need RewriteBench-local paths
6. PostgreSQL runtime still has to be scoped to the LearnedRewrite path
   - not generic PG availability, but the exact DB/schema strategy for this baseline
7. output claim boundary is not yet frozen
   - need explicit bounded non-leaderboard, non-speedup first-smoke contract

These are adapter/run-contract blockers, not substrate-absence blockers.

## 10. Direct Answers To Requested Questions

1. Does the embedded LearnedRewrite jar exist?
   - yes
2. Does `test_learned_rewrite.py` exist?
   - yes
3. What command would run it later?
   - `python3 test_learned_rewrite.py --database <dbname> --logdir <logdir>`
   - upstream examples use `tpch10`, `dsb10`, `calcite10`
4. What inputs does it expect?
   - SQL query text, schema `CREATE TABLE` statements, budget, PostgreSQL connection info, upstream dataset/log layout
5. Does it output SQL directly?
   - yes
6. Where is `output_sql` captured?
   - Java `LearnedRewriter.java` emits it; Python `test_learned_rewrite.py` writes it to `res.jsonl`
7. Does it require PostgreSQL?
   - yes
8. Does it require Calcite/JVM only?
   - no; it requires Calcite/JVM plus PostgreSQL
9. Does it require model/API?
   - no, from the visible embedded LearnedRewrite path
10. Can `PERF_0006` be mapped into its input contract?
   - yes, with a dedicated single-case adapter
11. Would the first smoke be 1-case PG-only?
   - yes
12. What blockers remain before execution?
   - bounded single-case adapter, log/layout handling, dbname/dataset mapping, artifact capture, and exact PG scoping

## 11. Recommended Next Step

- implement a documentation-scoped single-case adapter preflight for embedded `LearnedRewrite`

Reason:

- the substrate is present
- the output SQL path is visible
- the main remaining uncertainty is the RewriteBench wrapper contract, not whether a runnable embedded baseline exists at all

## 12. Non-Modification Note

No execution occurred.
No model/API was called.
No PostgreSQL query was run.
No R-Bot path was run.
No LearnedRewrite path was run.
No SQLGlot route was run.
No case files, registry files, review files, rules, `docs/EXECUTION_STATUS.md`, or taxonomy notes were modified.
