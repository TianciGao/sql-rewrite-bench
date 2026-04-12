# Current Phase Closeout Checklist

## 1. Goal of this checklist

This checklist is used to close the current phase before entering the next source-acquisition / next-batch construction stage.

Current phase identity:

- pilot benchmark consolidation
- external archetype completion
- promotion / admission governance for the first Batch-1 external cases

This phase should be considered closed only when documentation, case metadata, and repository state are all synchronized.

---

## 2. Current target state

At current closeout, the repository should consistently reflect the following:

- `PERF_0002` = admitted external common-core case
- `PORT_0002` = common-core candidate
- `LONGTAIL_0002` = staged draft case
- `CONS_0002` = staged draft case

The purpose of this checklist is to make sure that this state is reflected everywhere it needs to be reflected.

---

## 3. Governance and documentation sync

- [ ] `docs/PROJECT_PLAN.md` is updated to the current real phase, not the old early-bootstrap phase
- [ ] `docs/POOL_MAPPING_RULES.md` still matches the current four-pool interpretation
- [ ] `docs/ANCHOR_CASE_SUMMARY.md` still matches the current anchor layer
- [ ] `docs/EXTERNAL_DRAFT_CASE_STATUS.md` matches the latest external case state
- [ ] `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md` is frozen and no longer treated as a live working file
- [ ] `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md` is frozen and matches the current admission decision
- [ ] `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v0.md` is frozen and matches the current candidate decision
- [ ] `benchmark_spec/decision_log.md` contains the required project-level decisions
- [ ] `docs/DOC_MAP.md` exists and reflects the current document roles
- [ ] outdated files have been archived or explicitly marked as historical rather than current operational files

---

## 4. Case-local metadata sync

### 4.1 PERF_0002
- [ ] `cases/PERF/PERF_0002/manifest.yaml` reflects admitted common-core status
- [ ] `cases/PERF/PERF_0002/taxonomy_trial_v0.2.yaml` reflects admitted common-core status
- [ ] `cases/PERF/PERF_0002/data_profile.json` reflects PG / MySQL / Spark validation
- [ ] source / positive / negative artifacts are all referenced correctly
- [ ] plan artifacts are all referenced correctly

### 4.2 PORT_0002
- [ ] `cases/PORT/PORT_0002/manifest.yaml` reflects common-core candidate status
- [ ] `cases/PORT/PORT_0002/taxonomy_trial_v0.2.yaml` reflects common-core candidate status
- [ ] `cases/PORT/PORT_0002/data_profile.json` reflects PG source + MySQL positive/negative validation
- [ ] source / positive / negative artifacts are all referenced correctly
- [ ] plan artifacts are all referenced correctly

### 4.3 LONGTAIL_0002
- [ ] `cases/LONGTAIL/LONGTAIL_0002/manifest.yaml` still reflects staged / not_yet_admitted status
- [ ] `cases/LONGTAIL/LONGTAIL_0002/taxonomy_trial_v0.2.yaml` still reflects staged / not_yet_admitted status

### 4.4 CONS_0002
- [ ] `cases/CONS/CONS_0002/manifest.yaml` still reflects staged / not_yet_admitted status
- [ ] `cases/CONS/CONS_0002/taxonomy_trial_v0.2.yaml` still reflects staged / not_yet_admitted status

---

## 5. Inventory and seed-tracking sync

- [ ] `inventory/seed_candidates_phase3a_batch1.csv` reflects current outcomes for all four Batch-1 seeds
- [ ] `SEED_001` is no longer treated as shortlist / staging, but as promotion-complete / admitted outcome
- [ ] `SEED_004` is no longer treated as raw shortlist only, but as candidate-stage outcome
- [ ] `SEED_002` and `SEED_003` remain clearly marked as staged draft outcomes
- [ ] no inventory file still describes the project as if Batch-1 case extraction were unfinished

---

## 6. Artifact integrity check

- [ ] all files referenced in case manifests actually exist
- [ ] all result artifacts referenced in manifests actually exist
- [ ] all plan artifacts referenced in manifests actually exist
- [ ] no case-local manifest points to stale or renamed paths
- [ ] no checker script points to missing result files
- [ ] the latest committed repository state is reproducible from scripts already in the repo

---

## 7. Repository hygiene

- [ ] `git status --short` is clean before phase closeout is declared
- [ ] temporary `.rar` files or local packaging artifacts are not accidentally tracked
- [ ] no half-written or duplicated helper scripts remain in working directories
- [ ] no outdated intermediate files are still pretending to be current spec files

---

## 8. Closeout decision gate

This phase is considered closed only when all of the following are true:

- [ ] the project-level docs reflect the current real state
- [ ] case-local metadata reflects the current real state
- [ ] inventory / seed-tracking reflects the current real state
- [ ] artifact references are internally consistent
- [ ] the repository is clean
- [ ] next-phase work is explicitly defined

---

## 9. Next phase entry condition

Do **not** begin the next phase merely because more source files are available.

Only begin the next phase after this current phase is closed and the next phase has been explicitly defined.

Expected next-phase entry direction:

- controlled Batch-2 source acquisition
- likely first target: `Stack Queries`
- then decision on whether to introduce `JOB / DSB`
- then decision on consistency supplement source: `SQLEquiQuest` or `VeriEQL`
- then selected loading / preprocessing
- then first next-batch case construction using the archetype workflow rather than ad hoc manual exploration

---

## 10. Closeout sign-off

### Closeout owner
- [ ] checked

### Documentation synced
- [ ] checked

### Metadata synced
- [ ] checked

### Inventory synced
- [ ] checked

### Repo clean
- [ ] checked

### Phase officially closed
- [ ] checked