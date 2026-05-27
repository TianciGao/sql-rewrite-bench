# VeriEQL Support Dependency Probe v0

## Scope

- Repo: `datasets/raw/verieql/staged/VeriEQL/`
- Wrapper artifact: `reports/formal_expansion/verieql_support/cons_0007_pairs.jsonl`
- Boundary: dependency/runtime probe only, no actual equivalence verification, no PostgreSQL, no speedup, no baseline claim

## Environment

- Host Python version: `Python 3.12.3`
- Isolated probe environment: `/tmp/verieql-probe-venv`

## Dependency Install Status

- Status: `success`
- Install source: [requirements.txt](/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt)
- First sandboxed attempt failed on network/package resolution for `z3-solver`
- Rerun outside the sandbox into the isolated `/tmp` venv succeeded

Installed dependencies included:

- `z3-solver`
- `mo-sql-parsing==8.205.22260`
- `ujson`
- `ordered_set`
- `lark`
- `tqdm`
- `pandas`
- `pyyaml`
- `prettytable`
- `mysql-connector-python`
- `matplotlib`
- `sphinx`
- `sphinx-rtd-theme`

Failed dependency after approved install retry: `none`

## Wrapper Artifact Check

- Wrapper artifact exists: `yes`
- Path: `reports/formal_expansion/verieql_support/cons_0007_pairs.jsonl`
- Parseable JSON lines: `yes`
- Pair count: `2`

## Entrypoint Probe

### Imports

When the working directory is the VeriEQL root, module imports succeed:

- `import constants`: `ok`
- `import environment`: `ok`
- `import parallel.cli_within_timeout`: `ok`

### CLI / Help Status

- `python -m parallel.cli_within_timeout --help` from the VeriEQL root: `success`
- `python -m VeriEQL --help`: `failed`
  - reason: `ModuleNotFoundError: No module named 'constants'`
- `python __main__.py --help`: `failed`
  - reason: `__main__.py` is not a real argparse CLI; it executes a baked sample immediately
  - observed runtime failure: `TypeError: And() got an unexpected keyword argument 'ctx'`
- `python parallel/cli_within_timeout.py --help`: `failed`
  - reason: direct script launch from the `parallel/` subdirectory breaks absolute local imports such as `from constants import *`

## Interpretation

Dependency materialization is no longer the blocker. The staged VeriEQL tree can now be imported in an isolated environment, and the documented batch entrypoint is discoverable and responds to `--help` when launched as a module from the VeriEQL root.

The remaining runtime risk is entrypoint-specific:

- `__main__.py` should not be used as the benchmark entrypoint
- direct script invocation of `parallel/cli_within_timeout.py` should not be used
- the safe candidate entrypoint is module-mode batch execution:
  - `cd datasets/raw/verieql/staged/VeriEQL`
  - `/tmp/verieql-probe-venv/bin/python -m parallel.cli_within_timeout ...`

There is also one unresolved runtime risk beyond help/import:

- the baked sample path in `__main__.py` crashes with `TypeError: And() got an unexpected keyword argument 'ctx'`

That does not prove the bounded `CONS_0007` wrapper path will fail, because the wrapper currently uses an empty first-pass constraint policy and the sample path is not the intended batch route. But it does mean a bounded verification canary should be treated as an execution probe, not as already de-risked runtime closure.

## Is Actual Verification Now Feasible?

- Feasible enough for a bounded canary: `yes`
- Fully de-risked runtime closure: `no`

Reason:

- dependencies installed successfully
- wrapper artifact exists and is parseable
- the documented batch module entrypoint is callable with `--help`
- but there is still observed runtime fragility in the alternate `__main__.py` path

## Remaining Blockers

- `entrypoint_contract_is_module_mode_only`
- `__main___sample_path_runtime_failure`
- `actual_verification_not_yet_run`

## Recommended Next Action

Recommended next action: run a bounded `CONS_0007` verification canary through the batch module entrypoint only, using the emitted wrapper jsonlines and keeping the current explicit first-pass constraint policy.

If that canary fails, fix the runtime/entrypoint behavior before treating VeriEQL as a usable support-table method.
