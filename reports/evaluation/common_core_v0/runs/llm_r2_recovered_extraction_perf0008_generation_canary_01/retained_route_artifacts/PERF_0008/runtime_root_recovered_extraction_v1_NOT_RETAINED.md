# runtime_root_recovered_extraction_v1 not retained

The staged recovered-extraction runtime root is intentionally not retained in git.

Reason:
- it is a temporary staged runtime copy of the external LLM-R2 repository
- it contains its own .git metadata and would otherwise be committed as a gitlink/submodule-like entry
- paper evidence is retained through route artifacts, logs, generated SQL, raw output capture, extraction audit, patch audit, and checker artifacts instead

Canonical retained evidence for this canary remains under the surrounding run directory.
