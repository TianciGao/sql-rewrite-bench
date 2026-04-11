#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/port_0002/plans/mysql

SQL_TEXT="$(cat cases/PORT/PORT_0002/rewrite_pos_01.sql)"

printf 'EXPLAIN FORMAT=JSON %s\n' "$SQL_TEXT" | \
  mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  > runs/port_0002/plans/mysql/rewrite_pos_01.json
