#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/perf_0002/plans/mysql

SQL_TEXT="$(cat cases/PERF/PERF_0002/source.sql)"

printf 'EXPLAIN FORMAT=JSON %s\n' "$SQL_TEXT" | \
  mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  > runs/perf_0002/plans/mysql/source.json
