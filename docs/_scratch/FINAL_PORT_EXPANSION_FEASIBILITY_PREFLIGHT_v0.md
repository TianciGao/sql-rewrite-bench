# Final PORT Expansion Feasibility Preflight v0

## Status

This note is a final-cycle feasibility preflight for the remaining narrow PORT candidates:

- `PORT_0003`
- `PORT_0006`
- `PORT_0016`

It is read-only and PostgreSQL-side only. It does not execute SQL, call models, run SQLGlot, or change case packages.

## Inputs inspected

- [BATCH2C_PORT_PREFLIGHT_SUMMARY_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/BATCH2C_PORT_PREFLIGHT_SUMMARY_v0.md)
- [EXPANDED_PORT_RESULTS_CLOSEOUT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/EXPANDED_PORT_RESULTS_CLOSEOUT_v0.md)
- `cases/PORT/<CASE>/manifest.yaml`
- `cases/PORT/<CASE>/source.sql`
- `cases/PORT/<CASE>/rewrite_pos_01.sql`
- `cases/PORT/<CASE>/schema/ddl_pg.sql`
- `cases/PORT/<CASE>/validation/pg_witness_data.sql`
- `cases/PORT/<CASE>/runs/pg/result_check.json`
- existing `taxonomy_trial*.yaml` where present

## Candidate table

| case_id | source_dialect | pg_witness_data | pg_result_check | taxonomy_trial | classification | rationale |
|---|---|---:|---:|---|---|---|
| `PORT_0003` | `postgres_like_candidate` | no | no | `draft_trial_only` | `needs_pg_witness_backfill` | Missing PostgreSQL witness input and PG-local result evidence, so it is not a quick final-cycle add. |
| `PORT_0006` | `mysql_like_candidate` | no | no | `draft_trial_only` | `needs_pg_witness_backfill` | Same missing PG witness/result-check gap as `PORT_0003`; bounded PG matrix work cannot start cleanly. |
| `PORT_0016` | `mysql_like_candidate` | yes | no | missing | `too_slow_for_current_cycle` | Witness input exists, but the case still lacks PG-local result evidence and remains policy-sensitive / diagnostic-oriented. |

## Clean candidates

None.

## Backfill-sensitive cases

- `PORT_0003`
  - Missing:
    - `validation/pg_witness_data.sql`
    - `runs/pg/result_check.json`
  - Existing Batch 2C preflight already treated it as a reference-normalization / backfill case rather than a clean matrix add.
- `PORT_0006`
  - Missing:
    - `validation/pg_witness_data.sql`
    - `runs/pg/result_check.json`
  - Existing Batch 2C preflight already treated it as a diagnostic candidate needing package backfill before bounded PG expansion.

## Diagnostic / too-slow case

- `PORT_0016`
  - Present:
    - `validation/pg_witness_data.sql`
    - core SQL and PG schema files
  - Missing:
    - `runs/pg/result_check.json`
    - `taxonomy_trial*.yaml`
  - This case was already excluded from the earlier ready subset and kept in the diagnostic lane. In the current paper cycle, the remaining work is not a narrow witness-file backfill; it is additional policy/checker closure.

## Feasibility decision

The current evidence does not support adding any of these three cases as quick final-cycle PORT expansions.

- `quick_add_candidate`: none
- `needs_pg_witness_backfill`: `PORT_0003`, `PORT_0006`
- `diagnostic_only`: none
- `too_slow_for_current_cycle`: `PORT_0016`

## Recommended next action

Freeze the current `6`-case PORT packet.

Reason:

- the existing expanded PORT closeout already supports a bounded PostgreSQL-side paper packet;
- `PORT_0003` and `PORT_0006` still need explicit PG witness backfill;
- `PORT_0016` still needs additional diagnostic/policy closure and is not a narrow quick add.

## Claim boundaries

- PostgreSQL-side feasibility only
- not SQL execution
- not LLM evaluation
- not SQLGlot evaluation
- not translation correctness
- not cross-engine closure
- not registry writeback
- not formal review update

## Verification / non-modification note

Only this scratch note was created for the document layer in this turn.

- no SQL/database execution
- no model calls
- no SQLGlot runs
- no checker runs
- no case modifications
- no registry changes
- no `docs/EXECUTION_STATUS.md` changes
- taxonomy calibration notes untouched
