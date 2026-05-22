# Formal Generated-Output Exclusion Summary

## Status

- rows covered: `357`
- rows passed against visible text: `0`
- rows failed generated-output exclusion: `0`
- rows blocked by retention/provenance: `357`
- rows blocked by corpus text unavailability: `0`

## Corpus Availability

- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`
- manifest blockers: `0`
- generated-output family blockers: `0`
- ZIP metadata loaded: `yes`

## Coverage Scope

- generated-output families checked: `sqlglot`, `direct_llm`, `calcite`, `r_bot_pg1_recovery`
- Calcite generated path: `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`
- Calcite filename rule: `calcite_hep_pg_rewrite.sql`
- matching rule: `exact normalized hash match against visible included corpus text items`

## Gate Impact

- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`
