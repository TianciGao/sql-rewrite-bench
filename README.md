# SQL-RewriteBench

SQL-RewriteBench is a benchmark and artifact package for **statement-level SQL rewriting**. It does not evaluate hidden optimizer-rule traces or internal AST transformations as the primary output. It evaluates the emitted SQL statement that a rewrite method returns, together with the context needed to execute, check, diagnose, and reproduce that result.

The central question is not only whether a rewritten SQL query is faster. The benchmark asks:

- Did the method emit a candidate SQL statement?
- Does the candidate parse and execute on the declared engine?
- Does execution preserve the source-query semantics under the case checker?
- Is the output a meaningful rewrite, or only a no-op / source-like fallback?
- Is performance interpreted only after correctness is established?
- Does a cross-engine or cross-dialect result execute and remain consistent on the target engine?
- Are failures, regressions, and claim boundaries visible in the artifact?

The current repository state should be read as a **Common-core v0 paper-facing evidence and reproducibility bundle**, not as a final global leaderboard.

---

## 1. Current status

Current focus:

- Common-core v0 denominator: **40 case packages**.
- Same-engine Track A expansion: **40 cases × 3 engines = 120 rows**.
- Pool split: **16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL**.
- Main paper table style: **denominator-aware evidence ledger**, not a ranked leaderboard.
- Reviewer-facing static reproduction path is available through:

```bash
bash scripts/reproduce_common_core_v0.sh --mode artifact
```

The artifact-mode path regenerates the retained Table 12 evidence ledger and checks expected boundaries. It does **not** run DB engines, LLM/API calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection.

---

## 2. What SQL-RewriteBench evaluates

A benchmark unit is a **case package**, not a bare SQL string. A case package may include:

```text
cases/<POOL>/<CASE_ID>/
  manifest.yaml
  source.sql
  rewrite_pos_01.sql
  rewrite_neg_01.sql
  schema/
  validation/
  runs/
  provenance / notes / checker metadata / taxonomy tags
```

A case package is intended to carry:

- source SQL;
- trusted positive rewrite or target adaptation;
- hard negative or correctness guard;
- schema and witness/data context;
- result checker and normalization policy;
- execution and plan artifacts when available;
- provenance;
- 4+1 taxonomy tags;
- reporting and claim-boundary metadata.

This lets the benchmark separate method behavior from case support boundaries. A method failure, an unsupported engine combination, a checker mismatch, a no-op fallback, and a timing gap should remain visible rather than disappearing from the denominator.

---

## 3. Research questions

SQL-RewriteBench is organized around three research questions.

**RQ1 — Correctness.** How can we evaluate whether a statement-level SQL rewrite preserves semantics, especially across diverse and long-tail SQL structures?

**RQ2 — Observability.** How can rewrite outcomes expose enough evidence for diagnosis, instead of reporting only a latency label?

**RQ3 — Generalization.** How can SQL rewrite or adaptation be evaluated across dialects and engines beyond parser acceptance or single-engine success?

---

## 4. Common-core v0 denominator

Common-core v0 is a controlled coverage surface. It is not a workload-frequency sample.

| Pool | Cases | Same-engine rows | Main pressure | Paper role |
|---|---:|---:|---|---|
| PERF | 16 | 48 | performance-sensitive analytical rewrites | correctness-gated speedup, regressions, tool-route comparison |
| CONS | 9 | 27 | semantic edges, NULL/multiplicity/aggregation, hard negatives | correctness, false-accept guard, checker stress |
| PORT | 9 | 27 | dialect and engine-boundary risks | target execution / consistency, portability boundaries |
| LONGTAIL | 6 | 18 | realistic or structurally uncommon SQL | robustness and failure diagnosis |
| **Total** | **40** | **120** | mixed | main controlled denominator |

The denominator is designed to make failure modes visible. Unsupported rows, preflight-blocked rows, failed generations, parse failures, execution failures, mismatches, no-op/source-like outputs, and timing gaps are all part of the evidence.

---

## 5. 4+1 taxonomy

SQL-RewriteBench uses a 4+1 taxonomy for coverage characterization and failure slicing:

1. **SQL feature** — CTEs, correlated subqueries, outer joins, windows, date/time functions, expression complexity, etc.
2. **Plan operator** — scan, filter, project, join, aggregate, sort, limit, window, materialization/exchange, etc.
3. **Workload realism** — classic analytical baseline, realistic query style, long-tail structure, controlled semantic cases, etc.
4. **Portability risk** — identifier quoting, type semantics, datetime semantics, NULL semantics, limit/fetch gaps, function signatures, etc.
5. **Rewrite opportunity** — predicate pushdown, subquery decorrelation, aggregation rewrite, function normalization, dialect adaptation, materialization strategy, etc.

The taxonomy is not a score and is not used to rank methods. It explains what the denominator stresses and how failures should be sliced.

---

## 6. Baseline roles

Baselines are role-aware. They should not be collapsed into a single speed leaderboard.

| Role | Examples | Placement |
|---|---|---|
| Source / control | Native SQL, human positive rewrite, hard-negative guard | Controls and correctness tables |
| Same-engine rewrite | Direct LLM, Direct LLM + Repair-1, SQLGlot optimize, SQLGlot no-op, Calcite HEP | Track A evidence ledger |
| Bounded prior-method evidence | R-Bot, LLM-R2, LearnedRewrite | Appendix / bounded evidence |
| Portability / translation | SQLGlot Transpile, LLM Translate | Track C portability table |
| Support / verifier | SQLSolver, VeriEQL | Support table only |
| Observability | plan frontier, failure artifacts, plan deltas | Support / case-study evidence |

Verifier tools do not emit rewritten SQL. Portability routes do not answer same-engine speedup. No-op routes test infrastructure and low-transform behavior, not optimizer strength.

---

## 7. Current result summary

### 7.1 Denominator-aware method evidence

The retained Table 12 ledger is a route-aware evidence table. It is not a final leaderboard.

| Method / route | Scope | Planned | Generated / ready | Executed | Exact | Timed | GM | Regression@20 | Placement |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| Direct LLM original | tri-engine same-engine | 120 | 120 generated; 115 ready | 99 | 94 | 94 | 1.0436 | 3.19% | main same-engine evidence |
| Direct LLM + Repair-1 | tri-engine feedback route | 120 | 120 generated; 5 preflight-blocked | 97 | 96 | 96 | 1.0431 | 4.17% | route-level evidence; mixed-source timing |
| SQLGlot optimize | tri-engine route | 120 | 120 attempted; 75 generated | 65 | 63 | 63 | 0.9907 | 1.59% | revised exact63 route |
| SQLGlot no-op | tri-engine route | 120 | 120 attempted; 78 generated | 72 | 72 | 72 | 1.0001 | 1.39% | no-op / low-transform route |
| Calcite HEP fail-closed | tri-engine fail-closed route | 120 | retained route artifacts | 95 | 93 | 93 | 0.9959 | 7.53% | correctness-gated timing packet |
| R-Bot | mixed scope | formal 120 generation | PG-scoped subsets | 15 PG-only | 15 PG-only | 15 | 0.9218 | 20.00% | bounded / mixed appendix |
| LLM-R2 original | PG-only bounded | 9 | 9 | 3 exact + 6 execution failed | 3 | 0 | NA | NA | bounded appendix |
| LLM-R2 recovered | PG9 recovery audit | 9 | 9 | 6 | 6 | 0 | NA | NA | PG6 exact recovered subset |
| LearnedRewrite | PG10 bounded | 10 | 10 | NA_not_retained | 10 checker-consistent | NA | NA | NA | bounded appendix; 8 source-like/no-op |

### 7.2 Main findings

1. **Generated-subset and executed-subset reporting can overstate method quality.** The benchmark keeps planned, generated, executed, exact, and timed denominators separate.
2. **Hard-negative guardrails are necessary.** In the retained Common-core v0 hard-negative ledger, 111 tested hard-negative cells are executable semantic mismatches and all are rejected; false accepts are 0.
3. **Correctness is required before speed is meaningful, but correctness does not guarantee speedup.** Several exact timed slices are near parity or contain regressions.
4. **No-op / source-like fallback must remain visible.** Correct but low-transform outputs should not be counted as useful rewrite improvement.
5. **Cross-engine generalization must be layered.** Target execution and result consistency do not imply SpeedupTransferRate readiness.
6. **Verifier tools are support evidence, not rewrite baselines.** SQLSolver and VeriEQL are reported separately from rewrite-generation methods.

---

## 8. What not to claim

Do not claim:

- a final global leaderboard;
- a universal winner;
- production workload representativeness;
- full PORT9 or full registry portability closure;
- computed SpeedupTransferRate;
- full denominator-wide NodeAlignmentCoverage;
- full verifier coverage over all Common-core cases;
- that support tools such as SQLSolver / VeriEQL are rewrite speed baselines.

Supported wording:

- “denominator-aware method evidence ledger”;
- “correctness-gated speedup slices”;
- “bounded PORT6 execution / consistency evidence”;
- “selected-frontier observability”;
- “support-layer verifier evidence”;
- “not a ranked leaderboard.”

---

## 9. Repository layout

Recommended high-level layout:

```text
cases/                         # case packages
reports/evaluation/common_core_v0/
  08_SECTION8_EVIDENCE_FREEZE_V1/
  09_TAXONOMY_COVERAGE_V1/
  10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/
  11_TIMING_OBSERVABILITY_V1/
  12_PORT_VERIFIER_ARTIFACT_MAP_V1/
  14_REPRODUCIBILITY_MANIFEST_V1/
  15_PROGRAMMATIC_METRIC_AUDIT_V1/
  16_STATIC_RECOMPUTE_AUDIT_V1/
  17_TABLE12_ULTIMATE_PROVENANCE_V1/
  18_TABLE12_REGENERATION_V1/
  19_SPEEDUP_SUMMARY_REGENERATION_V1/
  scripts/
scripts/
  reproduce_common_core_v0.sh
```

Important report directories:

| Directory | Purpose |
|---|---|
| `08_SECTION8_EVIDENCE_FREEZE_V1` | Section 8 evidence source map and missing-data ledger |
| `09_TAXONOMY_COVERAGE_V1` | Common-core v0 taxonomy coverage artifacts |
| `10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1` | hard-negative guardrail and candidate failure accounting |
| `11_TIMING_OBSERVABILITY_V1` | method timing rows and speedup slice summaries |
| `12_PORT_VERIFIER_ARTIFACT_MAP_V1` | PORT bounded closure, verifier support, artifact index |
| `14_REPRODUCIBILITY_MANIFEST_V1` | environment and route metadata manifest |
| `15_PROGRAMMATIC_METRIC_AUDIT_V1` | metric-to-artifact trace and recompute readiness audit |
| `16_STATIC_RECOMPUTE_AUDIT_V1` | independent static recomputation results |
| `17_TABLE12_ULTIMATE_PROVENANCE_V1` | Table 12 cell provenance and dependency graph |
| `18_TABLE12_REGENERATION_V1` | regenerated Table 12 outputs and diff summary |
| `19_SPEEDUP_SUMMARY_REGENERATION_V1` | regenerated speedup summary outputs |

---

## 10. Reviewer reproduction path

### 10.1 Artifact-only smoke reproduction

Use this path to verify the retained paper evidence without running databases, LLMs, verifier tools, EXPLAIN collection, PORT9, or new timing collection.

```bash
cd /path/to/sql-rewrite-bench

bash scripts/reproduce_common_core_v0.sh --mode artifact
```

Expected high-level outcome:

```text
Reviewer reproduction artifact-mode passed.
Table 12 regenerated successfully.
cells_compared=90
exact_match=55
expected_NA_match=8
artifact_boundary_match=27
conflicts=0
missing_input=0
```

### 10.2 Table 12 direct static check

```bash
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

Expected high-level outcome:

```text
rows rendered: 9
cells compared: 90
exact matches: 55
expected NA matches: 8
artifact boundary matches: 27
conflicts: 0
```

### 10.3 Deterministic dry-run and preflight

Before executing deterministic runners, inspect and preflight them:

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight --steps table12
```

The `table12` step is static and should not require DB execution.

---

## 11. Full deterministic reproduction channel

The deterministic execution path is for configured machines. It may require PostgreSQL, MySQL, Spark, local schemas/data, timing policy, and retained route artifacts. Run preflight first.

### 11.1 Re-run deterministic runners

```bash
# 1. Rerun deterministic runners.
# These steps may require configured local DB engines and retained artifacts.

bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps hard-negative
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps sqlglot
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps calcite
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps pg-plan
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps direct-llm-timing-retained
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps rbot-pg15-timing
```

Optional: run only one selected step first:

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run --steps table12
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight --steps table12
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps table12
```

### 11.2 Regenerate speedup summary from retained timing rows

```bash
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check
```

Primary output:

```text
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regenerated_v1.csv
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_diff_v1.csv
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_readme_v1.md
```

### 11.3 Regenerate Table 12

```bash
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

Primary output:

```text
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.csv
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_diff_v1.csv
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_readme_v1.md
```

### 11.4 Inspect regenerated Table 12

```bash
sed -n '1,120p' \
  reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
```

---

## 12. Speedup-to-Table-12 dataflow

The Table 12 timing columns are intentionally derived through a static artifact chain.

```text
method_timing_case_level_v1.csv / timing_event_long.csv
        ↓
render_speedup_slice_summary_v1.py
        ↓
speedup_slice_summary_regenerated_v1.csv
        ↓
render_table12_method_evidence_ledger_v1.py
        ↓
Table 12 Timed / GM / Regression@20
```

Main retained inputs include:

```text
reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/method_timing_case_level_v1.csv
reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv
reports/evaluation/common_core_v0/runs/*/timing_event_long.csv       # when available in full local artifact workspaces
```

Static regeneration outputs:

```text
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regenerated_v1.csv
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.csv
```

Interpretation rule:

- `Timed` is the route-local exact-and-timing-success denominator.
- `GM` is the geometric mean speedup over the route-local exact timed rows.
- `Regression@20` is the fraction of exact timed rows with harmful slowdown under the retained threshold.
- These values are not comparable across routes unless route role, denominator, engine scope, and timing scope are aligned.

---

## 13. Environment notes

Artifact-only reproduction should work from a clean checkout with Python and Bash.

Deterministic execution may require:

- PostgreSQL;
- MySQL;
- Spark SQL;
- Python environment with project dependencies;
- Java/JVM where needed by Calcite/Spark routes;
- local schema/data setup;
- configured engine environment variables;
- retained route outputs for retained-timing paths.

Suggested local setup pattern:

```bash
cd /path/to/sql-rewrite-bench
source .venv/bin/activate

# Optional, depending on local setup.
source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh
```

Run preflight before execution:

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight
```

---

## 14. Source-of-truth and governance

This repository distinguishes facts, rules, status, and paper-facing artifacts.

| Layer | Files | Role |
|---|---|---|
| Case/source live facts | `inventory/case_registry.csv`, `inventory/source_registry.csv` | machine-readable object state |
| Current status | `docs/EXECUTION_STATUS.md` | interpretation dashboard |
| Long-term plan | `docs/PROJECT_PLAN.md` | research plan and scope |
| Benchmark rules | `benchmark_spec/*.md` | rules, metrics, admission/common-core boundaries |
| Review history | `benchmark_spec/reviews/*.md` | review-prep and historical judgment |
| Paper evidence | `reports/evaluation/common_core_v0/*` | retained evidence and paper table regeneration |

Do not update narrative status without checking whether case/source facts changed. Do not change protocol, metrics, registry admission status, or benchmark claims as part of a reproduction-only update.

---

## 15. Development and review discipline

Safe artifact/reproduction updates should:

- avoid `git add .`;
- avoid committing `reports/evaluation/common_core_v0/runs/...` unless the task explicitly requires retained run artifacts;
- avoid changing `inventory/`, `benchmark_spec/`, or `docs/EXECUTION_STATUS.md` unless the task is a source-of-truth update;
- run `git diff --check`;
- run `bash scripts/reproduce_common_core_v0.sh --mode artifact` for reviewer-facing table reproduction changes;
- run `python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check` for Table 12 changes;
- preserve claim boundaries such as `SpeedupTransferRate = NA` and `full NodeAlignmentCoverage = future work`.

Recommended staging checks:

```bash
git diff --cached --check

git diff --cached --name-only | grep '^reports/evaluation/common_core_v0/runs/' \
  && echo "BAD: runs files staged" \
  || echo "OK: no runs files staged"

git diff --cached --name-only | grep -E '^(inventory/|benchmark_spec/|docs/EXECUTION_STATUS.md)$' \
  && echo "BAD: source-of-truth file staged" \
  || echo "OK: no registry/protocol/status files staged"
```

---

## 16. One-sentence summary

SQL-RewriteBench is a correctness-first, observable, cross-engine-aware SQL rewrite benchmark. Its current Common-core v0 artifact reports denominator-aware evidence rather than a single winner, and provides a reviewer-facing path to regenerate the retained Table 12 evidence ledger from tracked artifacts.
