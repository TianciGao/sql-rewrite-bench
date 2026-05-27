# Status

This is a Batch 2 denominator-expansion preflight only. It reads registry, manifest, and existing artifact state and does not execute SQL, models, checkers, or plan collection.

# Inputs Inspected

- `inventory/case_registry.csv`
- [PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_EXPERIMENT_DENOMINATOR_FREEZE_PLAN_v0.md)
- [PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRELIM_PERF_PORT_COMMON_CORE_SEED_PROPOSAL.md)
- [PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRELIM_CONS_COMMON_CORE_EXTENDED_ADDENDUM.md)
- [FORMAL_COMMON_CORE_RESULTS_CLOSEOUT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/FORMAL_COMMON_CORE_RESULTS_CLOSEOUT_v0.md)
- [FORMAL_PORT_RESULTS_CLOSEOUT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/FORMAL_PORT_RESULTS_CLOSEOUT_v0.md)
- [PAPER_EXPERIMENT_RESULTS_ROLLUP_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_EXPERIMENT_RESULTS_ROLLUP_v0.md)
- case manifests and existing artifact paths under `cases/PERF`, `cases/CONS`, `cases/PORT`, and `cases/LONGTAIL`

# Current Seed Denominator

Common-core seed:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

PORT seed:

- `PORT_0004`
- `PORT_0012`
- `PORT_0022`

# Common-Core Batch 2 Ready Candidates

The preflight found a broad ready PERF wave with complete staged registry state, positive/negative rewrites, PG result evidence, and PG plan evidence:

- `PERF_0007`
- `PERF_0009`
- `PERF_0010`
- `PERF_0011`
- `PERF_0012`
- `PERF_0014`
- `PERF_0015`
- `PERF_0016`
- `PERF_0018`
- `PERF_0019`
- `PERF_0020`
- `PERF_0021`
- `PERF_0022`
- `PERF_0023`
- `PERF_0025`
- `PERF_0026`
- `PERF_0034`
- `PERF_0035`
- `PERF_0036`
- `PERF_0043`
- `PERF_0044`
- `PERF_0047`
- `PERF_0050`
- `PERF_0052`
- `PERF_0053`
- `PERF_0056`
- `PERF_0062`
- `PERF_0063`
- `PERF_0065`
- `PERF_0066`

Interpretation:

- the strongest first wave is the earlier staged TPC-H and TPC-DS set through `PERF_0036`
- the later PERF wave from `PERF_0043` onward is also artifact-complete by the current preflight rule, but can be treated as second-wave Batch 2 expansion if a smaller first batch is preferred

# Common-Core Batch 2 Minor-Backfill Candidates

The most important minor-backfill lane is CONS. These cases are structurally strong but still need narrow checker-policy or checker-artifact hardening before formal Batch 2 execution:

- `CONS_0024`
- `CONS_0031`
- `CONS_0034`

There is also a broader minor-backfill queue of mostly artifact-complete PERF and CONS cases that are held back by one narrow governance or artifact gap such as missing top-level `runs/result_check.json`, `checker.yaml`, or not-yet-staged registry state:

- PERF examples:
  - `PERF_0005`
  - `PERF_0027`
  - `PERF_0028`
  - `PERF_0029`
  - `PERF_0030`
  - `PERF_0031`
  - `PERF_0032`
  - `PERF_0037`
  - `PERF_0039`
  - `PERF_0040`
  - `PERF_0041`
  - `PERF_0042`
- CONS examples:
  - `CONS_0006`
  - `CONS_0011`
  - `CONS_0017`
  - `CONS_0023`
  - `CONS_0029`
  - `CONS_0032`
  - `CONS_0036`
  - `CONS_0037`
  - `CONS_0040`

# PORT Batch 2 Ready Candidates

No additional non-seed PORT cases were classified as clean Batch 2 ready under the current rule set.

Interpretation:

- current non-seed PORT packages are usually structurally present at the case root
- but they generally lack bounded formal PG route evidence, checker closure, or explicit denominator policy

# PORT Minor-Policy / Checker Candidates

The strongest next PORT candidates are:

- `PORT_0003`
- `PORT_0006`
- `PORT_0013`
- `PORT_0016`
- `PORT_0024`
- `PORT_0025`

These cases have good package shape and existing case-root evidence, but still need portability policy / checker scope freeze before Batch 2 PG-route execution work.

The broader PORT policy/checker queue includes:

- `PORT_0005`
- `PORT_0008`
- `PORT_0009`
- `PORT_0010`
- `PORT_0011`
- `PORT_0014`
- `PORT_0015`
- `PORT_0017`
- `PORT_0018`
- `PORT_0019`
- `PORT_0020`
- `PORT_0021`
- `PORT_0023`
- `PORT_0026`
- `PORT_0027`
- `PORT_0028`

Important caveats:

- `PORT_0003` still carries the taxonomy-exception caveat from the earlier seed proposal
- `PORT_0016` remains a portability-interpretation fairness case and should stay under explicit human review
- `PORT_0012` remains a holdout and is not auto-promoted by this preflight

# Extended / Diagnostic Candidates

Recommended extended or diagnostic lane:

- `PERF_0038`
- `PERF_0076`
- `CONS_0005`
- `CONS_0037`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

Broader longtail diagnostic material was also detected as executable and tri-engine-backed, including:

- `LONGTAIL_0003`
- `LONGTAIL_0004`
- `LONGTAIL_0005`
- `LONGTAIL_0007`
- `LONGTAIL_0008`
- `LONGTAIL_0009`
- `LONGTAIL_0010`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0014`
- `LONGTAIL_0015`
- `LONGTAIL_0016`
- `LONGTAIL_0018`
- `LONGTAIL_0019`
- `LONGTAIL_0020`
- `LONGTAIL_0021`

# Not-Ready Blockers

Main blocker patterns:

- already in the frozen seed denominator:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0013`
  - `PERF_0017`
  - `PERF_0024`
  - `PERF_0033`
  - `PERF_0054`
  - `CONS_0007`
  - `CONS_0012`
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`
- missing PG result evidence or missing plan-check evidence:
  - common in early pre-governed PERF and many non-seed PORT cases
- missing checker policy or `checker.yaml`:
  - common in the next CONS wave and most non-seed PORT cases
- not clean denominator by prior governance notes:
  - `PERF_0038`
  - `PERF_0076`
- not multi-engine closed enough for expansion:
  - e.g. early non-closed performance or longtail packages such as `LONGTAIL_0002`

# Recommended Next Experiment Batch

Run first:

- Common-core Batch 2 ready PERF first wave:
  - `PERF_0007`
  - `PERF_0009`
  - `PERF_0010`
  - `PERF_0011`
  - `PERF_0012`
  - `PERF_0014`
  - `PERF_0015`
  - `PERF_0016`
  - `PERF_0018`
  - `PERF_0019`
  - `PERF_0020`
  - `PERF_0021`
  - `PERF_0022`
  - `PERF_0023`
  - `PERF_0025`
  - `PERF_0026`
  - `PERF_0034`
  - `PERF_0035`
  - `PERF_0036`

Then queue:

- Common-core minor backfill before execution:
  - `CONS_0024`
  - `CONS_0031`
  - `CONS_0034`

Do not run yet as Batch 2 denominator material:

- non-seed PORT cases until policy/checker scope is frozen
- `PORT_0012` until a separate denominator decision is taken
- extended / diagnostic cases such as `PERF_0038`, `PERF_0076`, and the LONGTAIL lane

Recommended next action:

- run artifact/execution preflight for the selected common-core Batch 2 ready cases

