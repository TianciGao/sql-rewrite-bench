# LLM-R2 120 Recovery Checklist v1

This checklist supports review of the LLM-R2 recovery plan. It does not
authorize generation, execution, or timing.

## Runner recovery

### Codex-can-prepare

- summarize retained runner-related artifacts
- draft expected runner input/output contract
- list retained path assumptions for wrapper, logs, metadata, and generated SQL

### Human-must-provide

- confirm whether a recoverable runner entrypoint still exists
- confirm whether the relevant external runtime substrate is available

### Forbidden-until-approved

- do not run LLM-R2
- do not generate SQL

## Logical-plan substrate recovery

### Codex-can-prepare

- summarize retained logical-plan failure evidence
- draft substrate contract notes
- separate route-wrapper blockers from substrate blockers

### Human-must-provide

- confirm which logical-plan dependencies are expected to be recoverable
- confirm whether unresolved substrate issues should block all further work

### Forbidden-until-approved

- do not rerun logical-plan probes
- do not treat one-case probe evidence as a reusable route by default

## Output SQL extraction

### Codex-can-prepare

- summarize one-case extraction cleanup evidence
- draft reusable extraction contract candidates
- define expected generated-output artifact schema

### Human-must-provide

- decide whether one-case extraction evidence is strong enough to justify a
  bounded recovery subtask later

### Forbidden-until-approved

- do not test extraction on new model outputs
- do not assume MySQL/Spark extraction support

## Reproducibility contract

### Codex-can-prepare

- enumerate reproducibility-sensitive inputs
- draft environment/runtime identity checklist
- draft generated-SQL retention and metadata-retention expectations

### Human-must-provide

- confirm acceptable reproducibility contract for retrieval/demo/runtime inputs

### Forbidden-until-approved

- do not rebuild indexes
- do not stage new corpora

## Bounded PG overlap dry-run

### Codex-can-prepare

- outline a planning-only bounded PG overlap package shape
- identify what later outputs would be required if approved

### Human-must-provide

- approve whether a bounded PG overlap dry-run should be pursued after core
  recovery phases are resolved

### Forbidden-until-approved

- do not run PG overlap generation
- do not upgrade PG10 evidence into `120` evidence

## Approval before generation

### Codex-can-prepare

- assemble the recovery review packet
- summarize unresolved blockers and stop conditions

### Human-must-provide

- explicit approval before any generation scaffold is turned into an execution
  package

### Forbidden-until-approved

- no generation
- no execution
- no timing
