#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/longtail_case/mysql

for sql_file in   cases/LONGTAIL/LONGTAIL_0001/source.sql   cases/LONGTAIL/LONGTAIL_0001/rewrite_pos_01.sql   cases/LONGTAIL/LONGTAIL_0001/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  echo "=== MySQL :: $base ==="
  mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$sql_file" | tee "runs/longtail_case/mysql/${base}.tsv"
  echo
done
