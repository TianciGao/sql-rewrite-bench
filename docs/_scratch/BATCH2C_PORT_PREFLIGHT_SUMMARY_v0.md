# Status

This is a Batch 2C PORT preflight only for the next portability expansion lane.

It reads existing package files, registry facts, and tracked report state only.

It does not execute SQL, models, SQLGlot, or checkers.

# Candidate List

- `PORT_0003`
- `PORT_0006`
- `PORT_0013`
- `PORT_0016`
- `PORT_0024`
- `PORT_0025`

# Artifact Readiness Table

| case_id | source | ref | neg | pg schema | pg witness | root result_check | pg result_check | checker.yaml | taxonomy_trial | role | readiness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0003` | yes | yes | yes | yes | no | yes | no | yes | yes | `reference_normalization_needed` | `needs_minor_backfill` |
| `PORT_0006` | yes | yes | yes | yes | no | yes | no | yes | yes | `diagnostic_candidate` | `needs_minor_backfill` |
| `PORT_0013` | yes | yes | yes | yes | yes | yes | no | no | no | `clean_candidate` | `needs_reference_policy` |
| `PORT_0016` | yes | yes | yes | yes | yes | yes | no | no | no | `diagnostic_candidate` | `needs_reference_policy` |
| `PORT_0024` | yes | yes | yes | yes | yes | yes | no | no | no | `clean_candidate` | `needs_reference_policy` |
| `PORT_0025` | yes | yes | yes | yes | yes | yes | no | no | no | `clean_candidate` | `needs_reference_policy` |

# Clean Candidates

No candidate is currently clean-ready under the bounded PostgreSQL route-matrix plus reference-consistency rule.

Closest clean-candidate lane:

- `PORT_0013`
- `PORT_0024`
- `PORT_0025`

These three have:

- `manifest.yaml`
- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- `schema/ddl_pg.sql`
- `validation/pg_witness_data.sql`
- `runs/result_check.json`

They are still blocked from immediate selection because bounded PostgreSQL reference/checker policy is not yet frozen and there is no tracked `runs/pg/result_check.json`.

# Diagnostic / Reference-Policy Candidates

Reference-policy lane:

- `PORT_0013`
- `PORT_0024`
- `PORT_0025`

Shared current blockers:

- missing `runs/pg/result_check.json`
- missing `validation/checker.yaml`
- no bounded PG route-matrix reference/checker policy has been frozen for this expansion wave

Diagnostic or fairness-sensitive lane:

- `PORT_0016`

Reason:

- portability focus is explicitly date/time semantics
- earlier expansion notes already flagged this case as a fairness / interpretation case that should remain under explicit human review

Additional diagnostic candidate:

- `PORT_0006`

Reason:

- missing PostgreSQL witness-data package support
- current structure is useful, but not yet clean denominator material for the next bounded PG matrix

# Blockers

Minor backfill blockers:

- `PORT_0003`
  - missing `validation/pg_witness_data.sql`
  - missing `runs/pg/result_check.json`
  - existing taxonomy trial remains `draft_trial_only`
- `PORT_0006`
  - missing `validation/pg_witness_data.sql`
  - missing `runs/pg/result_check.json`
  - existing taxonomy trial remains `draft_trial_only`

Reference-policy blockers:

- `PORT_0013`
- `PORT_0016`
- `PORT_0024`
- `PORT_0025`

Shared blocker shape:

- no `runs/pg/result_check.json`
- no `validation/checker.yaml`
- bounded PG reference-consistency policy for the expansion lane is not yet frozen

# Recommended Batch 2C PG Route Matrix Subset

Immediate ready subset:

- none

Post-policy / post-backfill next wave:

- likely clean-first lane:
  - `PORT_0013`
  - `PORT_0024`
  - `PORT_0025`
- keep diagnostic review on:
  - `PORT_0016`
- backfill first before reconsidering:
  - `PORT_0003`
  - `PORT_0006`

# Claim Boundaries

- preflight only
- PostgreSQL only in this readiness step
- not execution
- not translation correctness
- not checker closure
- not denominator expansion by itself
- not registry writeback
- not formal review update

# Recommended Next Action

- run bounded Batch 2C PORT PG route matrix only for ready cases; the current ready subset is empty, so first freeze PG reference/checker policy for `PORT_0013`, `PORT_0016`, `PORT_0024`, and `PORT_0025`, and backfill PostgreSQL witness support for `PORT_0003` and `PORT_0006`
