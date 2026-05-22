# SQLGlot PORT Same-Engine Execution

This package is human-run only. Codex must not execute the script in this directory.

Purpose:
- prepare a PORT-only same-engine SQLGlot execution pass for Common-core v0
- keep all `9` PORT cases denominator-visible
- execute only native-engine-supported PORT rows
- keep unsupported, generation-failed, and explicit no-op rows visible

This package does not:
- run timing
- compute speedup
- compute regression metrics
- create a final leaderboard

Scope summary:
- cases: `9`
- rows: `54`
- ready-to-execute rows: `9`
- unsupported rows: `36`
- explicit no-op rows: `9`
- explicit generation-failed rows: `0`

Important PORT caveat:
- same-engine accounting for PORT must preserve unsupported route/engine combinations explicitly
- these rows remain portability-stress evidence and must not be over-interpreted as ordinary same-engine leaderboard rows

