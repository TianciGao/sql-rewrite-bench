#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"
mkdir -p runs/plans/mysql

for sql_file in \
  cases/PERF/PERF_0001/source.sql \
  cases/PERF/PERF_0001/rewrite_pos_01.sql \
  cases/PERF/PERF_0001/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  sql_text="$(cat "$sql_file")"
  printf "EXPLAIN FORMAT=JSON %s\n" "$sql_text" | \
    mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
    > "runs/plans/mysql/${base}.json"
done
