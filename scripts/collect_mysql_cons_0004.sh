#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/cons_0004/plans/mysql

for sql_file in \
  cases/CONS/CONS_0004/source.sql \
  cases/CONS/CONS_0004/rewrite_pos_01.sql \
  cases/CONS/CONS_0004/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  SQL_TEXT="$(cat "$sql_file")"
  printf 'EXPLAIN FORMAT=JSON %s\n' "$SQL_TEXT" | \
    mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
    > "runs/cons_0004/plans/mysql/${base}.json"
done
