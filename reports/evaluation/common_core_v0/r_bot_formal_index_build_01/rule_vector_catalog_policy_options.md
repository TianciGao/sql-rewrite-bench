## Rule-Vector Catalog Policy Options

Date: 2026-05-08

### Policy Frame

The formal contract currently freezes:

- `rule_vector_width = 100`
- `total_dimension = 3172`
- `current_benchmark_gate_ready = false`

The current build failure arises because the visible formal builder only recovers `30 + 37 = 67` named slots from its present source path.

### Option 1: Recover the missing catalog from upstream and retained source artifacts

Description:

- reconstruct the formal Calcite catalog from the retained 70-row structured artifacts
- reconcile the two names missing from the visible Java parse
- freeze a canonical 70-name Calcite slot order
- keep the total formal vector contract `30 + 70 = 100`

Pros:

- best match to the frozen `3172` contract
- best match to the strongest retained artifact evidence
- avoids changing the formal retrieval/index dimension
- avoids pretending that unknown slots are harmless padding

Cons:

- requires one more catalog-freeze patch
- requires explicit treatment of the two structured names absent from the visible Java maps

Assessment:

- recommended
- this is the cleanest way to make the formal build deterministic without changing the benchmark contract

### Option 2: Define a formal 100-slot catalog with 67 named slots and 33 reserved zero slots

Description:

- formalize the current 67 recovered names
- reserve 33 trailing slots as permanent zeros
- keep total width at 100

Pros:

- easy to implement mechanically
- preserves `3172` dimension

Cons:

- strongest visible evidence points to a retained 70-name Calcite catalog, not 37 Calcite names plus 33 anonymous placeholders
- scratch/runtime padding evidence was a temporary compatibility patch, not a formal benchmark policy
- would silently bake unknown semantics into the formal contract

Assessment:

- not recommended
- not formally justified by current evidence

### Option 3: Rebuild with a 67-wide rule vector and change total dimension

Description:

- accept the current `30 + 37 = 67` parse as authoritative
- change total dimension from `3172` to `3139`

Pros:

- aligns with the current narrow parser

Cons:

- contradicts the frozen formal dimension contract
- contradicts prior retained `3172` collection evidence
- would invalidate existing formal retrieval assumptions
- would require a benchmark-level contract change, not a local implementation fix

Assessment:

- reject

### Option 4: Keep the formal build blocked until the full 100-slot catalog is recovered

Description:

- do not alter build behavior yet
- explicitly retain the blocker
- require a canonical slot-order artifact before allowing execute-build to proceed as formal

Pros:

- safest governance posture
- avoids formalizing the wrong catalog

Cons:

- delays formal index materialization
- does not by itself resolve the underlying catalog gap

Assessment:

- required as the current gate state
- should remain in effect until Option 1 is completed

### Recommended Policy

Recommended sequence:

1. Keep the gate closed now.
2. Pursue Option 1 as the next patch.
3. Reject Option 3.
4. Do not adopt Option 2 unless a retained artifact explicitly freezes named reserved slots and their semantics, which is not the case today.

### Formal Judgment on the 100-Slot Meaning

Current formal judgment:

- not yet safe to declare `100 = 67 named + 33 reserved zeros`
- most plausible reconstruction is `100 = 30 NL + 70 Calcite`
- because slot order and source lineage are not yet fully frozen, the formal policy state remains blocked

### Next Patch Recommendation

The next patch should:

1. introduce a retained formal Calcite catalog artifact with exactly 70 names and fixed ordering
2. document source lineage for all 70 names, including the two names not present in the visible Java union
3. update the formal build helper to use that retained 70-name artifact for rule-vector construction
4. keep `current_benchmark_gate_ready = false` and formal `@120` generation blocked until artifact-contract validation passes
