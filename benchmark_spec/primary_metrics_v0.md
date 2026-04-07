# Primary Metrics v0

## 1. Role of this document

This file defines the **primary metrics** for the current benchmark version.

Its purpose is to:
- fix the main scoring dimensions before larger benchmark expansion
- prevent post-hoc metric selection
- make future experiment reporting comparable across pools and cases
- give CLI / reports / artifact-preflight a stable metric target

This file does **not** define every possible diagnostic metric.
It only defines the metrics that should be treated as the primary scorecard for v0 / early pilot.

For full project scope, see `docs/PROJECT_PLAN.md`.
For current executable boundary, see `benchmark_spec/benchmark_spec_v0.md`.

---

## 2. Current metric philosophy

The benchmark is not a single-score benchmark.

The current benchmark evaluates four first-class dimensions:

1. correctness
2. performance
3. plan observability
4. generalization

These four dimensions are treated as co-equal top-level groups.
No single scalar score is used to replace them in v0.

---

## 3. Primary metric groups

## 3.1 Correctness

### result_consistency_rate
**Definition**  
Fraction of evaluated positive rewrites whose results match the source query under the defined checker.

**Purpose**  
This is the main correctness metric for positive rewrites.

### negative_rejection_rate
**Definition**  
Fraction of negative rewrites correctly identified as non-equivalent by result comparison and/or benchmark checking logic.

**Purpose**  
This is the main correctness metric for negative rewrites.

### Why correctness is primary
A SQL rewrite benchmark must not evaluate only speedup.
A rewrite that changes results is not a valid success.

---

## 3.2 Performance

### gm_speedup
**Definition**  
Geometric-mean speedup of valid positive rewrites against the source query on the evaluated case subset.

**Purpose**  
Primary summary metric for performance gain.

### regression_rate
**Definition**  
Fraction of positive rewrites whose runtime becomes worse than the source query beyond the accepted threshold.

**Purpose**  
Captures harmful rewrites rather than only average win behavior.

### Reporting note
Performance metrics must be reported only on cases that have passed the required correctness gate for the relevant comparison.

---

## 3.3 Plan Observability

### node_alignment_coverage
**Definition**  
Fraction of evaluated cases for which source / rewrite plan differences can be mapped to the benchmark’s normalized plan operator space.

**Purpose**  
Main indicator for whether the benchmark can support plan-level interpretation.

### Reporting note
This metric is not a speed metric.
It is an interpretability / observability metric.

---

## 3.4 Generalization

### cross_engine_executable_rate
**Definition**  
Fraction of intended cross-engine or cross-dialect cases that remain executable in their declared target setting.

**Purpose**  
Primary metric for portability at the execution level.

### cross_engine_consistency_rate
**Definition**  
Fraction of intended cross-engine or cross-dialect cases whose outputs remain semantically consistent after translation / adaptation.

**Purpose**  
Primary metric for portability at the semantic level.

---

## 4. Secondary metrics (non-primary, allowed but not required)

The following may be reported as supporting metrics, but they are not the primary scorecard in v0:

- win / tie / loss
- p95 regression tail
- bottleneck removal rate
- operator delta diversity
- attribution agreement
- verifier support rate
- speedup transfer rate
- dialect portability coverage

These may be promoted later if the benchmark matures.

---

## 5. Current reporting rule

For the current version, benchmark results should be reported in the following order:

1. correctness
2. performance
3. plan observability
4. generalization

The benchmark should not claim success on performance if correctness fails.

---

## 6. Current freeze

For v0 / early pilot, the following are frozen as primary metrics:

- result_consistency_rate
- negative_rejection_rate
- gm_speedup
- regression_rate
- node_alignment_coverage
- cross_engine_executable_rate
- cross_engine_consistency_rate

Any change to this list should be recorded in `benchmark_spec/decision_log.md`