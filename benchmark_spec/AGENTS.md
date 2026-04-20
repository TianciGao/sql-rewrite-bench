# AGENTS.md

## What this directory contains

This directory contains **benchmark protocol, rules, and review records**.

Typical files include:

- `benchmark_spec_v0.md`
- `decision_log.md`
- `CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `common_core_extended_rules_v0.md`
- review files under `benchmark_spec/reviews/` if present

These files are not ordinary notes.
They define benchmark boundaries, rule semantics, and project-level review logic.

---

## 1. Directory-specific distinctions

### 1.1 Archetype completion is not admission
A case may be archetype-complete without being admitted.

Do not infer:

> archetype_complete = admitted

### 1.2 Common-core / extended is not primary pool
`common-core` / `extended` is a reporting / comparison line.
It does not replace pool assignment such as:

- performance
- longtail
- consistency
- portability

### 1.3 Review records are not live fact tables
Review files explain what was judged at that time.
They do not override current registry state.

If review prose conflicts with live case facts, prefer:

- `inventory/case_registry.csv` for current case facts
- `docs/EXECUTION_STATUS.md` for current stage interpretation
- `benchmark_spec/decision_log.md` for frozen decisions

---

## 2. Modification rules in this directory

### 2.1 Do not casually modify rule files
Do not modify the following without explicit human approval:

- `benchmark_spec_v0.md`
- `decision_log.md`
- `CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `common_core_extended_rules_v0.md`

### 2.2 Review files may be updated only when explicitly asked
Review files may be updated when the task is explicitly about:

- recording a review outcome
- consolidating review history
- aligning review prose with a human-approved decision

Do not use review-file edits as a shortcut for changing live status.

---

## 3. How to use review files

Review files belong to the **review-history layer**.

Use them to answer:

- what judgment was recorded
- what rationale was given
- what metadata consequence was expected

Do not use them as the only source for current live case status.

If a review outcome changes live case state, update order should be:

1. relevant review file
2. `benchmark_spec/decision_log.md` if needed
3. `inventory/case_registry.csv`
4. `docs/EXECUTION_STATUS.md` if the representative snapshot changes

---

## 4. Before editing this directory

Before editing files here, re-read:

- root `AGENTS.md`
- `docs/DOC_MAP.md`
- `benchmark_spec/decision_log.md`

If the task touches a specific case or review outcome, also read:

- `inventory/case_registry.csv`
- the relevant review file(s)

---

## 5. Stop-and-ask conditions

Stop and ask a human before:

- changing benchmark scope
- changing engine set
- changing primary metrics
- changing admission thresholds
- changing archetype-completion meaning
- changing common-core / extended meaning
- introducing a new status label
- treating a review note as a policy change

---

## 6. Bottom line

Inside `benchmark_spec/`, stability matters more than convenience.

When in doubt:

> preserve frozen protocol, treat reviews as reviews, and keep live facts in registries.