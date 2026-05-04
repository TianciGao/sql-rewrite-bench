# EXPANDED_PERF_DIRECT_LLM_PREFLIGHT_SUMMARY_v0

## Status

This is a read-only preflight for expanding `LLM_DIRECT_REWRITE_STRONG` from the seed packet to the current expanded PERF packet.

Scope:

- Batch 2A PERF: `19`
- Batch 3A PERF: `11`
- Batch 3B PERF: `4`
- total expanded PERF target: `34`

No model call, SQL execution, checker execution, or speedup run was performed here.

## Executive Summary

The expanded PERF Direct LLM route is structurally ready on all `34` target cases:

- `source.sql` present: `34 / 34`
- `manifest.yaml` present: `34 / 34`
- validation schema expected: `34 / 34`
- prior source execution evidence present: `34 / 34`
- checker gate present and passed: `34 / 34`
- prompt package buildable: `34 / 34`
- runtime policy present: `34 / 34`

The only blocker in the current shell is API environment visibility:

- API key status: `<missing>`
- base URL status: `<missing>`
- provider mode: `env_blocked`

Because of that, formal preflight status is:

- `ready_for_direct_llm_run`: `0`
- `env_blocked`: `34`
- other blocker classes: `0`

## Case coverage

Covered PERF cases:

- Batch 2A:
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
- Batch 3A:
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
- Batch 3B:
  - `PERF_0027`
  - `PERF_0028`
  - `PERF_0030`
  - `PERF_0031`

## Gate summary

| gate | result |
|---|---:|
| source SQL exists | `34 / 34` |
| manifest exists | `34 / 34` |
| validation schema expected | `34 / 34` |
| checker evidence exists | `34 / 34` |
| checker gate passed | `34 / 34` |
| prior source execution evidence exists | `34 / 34` |
| runtime policy exists | `34 / 34` |
| prompt package buildable | `34 / 34` |
| API env available | `0 / 34` under current shell |

Checker gate basis:

- Batch 2A no-opt checker consistent: `19 / 19`
- Batch 3A no-opt checker consistent: `11 / 11`
- Batch 3B no-opt checker consistent: `4 / 4`

This means the expanded PERF Direct LLM route is blocked by environment, not by prompt inputs, checker closure, runtime policy, or source execution evidence.

## Output paths reserved for a future run

For each case, the preflight records future report-local paths for:

- Direct LLM call report
- Direct LLM PostgreSQL execution report
- source TSV materialization
- candidate TSV materialization
- checker output
- later speedup report path

These are planning paths only in this preflight.

## Recommended execution subset

Current formal ready subset: none, because API env is blocked in this shell.

Structural ready subset if API env is later set:

- all `34` expanded PERF cases

## Recommended next action

Resolve the Direct LLM API environment and then run Direct LLM expanded PERF on the ready subset.

Given the current preflight, the ready subset after env repair should be the full `34`-case expanded PERF packet.

## Claim boundaries

- no model call
- no SQL execution
- no checker execution
- no speedup run
- no registry writeback
- not a correctness result by itself
- not a leaderboard artifact
