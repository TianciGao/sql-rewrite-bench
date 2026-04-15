# First Results Writeup Skeleton

## File role
This file is a writing skeleton for the **first paper-facing results section** based on the current pre-pilot / early-pilot slice.

It is intended to help the team:
- turn current repository state into paper-ready prose,
- separate already-supported claims from still-premature claims,
- and avoid over-claiming full pilot completion.

This file does **not** imply that the repository has reached M2 pilot scale.

---

## 1. Results section scope

The current first-results block should focus on **benchmark characterization and stabilized evidence**, not on full baseline comparison.

At this stage, the strongest evidence already available is:

- a four-pool benchmark structure,
- a clear separation between anchor cases, admitted external cases, and staged drafts,
- tri-engine validation on a stable subset,
- and machine-readable plan artifacts on the current first slice.

The current first-results block should therefore be written as:
**early benchmark evidence from a controlled pre-pilot slice**.

---

## 2. Current strongest claims

The following claims are currently supportable.

### Claim 1 — The benchmark already exhibits a structured multi-pool design
The repository is no longer a loose SQL collection.  
It already contains stable cases across:
- performance,
- longtail,
- consistency,
- and portability.

This should be demonstrated using:
- the case maturity matrix,
- and the source-to-case materialization table.

### Claim 2 — The repository already separates anchor, admitted, and staged lines
The current repository contains:
- stable pilot anchors,
- admitted external common-core cases,
- and staged drafts with different closure levels.

This is useful because it shows the benchmark is being built with maturity control rather than flat aggregation.

### Claim 3 — Tri-engine evidence already exists for a meaningful subset
The first slice already includes multiple cases with PostgreSQL / MySQL / Spark closure.
This provides early support for the benchmark’s correctness-aware and cross-engine orientation.

### Claim 4 — Consistency is already a first-class benchmark dimension
The current first slice includes:
- a dedicated consistency anchor,
- and tri-engine validated staged consistency drafts derived from VeriEQL.

This is already enough to show that correctness is not being treated as an afterthought.

---

## 3. Claims that should NOT be made yet

The following claims should be explicitly avoided in the first writeup:

- that the benchmark has reached full pilot scale,
- that the source universe is fully closed,
- that all pools have balanced coverage,
- that full baseline ranking is ready,
- that broad workload curation is complete,
- or that DSB / Stack query corpus issues have been fully resolved.

These are later-phase claims and should not be implied by first-slice evidence.

---

## 4. Suggested subsection structure

### 4.1 Repository state and first-slice boundary
Explain that the current evaluation slice is intentionally restricted to the most stable currently available cases.

Key points to mention:
- the slice is controlled,
- the slice is not the full benchmark,
- and inclusion is based on stability, not on raw case count.

### 4.2 Case maturity distribution
Use:
- `reports/pilot/admitted_vs_staged_summary_v0.csv`
- `reports/pilot/case_maturity_matrix_v0.csv`

Explain:
- how many anchors exist,
- how many admitted external cases exist,
- how many staged drafts remain,
- and which of them are included in the first slice.

### 4.3 Source-to-case materialization
Use:
- `reports/pilot/source_to_case_mapping_v0.csv`

Explain:
- which source families already materialized into cases,
- which remain substrate-only or target-only,
- and how the benchmark is being built through controlled source-to-case translation rather than flat union.

### 4.4 Engine-validation coverage
Use:
- `reports/pilot/engine_validation_summary_v0.csv`

Explain:
- that the current first slice is intentionally restricted to cases with stronger engine evidence,
- and that tri-engine closure is already available for the first-slice subset.

### 4.5 Interpretation
Conclude the section by emphasizing:
- the benchmark is already structurally meaningful,
- but still pre-pilot in scale,
- and the current evidence is best understood as an early stable slice rather than a final benchmark release.

---

## 5. Draft paragraph skeletons

### 5.1 Opening paragraph
At the current repository stage, the benchmark has not yet reached full pilot scale, but it already supports a stable pre-pilot evaluation slice. Rather than aggregating all currently tracked cases, we intentionally restrict the first reporting slice to the most stable subset, including four pool anchors, two admitted external common-core cases, and two tri-engine validated staged consistency drafts. This choice allows us to report repository structure and engine-closure evidence without overstating benchmark completeness.

### 5.2 Case maturity paragraph
The current repository exhibits a non-flat maturity structure. Specifically, the tracked case universe already separates into stable pilot anchors, admitted external common-core cases, and staged drafts with different closure levels. This stratification is important because it shows that benchmark construction is being controlled through explicit admission and staging logic rather than through simple case accumulation.

### 5.3 Source materialization paragraph
The benchmark is also structured at the source layer. Different source families currently play different roles: some have already materialized into admitted external cases, some have materialized into staged drafts, and some remain target-only or substrate-only sources. This source-to-case distinction is central to the repository design, since source families are treated as raw inputs while case packages remain the true benchmark unit.

### 5.4 Engine-validation paragraph
Although the repository is still early in scale, the first evaluation slice already contains meaningful multi-engine evidence. All cases included in the first slice have stable result and plan artifacts, and the current consistency line now includes tri-engine validated staged drafts. This provides early support for the benchmark’s core emphasis on correctness-aware, cross-engine evaluation.

### 5.5 Closing paragraph
Taken together, these results indicate that the repository has progressed beyond bootstrap and now supports a meaningful pre-pilot benchmark slice. At the same time, the current results should be interpreted conservatively: they demonstrate structural readiness and early evidence, not full pilot completion.

---

## 6. Figure / table references to use

Recommended references in the first writeup:

- Table 1 — Case maturity summary
- Table 2 — Case-level maturity matrix
- Table 3 — Source-to-case materialization map
- Table 4 — Engine-validation summary
- Table 5 — First-slice inclusion / exclusion summary

These should appear before any stronger claims about large-scale benchmark comparison.

---

## 7. Immediate next use
This file should be used to draft:
- the first evaluation subsection,
- the first benchmark-characterization subsection,
- and a compact appendix summary of repository maturity.

It should not yet be used as the basis for a full baseline-comparison section.