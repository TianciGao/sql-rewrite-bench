# Expected Artifacts

This package defines and produces the following artifacts.

## Frozen Contract Inputs

- `formal_artifact_contract_matrix.csv`
- `formal_artifact_expected_paths.json`
- `artifact_contract_validation_plan.md`
- `README.md`

## Human-Run Validator

- `run_manual_r_bot_formal_artifact_contract_validate.py`

## Validator Outputs

When the validator is run manually, it writes:

- `formal_artifact_contract_validation_report.md`
- `formal_artifact_contract_validation_report.json`

## Output Semantics

The validator output is a pre-generation decision artifact.

It reports whether:

- the contract package covers all `120` formal rows
- row-level and package-level path definitions are complete
- required schema keys are defined
- non-success rows remain explicitly representable
- secret-hygiene rules are present

It must not treat absent generated run outputs as a failure by itself.
