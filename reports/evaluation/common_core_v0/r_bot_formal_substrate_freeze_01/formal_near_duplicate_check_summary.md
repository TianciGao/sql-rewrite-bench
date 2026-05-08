# Formal Near-Duplicate Check Summary

## Status

- rows covered: `40`
- rows passed: `0`
- rows failed near-duplicate detection: `0`
- rows blocked: `40`

## Heuristic Features

- token-set similarity: `jaccard`
- token-3-gram similarity: `jaccard`
- structural similarity: `keyword-count and shape overlap`
- token-set trigger threshold: `0.9`
- token-3-gram trigger threshold: `0.85`
- structural trigger threshold: `0.95`
- combined trigger threshold: `0.9`

## Corpus Availability

- visible text-readable included manifest items: `4`
- manifest blockers: `4`

## Gate Impact

- formal gate open: `no`
- formal `R-Bot @120` generation may start: `no`
