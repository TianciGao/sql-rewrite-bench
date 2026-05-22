## Formal Index Build Gate Status v2

Date: 2026-05-08

### Status

- formal index dry-run metadata: retained
- ZIP provenance closure: retained
- frozen extracted text row count: `18744`
- provider-family metadata recording: retained
- real execute-build implementation: present but blocked for formal use
- formal rule-vector catalog: unresolved
- current benchmark gate ready: `false`
- formal `@120` generation may start: `no`

### Current Blocking Issue

The formal build remains blocked by rule-catalog reconciliation.

Current failure:

- `Rule catalog width mismatch: NL=30, NORMAL=37, TOTAL=67`

Read-only reconciliation result:

- strongest visible formal reconstruction is `30 NL + 70 Calcite = 100`
- the current builder only recovers `30 NL + 37 Calcite = 67`
- the retained 70-row Calcite structured catalog is not yet frozen as the canonical formal slot-order artifact
- two structured Calcite names are not yet reconciled to the visible Java rule maps

### Gate Decision

The formal Chroma index blocker is **not closed**.

Required before the gate may change:

1. retain a canonical 70-name Calcite catalog artifact and fixed slot order
2. reconcile the two names absent from the visible Java normal/explore parse
3. patch the builder to use the retained formal catalog instead of the current narrow 37-name source
4. rerun formal inspect and artifact-contract validation after that patch

### Non-Decisions Preserved

- no benchmark protocol change
- no change to `rule_vector_width = 100`
- no change to `total_dimension = 3172`
- no silent reserved-slot policy adoption
- no formal `@120` generation start

### Bottom Line

The current evidence is strong enough to reject a `67`-wide formal rebuild and strong enough to suspect a `30 + 70` catalog contract, but not yet strong enough to declare the full `100`-slot catalog formally frozen.
