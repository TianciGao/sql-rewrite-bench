# Formal Near-Duplicate Check Summary

## Status

- rows covered: `40`
- rows passed against visible text: `0`
- rows failed near-duplicate detection: `0`
- rows blocked by retention/provenance: `40`
- rows blocked by corpus text unavailability: `0`

## Heuristic Features

- token-set similarity: `jaccard`
- token-3-gram similarity: `jaccard`
- structural similarity: `keyword-count and shape overlap`
- token-set trigger threshold: `0.9`
- token-3-gram trigger threshold: `0.85`
- structural trigger threshold: `0.95`
- combined trigger threshold: `0.9`

## Corpus Availability

- visible flat-file included manifest items: `31`
- ZIP-derived text rows available: `18744`
- corpus availability blockers: `0`
- ZIP metadata loaded: `yes`
- formal retention blocker present in loaded corpus rows: `yes`

## Gate Impact

- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`
