# R-Bot PG1 Recovery Canary

This package prepares a one-case PostgreSQL recovery canary for `R-Bot` on `PERF_0006`.

It does not generate current benchmark metrics.
It does not reuse historical `prior_method_pg10` numbers as current Common-core v0 metrics.

The exact repo-local scaffold is:

```bash
python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006
```

This run package wraps that scaffold with:

- explicit preflight commands
- explicit blocked-state reporting
- optional actual generation only when the human sets `RBOT_CANARY_ALLOW_ACTUAL_RUN=1`

Run from repo root:

```bash
bash reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_manual_r_bot_pg1_recovery_canary.sh
```
