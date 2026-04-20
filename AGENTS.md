# AGENTS.md

## Project identity

This repository is a SQL rewrite benchmark project.

Current benchmark scope is limited to:

- Spark SQL
- PostgreSQL
- MySQL

The benchmark treats the following as first-class dimensions:

- consistency
- plan observability
- cross-engine / cross-dialect generalization

The minimum benchmark unit is a **case package**, not a single SQL string.

---

## 1. Current phase

Current repository stage:

> pilot benchmark consolidation with selective deepening and governance hardening

This means the current focus is:

- stabilizing the strongest existing cases
- maintaining source / case registries
- strengthening case governance
- consolidating workflow and documentation
- improving reusable case-construction patterns
- preparing for later benchmark characterization

This is **not** currently a broad-expansion phase.

Do not default to:

- broad source expansion
- workload curation
- mass case generation
- protocol redesign
- expansion to new engines or dialects

---

## 2. Read-first order

Before doing substantial work, read these files first:

1. `AGENTS.md`
2. `docs/DOC_MAP.md`
3. `docs/EXECUTION_STATUS.md`
4. `benchmark_spec/decision_log.md`

Then read additional files depending on task type:

- source task → `inventory/source_registry.csv`, `docs/POOL_MAPPING_RULES.md`
- case task → `inventory/case_registry.csv`, `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`, `benchmark_spec/common_core_extended_rules_v0.md`
- protocol / direction task → `docs/PROJECT_PLAN.md`, `benchmark_spec/benchmark_spec_v0.md`

---

## 3. Source-of-truth map

Use the correct file for the correct question.

- long-term direction → `docs/PROJECT_PLAN.md`
- frozen decisions → `benchmark_spec/decision_log.md`
- current phase / current focus / current representative snapshot → `docs/EXECUTION_STATUS.md`
- source-level live facts → `inventory/source_registry.csv`
- case-level live facts → `inventory/case_registry.csv`
- archetype completion rules → `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- common-core / extended rules → `benchmark_spec/common_core_extended_rules_v0.md`
- file placement / workflow discipline → `docs/DOC_MAP.md`

Important:

- review documents are **review history**, not live fact tables
- registries are the live source-of-truth for source / case facts

---

## 4. Core distinctions that must not be confused

- archetype completion is **not** admission
- `common-core` / `extended` is **not** the same thing as `primary_pool`
- promotion review is **not** the same thing as final admission
- one successful run is **not** sufficient evidence for promotion

If unsure, stop and read the relevant rules before acting.

---

## 5. Registry-first rule

If source or case facts change, update the registry first.

### If source facts change
Update order:

1. `inventory/source_registry.csv`
2. `docs/EXECUTION_STATUS.md` if the current source-line interpretation changes
3. `benchmark_spec/decision_log.md` only if it reflects a true frozen project decision

### If case facts change
Update order:

1. `inventory/case_registry.csv`
2. case-local files / manifests / artifacts if needed
3. `docs/EXECUTION_STATUS.md` if the representative snapshot changes
4. `benchmark_spec/decision_log.md` only if a real project-level decision has been taken

Do **not** update only narrative files while leaving registries stale.

---

## 6. Allowed work in the current phase

Allowed work includes:

- CLI scaffolding
- environment checks
- artifact-preflight
- machine-readable report generation
- helper scripts under `scripts/` and `tools/`
- documentation cleanup and role alignment
- registry maintenance consistent with evidence
- case package engineering on already approved cases
- checker / plan / artifact strengthening
- non-semantic refactoring for maintainability

---

## 7. Disallowed work in the current phase

Do not do the following without explicit human instruction:

- add new benchmark workloads
- generate new benchmark cases
- start workload curation
- redesign taxonomy principles
- change primary metrics
- change benchmark protocol files
- expand beyond Spark / PostgreSQL / MySQL
- introduce local-LLM dependency as a startup requirement
- make autonomous promotion / admission decisions

---

## 8. Canonical commands

Use stable command entrypoints when possible.

### Environment / health checks
- `python -m scripts.cli env-check`
- `python -m scripts.cli pg-check`
- `python -m scripts.cli mysql-check`
- `python -m scripts.cli spark-check`

### Artifact checks
- `python -m scripts.cli artifact-preflight`

### Current minimal case closure check
- `python scripts/check_smoke_case_consistency.py`

### Before reviewing modifications
- `git status --short`

If a new stable CLI command becomes canonical, add it here.

---

## 9. Environment conventions

- primary development environment: WSL Ubuntu
- Git over SSH
- PostgreSQL runs on Windows host, accessed from WSL through NAT
- MySQL may run inside WSL during bootstrap / early pilot on this machine
- Spark runs in local mode inside WSL
- required environment variables must be set in the **same WSL shell** before starting Codex

Do not assume Windows PowerShell is the primary automation environment.

---

## 10. Stop-and-ask conditions

Stop and ask a human before:

- changing benchmark protocol files
- changing long-term project direction
- adding or editing benchmark cases beyond explicitly approved scope
- downloading or staging new workloads
- expanding taxonomy scope
- changing primary metrics
- changing result-checking rules
- moving a case across pools without explicit justification
- promoting a case to candidate / admitted without explicit review basis
- changing engine scope
- entering workload curation

---

## 11. Operational bottom line

When in doubt:

> do not improvise new benchmark policy; read the correct source-of-truth, update the registry first, and ask before crossing a phase boundary.