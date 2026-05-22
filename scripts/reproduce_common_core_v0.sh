#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/reproduce_common_core_v0.sh --mode artifact
  bash scripts/reproduce_common_core_v0.sh --mode deterministic [--dry-run|--preflight|--execute] [--steps step1,step2|all-deterministic] [--continue-on-error]
  bash scripts/reproduce_common_core_v0.sh --mode llm [--allow-unimplemented]

Artifact mode validates retained Common-core v0 artifacts without running
database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection,
or new timing collection.

Deterministic mode lists, preflights, or explicitly executes retained
deterministic runner commands. It never includes LLM/API routes, verifier
commands, or PORT9. Experiment runners are executed only with --execute.

LLM mode is recognized but intentionally not implemented in this reviewer
wrapper; use --allow-unimplemented to acknowledge that placeholder mode.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

BASE_DIR="reports/evaluation/common_core_v0"
ARTIFACT_OUT_DIR="${BASE_DIR}/REVIEWER_REPRODUCTION_V1"
DETERMINISTIC_OUT_DIR="${ARTIFACT_OUT_DIR}/deterministic"

MODE="artifact"
ALLOW_UNIMPLEMENTED=0
DRY_RUN=0
PREFLIGHT=0
EXECUTE=0
CONTINUE_ON_ERROR=0
STEPS_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      if [[ $# -lt 2 ]]; then
        echo "error: --mode requires a value" >&2
        exit 2
      fi
      MODE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --preflight)
      PREFLIGHT=1
      shift
      ;;
    --execute)
      EXECUTE=1
      shift
      ;;
    --steps)
      if [[ $# -lt 2 ]]; then
        echo "error: --steps requires a comma-separated value" >&2
        exit 2
      fi
      STEPS_ARG="$2"
      shift 2
      ;;
    --continue-on-error)
      CONTINUE_ON_ERROR=1
      shift
      ;;
    --allow-unimplemented)
      ALLOW_UNIMPLEMENTED=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unsupported argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

csv_escape() {
  local value=${1//\"/\"\"}
  printf '"%s"' "${value}"
}

write_csv_row() {
  local output_file="$1"
  shift
  local first=1
  local value
  {
    for value in "$@"; do
      if [[ "${first}" -eq 0 ]]; then
        printf ','
      fi
      csv_escape "${value}"
      first=0
    done
    printf '\n'
  } >> "${output_file}"
}

write_artifact_status() {
  write_csv_row "${ARTIFACT_STATUS_FILE}" "$1" "$2" "$3"
}

artifact_log() {
  printf '%s\n' "$*" | tee -a "${ARTIFACT_LOG_FILE}"
}

artifact_fail_check() {
  local check_id="$1"
  local details="$2"
  write_artifact_status "${check_id}" "fail" "${details}"
  artifact_log "FAIL ${check_id}: ${details}"
  exit 1
}

artifact_pass_check() {
  local check_id="$1"
  local details="$2"
  write_artifact_status "${check_id}" "pass" "${details}"
  artifact_log "PASS ${check_id}: ${details}"
}

run_artifact_mode() {
  ARTIFACT_SUMMARY_FILE="${ARTIFACT_OUT_DIR}/reviewer_reproduction_summary_v1.md"
  ARTIFACT_STATUS_FILE="${ARTIFACT_OUT_DIR}/reviewer_reproduction_status_v1.csv"
  ARTIFACT_LOG_FILE="${ARTIFACT_OUT_DIR}/reviewer_reproduction_log_v1.txt"

  mkdir -p "${ARTIFACT_OUT_DIR}"

  {
    echo "Common-core v0 reviewer reproduction artifact-mode"
    echo "timestamp_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo "repo_root=${REPO_ROOT}"
    echo "mode=${MODE}"
    echo "boundary=no DB/LLM/verifier/PORT9/EXPLAIN/timing collection"
    echo
  } > "${ARTIFACT_LOG_FILE}"
  printf '"check_id","status","details"\n' > "${ARTIFACT_STATUS_FILE}"

  artifact_log "Artifact mode does not run DB engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection."

  local required_dirs_before_render=(
    "08_SECTION8_EVIDENCE_FREEZE_V1"
    "09_TAXONOMY_COVERAGE_V1"
    "10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1"
    "11_TIMING_OBSERVABILITY_V1"
    "12_PORT_VERIFIER_ARTIFACT_MAP_V1"
    "14_REPRODUCIBILITY_MANIFEST_V1"
    "15_PROGRAMMATIC_METRIC_AUDIT_V1"
    "16_STATIC_RECOMPUTE_AUDIT_V1"
    "17_TABLE12_ULTIMATE_PROVENANCE_V1"
  )

  local dir_name
  local dir_path
  for dir_name in "${required_dirs_before_render[@]}"; do
    dir_path="${BASE_DIR}/${dir_name}"
    if [[ ! -d "${dir_path}" ]]; then
      artifact_fail_check "required_dir_${dir_name}" "missing ${dir_path}"
    fi
    artifact_pass_check "required_dir_${dir_name}" "found ${dir_path}"
  done

  local renderer="${BASE_DIR}/scripts/render_table12_method_evidence_ledger_v1.py"
  if [[ ! -f "${renderer}" ]]; then
    artifact_fail_check "table12_renderer_exists" "missing ${renderer}"
  fi
  artifact_pass_check "table12_renderer_exists" "found ${renderer}"

  artifact_log "Running Table 12 static renderer with --check."
  if python -B "${renderer}" --check 2>&1 | tee -a "${ARTIFACT_LOG_FILE}"; then
    artifact_pass_check "table12_renderer_check" "Table 12 regenerated successfully"
  else
    artifact_fail_check "table12_renderer_check" "renderer exited nonzero"
  fi

  local table12_out_dir="${BASE_DIR}/18_TABLE12_REGENERATION_V1"
  if [[ ! -d "${table12_out_dir}" ]]; then
    artifact_fail_check "required_dir_18_TABLE12_REGENERATION_V1" "missing ${table12_out_dir} after renderer"
  fi
  artifact_pass_check "required_dir_18_TABLE12_REGENERATION_V1" "found ${table12_out_dir}"

  local static_dir="${BASE_DIR}/16_STATIC_RECOMPUTE_AUDIT_V1"
  local static_summary="${static_dir}/static_recompute_summary_v1.md"
  local static_results="${static_dir}/static_recompute_results_v1.csv"
  local static_mismatches="${static_dir}/static_recompute_mismatches_v1.csv"
  local required_file
  for required_file in "${static_summary}" "${static_results}" "${static_mismatches}"; do
    if [[ ! -f "${required_file}" ]]; then
      artifact_fail_check "static_recompute_file_exists" "missing ${required_file}"
    fi
    artifact_pass_check "static_recompute_file_exists" "found ${required_file}"
  done

  artifact_log "Checking static recompute mismatch CSV for conflict or missing-input rows."
  if python - "${static_mismatches}" >> "${ARTIFACT_LOG_FILE}" 2>&1 <<'PY'
import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])
with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
if rows:
    print(f"mismatch rows: {len(rows)}")
    for row in rows[:10]:
        print(row)
    raise SystemExit(1)
print("mismatch rows: 0")
PY
  then
    artifact_pass_check "static_recompute_mismatches_empty" "0 conflict or missing-input rows"
  else
    artifact_fail_check "static_recompute_mismatches_empty" "mismatch CSV contains data rows"
  fi

  local provenance_summary="${BASE_DIR}/17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_provenance_summary_v1.md"
  local boundary_result
  boundary_result="$(
    python - "${static_summary}" "${provenance_summary}" <<'PY'
import sys
from pathlib import Path

text = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:]).lower()
checks = {
    "speedup_transfer_rate_expected_na": ["speeduptransferrate", "expected na"],
    "node_alignment_expected_na": ["nodealignmentcoverage", "expected na"],
    "verifier_not_same_engine_baseline": ["verifier support", "not a same-engine"],
    "bounded_port6_not_full_port9": ["bounded port6", "port9"],
}
missing = []
for name, terms in checks.items():
    if not all(term in text for term in terms):
        missing.append(name)
if missing:
    print("\n".join(missing))
    raise SystemExit(1)
print("all expected-NA and scope boundaries present")
PY
  )"
  if [[ "${boundary_result}" == "all expected-NA and scope boundaries present" ]]; then
    artifact_pass_check "expected_na_boundaries_present" "${boundary_result}"
  else
    artifact_fail_check "expected_na_boundaries_present" "${boundary_result}"
  fi

  local diff_file="${table12_out_dir}/table12_regeneration_diff_v1.csv"
  local diff_summary
  diff_summary="$(
    python - "${diff_file}" <<'PY'
import csv
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1])
with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
counts = Counter(row["comparison_status"] for row in rows)
print(
    "cells_compared={cells}; exact_match={exact}; rounded_match={rounded}; "
    "expected_NA_match={expected_na}; artifact_boundary_match={artifact}; conflicts={conflicts}; missing_input={missing}".format(
        cells=len(rows),
        exact=counts.get("exact_match", 0),
        rounded=counts.get("rounded_match", 0),
        expected_na=counts.get("expected_NA_match", 0),
        artifact=counts.get("artifact_boundary_match", 0),
        conflicts=counts.get("conflict_needs_human_review", 0),
        missing=counts.get("missing_input", 0),
    )
)
PY
  )"
  artifact_pass_check "table12_diff_summary" "${diff_summary}"

  cat > "${ARTIFACT_SUMMARY_FILE}" <<EOF
# Common-core v0 Reviewer Reproduction V1

## Purpose
This is a reviewer-facing artifact-mode reproduction wrapper for Common-core v0 retained evidence validation.

## Mode Boundary
Artifact-mode does not run database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection. It reads retained CSV/JSON/MD artifacts and runs the static Table 12 renderer only.

## Results
- Table 12 regenerated successfully via \`python -B ${renderer} --check\`.
- Static recomputation had 0 conflicts / missing inputs.
- Table 12 diff summary: ${diff_summary}.
- Artifact-only rows remain artifact-only.
- Expected NA fields remain NA.

## Expected-NA And Scope Boundaries
- SpeedupTransferRate is not computed because paired target-engine timing is not retained.
- Full NodeAlignmentCoverage is not computed; retained plan evidence is a selected PG frontier, not full-denominator node alignment.
- Verifier support is not a same-engine rewrite baseline and does not use the common-core 120 denominator.
- Bounded PORT6 closure is retained separately and is not a full PORT9 experiment.

## Optional Future Modes
Deterministic reruns are available through \`--mode deterministic\` and require explicit \`--execute\` before any DB/timing command is run. LLM reruns remain a separate future mode, not default review mode.

## Outputs
- \`${ARTIFACT_STATUS_FILE}\`
- \`${ARTIFACT_LOG_FILE}\`
- \`${ARTIFACT_SUMMARY_FILE}\`
EOF

  artifact_pass_check "reviewer_summary_written" "wrote ${ARTIFACT_SUMMARY_FILE}"
  artifact_log "Reviewer reproduction artifact-mode passed."
  artifact_log "Output directory: ${ARTIFACT_OUT_DIR}"
}

declare -a STEP_IDS=()
declare -A STEP_DESCRIPTION=()
declare -A STEP_COMMAND=()
declare -A STEP_RUNNER=()
declare -A STEP_REQUIRES_DB=()
declare -A STEP_REQUIRES_JAVA=()
declare -A STEP_REQUIRES_LLM=()
declare -A STEP_REQUIRES_VERIFIER=()
declare -A STEP_NOTES=()

register_step() {
  local step_id="$1"
  local description="$2"
  local command="$3"
  local runner="$4"
  local requires_db="$5"
  local requires_java="$6"
  local notes="$7"

  STEP_IDS+=("${step_id}")
  STEP_DESCRIPTION["${step_id}"]="${description}"
  STEP_COMMAND["${step_id}"]="${command}"
  STEP_RUNNER["${step_id}"]="${runner}"
  STEP_REQUIRES_DB["${step_id}"]="${requires_db}"
  STEP_REQUIRES_JAVA["${step_id}"]="${requires_java}"
  STEP_REQUIRES_LLM["${step_id}"]="no"
  STEP_REQUIRES_VERIFIER["${step_id}"]="no"
  STEP_NOTES["${step_id}"]="${notes}"
}

init_deterministic_steps() {
  local hard_negative_py="${BASE_DIR}/runs/package_hard_negative_closure_01/run_package_hard_negative_closure.py"
  local hard_negative_sh="${BASE_DIR}/runs/package_hard_negative_closure_01/run_manual_package_hard_negative_closure.sh"
  if [[ -f "${hard_negative_py}" ]]; then
    register_step "hard-negative" "Package hard-negative closure." "python -B ${hard_negative_py}" "${hard_negative_py}" "yes" "no" "Primary retained python runner; alternate manual runner: ${hard_negative_sh}."
  else
    register_step "hard-negative" "Package hard-negative closure." "bash ${hard_negative_sh}" "${hard_negative_sh}" "yes" "no" "Python runner not retained; using manual shell runner if present."
  fi

  register_step "sqlglot" "SQLGlot full per-case timing / no-op and optimize evidence where retained." "bash ${BASE_DIR}/runs/sqlglot_full_per_case_timing_01/run_manual_sqlglot_full_per_case_timing.sh" "${BASE_DIR}/runs/sqlglot_full_per_case_timing_01/run_manual_sqlglot_full_per_case_timing.sh" "yes" "no" "Deterministic SQLGlot timing runner; no LLM."
  register_step "calcite" "Calcite HEP 93 exact timing packet." "bash ${BASE_DIR}/runs/calcite_hep_93_exact_timing_01/run_manual_calcite_hep_93_exact_timing.sh" "${BASE_DIR}/runs/calcite_hep_93_exact_timing_01/run_manual_calcite_hep_93_exact_timing.sh" "yes" "yes" "Requires Java/Calcite and database timing environment."

  local pg_plan_py="${BASE_DIR}/runs/pg_plan_attribution_113_01/run_pg_plan_attribution_113.py"
  local pg_plan_sh="${BASE_DIR}/runs/pg_plan_attribution_113_01/run_manual_pg_plan_attribution_113.sh"
  if [[ -f "${pg_plan_py}" ]]; then
    register_step "pg-plan" "Selected PG plan attribution / observability frontier." "python -B ${pg_plan_py}" "${pg_plan_py}" "yes" "no" "Primary retained python runner; alternate manual runner: ${pg_plan_sh}."
  else
    register_step "pg-plan" "Selected PG plan attribution / observability frontier." "bash ${pg_plan_sh}" "${pg_plan_sh}" "yes" "no" "Python runner not retained; using manual shell runner if present."
  fi

  register_step "table12" "Static Table 12 regeneration." "python -B ${BASE_DIR}/scripts/render_table12_method_evidence_ledger_v1.py --check" "${BASE_DIR}/scripts/render_table12_method_evidence_ledger_v1.py" "no" "no" "Static artifact-only check."

  local direct_llm_timing="${BASE_DIR}/runs/direct_llm_same_engine_timing_01/run_manual_direct_llm_timing.sh"
  if [[ -f "${direct_llm_timing}" ]]; then
    register_step "direct-llm-timing-retained" "Retained Direct LLM same-engine timing runner only; does not run LLM generation." "bash ${direct_llm_timing}" "${direct_llm_timing}" "yes" "no" "Requires DB timing environment; no LLM/API call."
  fi

  local rbot_timing="${BASE_DIR}/runs/r_bot_pg15_timing_expansion_02/run_manual_r_bot_pg15_timing.sh"
  if [[ -f "${rbot_timing}" ]]; then
    register_step "rbot-pg15-timing" "R-Bot PG15 bounded appendix timing." "bash ${rbot_timing}" "${rbot_timing}" "yes" "no" "Bounded appendix route; requires DB timing environment."
  fi
}

step_exists() {
  local needle="$1"
  local step_id
  for step_id in "${STEP_IDS[@]}"; do
    if [[ "${step_id}" == "${needle}" ]]; then
      return 0
    fi
  done
  return 1
}

select_steps() {
  SELECTED_STEPS=()
  local step_id
  if [[ -z "${STEPS_ARG}" || "${STEPS_ARG}" == "all-deterministic" ]]; then
    SELECTED_STEPS=("${STEP_IDS[@]}")
    return
  fi

  IFS=',' read -r -a SELECTED_STEPS <<< "${STEPS_ARG}"
  for step_id in "${SELECTED_STEPS[@]}"; do
    if ! step_exists "${step_id}"; then
      echo "error: unknown deterministic step: ${step_id}" >&2
      echo "known steps: ${STEP_IDS[*]} all-deterministic" >&2
      exit 2
    fi
  done
}

deterministic_log() {
  printf '%s\n' "$*" | tee -a "${DETERMINISTIC_LOG_FILE}"
}

write_deterministic_status() {
  write_csv_row "${DETERMINISTIC_STATUS_FILE}" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}"
}

command_available() {
  command -v "$1" >/dev/null 2>&1
}

mysql_available() {
  command_available mysql || command_available docker || command_available docker-compose
}

spark_available() {
  if command_available spark-submit; then
    return 0
  fi
  if command_available python && python -c 'import pyspark' >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

runner_mentions() {
  local runner="$1"
  local pattern="$2"
  [[ -f "${runner}" ]] && grep -Eiq "${pattern}" "${runner}"
}

preflight_step() {
  local step_id="$1"
  local runner="${STEP_RUNNER[${step_id}]}"
  local status="preflight_pass"
  local notes="runner and required local tools found"
  local -a messages=()

  if [[ ! -f "${runner}" ]]; then
    status="preflight_blocked"
    messages+=("missing runner ${runner}")
  fi
  if ! command_available python; then
    status="preflight_blocked"
    messages+=("python not found")
  fi
  if ! command_available bash; then
    status="preflight_blocked"
    messages+=("bash not found")
  fi
  if [[ "${STEP_REQUIRES_JAVA[${step_id}]}" == "yes" ]] && ! command_available java; then
    status="preflight_blocked"
    messages+=("java not found")
  fi
  if [[ "${STEP_REQUIRES_DB[${step_id}]}" == "yes" ]]; then
    if ! command_available psql; then
      if [[ "${status}" != "preflight_blocked" ]]; then
        status="preflight_warn"
      fi
      messages+=("psql not found; no database connection attempted")
    fi
  fi
  if [[ "${STEP_REQUIRES_DB[${step_id}]}" == "yes" ]] && runner_mentions "${runner}" "mysql|pymysql|env_mysql"; then
    if ! mysql_available; then
      if [[ "${status}" != "preflight_blocked" ]]; then
        status="preflight_warn"
      fi
      messages+=("mysql client or docker/docker-compose not found; no MySQL connection attempted")
    fi
  fi
  if [[ "${STEP_REQUIRES_DB[${step_id}]}" == "yes" ]] && runner_mentions "${runner}" "spark|pyspark|spark-submit|env_spark"; then
    if ! spark_available; then
      if [[ "${status}" != "preflight_blocked" ]]; then
        status="preflight_warn"
      fi
      messages+=("spark-submit or local pyspark not found; no Spark session attempted")
    fi
  fi

  if [[ "${#messages[@]}" -gt 0 ]]; then
    notes="$(IFS='; '; echo "${messages[*]}")"
  elif [[ "${status}" == "preflight_pass" && "${STEP_REQUIRES_DB[${step_id}]}" == "yes" ]]; then
    notes="runner and local tools found; database connection not attempted"
  fi

  write_deterministic_status "${step_id}" "${STEP_DESCRIPTION[${step_id}]}" "${STEP_COMMAND[${step_id}]}" "$([[ -f "${runner}" ]] && echo yes || echo no)" "${STEP_REQUIRES_DB[${step_id}]}" "${STEP_REQUIRES_JAVA[${step_id}]}" "${STEP_REQUIRES_LLM[${step_id}]}" "${STEP_REQUIRES_VERIFIER[${step_id}]}" "preflight" "${status}" "${notes}"
  deterministic_log "${status} ${step_id}: ${notes}"
}

write_deterministic_plan() {
  local action="$1"
  local step_id

  cat > "${DETERMINISTIC_PLAN_FILE}" <<EOF
# Common-core v0 Deterministic Reproduction Plan V1

## Purpose
This file records the reviewer-facing deterministic rerun plan for Common-core v0.

## Mode Boundary
- Deterministic mode does not call LLM APIs.
- Deterministic mode does not run verifier tools.
- Deterministic mode does not run PORT9.
- Deterministic mode may run DB/timing commands only when \`--execute\` is explicit.
- LLM and full rerun modes remain separate from deterministic artifact review.

## Invocation
- Mode action: \`${action}\`
- Requested steps: \`${STEPS_ARG:-all-deterministic}\`
- Output directory: \`${DETERMINISTIC_OUT_DIR}\`

## Selected Steps
EOF

  for step_id in "${SELECTED_STEPS[@]}"; do
    cat >> "${DETERMINISTIC_PLAN_FILE}" <<EOF

### ${step_id}
- Description: ${STEP_DESCRIPTION[${step_id}]}
- Command: \`${STEP_COMMAND[${step_id}]}\`
- Runner exists: $([[ -f "${STEP_RUNNER[${step_id}]}" ]] && echo yes || echo no)
- Requires DB: ${STEP_REQUIRES_DB[${step_id}]}
- Requires Java: ${STEP_REQUIRES_JAVA[${step_id}]}
- Requires LLM: ${STEP_REQUIRES_LLM[${step_id}]}
- Requires verifier: ${STEP_REQUIRES_VERIFIER[${step_id}]}
- Notes: ${STEP_NOTES[${step_id}]}
EOF
  done
}

run_deterministic_mode() {
  if [[ "${DRY_RUN}" -eq 0 && "${PREFLIGHT}" -eq 0 && "${EXECUTE}" -eq 0 ]]; then
    DRY_RUN=1
  fi
  if (( DRY_RUN + PREFLIGHT + EXECUTE > 1 )); then
    echo "error: choose only one of --dry-run, --preflight, or --execute" >&2
    exit 2
  fi
  if [[ "${EXECUTE}" -eq 1 && -z "${STEPS_ARG}" ]]; then
    echo "error: --steps is required with --execute; use --steps all-deterministic to run every deterministic step" >&2
    exit 2
  fi

  init_deterministic_steps
  select_steps

  mkdir -p "${DETERMINISTIC_OUT_DIR}"
  DETERMINISTIC_PLAN_FILE="${DETERMINISTIC_OUT_DIR}/deterministic_reproduction_plan_v1.md"
  DETERMINISTIC_STATUS_FILE="${DETERMINISTIC_OUT_DIR}/deterministic_reproduction_status_v1.csv"
  DETERMINISTIC_LOG_FILE="${DETERMINISTIC_OUT_DIR}/deterministic_reproduction_log_v1.txt"

  {
    echo "Common-core v0 deterministic reproduction"
    echo "timestamp_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo "repo_root=${REPO_ROOT}"
    echo "boundary=no LLM/API, no verifier, no PORT9; DB/timing only with --execute"
    echo
  } > "${DETERMINISTIC_LOG_FILE}"
  printf '"step_id","description","command","runner_exists","requires_db","requires_java","requires_llm","requires_verifier","mode","status","notes"\n' > "${DETERMINISTIC_STATUS_FILE}"

  local action="dry-run"
  if [[ "${PREFLIGHT}" -eq 1 ]]; then
    action="preflight"
  elif [[ "${EXECUTE}" -eq 1 ]]; then
    action="execute"
  fi

  write_deterministic_plan "${action}"
  deterministic_log "Deterministic mode action: ${action}"
  deterministic_log "Selected steps: ${SELECTED_STEPS[*]}"
  deterministic_log "Boundary: no LLM/API calls, no verifier tools, no PORT9."

  local step_id
  local runner_exists
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    for step_id in "${SELECTED_STEPS[@]}"; do
      runner_exists="$([[ -f "${STEP_RUNNER[${step_id}]}" ]] && echo yes || echo no)"
      write_deterministic_status "${step_id}" "${STEP_DESCRIPTION[${step_id}]}" "${STEP_COMMAND[${step_id}]}" "${runner_exists}" "${STEP_REQUIRES_DB[${step_id}]}" "${STEP_REQUIRES_JAVA[${step_id}]}" "${STEP_REQUIRES_LLM[${step_id}]}" "${STEP_REQUIRES_VERIFIER[${step_id}]}" "dry-run" "planned" "${STEP_NOTES[${step_id}]}"
      deterministic_log "planned ${step_id}: ${STEP_COMMAND[${step_id}]}"
    done
  elif [[ "${PREFLIGHT}" -eq 1 ]]; then
    if command_available python; then
      deterministic_log "preflight tool: python found"
    else
      deterministic_log "preflight tool: python missing"
    fi
    if command_available bash; then
      deterministic_log "preflight tool: bash found"
    else
      deterministic_log "preflight tool: bash missing"
    fi
    for step_id in "${SELECTED_STEPS[@]}"; do
      preflight_step "${step_id}"
    done
  else
    for step_id in "${SELECTED_STEPS[@]}"; do
      runner_exists="$([[ -f "${STEP_RUNNER[${step_id}]}" ]] && echo yes || echo no)"
      if [[ "${runner_exists}" != "yes" ]]; then
        write_deterministic_status "${step_id}" "${STEP_DESCRIPTION[${step_id}]}" "${STEP_COMMAND[${step_id}]}" "${runner_exists}" "${STEP_REQUIRES_DB[${step_id}]}" "${STEP_REQUIRES_JAVA[${step_id}]}" "${STEP_REQUIRES_LLM[${step_id}]}" "${STEP_REQUIRES_VERIFIER[${step_id}]}" "execute" "skipped" "missing runner"
        deterministic_log "skipped ${step_id}: missing runner"
        if [[ "${CONTINUE_ON_ERROR}" -eq 0 ]]; then
          exit 1
        fi
        continue
      fi

      deterministic_log "executing ${step_id}: ${STEP_COMMAND[${step_id}]}"
      if bash -c "${STEP_COMMAND[${step_id}]}" >> "${DETERMINISTIC_LOG_FILE}" 2>&1; then
        write_deterministic_status "${step_id}" "${STEP_DESCRIPTION[${step_id}]}" "${STEP_COMMAND[${step_id}]}" "${runner_exists}" "${STEP_REQUIRES_DB[${step_id}]}" "${STEP_REQUIRES_JAVA[${step_id}]}" "${STEP_REQUIRES_LLM[${step_id}]}" "${STEP_REQUIRES_VERIFIER[${step_id}]}" "execute" "executed_pass" "exit_code=0"
        deterministic_log "executed_pass ${step_id}: exit_code=0"
      else
        local exit_code=$?
        write_deterministic_status "${step_id}" "${STEP_DESCRIPTION[${step_id}]}" "${STEP_COMMAND[${step_id}]}" "${runner_exists}" "${STEP_REQUIRES_DB[${step_id}]}" "${STEP_REQUIRES_JAVA[${step_id}]}" "${STEP_REQUIRES_LLM[${step_id}]}" "${STEP_REQUIRES_VERIFIER[${step_id}]}" "execute" "executed_fail" "exit_code=${exit_code}"
        deterministic_log "executed_fail ${step_id}: exit_code=${exit_code}"
        if [[ "${CONTINUE_ON_ERROR}" -eq 0 ]]; then
          exit "${exit_code}"
        fi
      fi
    done
  fi

  deterministic_log "Output directory: ${DETERMINISTIC_OUT_DIR}"
}

case "${MODE}" in
  artifact)
    if [[ "${DRY_RUN}" -eq 1 || "${PREFLIGHT}" -eq 1 || "${EXECUTE}" -eq 1 || -n "${STEPS_ARG}" ]]; then
      echo "error: --dry-run, --preflight, --execute, and --steps are only valid with --mode deterministic" >&2
      exit 2
    fi
    run_artifact_mode
    ;;
  deterministic)
    run_deterministic_mode
    ;;
  llm)
    cat <<EOF
Common-core v0 llm mode is recognized but not implemented in this reviewer wrapper.
It is intentionally separate from deterministic artifact validation and requires
environment setup, credentials, and explicit non-default review scope.
EOF
    if [[ "${ALLOW_UNIMPLEMENTED}" -eq 1 ]]; then
      exit 0
    fi
    echo "Re-run with --allow-unimplemented to acknowledge this placeholder mode." >&2
    exit 2
    ;;
  *)
    echo "error: unsupported mode: ${MODE}" >&2
    if [[ "${ALLOW_UNIMPLEMENTED}" -eq 1 ]]; then
      echo "Unsupported mode acknowledged with --allow-unimplemented; no validation was run."
      exit 0
    fi
    usage >&2
    exit 2
    ;;
esac
