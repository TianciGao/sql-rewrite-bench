# AGENTS.md

## What this directory contains

This directory contains **case packages**.

A case package is the minimum benchmark unit.
It is not just a SQL file.
It should preserve enough structure for execution, checking, plan collection, and later reuse.

Typical case-local artifacts may include:

- `manifest.yaml`
- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- provenance files
- `taxonomy_trial_v0.2.yaml`
- `data_profile.json`
- plan artifacts
- validation artifacts
- notes

---

## 1. What a case package is for

A case package should make it possible to answer:

- what is the source query
- what is the positive rewrite
- what is the negative rewrite
- what data / witness strategy is used
- what plans were collected
- what checker or result-comparison path exists
- what evidence supports its current maturity

Do not reduce a case directory to “just a few SQL files”.

---

## 2. Core distinctions

### 2.1 A case can exist without being admitted
A case may be:

- draft_constructed
- witness_validated
- archetype_complete
- common-core candidate
- admitted common-core

Do not collapse these.

### 2.2 Case-local completeness is different from project-level admission
A well-shaped case package does not automatically imply promotion or admission.

### 2.3 Pool role and reporting line are different
A case belongs to a pool such as:

- performance
- longtail
- consistency
- portability

But its reporting line may be:

- common-core
- extended
- staging / not_yet_admitted

Do not mix these dimensions.

---

## 3. Before editing a case

Before editing a case package, read:

1. root `AGENTS.md`
2. `docs/EXECUTION_STATUS.md`
3. `inventory/case_registry.csv`
4. `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
5. `benchmark_spec/common_core_extended_rules_v0.md`

If the case has review history, also inspect the relevant review record.

---

## 4. Allowed work in this directory

Allowed work includes:

- case-local artifact completion
- provenance cleanup
- manifest cleanup
- taxonomy file completion
- data-profile completion
- plan collection
- validation artifact generation
- checker-path clarification
- non-semantic organization cleanup

---

## 5. Disallowed work without human approval

Do not do the following without explicit human approval:

- create new benchmark cases beyond approved scope
- rename case IDs casually
- change primary pool semantics
- declare admission in case-local prose without review basis
- invent new maturity labels
- redefine the meaning of common-core / extended
- rewrite benchmark protocol from inside a case directory

---

## 6. Case-local discipline

Each case should preserve:

- stable case ID
- explicit provenance
- frozen source layer
- clear rewrite layer
- reproducible data / witness strategy
- actual execution evidence
- plan artifacts
- taxonomy layer
- machine-readable profile artifact
- checker or explicit comparison workflow when relevant

These are aligned with archetype-completion expectations.

---

## 7. Case update protocol

If you edit a case package:

1. update case-local files
2. update or regenerate relevant artifacts
3. update `inventory/case_registry.csv` if case facts changed
4. update `docs/EXECUTION_STATUS.md` if this case is part of the representative snapshot
5. update review records only if a real review-level judgment is being recorded

Do not stop at case-local edits if registry facts changed.

---

## 8. Minimal validation expectation

When a case changes, confirm at least:

- the relevant files exist
- the manifest remains parseable
- result evidence still supports the stated behavior
- the plan artifacts are still present if claimed
- the registry row still matches the case directory reality

---

## 9. Pool-sensitive expectations

Different pools emphasize different strengths:

- performance → stable analytical source, cross-engine execution, rewrite behavior, plan observability
- longtail → structural richness, syntax / logic coverage, controlled witness sensitivity
- consistency → source / positive / negative semantic distinction with explicit witness logic
- portability → source-side / target-side behavior and divergence under dialect change

Do not force every case into the same interpretation without regard to pool purpose.

---

## 10. Stop-and-ask conditions

Stop and ask a human before:

- creating a new case
- deleting a case
- renaming a case ID
- changing a case's pool
- changing a case's promotion / admission status without review basis
- moving a case from staging to common-core / extended without registry and rule alignment
- replacing evidence-backed artifacts with speculative placeholders

---

## 11. Bottom line

This directory is where benchmark units live.

When in doubt:

> keep the case package evidence-backed, keep the registry aligned, and do not confuse local completeness with project-level admission.