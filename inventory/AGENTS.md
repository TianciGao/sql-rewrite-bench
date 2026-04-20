# AGENTS.md

## What this directory contains

This directory contains **machine-readable live registries**.

These files are the live source-of-truth for operational source / case facts.

Typical files:

- `source_registry.csv`
- `case_registry.csv`

Do not treat these as narrative documents.
They are structured fact tables.

---

## 1. Registry roles

### 1.1 Source registry
`source_registry.csv` answers:

- which sources are active
- which sources are only target / planned
- which sources are partial-realized
- which sources back real cases
- how a source should currently be interpreted

### 1.2 Case registry
`case_registry.csv` answers:

- current case maturity
- current benchmark line / dataset line
- package engineering status
- validated engines
- closure state
- promotion / admission status
- next gap / blockers

If a question is about **current case facts**, prefer `case_registry.csv` over prose.

---

## 2. Registry-first discipline

If live facts change, update the registry first.

### 2.1 Source fact changes
Examples:
- inspection status changes
- source becomes active
- source becomes partial-realized
- source becomes current-phase relevant

Update order:

1. `source_registry.csv`
2. `docs/EXECUTION_STATUS.md` if interpretation changes
3. `benchmark_spec/decision_log.md` only if a frozen decision is involved

### 2.2 Case fact changes
Examples:
- validated engines change
- package engineering status changes
- benchmark line changes
- next gap changes
- promotion status changes
- admission status changes

Update order:

1. `case_registry.csv`
2. case-local files / artifacts if needed
3. `docs/EXECUTION_STATUS.md` if representative snapshot changes
4. review documents / decision log if required

---

## 3. Minimum quality rule for registry edits

Every registry edit should satisfy three conditions:

1. it reflects a concrete fact or evidence-backed judgment
2. it is consistent with the current rules and review basis
3. it leaves the row more machine-readable, not less

Do not replace structured fields with vague prose.

---

## 4. Expected discipline for case registry rows

A case row should help answer:

- what this case is
- where it came from
- what status it is currently in
- what evidence exists
- what is still missing

If a row changes, the update should keep those questions answerable.

---

## 5. Review-aware registry behavior

Review records may justify changes, but registries remain the live fact layer.

Examples:

- promotion review may justify `promotion_status`
- admission check may justify `admission_status`
- common-core / extended review may justify `dataset_line`

But the review file itself is not enough.
The registry must still be updated.

---

## 6. After-registry-edit checks

After editing a registry, do the following:

1. review the diff
   - `git diff -- inventory/source_registry.csv inventory/case_registry.csv`

2. make sure no contradictory narrative files remain unstaged

3. if the edit changes current interpretation, update:
   - `docs/EXECUTION_STATUS.md`

4. if the edit changes a frozen decision or reviewed status, update:
   - relevant review file
   - `benchmark_spec/decision_log.md` if needed

5. run:
   - `git status --short`

If a stable CLI registry check exists later, use that as well.

---

## 7. What not to do

Do not:

- treat registry rows as long narrative paragraphs
- use review prose as a substitute for registry updates
- update only status prose while leaving registry stale
- infer admission from execution success without review basis
- infer common-core from “interestingness”

---

## 8. Stop-and-ask conditions

Stop and ask a human before:

- adding new registry columns
- removing registry columns
- changing controlled vocabularies
- changing status label semantics
- making a promotion / admission change without clear review basis
- backfilling large sets of rows using guesswork

---

## 9. Bottom line

This directory is the live fact layer.

When in doubt:

> update the registry first, keep it structured, and make prose follow the facts rather than replace them.